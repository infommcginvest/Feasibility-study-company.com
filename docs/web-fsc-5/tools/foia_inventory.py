import csv,sys,collections,os,json
d,outdir=sys.argv[1],sys.argv[2]
naics=collections.defaultdict(lambda:{'n':0,'fy_min':9999,'fy_max':0,'desc':collections.Counter(),'prog':collections.Counter()})
cty=collections.defaultdict(lambda:{'n':0,'fy_min':9999,'fy_max':0})
for f in sorted(os.listdir(d)):
    if not f.endswith('.csv'): continue
    prog='504' if '_504_' in f else '7a'
    with open(os.path.join(d,f),newline='',encoding='utf-8',errors='replace') as fh:
        for row in csv.DictReader(fh):
            fy=int(row['ApprovalFY'])
            c=(row['NaicsCode'] or '').strip()
            r=naics[c]; r['n']+=1; r['fy_min']=min(r['fy_min'],fy); r['fy_max']=max(r['fy_max'],fy); r['desc'][(row['NaicsDescription'] or '').strip()]+=1; r['prog'][prog]+=1
            k=(row['ProjectState'].strip(),row['ProjectCounty'].strip())
            q=cty[k]; q['n']+=1; q['fy_min']=min(q['fy_min'],fy); q['fy_max']=max(q['fy_max'],fy)
with open(os.path.join(outdir,'foia_naics_inventory.tsv'),'w') as o:
    o.write('naics\tloans\tfy_min\tfy_max\t7a\t504\tdescriptions\n')
    for c,r in sorted(naics.items()):
        o.write(f"{c}\t{r['n']}\t{r['fy_min']}\t{r['fy_max']}\t{r['prog']['7a']}\t{r['prog']['504']}\t{' || '.join(f'{k} ({v})' for k,v in r['desc'].most_common(3))}\n")
with open(os.path.join(outdir,'foia_county_inventory.tsv'),'w') as o:
    o.write('state\tproject_county\tloans\tfy_min\tfy_max\n')
    for (s,c),r in sorted(cty.items()):
        o.write(f"{s}\t{c}\t{r['n']}\t{r['fy_min']}\t{r['fy_max']}\n")
print(len(naics),'naics codes;',len(cty),'state-county strings')
