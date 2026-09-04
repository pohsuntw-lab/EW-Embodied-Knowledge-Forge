# Public listing / 公開頁面

## Name

EW_knowledge_forge

## Category

Productivity

## Short description

Forge chats for Obsidian

將聊天鍛造成 Obsidian 知識。

## Long description

EW_knowledge_forge turns conversations, generated documents, and uploaded source files into a validated Obsidian Vault. For complete projects, it works in bounded batches, delivers mergeable ZIP volumes, and maintains a compact `FORGE-CHECKPOINT.md` so a new ChatGPT conversation can continue without pretending to see the user's entire history at once.

Start in ChatGPT, download each validated Vault ZIP, extract all volumes into the same Vault folder, and open that folder in Obsidian. No Obsidian community plugin or separate API key is required.

具象知識鍛造器會把對話、生成文件與來源檔案整理成經驗證的 Obsidian Vault。完整專案會分批處理、交付可合併的 ZIP 分卷，並使用 `FORGE-CHECKPOINT.md` 讓新對話安全續作，不會假裝 ChatGPT 能一次看見全部歷史。

使用者在 ChatGPT 中逐批完成知識鍛造，下載並解壓各個 Vault ZIP 到同一資料夾，再由 Obsidian 開啟該資料夾。不需要 Obsidian 社群外掛或額外 API 金鑰。

## Workflow responsibilities / 流程分工

| | ChatGPT | Obsidian |
| --- | --- | --- |
| Role | Knowledge reasoning and forging | Local storage and graph materialization |
| Work | Extract, classify, link, version, and package | Validate, preview, write, back up, and protect conflicts |
| Data boundary | Uses only the chat and user-provided sources | Uses only the selected package and configured Vault root |
| Network | Runs in the user's existing ChatGPT environment | Offline importer; no network request |
| Additional API | No separate OpenAI API key or usage billing | None |

ChatGPT performs the knowledge reasoning; Obsidian remains the user-controlled knowledge repository. / ChatGPT 負責理解與鍛造，Obsidian 負責本機保存與形成知識圖譜。

## Publisher

Embodied Worker Co., Ltd. / 具象職人股份有限公司

## URLs

- Website: https://www.embodiedworker.com
- Support: https://github.com/pohsuntw-lab/EW-Embodied-Knowledge-Forge/blob/main/SUPPORT.md
- Privacy: https://github.com/pohsuntw-lab/EW-Embodied-Knowledge-Forge/blob/main/PRIVACY.md
- Terms: https://github.com/pohsuntw-lab/EW-Embodied-Knowledge-Forge/blob/main/TERMS.md

## Availability

Recommended: all countries and regions supported by the Plugins Directory where the publisher can provide English or Traditional Chinese support. Final selection remains a publisher decision in the submission portal.
