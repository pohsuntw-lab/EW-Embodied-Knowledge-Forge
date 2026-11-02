#!/usr/bin/env python3
"""Validate/build EW knowledge interchange packages using Python's standard library.

The schema walker implements only keywords used by the bundled contract. It is
not a general JSON Schema implementation. Unsupported keywords fail closed.
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
SCHEMA = ASSETS / 'knowledge.schema.json'


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f'duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f'invalid constant: {x}')))


def timestamp(value):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', value):
        raise ValueError('timezone-bearing timestamp required')
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00'))


def shape(value, schema, path, errors):
    supported = {'$schema', 'type', 'properties', 'required', 'additionalProperties',
                 'items', 'minItems', 'uniqueItems', 'minLength', 'pattern', 'enum',
                 'const', 'format', 'minimum'}
    unknown = set(schema) - supported
    if unknown:
        errors.append(f'{path}: unsupported schema keywords {sorted(unknown)}')
        return
    types = schema.get('type', [])
    types = [types] if isinstance(types, str) else types
    checks = {'object': lambda x: isinstance(x, dict), 'array': lambda x: isinstance(x, list),
              'string': lambda x: isinstance(x, str), 'null': lambda x: x is None,
              'integer': lambda x: type(x) is int}
    if types and not any(checks[t](value) for t in types):
        errors.append(f'{path}: expected {types}')
        return
    if 'const' in schema and value != schema['const']:
        errors.append(f'{path}: incorrect contract value')
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{path}: unsupported value')
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value:
                errors.append(f'{path}.{key}: missing')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            for key in value.keys() - props.keys():
                errors.append(f'{path}.{key}: unexpected field')
        for key in value.keys() & props.keys():
            shape(value[key], props[key], f'{path}.{key}', errors)
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            errors.append(f'{path}: too few items')
        if schema.get('uniqueItems') and len({json.dumps(x, sort_keys=True, ensure_ascii=False) for x in value}) != len(value):
            errors.append(f'{path}: duplicate items')
        for i, item in enumerate(value):
            shape(item, schema.get('items', {}), f'{path}[{i}]', errors)
    if isinstance(value, str):
        if 'minLength' in schema and (len(value) < schema['minLength'] or not value.strip()):
            errors.append(f'{path}: blank text')
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            errors.append(f'{path}: invalid pattern')
        try:
            if schema.get('format') == 'date':
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                    raise ValueError('date must use YYYY-MM-DD')
                dt.date.fromisoformat(value)
            elif schema.get('format') == 'date-time':
                timestamp(value)
        except ValueError:
            errors.append(f'{path}: invalid {schema["format"]}')
    if type(value) is int and value < schema.get('minimum', value):
        errors.append(f'{path}: below minimum')


def validate(data):
    errors, warnings = [], []
    shape(data, load_json(SCHEMA), '$', errors)
    if errors:
        return {'valid': False, 'errors': errors, 'warnings': warnings, 'record_count': 0, 'index_count': 0}
    sources, records = {}, {}
    for src in data['sources']:
        sid = src['source_id']
        if sid in sources:
            errors.append(f'{sid}: duplicate source ID')
        sources[sid] = src
        if src['extraction_status'] != 'complete' or src['warnings']:
            warnings.append(f'{sid}: extraction incomplete or source warnings present')
    for rec in data['records']:
        kid = rec['knowledge_id']
        if kid in records:
            errors.append(f'{kid}: duplicate knowledge ID')
        records[kid] = rec
    for kid, rec in records.items():
        if timestamp(rec['updated_at']) < timestamp(rec['created_at']):
            errors.append(f'{kid}: updated_at precedes created_at')
        for field in ['validity', 'legal']:
            period = rec[field]
            if not period:
                continue
            if period['effective_from'] and period['effective_until'] and period['effective_until'] < period['effective_from']:
                errors.append(f'{kid}.{field}: reversed validity period')
        if rec['legal'] and (rec['legal']['effective_from'] is None or rec['legal']['verified_at'] is None):
            warnings.append(f'{kid}: legal validity or verification date unknown')
        uncertain = False
        for ref in rec['source_refs']:
            src = sources.get(ref['source_id'])
            if src is None:
                errors.append(f'{kid}: missing source {ref["source_id"]}')
            elif src['extraction_status'] != 'complete' or src['warnings']:
                uncertain = True
            loc = ref['locator']
            if loc['kind'] == 'unlocated':
                uncertain = True
                if loc['value'] is not None:
                    errors.append(f'{kid}: unlocated reference must use null value')
                warnings.append(f'{kid}: source location unknown')
            elif loc['value'] is None:
                errors.append(f'{kid}: source location required')
        access, approval = rec['access'], rec['approval']
        if access['classification'] == 'unknown':
            warnings.append(f'{kid}: classification unresolved')
        if access['classification'] == 'P3' and access['route'] not in ['local-only', 'blocked']:
            errors.append(f'{kid}: P3 requires local-only route')
        if access['classification'] == 'P2' and access['route'] not in ['local-only', 'cloud-sanitized', 'blocked']:
            errors.append(f'{kid}: P2 route invalid')
        if approval['status'] == 'approved':
            if not all(approval[k] for k in ['reviewer', 'reviewed_at', 'evidence']):
                errors.append(f'{kid}: approval evidence incomplete')
            elif timestamp(approval['reviewed_at']) < timestamp(rec['updated_at']):
                errors.append(f'{kid}: approval predates content update')
        if rec['status'] == 'approved':
            if approval['status'] != 'approved':
                errors.append(f'{kid}: approved record lacks approval')
            if access['classification'] == 'unknown' or access['route'] == 'blocked' or not access['audiences'] or uncertain or rec['content_kind'] == 'unresolved':
                errors.append(f'{kid}: approved record has unresolved source/access/content')
        elif rec['status'] == 'candidate' and approval['status'] != 'pending':
            errors.append(f'{kid}: candidate must have pending approval')
        elif rec['status'] == 'rejected' and approval['status'] != 'rejected':
            errors.append(f'{kid}: rejected record must have rejected approval')
        for relation, targets in rec['relations'].items():
            for target in targets:
                if target == kid or target not in records:
                    errors.append(f'{kid}.{relation}: self or missing relation {target}')
                elif relation == 'replaces' and records[target]['status'] not in ['superseded', 'withdrawn']:
                    errors.append(f'{kid}: replaced record {target} remains active')
    # Iterative traversal avoids recursion depth failures on large chains.
    for relation in ['up', 'replaces']:
        finished = set()
        for kid in records:
            active, stack = set(), [(kid, False)]
            while stack:
                node, leaving = stack.pop()
                if leaving:
                    active.discard(node)
                    finished.add(node)
                elif node in active:
                    errors.append(f'{node}: cyclic {relation} relations')
                    break
                elif node not in finished and node in records:
                    active.add(node)
                    stack.append((node, True))
                    stack.extend((n, False) for n in records[node]['relations'][relation])
    eligible = [r for r in records.values() if r['status'] == 'approved']
    return {'valid': not errors, 'errors': errors, 'warnings': warnings,
            'record_count': len(data['records']), 'index_count': len(eligible) if not errors else 0}


def encode(data):
    return (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def build(source, output, review_dir=None):
    data = load_json(source)
    report = validate(data)
    if not report['valid']:
        raise ValueError(json.dumps(report, ensure_ascii=False))
    index = {'format': 'ew-mcp-retrieval-index', 'schema_version': '1.0.0',
             'knowledge_base_id': data['knowledge_base_id'], 'records': []}
    for record in data['records']:
        if record['status'] == 'approved':
            entry = {k: record[k] for k in ['knowledge_id', 'version', 'title', 'category', 'summary',
                     'keywords', 'synonyms', 'questions', 'source_refs', 'access', 'approval', 'validity', 'legal']}
            entry['sha256'] = hashlib.sha256(encode(record)).hexdigest()
            index['records'].append(entry)
    files = {'knowledge.json': encode(data), 'knowledge.schema.json': SCHEMA.read_bytes(),
             'retrieval-index.json': encode(index), 'validation-report.json': encode(report)}
    if review_dir:
        root = Path(review_dir)
        if not root.is_dir() or root.is_symlink():
            raise ValueError('review-dir must be a real directory')
        for path in sorted(root.rglob('*')):
            if path.is_symlink():
                raise ValueError('symlinks are not allowed in review directory')
            if path.is_file():
                rel = path.relative_to(root)
                if path.suffix.lower() != '.md' or any(x.startswith('.') for x in rel.parts):
                    raise ValueError('review directory permits visible Markdown files only')
                files['review/' + rel.as_posix()] = path.read_bytes()
    output = Path(output)
    if output.resolve() == Path(source).resolve() or output.exists():
        raise ValueError('output must be a new path; refusing overwrite')
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'x', zipfile.ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP integrity failure')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'build'])
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--review-dir', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'build':
            if args.output is None:
                parser.error('build requires --output')
            report = build(args.input, args.output, args.review_dir)
        else:
            report = validate(load_json(args.input))
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report['valid'] else 1
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        print(json.dumps({'valid': False, 'errors': [str(exc)]}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
