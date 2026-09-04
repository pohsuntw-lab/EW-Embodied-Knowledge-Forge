const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const pkgPath = path.join(root, "examples", "welcome.ewforge");
const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));

assert.equal(pkg.format, "ew-knowledge-forge");
assert.match(pkg.format_version, /^1\./);
assert.ok(pkg.notes.length > 0);

const ids = new Set();
for (const note of pkg.notes) {
  assert.match(note.path, /^[^/.][^\\]*\.md$/);
  assert.ok(!note.path.split("/").includes(".."));
  assert.ok(!note.path.toLowerCase().includes(".obsidian"));
  assert.ok(!ids.has(note.knowledge_id));
  ids.add(note.knowledge_id);
  assert.match(note.content, /^---\n/);
  assert.match(note.content, /\new_managed: true\n/);
  assert.match(note.content, new RegExp(`\\nknowledge_id: ${note.knowledge_id}\\n`));
  assert.equal(crypto.createHash("sha256").update(note.content, "utf8").digest("hex"), note.sha256);
}

const source = fs.readFileSync(path.join(root, "src", "main.js"), "utf8");
assert.ok(!/require\(["'](?:fs|path|http|https|electron|child_process)["']\)/.test(source));
assert.ok(!/\bfetch\s*\(/.test(source));
assert.ok(!/requestUrl\s*\(/.test(source));
assert.ok(!/\.style\.[A-Za-z]+\s*=/.test(source));
console.log(`Validated ${pkg.notes.length} example note(s) and mobile-safe runtime boundaries.`);
