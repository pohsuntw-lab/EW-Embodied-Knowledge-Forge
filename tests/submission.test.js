const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const pluginRoot = path.join(root, "plugins", "ew-obsidian-knowledge-forge");
const manifest = JSON.parse(fs.readFileSync(path.join(pluginRoot, ".codex-plugin", "plugin.json"), "utf8"));
const skill = fs.readFileSync(path.join(pluginRoot, "skills", "obsidian-knowledge-forge", "SKILL.md"), "utf8");
const tests = fs.readFileSync(path.join(root, "submission", "TEST_CASES.md"), "utf8");

assert.equal(manifest.version, "0.4.0");
assert.equal(manifest.interface.displayName, "EW_knowledge_forge");
assert.ok(manifest.interface.displayName.length <= 30, "OpenAI plugin name must be at most 30 characters");
assert.ok(manifest.interface.shortDescription.length <= 30, "OpenAI subtitle must be at most 30 characters");
assert.ok(manifest.interface.defaultPrompt.length <= 3, "OpenAI accepts at most three default prompts");
assert.equal(manifest.skills, "./skills/");
assert.ok(!Object.hasOwn(manifest, "mcpServers"));
assert.ok(!fs.existsSync(path.join(pluginRoot, ".mcp.json")));
assert.match(skill, /FORGE-CHECKPOINT\.md/);
assert.match(skill, /Obsidian Vault ZIP/);
assert.equal((tests.match(/^### P\d/gm) || []).length, 5);
assert.equal((tests.match(/^### N\d/gm) || []).length, 3);

for (const required of ["PRIVACY.md", "TERMS.md", "SUPPORT.md", "submission/LISTING.md", "submission/STARTER_PROMPTS.md", "submission/RELEASE_NOTES.md"]) {
  assert.ok(fs.existsSync(path.join(root, required)), `Missing ${required}`);
}

console.log("Validated public skills-only plugin and OpenAI submission materials.");
