#!/usr/bin/env python3
"""docx -> text with headings and page markers.

Page markers come from Word's lastRenderedPageBreak and explicit page breaks,
so a [PAGE n] marker means "Word last rendered a page break here". Numbering
starts at 1 on the first page of the file (cover). Tables are flattened row by
row with " | " between cells.
"""
import sys, re
from docx import Document
from docx.oxml.ns import qn

src, dst = sys.argv[1], sys.argv[2]
doc = Document(src)
page = 1
out = []

def para_text(p):
    global page
    parts = []
    for node in p._p.iter():
        tag = node.tag
        if tag == qn('w:lastRenderedPageBreak'):
            page += 1; parts.append(f"\n[PAGE {page}]\n")
        elif tag == qn('w:br') and node.get(qn('w:type')) == 'page':
            page += 1; parts.append(f"\n[PAGE {page}]\n")
        elif tag == qn('w:t'):
            parts.append(node.text or '')
        elif tag == qn('w:tab'):
            parts.append('\t')
        elif tag == qn('w:footnoteReference'):
            parts.append(f"[fn{node.get(qn('w:id'))}]")
    return ''.join(parts)

def style_prefix(p):
    name = (p.style.name if p.style is not None else '') or ''
    m = re.match(r'[Hh]eading (\d)', name)
    if m: return '#' * int(m.group(1)) + ' '
    if name.lower().startswith('title'): return '# '
    return ''

body = doc.element.body
for child in body.iterchildren():
    if child.tag == qn('w:p'):
        from docx.text.paragraph import Paragraph
        p = Paragraph(child, doc)
        t = para_text(p)
        # numbering (list) level hint
        out.append(style_prefix(p) + t)
    elif child.tag == qn('w:tbl'):
        from docx.table import Table
        tbl = Table(child, doc)
        for row in tbl.rows:
            cells = []
            for c in row.cells:
                ct = ' '.join(para_text(p) for p in c.paragraphs)
                cells.append(ct.strip())
            out.append(' | '.join(cells))
        out.append('')
    elif child.tag == qn('w:sectPr'):
        pass

# footnotes
try:
    fn_part = None
    for rel in doc.part.rels.values():
        if 'footnotes' in rel.reltype:
            fn_part = rel.target_part
    if fn_part is not None:
        from lxml import etree
        root = etree.fromstring(fn_part.blob)
        out.append('\n\n== FOOTNOTES ==')
        for fn in root.iter(qn('w:footnote')):
            fid = fn.get(qn('w:id'))
            txt = ''.join(t.text or '' for t in fn.iter(qn('w:t')))
            if txt.strip(): out.append(f"[fn{fid}] {txt.strip()}")
except Exception as e:
    out.append(f"(footnotes not extracted: {e})")

open(dst, 'w', encoding='utf-8').write('\n'.join(out))
print(f"{src} -> {dst}: {len(out)} blocks, last page marker {page}")
