const {
  Modal,
  Notice,
  Plugin,
  PluginSettingTab,
  Setting,
  TFile,
  normalizePath,
} = require("obsidian");

const DEFAULT_SETTINGS = {
  language: "auto",
  knowledgeRoot: "EW-Knowledge",
  keepBackups: true,
};

const I18N = {
  "zh-TW": {
    name: "EW 具象知識鍛造器",
    subtitle: "把 ChatGPT 生成文件一鍵匯入 Obsidian 知識圖譜",
    import: "選取 EW 知識包",
    choose: "從『檔案』選擇 .ewforge",
    ready: "知識包已驗證，可以安全匯入。",
    confirm: "確認匯入",
    cancel: "取消",
    invalid: "無法讀取知識包",
    complete: "知識匯入完成",
    settings: "EW 具象知識鍛造器",
    language: "介面語言",
    languageDesc: "自動依裝置語言顯示，或固定使用中文／英文。",
    root: "知識根目錄",
    rootDesc: "所有匯入內容只會寫入這個 Vault 目錄。",
    backups: "更新前保留備份",
    backupsDesc: "更新 EW 管理的同一知識時，先在 99-System/Backups 保存舊版。",
    command: "匯入 EW 知識包",
    summary: "匯入預覽",
    notes: "筆記",
    attachments: "附件",
    destination: "目的地",
    type: "類型",
    incremental: "增量更新",
    full: "完整匯入",
    importing: "正在匯入…",
    created: "新增",
    updated: "更新",
    skipped: "略過",
    conflicts: "衝突副本",
    privacy: "此外掛不連網；只在你的 Vault 內驗證與匯入檔案。",
  },
  en: {
    name: "EW Embodied Knowledge Forge",
    subtitle: "Import ChatGPT-generated documents into an Obsidian knowledge graph in one step",
    import: "Choose EW Knowledge Package",
    choose: "Choose a .ewforge file from Files",
    ready: "The package is valid and ready for a safe import.",
    confirm: "Import now",
    cancel: "Cancel",
    invalid: "Could not read the knowledge package",
    complete: "Knowledge import complete",
    settings: "EW Embodied Knowledge Forge",
    language: "Interface language",
    languageDesc: "Follow the device language or always use Chinese/English.",
    root: "Knowledge root",
    rootDesc: "All imported content stays inside this Vault folder.",
    backups: "Back up before update",
    backupsDesc: "Before updating the same EW-managed knowledge, preserve its prior version in 99-System/Backups.",
    command: "Import EW Knowledge Package",
    summary: "Import preview",
    notes: "Notes",
    attachments: "Attachments",
    destination: "Destination",
    type: "Type",
    incremental: "Incremental update",
    full: "Full import",
    importing: "Importing…",
    created: "Created",
    updated: "Updated",
    skipped: "Skipped",
    conflicts: "Conflict copies",
    privacy: "This plugin makes no network requests; it only validates and imports inside your Vault.",
  },
};

function languageFor(settings) {
  if (settings.language === "zh-TW" || settings.language === "en") return settings.language;
  const language = (globalThis.navigator?.language || "en").toLowerCase();
  return language.startsWith("zh") ? "zh-TW" : "en";
}

function t(settings, key) {
  return I18N[languageFor(settings)][key] || key;
}

function safeRoot(value) {
  const root = normalizePath(String(value || "EW-Knowledge").trim().replace(/^\/+|\/+$/g, ""));
  if (!root || root === "." || root.startsWith(".") || root.includes("..") || root.includes(".obsidian")) {
    throw new Error("Unsafe knowledge root");
  }
  return root;
}

function safeRelativePath(value, allowedExtensions) {
  const raw = String(value || "").replace(/\\/g, "/").trim();
  const path = normalizePath(raw.replace(/^\/+/, ""));
  const parts = path.split("/");
  if (!path || raw.startsWith("/") || parts.includes("..") || parts.some((part) => !part || part.startsWith("."))) {
    throw new Error(`Unsafe path: ${value}`);
  }
  const lower = path.toLowerCase();
  if (lower.includes(".obsidian") || !allowedExtensions.some((ext) => lower.endsWith(ext))) {
    throw new Error(`Unsupported path: ${value}`);
  }
  return path;
}

