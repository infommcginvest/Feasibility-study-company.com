#!/usr/bin/env python3
# Tree B simulation for tranche c1 (CASE-NEW-1 practice): the integrator writes the /case-studies/ cards at landing;
# here they are added in the throwaway copy with the lane's addcards.py so casemodel.py and the gates can run.
import os, subprocess, sys
tree = sys.argv[1]
slugs = [s for s in os.environ.get("C1_SLUGS", "").split() if os.path.exists(os.path.join(tree, "src/case-cards", s + ".json"))]
if slugs:
    subprocess.run([sys.executable, os.path.join(tree, "docs/rollout/case-new-1/tools/addcards.py"), tree] + slugs, check=True)
