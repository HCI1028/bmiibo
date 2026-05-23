# bmiibo-python
# 🎮 bmiibo - 虛擬玩具生態系 (Virtual Toy System)

`bmiibo` 是一個開源、跨平台且完全免費的虛擬玩具檔案格式與生態系。它的功能類似實體 amiibo，但完全數位化，旨在為獨立遊戲、Minecraft 模組和教育程式平台帶來全新的收藏儀式感。

## 📦 檔案格式規範 (.bmiibo)
`.bmiibo` 本質上是一個自訂副檔名的壓縮檔（ZIP 格式），內部包含以下標準結構：
```text
my_character.bmiibo
├── bmiibo.json      # 核心數據（名稱、唯一ID、各平台專屬數值）
└── icon.png         # 虛擬玩具的圖示 (建議 512x512 PNG)
