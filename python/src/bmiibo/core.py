import zipfile
import json
import os
import io
from datetime import datetime
from .exceptions import FileTooLargeError, InvalidFormatError, DailyLimitExceededError

class Bmiibo:
    def __init__(self, filepath, log_path="bmiibo_cooldown.json"):
        self.filepath = filepath
        self.log_path = log_path
        
        # 玩具的基本屬性
        self.id = ""
        self.name = ""
        self.version = ""
        self.author = ""
        self.description = ""
        self._raw_game_data = {}
        self._icon_bytes = b"" # 暫存圖片二進位資料，不強綁任何遊戲引擎

        # 一建立就立刻發動安全掃描三部曲
        self._scan_and_load()

    def _scan_and_load(self):
        # 【第一關】檔案大小安檢（上限 5MB）
        if os.path.getsize(self.filepath) > 5 * 1024 * 1024:
            raise FileTooLargeError("檔案超過 5MB 安全限制，拒絕讀取。")

        try:
            with zipfile.ZipFile(self.filepath, 'r') as b_file:
                namelist = b_file.namelist()

                # 【第二關】結構完好度檢查
                if "bmiibo.json" not in namelist or "icon.png" not in namelist:
                    raise InvalidFormatError("損壞的 bmiibo：根目錄缺少 bmiibo.json 或 icon.png！")

                # 【第三關】語法解析與欄位驗證
                with b_file.open('bmiibo.json') as f:
                    full_data = json.load(f)

                self.id = full_data.get("id")
                self.name = full_data.get("name", "未命名 bmiibo")
                self.version = full_data.get("bmiibo_version", "1.0")
                self.author = full_data.get("author", "未知")
                self.description = full_data.get("description", "")
                self._raw_game_data = full_data.get("game_data", {})

                if not self.id:
                    raise InvalidFormatError("bmiibo.json 內缺少必要的 'id' 欄位。")

                # ⏳ 【第四關】每日限讀一次防刷偵測
                self._verify_daily_limit()

                # 通過所有考驗，把圖示讀入記憶體
                with b_file.open('icon.png') as img_f:
                    self._icon_bytes = img_f.read()

        except zipfile.BadZipFile:
            raise InvalidFormatError("這不是一個合法的壓縮檔案。")
        except json.JSONDecodeError:
            raise InvalidFormatError("bmiibo.json 語法錯誤，無法解析。")

    def _verify_daily_limit(self):
        """處理本機對時防刷"""
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        # 讀取或初始化記帳本
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r', encoding='utf-8') as f:
                try: log = json.load(f)
                except json.JSONDecodeError: log = {}
        else:
            log = {}

        # 檢查冷卻時間
        if log.get(self.id) == today_str:
            raise DailyLimitExceededError(f"玩具【{self.name}】今天在本作已讀取過，冷卻中。")

        # 驗證通過，刻入紀錄
        log[self.id] = today_str
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(log, f, indent=4)

    def get_data(self, platform="pygame"):
        """讓開發者快速獲取特定平台的數據字典"""
        return self._raw_game_data.get(platform, {})

    def to_pygame_surface(self):
        """🎯 完美的擴充功能：如果開發者用 Pygame，一鍵幫他把圖示轉成 Surface"""
        try:
            import pygame
            img_stream = io.BytesIO(self._icon_bytes)
            return pygame.image.load(img_stream).convert_alpha()
        except ImportError:
            raise RuntimeError("偵測到您的環境未安裝 pygame，無法轉換圖示！")
