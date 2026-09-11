# EW_knowledge_forge v0.5.0

## Enterprise Secure Forge

This release adds a separate `enterprise-secure-knowledge-forge` skill while preserving the existing personal and complete-project forge.

- Classifies source metadata P0-P3 before requesting source body content.
- Routes work to approved cloud, locally sanitized cloud, local-only, or blocked states.
- Keeps P2 originals and rehydration maps local; P3 is local-only.
- Warns when content is already visible and cannot be protected retroactively.
- Separates candidate knowledge from human-approved published knowledge.
- Adds security intake, source, and approval registers plus `FORGE-MANIFEST.json`.
- Adds deterministic structure and representative secret-pattern validation.
- States explicitly that the ChatGPT skill is governance and packaging control, not endpoint DLP or compliance certification.

## 企業安全知識鍛造

本版在保留既有個人版與完整專案鍛造流程的前提下，新增獨立的 `enterprise-secure-knowledge-forge` Skill。

- 在索取來源正文前，先以來源資訊完成 P0-P3 分級。
- 將工作路由為核准雲端、本地脫敏後上雲、完全本地或暫停處理。
- P2 原文與還原對照表留在本地；P3 僅能本地處理。
- 如果內容已出現在對話中，明確說明無法追溯保護。
- 將候選知識與經人員核准的正式知識分開。
- 新增安全受理、來源、核准清冊及 `FORGE-MANIFEST.json`。
- 新增結構及代表性機密格式的確定性驗證。
- 明確說明 ChatGPT Skill 是治理與封裝控制，不是端點 DLP 或合規認證。
