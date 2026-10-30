import re,os
here=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
A4={ # reader hand-backs that stated the A4 reading (counted,research), 29 Oct
 'self-storage-bardstown-kentucky-usda':(42,32),'self-storage-pataskala-ohio-sba':(20,10),
 'restaurant-acquisition-broussard-louisiana-sba':(38,28),'urgent-care-elizabethtown-kentucky-sba':(33,23),
 'hotel-south-carolina-sba':(37,27),'rv-park-arizona-usda':(31,21),'rv-park-pennsylvania-usda':(31,31),
 'rv-park-maine-usda':(22,13),'marina-maryland-sba':(40,31),'auto-service-new-jersey-sba':(56,47),
 'marina-new-baltimore-michigan-sba':(28,18),'hotel-acquisition-fairlawn-ohio-sba':(21,13),'hotel-hays-kansas-usda':(24,15),'marina-shell-knob-missouri-usda':(27,17)}
HOLD={'marina-gig-harbor-washington-sba':'WAIT-OWNER (CASE-4 engine + hypothetical transient-heavy subject, 28 Oct)',
 'retreat-center-kerhonkson-new-york-usda':'FOLD-OWNER (28 Oct)'}
REAL={'hotel-acquisition-fairlawn-ohio-sba','laundromat-acquisition-huron-county-ohio-sba','marina-gig-harbor-washington-sba','marina-maryland-sba','auto-service-new-jersey-sba','restaurant-missouri-sba'}
tal={}
for l in list(open(here+'/tools/tally_raw.tsv'))[1:]:
    p=l.rstrip('\n').split('\t'); tal[p[0]]=p
out=['slug\tclass\treader_counted\treader_research\treader_register\ta4_counted\ta4_research\ttally_counted\ttally_research\tengine\tverdict\tnote']
for l in list(open(here+'/MANIFEST.tsv'))[1:]:
    slug,cls=l.split('\t')[:2]
    s=''.join(x for x in open(f'{here}/precount/{slug}.tsv') if x.startswith('#SUMMARY'))
    m=re.search(r'counted=(\d+) research=(\d+) register=(\d+) (?:verdict=)?(PAGE|FOLD) engine=(\w)',s)
    rc,rr,rg,rv,eng=int(m[1]),int(m[2]),int(m[3]),m[4],m[5]
    a=A4.get(slug,('',''))
    tc,tr=int(tal[slug][2]),int(tal[slug][3])
    best=a if a[0]!='' else (rc,rr)
    page_reader = best[0]>=30 and best[1]>=20
    page_tally = tc>=30 and tr>=20
    if slug in HOLD: v=HOLD[slug]
    elif page_reader and page_tally: v='PAGE'
    else: v='FOLD'
    if v=='PAGE' and eng=='Y': v='PAGE-WAIT-ENGINE'
    if v=='FOLD' and eng=='Y': v='FOLD(engine)'
    notes=[]
    if v.startswith('PAGE'):
        mg=min(best[0]-30,best[1]-20,tc-30,tr-20)
        if mg<=3: notes.append('thin margin %d'%mg)
    if slug in REAL: notes.append('real-subject file: hypothetical subject only')
    if page_reader!=page_tally: notes.append('reader and tally disagree')
    if slug in A4: notes.append('A4 reading used')
    out.append('\t'.join(map(str,[slug,cls,rc,rr,rg,a[0],a[1],tc,tr,eng,v,'; '.join(notes)])))
open(here+'/PRECOUNT.tsv','w').write('\n'.join(out)+'\n')
import collections
print(collections.Counter(x.split('\t')[10] for x in out[1:]))
for x in out[1:23]: print(x.split('\t')[0],x.split('\t')[10],x.split('\t')[11])
