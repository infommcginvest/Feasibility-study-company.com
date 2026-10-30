#!/usr/bin/env python3
"""Add the /case-studies/ card and JSON-LD item for each given case (the integrator's index_entry, REQUESTS.md).
usage: addcards.py ROOT slug [slug...]    reads ROOT/src/case-cards/<slug>.json; casemodel.py fills the region text."""
import html,json,os,re,sys
root=sys.argv[1]; p=os.path.join(root,'case-studies/index.html')
s=open(p,encoding='utf-8').read()
for slug in sys.argv[2:]:
    spec=json.load(open(os.path.join(root,'src/case-cards',slug+'.json'),encoding='utf-8'))
    if f'/case-studies/{slug}/' in s: print('already',slug); continue
    cat=html.escape(spec['category']).replace('·','&middot;'); asset=html.escape(spec['asset']); title=html.escape(spec['title'])
    art=f'''        <article class="card">
          <div class="card-top">
            <div class="card-cat">{cat}</div>
            <div class="card-cite">{asset}</div>
          </div>
          <div class="card-body">
            <h3><a href="/case-studies/{slug}/">{title}</a></h3>
            <p><!--case:{slug}.card-->{spec['card']}<!--/case:{slug}.card--></p>
            <span class="card-link">Read the case study &rarr;</span>
          </div>
        </article>
'''
    cta=s.index('<h2 id="h-cta">'); pub=s.index('<h2 id="h-published">')
    last=s.rindex('</article>\n',pub,cta)+len('</article>\n')
    s=s[:last]+art+s[last:]
    lines=s.split('\n'); idx=max(i for i,l in enumerate(lines) if '"@type": "Article"' in l)
    ld='        { "@type": "Article", "name": %s, "url": "https://feasibility-study-company.com/case-studies/%s/" }'%(json.dumps(spec['title'].replace('&','&')),slug)
    if not lines[idx].rstrip().endswith(','): lines[idx]=lines[idx].rstrip()+','
    lines.insert(idx+1,ld+(',' if lines[idx+1].lstrip().startswith('{') else ''))
    s='\n'.join(lines); print('added',slug)
open(p,'w',encoding='utf-8').write(s)
