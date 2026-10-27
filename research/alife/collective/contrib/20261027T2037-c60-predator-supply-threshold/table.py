"""Per-target fate in each hold arm: death time after the fork and the area of the prey it touched just before (prey0 = eaten out)."""
import json, glob, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runs'))
for f in sorted(glob.glob('*.json')):
    d = json.load(open(f)); r = d['rows']; out = []
    for k in range(len(d['targets'])):
        al = [x['targets'][k]['alive'] for x in r]
        if False in al:
            i = al.index(False); out.append(f"dead {int(r[i]['t'] - d['t0'])} (prey {r[i-1]['targets'][k]['prey_area']} px)")
        else: out.append('alive')
    print(f, out)
