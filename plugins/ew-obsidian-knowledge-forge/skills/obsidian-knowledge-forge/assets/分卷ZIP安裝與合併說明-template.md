# 分卷 ZIP 安裝與合併說明

Vault：`{{VAULT_NAME}}`

## 重要原則

- 所有 Part 都屬於同一個 Vault。
- 不要把每個 Part 分別開成不同 Vault。
- 依序將所有 Part 解壓到同一個上層位置，合併同名的 `{{VAULT_NAME}}` 資料夾。
- 保留所有原始 ZIP，直到完成筆記數量檢查。

## 分卷清單

由 `00-Home/Forge Progress.md` 列出已完成分卷、來源與累計筆記數。

## 合併步驟

1. 解壓 Part00。
2. 依序解壓 Part01、Part02 及後續分卷到相同位置。
3. 選擇合併 `{{VAULT_NAME}}` 資料夾。
4. `README-START-HERE.md`、`使用說明-請先閱讀.md`、`分卷ZIP安裝與合併說明.md` 在每卷都相同，可保留或取代。其他檔案若出現同名衝突，不要覆蓋；回到最新 `FORGE-CHECKPOINT.md` 核對預期路徑。
5. 完成全部分卷後，核對 `Forge Progress.md` 記錄的預期 Markdown 筆記總數。
6. 在 Obsidian 將唯一的 `{{VAULT_NAME}}` 資料夾作為 Vault 開啟。

## 繼續鍛造

最新的 `FORGE-CHECKPOINT.md` 應保存在 Vault 外。開啟新的 ChatGPT 對話、呼叫 EW Knowledge Forge、選擇「繼續既有專案」，再上傳該檔與下一批來源。
