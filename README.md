<p align="center">
  <img src="assets/embodied-worker-logo.jpeg" width="280" alt="Embodied Worker logo">
</p>

# EW Embodied Knowledge Forge / 具象知識鍛造器

Turn a ChatGPT conversation into one `.ewforge` knowledge package, then choose it in Obsidian. The plugin validates and safely imports linked Markdown notes into your Vault.

聊完 ChatGPT，把生成文件變成一個 `.ewforge` 知識包；在手機 Obsidian 選取它，外掛便會自動驗證、建立 Markdown、補上版本與知識關聯。

## English

### Version 1 workflow

1. Finish a discussion or generate documents in ChatGPT.
2. Use EW Embodied Knowledge Forge to create a `.ewforge` file.
3. Tap the package icon in Obsidian on mobile.
4. Choose the file, review the count and destination, then tap **Import now**.

No API key is required. Users do not need to manage YAML, folders, tags, versions, or backlinks manually.

### ChatGPT plugin

The complete ChatGPT/Codex skill is included under `chatgpt-plugin/skills/obsidian-knowledge-forge/`. It formats conversations and generated documents, applies the knowledge schema, validates graph links, and produces the one-click `.ewforge` package.

### Safety

- No network requests and no telemetry in the Obsidian importer.
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

## 中文

### 第一版操作

1. 在 ChatGPT 完成討論或文件生成。
2. 使用「具象知識鍛造器」產生 `.ewforge` 檔案。
3. 在手機 Obsidian 點選左側功能列的開箱圖示。
4. 選擇 `.ewforge`，查看筆記數量與目的地後按「確認匯入」。

使用者不需要設定 API 金鑰，也不必自己處理 YAML、資料夾、標籤或雙向連結。

### ChatGPT 外掛

完整知識鍛造技能已放入 `chatgpt-plugin/skills/obsidian-knowledge-forge/`。它會整理聊天與生成文件、套用知識規範、驗證圖譜連結，最後產生可一鍵匯入的 `.ewforge` 知識包。

### 安全設計

- Obsidian 匯入器不會連線到網路，也不含遙測。
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

## Repository layout / 專案結構

- `src/main.js` — mobile-compatible Obsidian source / 手機相容原始碼
- `manifest.json` and `versions.json` — Obsidian release metadata / 發行資訊
- `styles.css` — touch-friendly bilingual interface / 雙語觸控介面
- `chatgpt-plugin/` — ChatGPT/Codex plugin with the knowledge-forging skill / 含知識鍛造技能的 ChatGPT 外掛
- `docs/EWFORGE-SPEC.md` — portable package format / 知識包格式
- `examples/` — valid example package and Markdown / 範例
- `tests/` — package validator and safety tests / 驗證測試
- `scripts/make-release.js` — installable release builder / 安裝包建置程式

## Trademark / 商標

The Embodied Worker name, elephant mark, and supplied artwork are trademarks or proprietary brand assets of Embodied Worker Co., Ltd. Their inclusion does not grant reuse rights.

Embodied Worker 名稱、金色大象圖樣及提供的商標素材，均為具象職人股份有限公司的商標或專有品牌資產；收錄於本專案不代表授權第三方使用。

