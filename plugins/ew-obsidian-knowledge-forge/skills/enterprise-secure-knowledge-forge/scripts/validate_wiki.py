#!/usr/bin/env python3
"""Validate portable wiki dependencies and byte integrity, not semantic truth."""
import hashlib
import json
import re
import sys
from pathlib import Path

def validate(root):
    root = Path(root).resolve(); errors=[]
    def fail(message): errors.append(message)
    def file_path(value):
        if not isinstance(value,str) or not value or '\\' in value or Path(value).is_absolute() or '..' in Path(value).parts: raise ValueError('unsafe relative path')
        path=root/value
        if any(p.is_symlink() for p in [path,*path.parents] if p!=root.parent) or not path.resolve().is_relative_to(root): raise ValueError('symlink or escaping path')
        if path.suffix!='.md' or not path.is_file(): raise ValueError('missing Markdown: '+value)
        return path
    try:
        m=json.loads((root/'WIKI-MANIFEST.json').read_text())
        if m.get('schema_version')!='1.0': raise ValueError('unsupported wiki schema')
        sources=m['sources']; topics=m['topics']; decisions=m['decisions']
        if not all(isinstance(x,list) for x in (sources,topics,decisions)): raise ValueError('expected arrays')
        ids=[s['source_id'] for s in sources]; tids=[t['knowledge_id'] for t in topics]
        if any(not isinstance(x,str) or not x for x in ids+tids): raise ValueError('invalid identity')
        if len(ids)!=len(set(ids)) or len(tids)!=len(set(tids)): fail('duplicate identity')
        available=set()
        for s in sources:
            if s.get('path') is None:
                if s.get('sha256') is not None: fail('metadata-only source hash must be null')
                continue
            path=file_path(s['path']); actual=hashlib.sha256(path.read_bytes()).hexdigest()
            if actual!=s.get('sha256'): fail('source changed: '+s['source_id'])
            available.add(s['source_id'])
        seen=[]
        for d in decisions:
            sid=d['source_id']; seen.append(sid)
            if sid not in ids or d.get('action') not in {'create','update','duplicate','no_change','deferred','blocked'} or not d.get('reason','').strip(): fail('invalid source decision')
            if not isinstance(d.get('topic_ids'),list) or not set(d['topic_ids'])<=set(tids): fail('invalid decision topic')
            if d.get('action') in {'create','update'} and not d['topic_ids']: fail('create/update requires topic')
            if sid not in available and d.get('action') not in {'blocked','deferred'}: fail('unavailable source used')
        if sorted(seen)!=sorted(ids): fail('every source needs exactly one impact decision')
        enterprise=root/'FORGE-MANIFEST.json'
        if enterprise.exists():
            em=json.loads(enterprise.read_text()); es={s['source_id']:s for s in em['sources']}
            if set(ids)!=set(es): fail('enterprise source coverage mismatch')
        else: es=None
        paths=[]
        for t in topics:
            path=file_path(t['path']); paths.append(t['path'])
            if hashlib.sha256(path.read_bytes()).hexdigest()!=t.get('sha256'): fail('topic changed: '+t['knowledge_id'])
            if not re.fullmatch(r'\d+\.\d+\.\d+',t.get('version','')): fail('invalid topic version')
            if t.get('status') not in {'draft','proposed','current','superseded','archived','disputed'}: fail('invalid topic status')
            deps=t['source_ids']
            if not isinstance(deps,list) or not deps or not set(deps)<=available: fail('missing topic sources')
            evidence=t['evidence']
            if not isinstance(evidence,list) or {e['source_id'] for e in evidence}!=set(deps) or any(not isinstance(e.get('locator'),str) or not e['locator'].strip() for e in evidence): fail('missing source locator')
            if es is not None:
                notes={n['path']:n for n in em['notes']};n=notes.get(t['path'])
                if not n or set(n.get('source_ids',[]))!=set(deps): fail('enterprise topic registration mismatch')
                elif n.get('approval_status')!='approved' and not t['path'].startswith('10-Candidates/Wiki/'): fail('unapproved topic outside candidate area')
                elif n.get('approval_status')=='approved' and (not n.get('approved_by') or not n.get('approved_at')): fail('missing enterprise approval')
                if n and any(not set(n.get('audience',[]))<=set(es[s].get('audience',[])) for s in deps if s in es): fail('topic broadens source audience')
        if len(paths)!=len(set(paths)): fail('duplicate topic paths')
        for p in ['00-Home/Wiki Index.md','00-Home/Wiki Change Log.md','00-Home/Wiki Review Queue.md']:
            file_path(p)
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as e: fail(str(e))
    return {'valid':not errors,'errors':errors,'semantic_review':'not_performed','mcp_publication':'not_performed'}
if __name__=='__main__':
    result=validate(sys.argv[1]);print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if result['valid'] else 1)
