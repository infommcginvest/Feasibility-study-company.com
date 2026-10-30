#!/usr/bin/env python3
"""Print the frames of state/metro page sources: hero, description, section ids and h2s, FAQ questions, CTA, card text.
   python3 frames.py <source.html> ..."""
import json, re, sys, html
for p in sys.argv[1:]:
    s = open(p, encoding="utf-8").read()
    fm = json.loads(s.split("\n---\n", 1)[0][4:])
    body = s.split("\n---\n", 1)[1]
    print("=" * 8, p.replace(__import__("os").path.expanduser("~"), "~"))
    print("DESC:", fm.get("description"))
    print("HERO:", re.sub(r"\[\^[\d,]+\]", "", fm.get("hero_sub", ""))[:600])
    for m in re.finditer(r'<section id="([^"]+)"[^>]*?data-h2="([^"]*)"', body):
        print(f"  #{m.group(1)}: {html.unescape(m.group(2))}")
    print("FAQ:", " | ".join(q["q"] for q in fm.get("faq", {}).get("items", [])))
    print("CTA:", fm.get("cta", {}).get("h2"), "//", fm.get("cta", {}).get("p", "")[:200])
    print("SRCLEDE:", fm.get("sources_lede", "")[:200])
    if "--cards" in sys.argv[0:1] or True:
        for m in re.finditer(r'<div class="metro">(.*?)</div>\s*</div>|<div class="metro">(.*?)</p>', body, re.S):
            t = re.sub(r"<[^>]+>", " ", m.group(0)); t = re.sub(r"\s+", " ", html.unescape(t)).strip()
            print("   card:", t[:220])
