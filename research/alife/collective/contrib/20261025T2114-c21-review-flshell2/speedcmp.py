"""(c21: the claim's script on seeds 7-8 of rerun/.) motion with and without the shell feedback: labkit motion_top (most-travelled tracks) per seed."""
import json, sys, numpy as np
rows = {}
for lab, d in (('h5=0 (shell readout only)', 'control_h5_0'), ('h5=0.3 (shell feeds back)', 'rerun')):
    for s in (7, 8):
        m = json.load(open(f'{d}/seed{s}/metrics.json')); mt = m['motion_top']; su = m['summary']
        sp = [x['speed'] for x in mt]; bl = [x['body_lengths'] for x in mt]
        rows[f'{lab} seed{s}'] = {"moving_tracks": su['moving_tracks'], "top_tracks_median_speed": round(float(np.median(sp)), 3), "top_tracks_median_body_lengths": round(float(np.median(bl)), 2),
                                  "max_body_lengths": round(su['max_body_lengths'], 1), "persistent_splits": su['persistent_splits'], "max_generation": su['max_generation'], "merge_split_ratio": round(su['merge_split_ratio'], 2)}
print(json.dumps(rows, indent=1)); json.dump(rows, open('speedcmp.json', 'w'), indent=1)
