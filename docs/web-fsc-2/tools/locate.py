#!/usr/bin/env python3
"""Map a line number in an SOP text extract to its section path and TOC page range.

The docx carries rendered page breaks only to page 133, so pages come from the
SOP's own table of contents. TOC entries are matched to body headings IN ORDER,
so duplicate titles (several chapters have a "Credit Standards") resolve to the
right place. A body line belongs to the last matched heading before it; its page
range runs from that heading's TOC page to the next TOC page.
"""
import re, sys, bisect

def _key(s): return re.sub(r'[^a-z0-9]', '', s.lower())

def build(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    start = next(i for i, l in enumerate(lines) if l.strip() == 'Table of Contents')
    end = next(i for i, l in enumerate(lines) if l.startswith('# User Tips'))
    toc = []  # (title, page, level) level 0 = Section/Appendix, 1 = Chapter, 2 = lettered
    for l in lines[start + 1:end]:
        m = re.match(r'^(?:([A-Z])\.\t)?(.+?)\t(\d+)\s*$', l.rstrip('\n'))
        if not m: continue
        title = re.sub(r'\s+', ' ', m.group(2)).strip()
        lvl = 2 if m.group(1) else (1 if title.startswith('Chapter') else 0)
        toc.append((title, int(m.group(3)), lvl))
    heads = []  # (line_no, toc_index)
    j = 0
    for i in range(end, len(lines)):
        s = re.sub(r'^#+\s*', '', lines[i]).strip()
        if not s or len(s) > 140: continue
        k = _key(s)
        for cand in range(j, min(j + 8, len(toc))):
            if _key(toc[cand][0]) == k:
                heads.append((i + 1, cand)); j = cand + 1; break
    return lines, toc, heads

def locate(lines, toc, heads, line_no):
    pos = bisect.bisect_right([h[0] for h in heads], line_no) - 1
    if pos < 0: return ('front matter', 'pp. 1-10')
    ti = heads[pos][1]
    title, page, lvl = toc[ti]
    nxt = [p for t, p, l in toc[ti + 1:] if p > page]
    end_page = min(nxt) if nxt else page
    # path: nearest level-0 and level-1 ancestors
    path = []
    for t, p, l in reversed(toc[:ti]):
        if l < lvl and (not path or l < path[-1][1]):
            path.append((t, l))
            if l == 0: break
    parts = [t for t, l in reversed(path)] + [title]
    parts = [re.sub(r'^Section ([ABC])\..*', r'Section \1', p) if p.startswith('Section') else p for p in parts]
    parts = [re.sub(r'^(Chapter \d+):.*', r'\1', p) if p.startswith('Chapter') else p for p in parts]
    parts = [re.sub(r'^(Appendix \d+):.*', r'\1', p) if p.startswith('Appendix') else p for p in parts]
    rng = f'p. {page}' if end_page <= page else f'pp. {page}-{end_page}'
    return (', '.join(parts), rng)

if __name__ == '__main__':
    lines, toc, heads = build(sys.argv[1])
    print(f'# TOC entries {len(toc)}, headings matched {len(heads)}')
    for n in sys.argv[2:]:
        n = int(n); sec, pg = locate(lines, toc, heads, n)
        print(n, '|', sec, '|', pg, '|', lines[n - 1][:100])
