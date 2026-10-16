#!/usr/bin/env python3
"""Freeze the lane at HEAD: record the commit, the sha256 of `git archive HEAD`,
and the state of the data, not just the files: every raw file (URL, retrieval
time, bytes, sha256, re-hashed now from disk) and every file under data/markets/.

    python3 docs/web-fsc-5/tools/freeze.py

Refuses to run with uncommitted changes under the lane's paths. Writes
docs/web-fsc-5/freeze/freeze-<short sha>.json and an extract of the archive under
_cache/markets/freeze-<short sha>/tree for the attackers and the verifier. The
record is committed afterwards in a records-only commit; the frozen tree itself
never contains its own freeze record.
"""
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def git(*a, binary=False):
    r = subprocess.run(['git', '-C', ROOT, *a], capture_output=True, timeout=600)
    if r.returncode:
        raise SystemExit(r.stderr.decode())
    return r.stdout if binary else r.stdout.decode().strip()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    dirty = git('status', '--porcelain', '--', 'data/markets', 'scripts', 'docs/web-fsc-5', '.gitignore')
    if dirty:
        raise SystemExit('uncommitted changes; commit before freezing:\n' + dirty)
    head = git('rev-parse', 'HEAD')
    archive = git('archive', '--format=tar', 'HEAD', binary=True)
    man = json.load(open(os.path.join(ROOT, '_cache', 'markets', 'manifest.json')))
    raw = []
    for rel, rec in sorted(man['files'].items()):
        p = os.path.join(ROOT, rel)
        now = sha256_file(p) if os.path.exists(p) else None
        raw.append({'path': rel, 'url': rec['url'], 'retrieved_at': rec['retrieved_at'], 'bytes': rec['bytes'],
                    'sha256_manifest': rec['sha256'], 'sha256_now': now, 'same': now == rec['sha256']})
    data = []
    for d, _, fs in os.walk(os.path.join(ROOT, 'data', 'markets')):
        for f in sorted(fs):
            p = os.path.join(d, f)
            data.append({'path': os.path.relpath(p, ROOT), 'bytes': os.path.getsize(p), 'sha256': sha256_file(p)})
    data.sort(key=lambda x: x['path'])
    state = {'raw': raw, 'data': data, 'sources': {k: {kk: v.get(kk) for kk in ('status', 'vintage', 'reason')} for k, v in man['sources'].items()}}
    canon = json.dumps(state, sort_keys=True, separators=(',', ':')).encode()
    rec = {'head': head, 'archive_sha256': sha256_bytes(archive), 'data_manifest_sha256': sha256_bytes(canon),
           'raw_files_all_unchanged': all(r['same'] for r in raw), **state}
    out = os.path.join(ROOT, 'docs', 'web-fsc-5', 'freeze', f'freeze-{head[:7]}.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(rec, open(out, 'w'), indent=1, sort_keys=True)
    tree = os.path.join(ROOT, '_cache', 'markets', f'freeze-{head[:7]}', 'tree')
    os.makedirs(tree, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive)) as t:
        t.extractall(tree)
    print(f'head {head}\narchive sha256 {rec["archive_sha256"]}\ndata manifest sha256 {rec["data_manifest_sha256"]}\n'
          f'raw files {len(raw)} (all unchanged: {rec["raw_files_all_unchanged"]}); data files {len(data)}\nrecord {os.path.relpath(out, ROOT)}\ntree {os.path.relpath(tree, ROOT)}')


if __name__ == '__main__':
    sys.exit(main())
