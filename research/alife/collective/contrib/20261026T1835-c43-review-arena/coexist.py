"""c43 (uses c42 drive.py outputs: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/drive.py): the finding's coexistence rule on drive.py outputs: predators present at every count from t=6000 on and prey
present at >= 50% of them; also the predator last-alive time.
usage: python coexist.py drive/*.json"""
import sys, json
for f in sys.argv[1:]:
    d = json.load(open(f)); R = [r for r in d["rows"] if r[0] >= 6000]
    pred = all(r[2] > 0 for r in R); prey = sum(r[1] > 0 for r in R) / max(len(R), 1)
    last = max([r[0] for r in d["rows"] if r[2] > 0], default=None)
    print(f, "coexist" if pred and prey >= 0.5 else "no", "prey_frac %.2f" % prey, "pred_last", last)