function parseScalar(content, key) {
  const frontmatter = content.match(/^---\s*\n([\s\S]*?)\n---(?:\s*\n|$)/);
  if (!frontmatter) return null;
  const match = frontmatter[1].match(new RegExp(`^${key}:\\s*(.+?)\\s*$`, "m"));
  return match ? match[1].trim().replace(/^['"]|['"]$/g, "") : null;
}

function semver(value) {
  const match = String(value || "0.0.0").match(/^(\d+)\.(\d+)\.(\d+)$/);
  return match ? match.slice(1).map(Number) : [0, 0, 0];
}

function compareVersion(a, b) {
  const aa = semver(a);
  const bb = semver(b);
  for (let i = 0; i < 3; i += 1) {
    if (aa[i] !== bb[i]) return aa[i] - bb[i];
  }
  return 0;
}

function bytesFromBase64(value) {
  const decoded = globalThis.atob(value);
  const bytes = new Uint8Array(decoded.length);
  for (let i = 0; i < decoded.length; i += 1) bytes[i] = decoded.charCodeAt(i);
  return bytes.buffer;
}

async function sha256Text(text) {
  const bytes = new TextEncoder().encode(text);
  const digest = await globalThis.crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest)).map((x) => x.toString(16).padStart(2, "0")).join("");
}

