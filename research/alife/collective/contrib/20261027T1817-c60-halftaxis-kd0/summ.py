"""Summarise kdarms outputs: per target survival, death time, max c_b, prey area and eating at start/end; arm counts."""
import json, glob, sys, numpy as np
out = {}
for f in sorted(glob.glob('arms/*_s*.json')):
    d = json.load(open(f)); rows = d['rows']; nt = len(d['targets'])
    tg = []
    for k in range(nt):
        tr = [r['targets'][k] for r in rows]
        dead = [r['t'] - d['t0'] for r, x in zip(rows, tr) if not x['alive']]
        last = [x for x in tr if x['alive']][-1]
        # prey area at the time of death (last alive record) and max over the run
        tg.append(dict(death=dead[0] if dead else None, prey0=tr[0]['prey_area'], prey_last=last['prey_area'],
                       maxcb0=round(tr[0]['max_cb'], 2), maxcb_last=round(last['max_cb'], 2), q_last=round(last['q_max'], 3),
                       eat0=round(tr[0]['eat_on_pred'], 3), eat_last=round(last['eat_on_pred'], 3), t_last=round(rows[[x['alive'] for x in tr].index(False) - 1 if dead else -1]['t'] - d['t0'])))
    key = f.split('/')[-1][:-5]
    out[key] = dict(n_pred=[rows[0]['n_pred'], rows[len(rows)//3]['n_pred'], rows[-1]['n_pred']], n_prey=[rows[0]['n_prey'], rows[-1]['n_prey']],
                    eat_total=[round(rows[0]['eat_total'], 2), round(rows[-1]['eat_total'], 2)], alive=sum(t['death'] is None for t in tg), targets=tg)
    print(key, out[key]['n_pred'], out[key]['n_prey'], 'alive', out[key]['alive'], '/', nt)
    for t in tg: print('   ', t)
json.dump(out, open('arms_summary.json', 'w'), indent=1)
