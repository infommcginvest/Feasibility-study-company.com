#!/usr/bin/env python3
"""Integrator edit for the CASE-NEW-1 t2 landing: the Nashville metro page names its first case in the fourteen counties.
usage: nashville_edit.py ROOT   (idempotent; sets updated to DEPLOY, ruling 12)"""
import re,sys,os
p=os.path.join(sys.argv[1],'src/pages/states/tennessee/nashville.html')
s=open(p,encoding='utf-8').read()
if 'medical-office-lebanon-tennessee-sba' in s: print('already'); sys.exit(0)
old_h='data-h2="A Blount County cabin resort case, and none yet in the fourteen counties."'
new_h='data-h2="A Wilson County medical office case and a Blount County cabin resort case."'
old_p='<p>No published case names a site in the fourteen counties of the Nashville metro area. The <a href="/case-studies/cabin-resort-townsend-tennessee-sba/">cabin resort case</a>,'
new_p='<p>One published case names a site in the fourteen counties of the Nashville metro area: the <a href="/case-studies/medical-office-lebanon-tennessee-sba/">Lebanon medical office case</a> tests whether a medical office building with an ambulatory surgery center, on a generic site in Lebanon in Wilson County, can carry SBA 504 debt. The <a href="/case-studies/cabin-resort-townsend-tennessee-sba/">cabin resort case</a>,'
assert old_h in s and old_p in s
s=s.replace(old_h,new_h).replace(old_p,new_p)
s=re.sub(r'("updated"\s*:\s*)"[^"]*"',r'\1"DEPLOY"',s,count=1)
open(p,'w',encoding='utf-8').write(s); print('edited')