function validatePackage(pkg) {
  if (!pkg || pkg.format !== "ew-knowledge-forge" || !String(pkg.format_version || "").startsWith("1.")) {
    throw new Error("Unsupported EW Knowledge Package format");
  }
  if (!Array.isArray(pkg.notes) || !Array.isArray(pkg.attachments || [])) {
    throw new Error("Package entries are missing");
  }
  if (pkg.notes.length > 500 || (pkg.attachments || []).length > 100) {
    throw new Error("Package is too large for mobile import");
  }
  const ids = new Set();
  for (const note of pkg.notes) {
    safeRelativePath(note.path, [".md"]);
    if (!note.knowledge_id || ids.has(note.knowledge_id)) throw new Error("Duplicate or missing knowledge_id");
    if (parseScalar(note.content, "knowledge_id") !== note.knowledge_id) throw new Error(`knowledge_id mismatch: ${note.path}`);
    if (String(parseScalar(note.content, "ew_managed")).toLowerCase() !== "true") throw new Error(`Not EW-managed: ${note.path}`);
    ids.add(note.knowledge_id);
  }
  for (const attachment of pkg.attachments || []) {
    safeRelativePath(attachment.path, [".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".docx", ".xlsx", ".pptx", ".txt", ".csv"]);
    if (attachment.encoding !== "base64" || typeof attachment.data !== "string") throw new Error("Unsupported attachment encoding");
  }
  return pkg;
}

class ImportModal extends Modal {
  constructor(app, plugin) {
    super(app);
    this.plugin = plugin;
    this.pkg = null;
  }

  onOpen() {
    this.renderChooser();
  }

  renderBrand(container) {
    const brand = container.createDiv({ cls: "ew-forge-brand" });
    brand.createEl("img", { attr: { src: this.plugin.logoDataUrl, alt: "Embodied Worker" } });
    const copy = brand.createDiv();
    copy.createEl("h2", { text: t(this.plugin.settings, "name") });
    copy.createEl("p", { text: t(this.plugin.settings, "subtitle") });
  }

  renderChooser() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.addClass("ew-forge-modal");
    this.renderBrand(contentEl);
    const drop = contentEl.createDiv({ cls: "ew-forge-drop" });
    drop.createEl("p", { text: t(this.plugin.settings, "choose") });
    const input = drop.createEl("input", {
      type: "file",
      cls: "ew-forge-file-input",
      attr: { accept: ".ewforge,application/json" },
    });
    const button = drop.createEl("button", { text: t(this.plugin.settings, "import"), cls: "mod-cta" });
    button.addEventListener("click", () => input.click());
    input.addEventListener("change", async () => {
      try {
        const file = input.files?.[0];
        if (!file) return;
        if (file.size > 40 * 1024 * 1024) throw new Error("Package exceeds 40 MB");
        this.pkg = validatePackage(JSON.parse(await file.text()));
        this.renderPreview();
      } catch (error) {
        new Notice(`${t(this.plugin.settings, "invalid")}: ${error.message}`);
      }
    });
    contentEl.createEl("p", { text: t(this.plugin.settings, "privacy"), cls: "setting-item-description" });
  }

  renderPreview() {
    const { contentEl } = this;
    contentEl.empty();
    this.renderBrand(contentEl);
    contentEl.createEl("p", { text: t(this.plugin.settings, "ready"), cls: "ew-forge-success" });
    const summary = contentEl.createDiv({ cls: "ew-forge-summary" });
    summary.createEl("h3", { text: this.pkg.title || t(this.plugin.settings, "summary") });
    const list = summary.createEl("ul");
    list.createEl("li", { text: `${t(this.plugin.settings, "notes")}: ${this.pkg.notes.length}` });
    list.createEl("li", { text: `${t(this.plugin.settings, "attachments")}: ${(this.pkg.attachments || []).length}` });
    list.createEl("li", { text: `${t(this.plugin.settings, "destination")}: ${safeRoot(this.plugin.settings.knowledgeRoot)}` });
    list.createEl("li", { text: `${t(this.plugin.settings, "type")}: ${this.pkg.package_type === "full-import" ? t(this.plugin.settings, "full") : t(this.plugin.settings, "incremental")}` });
    const actions = contentEl.createDiv({ cls: "ew-forge-actions" });
    const confirm = actions.createEl("button", { text: t(this.plugin.settings, "confirm"), cls: "mod-cta" });
    actions.createEl("button", { text: t(this.plugin.settings, "cancel") }).addEventListener("click", () => this.close());
    confirm.addEventListener("click", async () => {
      confirm.disabled = true;
      confirm.setText(t(this.plugin.settings, "importing"));
      try {
        const receipt = await this.plugin.importPackage(this.pkg);
        this.close();
        new Notice(`${t(this.plugin.settings, "complete")} · ${t(this.plugin.settings, "created")} ${receipt.created} · ${t(this.plugin.settings, "updated")} ${receipt.updated} · ${t(this.plugin.settings, "skipped")} ${receipt.skipped} · ${t(this.plugin.settings, "conflicts")} ${receipt.conflicts}`, 10000);
      } catch (error) {
        confirm.disabled = false;
        confirm.setText(t(this.plugin.settings, "confirm"));
        new Notice(`${t(this.plugin.settings, "invalid")}: ${error.message}`, 10000);
      }
    });
  }

  onClose() {
    this.contentEl.empty();
  }
}

class ForgeSettingsTab extends PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display() {
    const { containerEl } = this;
    containerEl.empty();
    new Setting(containerEl).setName(t(this.plugin.settings, "settings")).setHeading();

    new Setting(containerEl)
      .setName(t(this.plugin.settings, "language"))
      .setDesc(t(this.plugin.settings, "languageDesc"))
      .addDropdown((dropdown) => dropdown
        .addOption("auto", "Auto / 自動")
        .addOption("zh-TW", "繁體中文")
        .addOption("en", "English")
        .setValue(this.plugin.settings.language)
        .onChange(async (value) => {
          this.plugin.settings.language = value;
          await this.plugin.saveSettings();
          this.display();
        }));

    new Setting(containerEl)
      .setName(t(this.plugin.settings, "root"))
      .setDesc(t(this.plugin.settings, "rootDesc"))
      .addText((text) => text
        .setPlaceholder("EW-Knowledge")
        .setValue(this.plugin.settings.knowledgeRoot)
        .onChange(async (value) => {
          try {
            this.plugin.settings.knowledgeRoot = safeRoot(value);
            await this.plugin.saveSettings();
          } catch (_) {
            new Notice("Invalid knowledge root");
          }
        }));

    new Setting(containerEl)
      .setName(t(this.plugin.settings, "backups"))
      .setDesc(t(this.plugin.settings, "backupsDesc"))
      .addToggle((toggle) => toggle
        .setValue(this.plugin.settings.keepBackups)
        .onChange(async (value) => {
          this.plugin.settings.keepBackups = value;
          await this.plugin.saveSettings();
        }));
  }
}

