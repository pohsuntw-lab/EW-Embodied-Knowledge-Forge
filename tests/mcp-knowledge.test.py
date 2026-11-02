import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'plugins/ew-obsidian-knowledge-forge/skills/mcp-knowledge-forge'
spec = importlib.util.spec_from_file_location('knowledge_package', SKILL / 'scripts/knowledge_package.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.data = module.load_json(SKILL / 'assets/example.knowledge.json')
        self.rec = self.data['records'][0]

    def invalid(self, fragment):
        result = module.validate(self.data)
        self.assertFalse(result['valid'], result)
        self.assertTrue(any(fragment in x for x in result['errors']), result)

    def approve(self):
        self.rec['status'] = 'approved'
        self.rec['approval'] = {'status': 'approved', 'reviewer': 'SYNTHETIC TEST REVIEWER',
                                'reviewed_at': self.rec['updated_at'], 'evidence': 'SYNTHETIC TEST ONLY'}

    def test_candidate_valid_but_not_indexed(self):
        result = module.validate(self.data)
        self.assertTrue(result['valid'], result)
        self.assertEqual(result['index_count'], 0)

    def test_approval_evidence(self):
        self.approve()
        self.rec['approval']['evidence'] = None
        self.invalid('approval evidence')

    def test_duplicate_record(self):
        self.data['records'].append(copy.deepcopy(self.rec))
        self.invalid('duplicate knowledge ID')

    def test_duplicate_source(self):
        self.data['sources'].append(copy.deepcopy(self.data['sources'][0]))
        self.invalid('duplicate source ID')

    def test_missing_source(self):
        self.rec['source_refs'][0]['source_id'] = 'MISSING'
        self.invalid('missing source')

    def test_dangling_relation(self):
        self.rec['relations']['related'] = ['MISSING']
        self.invalid('missing relation')

    def test_self_relation(self):
        self.rec['relations']['related'] = [self.rec['knowledge_id']]
        self.invalid('self or missing')

    def test_hierarchy_cycle(self):
        second = copy.deepcopy(self.rec)
        second['knowledge_id'] = 'KN-002'
        second['relations']['up'] = ['KN-001']
        self.rec['relations']['up'] = ['KN-002']
        self.data['records'].append(second)
        self.invalid('cyclic up')

    def test_replaced_record_still_active(self):
        second = copy.deepcopy(self.rec)
        second['knowledge_id'] = 'KN-002'
        self.rec['relations']['replaces'] = ['KN-002']
        self.data['records'].append(second)
        self.invalid('remains active')

    def test_invalid_types(self):
        self.rec['version'] = True
        self.invalid('expected')

    def test_missing_body(self):
        del self.rec['body']
        self.invalid('body: missing')

    def test_blank_body(self):
        self.rec['body'] = '  '
        self.invalid('blank text')

    def test_legal_date_order(self):
        self.rec['legal'] = {'law_name': 'SYNTHETIC', 'article': '1', 'jurisdiction': 'TEST',
                             'effective_from': '2026-11-02', 'effective_until': '2026-01-01',
                             'verified_at': None}
        self.invalid('reversed validity')

    def test_invalid_date(self):
        self.rec['validity']['effective_from'] = '2026-02-30'
        self.invalid('invalid date')

    def test_timestamp_timezone(self):
        self.rec['updated_at'] = '2026-11-02T12:00:00'
        self.invalid('invalid date-time')

    def test_p3_cloud(self):
        self.rec['access']['classification'] = 'P3'
        self.invalid('P3 requires')

    def test_approved_partial_source(self):
        self.approve()
        self.data['sources'][0]['extraction_status'] = 'partial'
        self.invalid('unresolved source')

    def test_unlocated_candidate_warning(self):
        self.rec['source_refs'][0]['locator'] = {'kind': 'unlocated', 'value': None}
        result = module.validate(self.data)
        self.assertTrue(result['valid'])
        self.assertTrue(result['warnings'])
        self.approve()
        self.invalid('unresolved source')

    def test_stale_approval(self):
        self.approve()
        self.rec['updated_at'] = '2026-11-03T00:00:00+08:00'
        self.invalid('approval predates')

    def test_unknown_class_approved(self):
        self.approve()
        self.rec['access']['classification'] = 'unknown'
        self.invalid('unresolved source/access')

    def test_duplicate_json_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'bad.json'
            path.write_text('{"body": "a", "body": "b"}')
            with self.assertRaisesRegex(ValueError, 'duplicate JSON key'):
                module.load_json(path)

    def test_build_and_candidate_exclusion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'source.json'
            source.write_bytes(module.encode(self.data))
            module.build(source, root / 'candidate.zip')
            with zipfile.ZipFile(root / 'candidate.zip') as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(json.loads(archive.read('retrieval-index.json'))['records'], [])
            self.approve()
            source.write_bytes(module.encode(self.data))
            review = root / 'review'
            review.mkdir()
            (review / 'check.md').write_text('# Synthetic review\n')
            module.build(source, root / 'approved.zip', review)
            with zipfile.ZipFile(root / 'approved.zip') as archive:
                index = json.loads(archive.read('retrieval-index.json'))
                self.assertEqual(len(index['records']), 1)
                self.assertNotIn('body', index['records'][0])
                self.assertIn('access', index['records'][0])
                self.assertIn('review/check.md', archive.namelist())

    def test_failed_build_no_artifact(self):
        self.rec['status'] = 'approved'
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / 'source.json', Path(tmp) / 'out.zip'
            source.write_bytes(module.encode(self.data))
            with self.assertRaises(ValueError):
                module.build(source, output)
            self.assertFalse(output.exists())

    def test_review_symlink_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'source.json'
            source.write_bytes(module.encode(self.data))
            review = root / 'review'
            review.mkdir()
            (review / 'linked.md').symlink_to(source)
            with self.assertRaisesRegex(ValueError, 'symlinks'):
                module.build(source, root / 'out.zip', review)


if __name__ == '__main__':
    unittest.main()
