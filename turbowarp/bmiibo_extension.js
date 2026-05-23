(function (Scratch) {
    'use strict';

    let currentBmiiboName = "尚未載入";
    let currentBmiiboData = {};
    
    // 🎯 新增：用來給 Scratch 偵測的狀態變數
    let scanStatus = "尚未讀取"; 
    let isScanSuccess = false;

    const globalInput = document.createElement('input');
    globalInput.type = 'file';
    globalInput.accept = '.bmiibo';
    globalInput.style.position = 'fixed';
    globalInput.style.bottom = '0';
    globalInput.style.right = '0';
    globalInput.style.width = '1px';
    globalInput.style.height = '1px';
    globalInput.style.opacity = '0';
    globalInput.style.zIndex = '-9999';
    document.body.appendChild(globalInput);

    globalInput.onchange = function (e) {
        const file = e.target.files[0];
        if (!file) return;

        // 重置狀態
        scanStatus = "讀取中...";
        isScanSuccess = false;

        if (file.size > 5 * 1024 * 1024) {
            scanStatus = "失敗：檔案超過 5MB";
            alert('❌ [掃描錯誤] 檔案超過 5MB 限制！');
            return;
        }

        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js';
        
        script.onload = function () {
            const reader = new FileReader();
            reader.onload = async function (event) {
                try {
                    const zip = await JSZip.loadAsync(event.target.result);
                    
                    if (!zip.file("bmiibo.json")) {
                        scanStatus = "失敗：找不到 json";
                        alert("❌ [掃描錯誤] 檔案結構錯誤：找不到 bmiibo.json！");
                        return;
                    }

                    const jsonText = await zip.file("bmiibo.json").async("text");
                    const fullData = JSON.parse(jsonText);
                    const bmiiboId = fullData.id;

                    if (!bmiiboId) {
                        scanStatus = "失敗：缺少唯一 ID";
                        alert("❌ [掃描錯誤] 找不到唯一 ID！");
                        return;
                    }

                    // 2026年每日檢查
                    const todayStr = new Date().toISOString().split('T')[0];
                    const storageKey = 'bmiibo_usage_log';
                    let usageLog = JSON.parse(localStorage.getItem(storageKey)) || {};

                    if (usageLog[bmiiboId] === todayStr) {
                        scanStatus = "失敗：今天已讀取過";
                        alert(`❌ 【${fullData.name || "這隻玩具"}】今天已經讀取過了！`);
                        return;
                    }

                    // 寫入冷卻時間
                    usageLog[bmiiboId] = todayStr;
                    localStorage.setItem(storageKey, JSON.stringify(usageLog));

                    // 讀取成功！更新狀態
                    currentBmiiboName = fullData.name || "未命名 bmiibo";
                    currentBmiiboData = (fullData.game_data && fullData.game_data.turbowarp) ? fullData.game_data.turbowarp : {};
                    
                    scanStatus = "成功";
                    isScanSuccess = true;

                    alert(`🎉 [掃描成功] 成功載入: ${currentBmiiboName}`);

                } catch (err) {
                    scanStatus = "失敗：檔案毀損";
                    alert(`❌ [讀取失敗] 檔案損壞: ${err.message}`);
                }
            };
            reader.readAsArrayBuffer(file);
        };
        document.head.appendChild(script);
    };

    class BmiiboExtension {
        getInfo() {
            return {
                id: 'bmiiboReader',
                name: 'bmiibo 虛擬玩具系統',
                blocks: [
                    {
                        opcode: 'loadBmiibo',
                        blockType: Scratch.BlockType.COMMAND,
                        text: '開啟選單載入 .bmiibo 檔案'
                    },
                    {
                        opcode: 'getBmiiboName',
                        blockType: Scratch.BlockType.REPORTER,
                        text: 'bmiibo 的名稱'
                    },
                    {
                        opcode: 'getBmiiboData',
                        blockType: Scratch.BlockType.REPORTER,
                        text: 'bmiibo 的 [FIELD] 數值',
                        arguments: {
                            FIELD: {
                                type: Scratch.ArgumentType.STRING,
                                defaultValue: 'score_multiplier'
                            }
                        }
                    },
                    // 🎯 新增的偵測積木
                    {
                        opcode: 'getScanStatus',
                        blockType: Scratch.BlockType.REPORTER,
                        text: 'bmiibo 掃描狀態'
                    },
                    {
                        opcode: 'checkScanSuccess',
                        blockType: Scratch.BlockType.BOOLEAN,
                        text: 'bmiibo 讀取成功？'
                    }
                ]
            };
        }

        loadBmiibo() {
            globalInput.value = '';
            globalInput.click();
        }

        getBmiiboName() { return currentBmiiboName; }
        getBmiiboData(args) {
            const field = args.FIELD;
            return (currentBmiiboData && currentBmiiboData[field] !== undefined) ? currentBmiiboData[field] : 0;
        }
        
        // 🎯 偵測積木的實作邏輯
        getScanStatus() { return scanStatus; }
        checkScanSuccess() { return isScanSuccess; }
    }

    Scratch.extensions.register(new BmiiboExtension());
})(Scratch);
