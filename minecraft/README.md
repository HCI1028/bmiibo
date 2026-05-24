# ⛏️ bmiibo - Minecraft Fabric 模組 API 專區

本資料夾包含了 `bmiibo` 虛擬玩具生態系在 Minecraft (Java Edition) 平台上的官方 Fabric 模組實作。

## 🚀 功能核心
1. **本機安全解包**：使用 Java `ZipInputStream` 讀取 `.bmiibo` 檔案，嚴格限制 5MB 大小，防止損壞檔案導致伺服器或客戶端閃退。
2. **動態紋理渲染**：將玩具內的 `icon.png` 轉化為遊戲內的 `NativeImageBackedTexture`，並可掛載至自訂 GUI 或實體上。
3. **指令連動**：提供 `/bmiibo summon <檔案名稱>` 指令，直接讀取晶片數據。

## 💻 玩家與開發者核心指令
* `/bmiibo reload`：重新整理 `config/bmiibo/vault/` 資料夾內的公仔晶片。
* `/bmiibo info <id>`：在聊天欄顯示該虛擬玩具的創作者、簡介與遊戲加成數據。