module.exports = class EWKnowledgeForgePlugin extends Plugin {
  async onload() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    this.logoDataUrl = "data:image/svg+xml," + encodeURIComponent("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='%23b89b5e'/><path d='M13 34V22c0-8 7-13 15-13 9 0 16 7 16 16v21H34v-8c0-5-8-5-8 0v8H13V34zm31-12c7 0 10 5 10 11v8' fill='none' stroke='%23131720' stroke-width='5' stroke-linecap='round'/><circle cx='22' cy='24' r='2.5' fill='%23131720'/></svg>");

    this.addRibbonIcon("package-open", t(this.settings, "name"), () => new ImportModal(this.app, this).open());
    this.addCommand({
      id: "import-ew-knowledge-package",
      name: t(this.settings, "command"),
      callback: () => new ImportModal(this.app, this).open(),
    });
    this.addSettingTab(new ForgeSettingsTab(this.app, this));
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }

  async ensureFolder(folderPath) {
    const parts = normalizePath(folderPath).split("/");
    let current = "";
    for (const part of parts) {
      current = current ? `${current}/${part}` : part;
      if (!this.app.vault.getAbstractFileByPath(current)) await this.app.vault.createFolder(current);
    }
  }

  async ensureParent(filePath) {
    const parent = filePath.split("/").slice(0, -1).join("/");
    if (parent) await this.ensureFolder(parent);
  }

  uniquePath(path, marker = "conflict") {
    const stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15);
    const dot = path.toLowerCase().lastIndexOf(".md");
    const base = dot >= 0 ? path.slice(0, dot) : path;
    const ext = dot >= 0 ? path.slice(dot) : "";
    let candidate = `${base}-${marker}-${stamp}${ext}`;
    let number = 2;
    while (this.app.vault.getAbstractFileByPath(candidate)) {
      candidate = `${base}-${marker}-${stamp}-${number}${ext}`;
      number += 1;
    }
    return candidate;
  }

  async verifyHashes(pkg) {
    for (const note of pkg.notes) {
      if (note.sha256 && await sha256Text(note.content) !== String(note.sha256).toLowerCase()) {
        throw new Error(`Checksum mismatch: ${note.path}`);
      }
    }
  }

  async backup(path, content) {
    if (!this.settings.keepBackups) return;
    const stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15);
    const backupPath = normalizePath(`${safeRoot(this.settings.knowledgeRoot)}/99-System/Backups/${stamp}/${path}`);
    await this.ensureParent(backupPath);
    await this.app.vault.create(backupPath, content);
  }

  async importPackage(rawPackage) {
    const pkg = validatePackage(rawPackage);
    await this.verifyHashes(pkg);
    const root = safeRoot(this.settings.knowledgeRoot);
    await this.ensureFolder(root);
    const receipt = { created: 0, updated: 0, skipped: 0, conflicts: 0 };

    for (const note of pkg.notes) {
      const relative = safeRelativePath(note.path, [".md"]);
      const targetPath = normalizePath(`${root}/${relative}`);
      const existing = this.app.vault.getAbstractFileByPath(targetPath);
      if (!existing) {
        await this.ensureParent(targetPath);
        await this.app.vault.create(targetPath, note.content);
        receipt.created += 1;
        continue;
      }
      if (!(existing instanceof TFile)) throw new Error(`Destination is not a file: ${targetPath}`);
      const current = await this.app.vault.read(existing);
      if (current === note.content) {
        receipt.skipped += 1;
        continue;
      }
      const currentId = parseScalar(current, "knowledge_id");
      const currentVersion = parseScalar(current, "version");
      const managed = String(parseScalar(current, "ew_managed")).toLowerCase() === "true";
      if (managed && currentId === note.knowledge_id && compareVersion(note.version, currentVersion) > 0) {
        await this.backup(relative, current);
        await this.app.vault.process(existing, () => note.content);
        receipt.updated += 1;
      } else {
        const conflictPath = this.uniquePath(targetPath);
        await this.ensureParent(conflictPath);
        await this.app.vault.create(conflictPath, note.content);
        receipt.conflicts += 1;
      }
    }

    for (const attachment of pkg.attachments || []) {
      const relative = safeRelativePath(attachment.path, [".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".docx", ".xlsx", ".pptx", ".txt", ".csv"]);
      const targetPath = normalizePath(`${root}/${relative}`);
      const existing = this.app.vault.getAbstractFileByPath(targetPath);
      if (existing) {
        receipt.skipped += 1;
        continue;
      }
      await this.ensureParent(targetPath);
      await this.app.vault.createBinary(targetPath, bytesFromBase64(attachment.data));
      receipt.created += 1;
    }
    return receipt;
  }
};
