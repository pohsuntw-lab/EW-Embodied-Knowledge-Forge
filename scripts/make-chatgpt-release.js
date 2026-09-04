const fs = require("node:fs");
const path = require("node:path");
const { execFileSync } = require("node:child_process");

const root = path.resolve(__dirname, "..");
const pluginRoot = path.join(root, "plugins", "ew-obsidian-knowledge-forge");
const manifest = JSON.parse(fs.readFileSync(path.join(pluginRoot, ".codex-plugin", "plugin.json"), "utf8"));
const dist = path.join(root, "dist");
fs.mkdirSync(dist, { recursive: true });
const output = path.join(dist, `ew-embodied-knowledge-forge-chatgpt-${manifest.version}.zip`);
if (fs.existsSync(output)) fs.unlinkSync(output);
execFileSync("zip", ["-r", "-9", output, ".", "-x", "*/__pycache__/*", "*.pyc"], {
  cwd: pluginRoot,
  stdio: "inherit",
});
console.log(output);
