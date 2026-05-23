# 🐍 bmiibo - Python 開發者套件 (Pygame 友善)

這個資料夾包含了 `bmiibo` 虛擬玩具系統的官方 Python 核心套件。它為遊戲開發者提供了完整的**安全掃描（防崩潰）**機制，以及**本機每日限讀一次（冷卻防刷）**的嚴格驗證。

套件內建了對 `pygame` 的完美支援，可以一鍵將玩具的外觀圖示轉換為 `pygame.Surface` 物件。

## 📥 安裝方法 (Installation)

目前本套件支援本地導入或透過設定檔打包。未來發布至 PyPI 後，開發者只需執行：
```bash
pip install bmiibo
