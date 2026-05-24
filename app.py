import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import json
import os
import io
import shutil
from PIL import Image, ImageTk

class BmiiboWallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 bmiibo 虛擬玩具公仔牆")
        self.root.geometry("750x600")
        self.root.configure(bg="#121212") # 更深、更有質感的極致黑背景

        # 圖片快取暫存器，避免圖片消失
        self.image_cache = []
        
        # 自動建立本機收藏夾 my_vault
        self.vault_dir = "my_vault"
        if not os.path.exists(self.vault_dir):
            os.makedirs(self.vault_dir)

        # ----- 🔝 頂部列：公仔統計與匯入功能 -----
        top_frame = tk.Frame(root, bg="#1a1a1a", height=70)
        top_frame.pack(fill="x", side="top")
        top_frame.pack_propagate(False)

        # 大大的收藏計數器
        self.counter_label = tk.Label(top_frame, text="📊 虛擬公仔牆總數：0 隻", font=("微軟正黑體", 15, "bold"), fg="#00ffcc", bg="#1a1a1a")
        self.counter_label.pack(side="left", padx=25, pady=20)

        # 匯入按鈕
        btn_add = tk.Button(top_frame, text="📥 擺放新公仔 (.bmiibo)", font=("微軟正黑體", 10, "bold"), bg="#007acc", fg="white", 
                             relief="flat", padx=15, command=self.import_bmiibo, cursor="hand2")
        btn_add.pack(side="right", padx=25, pady=20)

        # ----- 📜 滾動公仔牆主區域 -----
        canvas = tk.Canvas(root, bg="#121212", highlightthickness=0)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        
        self.wall_frame = tk.Frame(canvas, bg="#121212")
        self.wall_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.wall_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=25, pady=10)
        scrollbar.pack(side="right", fill="y")

        # 開機自動掃描公仔牆
        self.refresh_wall()

    def refresh_wall(self):
        """核心邏輯：把 my_vault 裡的所有公仔外觀、名字、ID 抓出來排滿整面牆"""
        # 1. 清空舊畫面
        for widget in self.wall_frame.winfo_children():
            widget.destroy()
        self.image_cache.clear()

        # 2. 搜尋資料夾內的所有玩具
        bmiibo_files = [f for f in os.listdir(self.vault_dir) if f.endswith(".bmiibo")]
        
        # 更新統計數量
        self.counter_label.config(text=f"📊 虛擬公仔牆總數：{len(bmiibo_files)} 隻")

        if not bmiibo_files:
            empty_lbl = tk.Label(self.wall_frame, text="🫙 牆上空空如也...\n把你的 .bmiibo 檔案丟進來展示吧！", 
                                 font=("微軟正黑體", 12), fg="#555555", bg="#121212")
            empty_lbl.pack(pady=150, padx=200)
            return

        # 3. 網格排版（一行排 4 隻公仔，畫面比例最完美）
        max_columns = 4
        
        for index, filename in enumerate(bmiibo_files):
            file_path = os.path.join(self.vault_dir, filename)
            
            try:
                # 拆解 .bmiibo 包裹
                with zipfile.ZipFile(file_path, 'r') as b_file:
                    # 讀取基本視覺欄位
                    json_data = json.loads(b_file.read("bmiibo.json").decode("utf-8"))
                    toy_name = json_data.get("name", "未命名")
                    toy_id = json_data.get("id", "未知 ID")
                    
                    # 讀取外觀並縮放成標準正方形公仔大頭貼 (130x130)
                    img_data = b_file.read("icon.png")
                    pil_img = Image.open(io.BytesIO(img_data))
                    pil_img = pil_img.resize((130, 130), Image.Resampling.LANCZOS)
                    tk_img = ImageTk.PhotoImage(pil_img)
                    self.image_cache.append(tk_img)

                # ----- 🎨 繪製精美公仔展示卡片（純視覺，不綁定點擊功能） -----
                card = tk.Frame(self.wall_frame, bg="#1e1e1e", padx=8, pady=8, bd=1, highlightbackground="#2d2d2d", highlightthickness=1)
                
                row = index // max_columns
                col = index % max_columns
                card.grid(row=row, column=col, padx=12, pady=12)

                # 玩具外觀大頭貼（單純展示，點擊無反應）
                img_label = tk.Label(card, image=tk_img, bg="#1e1e1e")
                img_label.image = tk_img
                img_label.pack(pady=5)

                # 玩具名稱
                name_lbl = tk.Label(card, text=toy_name, font=("微軟正黑體", 11, "bold"), fg="#ffffff", bg="#1e1e1e", wraplength=130)
                name_lbl.pack(pady=(5, 2))

                # 玩具 ID（小字）
                id_lbl = tk.Label(card, text=f"ID: {toy_id}", font=("Consolas", 8), fg="#777777", bg="#1e1e1e")
                id_lbl.pack(pady=(0, 5))

            except Exception:
                # 萬一遇到打包錯誤的壞檔案，顯示紅盒提示
                row = index // max_columns
                col = index % max_columns
                err_card = tk.Frame(self.wall_frame, bg="#2a1414", width=146, height=190, bd=1, highlightbackground="#421c1c", highlightthickness=1)
                err_card.grid(row=row, column=col, padx=12, pady=12)
                err_card.grid_propagate(False)
                tk.Label(err_card, text="⚠️\n公仔數據損壞", fg="#ff4444", bg="#2a1414", font=("微軟正黑體", 10)).pack(pady=70)

    def import_bmiibo(self):
        """點擊按鈕，自動複製 .bmiibo 檔案到公仔櫃夾中，牆面自動刷新"""
        src_path = filedialog.askopenfilename(filetypes=[("bmiibo 虛擬玩具", "*.bmiibo")])
        if not src_path:
            return
        
        dest_path = os.path.join(self.vault_dir, os.path.basename(src_path))
        try:
            shutil.copy(src_path, dest_path)
            self.refresh_wall() # 重新排版公仔牆
        except Exception as e:
            messagebox.showerror("錯誤", f"無法擺放公仔：{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BmiiboWallApp(root)
    root.mainloop()