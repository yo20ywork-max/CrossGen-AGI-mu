# CrossGen-AGI-μ

由來自台灣的**跨世代媒體科技股份有限公司**研發的 Windows 桌面 AI 助理。
支援文字輸入、離線語音輸入、檔案工具及瀏覽器操作。

**這是開發展示版（pre-release），完整產品發布門檻仍未通過。**
本次公開現有 v13 epoch 3 模型與 v0.1 Windows 程式，沒有新增模型訓練。

## Windows 一鍵安裝

1. 從 [Releases](https://github.com/yo20ywork-max/CrossGen-AGI-mu/releases/tag/v0.1-github-1) 下載
   [CrossGen-Setup.exe](https://github.com/yo20ywork-max/CrossGen-AGI-mu/releases/download/v0.1-github-1/CrossGen-Setup.exe)。
2. 執行安裝程式，按「開始自動安裝」。這個 GitHub 公開版不需要登入私有模型帳號。
3. 安裝器會下載並校驗程式、三份主模型分檔、LoRA 權重、Ollama 與 Chromium，完成後啟動 CrossGen。
4. 使用語音輸入前，允許 Windows 桌面程式存取麥克風。
   結束時按「一鍵全部關閉」，停止由控制台啟動的程式與模型服務。

環境：Windows 11；建議 24GB RAM、6GB VRAM；安裝磁碟至少保留 25GB。
主模型及適配權重合計約 5.01GB，另需程式、語音與執行環境下載空間。
RTX 4050 / 6GB / 24GB 目標電腦的效能與完整流程仍未驗收。
EXE 尚未簽章，可用 Releases 的 `CHECKSUMS.txt` 校驗下載內容。

## 可攜式安裝與模型檔

若不使用安裝器，從同一個 Release 下載：

- `CrossGen-AGI-mu-v0.1-Windows.zip`：程式與離線語音元件，完整解壓縮，保留 `_internal`。
- `CrossGen-core-Q4_K_M.gguf.part01`、`.part02`、`.part03`：主模型分檔，三份缺一不可。
- `CrossGen-v13-e3-LoRA.gguf`：v13 epoch 3 適配權重，不能單獨執行。
- `merge-model.ps1`：校驗三份分檔並串接為完整主模型。

在下載資料夾執行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\merge-model.ps1
```

把產生的 `CrossGen-core-Q4_K_M.gguf` 與下載的 LoRA 檔放進解壓縮程式的 `models` 資料夾。
先安裝並啟動 [Ollama](https://ollama.com/download/windows)，執行「首次匯入模型.cmd」，
需要網頁操作再執行「安裝瀏覽器.cmd」，最後開啟 `CrossGen-AGI-mu.exe`。
壓縮包內的舊會議文件若提及私有雲端下載，以本頁的 GitHub 公開下載步驟為準。

## llama.cpp

使用已合併的完整主模型與 LoRA 檔：

```powershell
.\llama-server.exe -m .\models\CrossGen-core-Q4_K_M.gguf --lora .\models\CrossGen-v13-e3-LoRA.gguf -c 4096 -ngl 28 --host 127.0.0.1 --port 8080
```

這是起始配置，尚未在 RTX 4050 實機驗證；顯存不足時降低 `-ngl`。
此部署沒有合併再量化為單一 GGUF。Windows 桌面程式使用 Ollama；llama.cpp 是另一種模型執行方式。

## 原始碼

本儲存庫提供目前產品執行器、Qt 介面、GitHub 公開安裝器及部分 v13 訓練程式。
Python 建議 3.12。以原始碼開啟介面：

```powershell
python -m pip install -r requirements-runtime.txt -r requirements-ui.txt -r requirements-speech.txt
python -m desktop_ui.app --development
```

原始碼介面使用現有環境模型設定；若使用此公開模型，先匯入模型並設定：

```powershell
$env:GHOST_PLANNER_MODELS = "crossgen-agi-mu:meeting-20260907"
$env:GHOST_VISION_MODELS = ""
$env:GHOST_USE_MICRO_HINT = "0"
python -m desktop_ui.app --development
```

`training/v13/config.json` 是保留的原始設定快照，部分啟動前欄位不代表最終訓練狀態。
最終完成證據見 `docs/TRAINING_EVIDENCE.json`；訓練資料、私有紀錄與帳號憑證不在本儲存庫。
本次公開不是完整訓練資料重現包。

## 版本與已知限制

- 主要研發階段為 v1～v13；不是 13 個通過驗收的正式模型。
- 最新完成訓練：v13，1,799 筆訓練資料、385 筆開發資料、雙卡、3 epochs、675 次更新。
- 本公開交付：v0.1 桌面展示程式 + v13 epoch 3 + `0.1-installer-github-1` 公開下載安裝器。
- v13 本機中性身分測試 15/16；runtime-v9 原檔案任務 6/8，0 次誤報完成。
  這些是已知開發題結果，不能代表任意工作成功率。
- 長流程、原生 App 與完整目標實機驗收仍有缺口。語音驗證範圍見 `docs/VOICE_VALIDATION.json`。
- 新增的 256 筆內容對照資料未用於本模型重訓。

詳見 [模型技術說明](docs/MODEL_CARD_EN.md) 及 [發布檔案清單](release-manifest.json)。
本次僅公開既有成果與必要的下載安裝調整，後續研發維持停止，等待使用者另行指示。

## 授權與來源

公開儲存庫不等於授予原創程式開源授權；原創程式及品牌資產保留權利，見 `LICENSE`。
模型及第三方元件各依原授權，見 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
與 `model-notices/`。技術來源記錄與產品對話身分分開處理。
