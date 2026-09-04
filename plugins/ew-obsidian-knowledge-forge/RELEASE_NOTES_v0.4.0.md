# EW_knowledge_forge v0.4.0

## 核心改版

本版將大型專案鍛造從「單次完整處理」改為「可中斷、可跨對話、可驗證的分批鍛造」。目標不是降低知識完整度，而是讓使用者能在 ChatGPT 的可見上下文與連線限制下，逐步完成整個專案知識庫。

## 新增能力

- 三種入口：開始完整專案、從 checkpoint 繼續、只鍛造本次對話或文件。
- 首次呼叫只進行選擇與界定，不立即啟動大型產檔。
- 每批只處理一段長對話、一份長文件或一組相關短文件。
- 新增穩定 `forge_id`、`project_id`、`source_id` 與 `knowledge_id`。
- 新增 `FORGE-CHECKPOINT.md`，可在全新 ChatGPT 對話續作。
- 新增 Part00／PartNN／Part99-Final 分卷規則。
- 新增累計來源清冊、進度頁、分卷清單與完整性收據。
- 新增 checkpoint 驗證腳本。
- 圖譜驗證器可根據 checkpoint 驗證跨分卷連結。
- 失敗時不推進來源狀態、分卷編號或 checkpoint 版本。
- 新增手機與桌面分卷合併說明。

## 修正

- 移除外掛 manifest 中目前驗證器不接受的 `interface.brandColorDark` 欄位。
- 不再把短提示詞、長上下文或網路錯誤混為同一原因。
- 不再暗示可以一次讀取使用者的全部 ChatGPT 歷史或 Project 內所有對話。
- 導航頁、checkpoint 與來源清冊不得替代實質知識內容。

## 相容性

- 維持標準 Obsidian Vault ZIP，不需要 Obsidian 社群外掛。
- 維持 A／B／C 三種精簡比例。
- 維持既有知識筆記 YAML schema 與穩定 `knowledge_id` 原則。
- 舊版單一 ZIP 仍可作為 standalone 模式使用。
