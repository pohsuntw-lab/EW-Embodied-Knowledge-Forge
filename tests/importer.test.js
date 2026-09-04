const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const Module = require("node:module");
const path = require("node:path");

class TFile {
  constructor(filePath, data = "") {
    this.path = filePath;
    this.data = data;
  }
}
class Plugin {}
class Modal {}
class PluginSettingTab {}
class Setting {}
class Notice {}

const originalLoad = Module._load;
Module._load = function load(request, parent, isMain) {
  if (request === "obsidian") {
    return {
      Modal,
      Notice,
      Plugin,
      PluginSettingTab,
      Setting,
      TFile,
      normalizePath: (value) => value.replace(/\\/g, "/").replace(/\/{2,}/g, "/").replace(/^\.\//, ""),
    };
  }
  return originalLoad(request, parent, isMain);
};
const ForgePlugin = require("../src/main.js");
Module._load = originalLoad;

class MemoryVault {
  constructor() {
    this.files = new Map();
    this.folders = new Set();
  }
  getAbstractFileByPath(filePath) { return this.files.get(filePath) || (this.folders.has(filePath) ? { path: filePath } : null); }
  async createFolder(folderPath) { this.folders.add(folderPath); }
  async create(filePath, content) { const file = new TFile(filePath, content); this.files.set(filePath, file); return file; }
  async createBinary(filePath, content) { const file = new TFile(filePath, content); this.files.set(filePath, file); return file; }
  async read(file) { return file.data; }
  async process(file, change) { file.data = change(file.data); }
}

function hash(content) {
  return crypto.createHash("sha256").update(content, "utf8").digest("hex");
}

(async () => {
  const root = path.resolve(__dirname, "..");
  const pkg = JSON.parse(fs.readFileSync(path.join(root, "examples", "welcome.ewforge"), "utf8"));
  const plugin = new ForgePlugin();
  plugin.settings = { language: "en", knowledgeRoot: "EW-Knowledge", keepBackups: true };
  plugin.app = { vault: new MemoryVault() };

  const first = await plugin.importPackage(pkg);
  assert.deepEqual(first, { created: 2, updated: 0, skipped: 0, conflicts: 0 });
  const second = await plugin.importPackage(pkg);
  assert.deepEqual(second, { created: 0, updated: 0, skipped: 2, conflicts: 0 });

  const update = JSON.parse(JSON.stringify(pkg));
  update.notes = [update.notes[1]];
  update.notes[0].version = "1.1.0";
  update.notes[0].content = update.notes[0].content
    .replace("version: 1.0.0", "version: 1.1.0")
    .replace("searchable Obsidian note.", "searchable Obsidian note with a tested update.");
  update.notes[0].sha256 = hash(update.notes[0].content);
  const third = await plugin.importPackage(update);
  assert.equal(third.updated, 1);
  assert.ok(Array.from(plugin.app.vault.files.keys()).some((item) => item.includes("99-System/Backups")));

  const conflict = JSON.parse(JSON.stringify(update));
  conflict.notes[0].knowledge_id = "different-knowledge-id";
  conflict.notes[0].content = conflict.notes[0].content.replace(/knowledge_id: ew-welcome-note/, "knowledge_id: different-knowledge-id");
  conflict.notes[0].sha256 = hash(conflict.notes[0].content);
  const fourth = await plugin.importPackage(conflict);
  assert.equal(fourth.conflicts, 1);
  assert.ok(Array.from(plugin.app.vault.files.keys()).some((item) => item.includes("-conflict-")));

  console.log("Validated create, idempotent skip, managed update backup, and unmanaged conflict behavior.");
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
