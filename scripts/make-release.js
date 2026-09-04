const fs = require("node:fs");
const path = require("node:path");
const { execFileSync } = require("node:child_process");

const root = path.resolve(__dirname, "..");
const manifest = JSON.parse(fs.readFileSync(path.join(root, "manifest.json"), "utf8"));
const dist = path.join(root, "dist");
fs.mkdirSync(dist, { recursive: true });
const output = path.join(dist, `ew-knowledge-forge-${manifest.version}.zip`);
if (fs.existsSync(output)) fs.unlinkSync(output);
const releaseMain = path.join(dist, "main.js");
fs.copyFileSync(path.join(root, "src", "main.js"), releaseMain);
execFileSync("zip", ["-j", "-9", output, "manifest.json", releaseMain, "styles.css"], {
  cwd: root,
  stdio: "inherit",
});
fs.unlinkSync(releaseMain);
console.log(output);
