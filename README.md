<p align="center">
  <img src="assets/embodied-worker-logo.jpeg" width="280" alt="Embodied Worker logo">
</p>

# EW 具象知識鍛造器 / EW Embodied Knowledge Forge

聊完 ChatGPT，把生成文件變成一個 `.ewforge` 知識包；在手機 Obsidian 選取它，外掛便會自動驗證、建立 Markdown、補上版本與知識關聯。

Turn a ChatGPT conversation into one `.ewforge` knowledge package, then choose it in Obsidian. The plugin validates and safely imports linked Markdown notes into your Vault.

## 中文

### 第一版操作

1. 在 ChatGPT 完成討論或文件生成。
2. 使用「EW 具象知識鍛造器」產生 `.ewforge` 檔案。
3. 在手機 Obsidian 點選左側功能列的開箱圖示。
4. 選擇 `.ewforge`，查看筆記數量與目的地後按「確認匯入」。

使用者不需要設定 API 金鑰，也不必自己處理 YAML、資料夾、標籤或雙向連結。

### 安全設計

- 外掛不會連線到網路，也不含遙測。
- 所有檔案只會寫入設定的 `EW-Knowledge` 根目錄。
- 不會讀寫 `.obsidian` 設定目錄。
- 非 EW 管理的既有檔案永不覆寫；路徑衝突時會建立衝突副本。
- 更新同一 `knowledge_id` 前可自動備份舊版本。
- 匯入前會驗證格式、路徑、知識 ID 與 SHA-256 雜湊。

### 安裝

目前是私人測試版，將 `manifest.json`、`main.js`、`styles.css` 放入 Vault 的：

```text
.obsidian/plugins/ew-knowledge-forge/
```

重新載入 Obsidian 後，到「設定 → 第三方外掛」啟用 `EW Embodied Knowledge Forge`。手機使用者可先在桌面端安裝到同一個 Vault，再透過支援 Vault 設定的同步方式帶到手機；正式上架 Obsidian Community Plugins 後即可在手機直接安裝。

## English

### Version 1 workflow

1. Finish a discussion or generate documents in ChatGPT.
2. Use EW Embodied Knowledge Forge to create a `.ewforge` file.
3. Tap the package icon in Obsidian on mobile.
4. Choose the file, review the count and destination, then tap **Import now**.

No API key is required. Users do not need to manage YAML, folders, tags, versions, or backlinks manually.

### Safety

- No network requests and no telemetry.
- Writes are confined to the configured `EW-Knowledge` root.
- The plugin never reads or writes the `.obsidian` settings directory.
- Existing unmanaged files are never overwritten; collisions produce conflict copies.
- Prior versions of the same `knowledge_id` can be backed up before updates.
- Packages are checked for format, safe paths, identity, and SHA-256 integrity before import.

### Install

For this private beta, copy `manifest.json`, `main.js`, and `styles.css` into:

```text
.obsidian/plugins/ew-knowledge-forge/
```

Reload Obsidian and enable `EW Embodied Knowledge Forge` under **Settings → Community plugins**. Mobile users can install it through a desktop copy of the same Vault and a sync method that includes Vault configuration. Once accepted into Obsidian Community Plugins, it can be installed directly on mobile.

## Repository layout

- `src/main.js` — mobile-compatible source; no Node.js runtime APIs
- `manifest.json` and `versions.json` — Obsidian release metadata
- `styles.css` — touch-friendly bilingual interface
- `chatgpt-plugin/` — installable ChatGPT/Codex plugin that formats conversations and generated files
- `docs/EWFORGE-SPEC.md` — portable package format
- `examples/` — valid example package and source Markdown
- `tests/` — package validator and safety tests
- `scripts/make-release.js` — builds the installable release ZIP

## Trademark

The Embodied Worker name, elephant mark, and supplied artwork are trademarks or proprietary brand assets of Embodied Worker Co., Ltd. Their inclusion does not grant reuse rights.
