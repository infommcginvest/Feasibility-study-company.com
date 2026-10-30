import os,re,glob,sys,csv
root=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../..'))
here=os.path.join(root,'docs/rollout/case-new-1')
man={}
for l in list(open(here+'/MANIFEST.tsv'))[1:]:
    p=l.rstrip('\n').split('\t'); man[p[0]]=p[1]
pages={}
for f in glob.glob(root+'/**/index.html',recursive=True):
    rel=os.path.relpath(f,root)
    if rel.startswith(('docs/','node_modules/')): continue
    t=open(f,errors='ignore').read()
    pages[rel]=set(re.findall(r'\d[\d,]*(?:\.\d+)?',re.sub(r'<[^>]+>',' ',t)))
    pages[rel]={x.rstrip(',') for x in pages[rel]}
def tok(v):
    m=re.search(r'\d[\d,]*(?:\.\d+)?',v)
    return m.group(0).rstrip(',') if m else ''
def checkable(v):
    d=re.sub(r'\D','',v)
    if len(d)<3: return False
    if re.fullmatch(r'(19|20)\d\d',v): return False
    return True
rows=[]
BLOCK=re.compile(r'undated|fetch|retriev|single|listing|subject|rule|assum|not found|stale|conflict|national|secondary|weak|summary|not case|no url|page must date',re.I)
PARENT=re.compile(r'states/|asset-classes/|metro|state page|hub|served page|appears on|already|collid|repeat|held by',re.I)
def ptype(k):
    return 'case' if k.startswith('case-studies/') else 'parent'
sib={}
cand={}
for slug,cls in man.items():
    f=f'{here}/precount/{slug}.tsv'
    if not os.path.exists(f): continue
    for l in open(f):
        p=l.rstrip('\n').split('\t')
        if len(p)<8 or p[0]=='fig_id': continue
        ok = p[7].strip()=='Y' or (p[7].strip()=='N' and PARENT.search(p[8] if len(p)>8 else '') and not BLOCK.search(p[8] if len(p)>8 else ''))
        if not ok: continue
        v=tok(p[1])
        if not v: continue
        cand.setdefault(slug,{})[v]=p
for slug,cls in man.items():
    f=f'{here}/precount/{slug}.tsv'
    if slug not in cand: rows.append([slug,cls,'','','','','','','MISSING','','']); continue
    summ=''.join(l for l in open(f) if l.startswith('#SUMMARY'))
    r=g=casedup=sibdup=parentcede=0; parents=set()
    for v,p in cand[slug].items():
        own=f'case-studies/{slug}/index.html'
        hits=[k for k,t in pages.items() if k!=own and checkable(v) and v in t]
        if any(ptype(k)=='case' for k in hits): casedup+=1; continue
        order=list(man)
        if any(o!=slug and order.index(o)<order.index(slug) and man[o]=='new' and v in cand.get(o,{}) and checkable(v) for o in cand): sibdup+=1; continue
        if hits: parentcede+=1; parents.update(hits)
        if p[3].strip()=='register': g+=1
        else: r+=1
    strict_ok=True
    g=min(g,10); c=r+g
    eng=re.search(r'engine=(\w)',summ); eng=eng.group(1) if eng else '?'
    note=re.search(r'notes=(.*)',summ); note=note.group(1).strip() if note else ''
    verdict='PAGE' if c>=30 and r>=20 else 'FOLD'
    rows.append([slug,cls,c,r,g,casedup,sibdup,parentcede,verdict,eng,';'.join(sorted(x.replace('/index.html','') for x in parents))[:150]])
with open(here+'/PRECOUNT.tsv','w') as o:
    o.write('slug\tclass\tcounted\tresearch\tregister\tdropped_case_dup\tdropped_sibling_dup\tfigures_ceded_by_parents\tverdict_A4\tengine\tparents_losing_figures\n')
    for x in rows: o.write('\t'.join(map(str,x))+'\n')
