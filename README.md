# 🧱 bmiibo - TurboWarp 擴展專區

這裡存放了 `bmiibo` 虛擬玩具系統在 TurboWarp (Scratch) 平台上的自訂擴展插件。

## 📥 如何在你的 TurboWarp 專案中載入？

1. 下載本資料夾中的 `bmiibo_extension.js` 檔案到你的電腦。
2. 開啟 [TurboWarp 編輯器](https://turbowarp.org/)。
3. 點擊左下角的 **「擴展選單」**（添加擴展）。
4. 捲動到最下方，選擇 **「自訂擴展 (Custom Extension)」**。
5. 切換到 **「檔案 (File)」** 標籤頁，並上傳你剛剛下載的 `bmiibo_extension.js`。
6. ⚠️ **重要安全性設定**：請確保在載入時或設定中**關閉「沙盒模式 (Sandbox)」**，否則瀏覽器會阻止擴展讀取 `.bmiibo` 檔案內的 JSON 數據。

## 🧱 內建積木功能
* `[開啟選單載入 .bmiibo 檔案]`：同步觸發系統選檔案視窗，並自帶 5MB 安檢與每日限讀一次防刷限制。
* `(bmiibo 的名稱)`：回傳當前成功載入的玩具名稱。
* `(bmiibo 的 [FIELD] 數值)`：獲取該玩具專屬於 TurboWarp 遊戲內的自訂參數。
* `(bmiibo 掃描狀態)`：即時回傳掃描進度或錯誤原因（如：`成功`、`失敗：今天已讀取過`）。
* `<bmiibo 讀取成功？>`：用於遊戲主程式判斷並發放獎勵的布林值偵測積木。