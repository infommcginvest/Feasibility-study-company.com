import csv,sys,collections,os,json
d=sys.argv[1]
out={}
for f in sorted(os.listdir(d)):
    if not f.endswith('.csv'): continue
    st=collections.Counter(); fy=collections.Counter(); naics_blank=collections.Counter(); naics_len=collections.Counter()
    co_blank=0; states=collections.Counter(); asof=collections.Counter(); prog=collections.Counter(); n=0
    chg_by_status=collections.Counter(); chgamt_by_status=collections.Counter(); cnt_status_fy=collections.Counter()
    sample_cty=collections.Counter()
    with open(os.path.join(d,f),newline='',encoding='utf-8',errors='replace') as fh:
        r=csv.DictReader(fh)
        for row in r:
            n+=1
            s=row['LoanStatus']; st[s]+=1
            fy[row['ApprovalFY']]+=1
            nc=(row['NaicsCode'] or '').strip()
            if not nc: naics_blank[row['ApprovalFY']]+=1
            naics_len[len(nc)]+=1
            if not (row['ProjectCounty'] or '').strip(): co_blank+=1
            states[row['ProjectState']]+=1
            asof[row['AsOfDate']]+=1; prog[row['Program']]+=1
            if (row['ChargeOffDate'] or '').strip(): chg_by_status[s]+=1
            try:
                if float(row['GrossChargeOffAmount'] or 0)>0: chgamt_by_status[s]+=1
            except: chgamt_by_status['BADNUM:'+row['GrossChargeOffAmount'][:10]]+=1
            sample_cty[row['ProjectCounty']]+=1
    out[f]=dict(rows=n,status=dict(st),fy_min=min(fy),fy_max=max(fy),naics_blank_rows=sum(naics_blank.values()),naics_blank_fys=dict(sorted(naics_blank.items())[:8]),naics_len=dict(naics_len),county_blank=co_blank,n_states=len(states),odd_states=[k for k in states if len(k)!=2],asof=dict(asof),program=dict(prog),chgdate_by_status=dict(chg_by_status),chgamt_by_status=dict(chgamt_by_status),n_county_strings=len(sample_cty),county_examples=[k for k,_ in sample_cty.most_common(8)])
print(json.dumps(out,indent=1))
