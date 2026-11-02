# Public listing / 公開頁面

## Name

EW_knowledge_forge

## Category

Productivity

## Short description

Forge governed knowledge

將個人與企業資料鍛造成可治理知識。

## Long description

EW_knowledge_forge turns conversations, generated documents, and uploaded source files into a validated Obsidian Vault. For complete projects, it works in bounded batches, delivers mergeable ZIP volumes, and maintains a compact `FORGE-CHECKPOINT.md` so a new ChatGPT conversation can continue without pretending to see the user's entire history at once.

For enterprise work, the separate Enterprise Secure Forge skill classifies source metadata before requesting contents, routes P0-P3 material to an approved cloud, sanitized-cloud, local-only, or blocked path, separates candidate from approved knowledge, and emits governance registers plus an auditable Forge Manifest. It is a governance and packaging control, not endpoint DLP, and cannot retroactively protect content already supplied to an AI service.

Start in ChatGPT, download each validated Vault ZIP, extract all volumes into the same Vault folder, and open that folder in Obsidian. No Obsidian community plugin or separate API key is required.

具象知識鍛造器會把對話、生成文件與來源檔案整理成經驗證的 Obsidian Vault。完整專案會分批處理、交付可合併的 ZIP 分卷，並使用 `FORGE-CHECKPOINT.md` 讓新對話安全續作，不會假裝 ChatGPT 能一次看見全部歷史。

企業工作使用獨立的 Enterprise Secure Forge Skill：先以來源資訊完成分級，再決定 P0-P3 資料應走核准雲端、本地脫敏後上雲、完全本地或暫停處理；候選知識與正式知識分開，並產生治理清冊及可稽核 Forge Manifest。此功能是治理與封裝控制，不是端點 DLP，也無法追溯保護已提交給 AI 服務的內容。

使用者在 ChatGPT 中逐批完成知識鍛造，下載並解壓各個 Vault ZIP 到同一資料夾，再由 Obsidian 開啟該資料夾。不需要 Obsidian 社群外掛或額外 API 金鑰。

## Workflow responsibilities / 流程分工

| | ChatGPT | Obsidian |
| --- | --- | --- |
| Role | Knowledge reasoning and forging | Local storage and graph materialization |
| Work | Classify routes; extract, link, version, approve, and package | Validate, preview, write, back up, and protect conflicts |
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


## v0.7.0 addition / 新增

Third starter: Build MCP knowledge-base JSON from my documents. / 將我的文件鍛造成 MCP 知識庫 JSON。 Existing Obsidian forging and continuation remain available; enterprise governance applies to both output paths. The new skill produces validated EW-contract JSON and review Markdown for backend integration, without deploying an MCP server. / 新增文件轉 MCP 知識 JSON，保留 Obsidian 與企業治理功能；產製文件，不代表已連接伺服器。
