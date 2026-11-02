const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const pluginRoot = path.join(root, "plugins", "ew-obsidian-knowledge-forge");
const manifest = JSON.parse(fs.readFileSync(path.join(pluginRoot, ".codex-plugin", "plugin.json"), "utf8"));
const skill = fs.readFileSync(path.join(pluginRoot, "skills", "obsidian-knowledge-forge", "SKILL.md"), "utf8");
const enterpriseSkill = fs.readFileSync(path.join(pluginRoot, "skills", "enterprise-secure-knowledge-forge", "SKILL.md"), "utf8");
const tests = fs.readFileSync(path.join(root, "submission", "TEST_CASES.md"), "utf8");

assert.equal(manifest.version, "0.7.1");
assert.equal(manifest.interface.defaultPrompt.length, 3);
assert.match(manifest.interface.defaultPrompt[0], /Obsidian/);
assert.match(manifest.interface.defaultPrompt[1], /FORGE-CHECKPOINT/);
assert.match(manifest.interface.defaultPrompt[2], /MCP knowledge-base JSON/);
assert.ok(fs.existsSync(path.join(pluginRoot, "skills", "mcp-knowledge-forge", "SKILL.md")));
assert.equal(manifest.interface.displayName, "EW_knowledge_forge");
assert.ok(manifest.interface.displayName.length <= 30, "OpenAI plugin name must be at most 30 characters");
assert.ok(manifest.interface.shortDescription.length <= 30, "OpenAI subtitle must be at most 30 characters");
assert.ok(manifest.interface.defaultPrompt.length <= 3, "OpenAI accepts at most three default prompts");
assert.equal(manifest.skills, "./skills/");
assert.ok(!Object.hasOwn(manifest, "mcpServers"));
assert.ok(!fs.existsSync(path.join(pluginRoot, ".mcp.json")));
assert.match(skill, /FORGE-CHECKPOINT\.md/);
assert.match(skill, /Obsidian Vault ZIP/);
assert.match(enterpriseSkill, /classify before content/i);
assert.match(enterpriseSkill, /P3: local-only/);
assert.match(enterpriseSkill, /not endpoint DLP/i);
assert.equal((tests.match(/^### P\d/gm) || []).length, 8);
assert.equal((tests.match(/^### N\d/gm) || []).length, 7);

for (const required of ["PRIVACY.md", "TERMS.md", "SUPPORT.md", "submission/LISTING.md", "submission/STARTER_PROMPTS.md", "submission/RELEASE_NOTES.md"]) {
  assert.ok(fs.existsSync(path.join(root, required)), `Missing ${required}`);
}

console.log("Validated public skills-only plugin and OpenAI submission materials.");

assert.equal(manifest.interface.websiteURL, "https://www.embodiedworker.com");
assert.equal(manifest.interface.supportURL, "https://www.embodiedworker.com/support");
assert.equal(manifest.interface.privacyPolicyURL, "https://www.embodiedworker.com/privacy");
assert.equal(manifest.interface.termsOfServiceURL, "https://www.embodiedworker.com/terms");

for (const [index, prompt] of manifest.interface.defaultPrompt.entries()) {
  assert.ok(prompt.length <= 128, `Conversation starter ${index + 1} exceeds 128 characters`);
}
assert.deepEqual(JSON.parse(fs.readFileSync(path.join(root, ".codex-plugin", "plugin.json"), "utf8")), manifest);
