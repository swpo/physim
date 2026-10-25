"""Cog matter inside r<12 (relative to the fork) and mean food inside r<6 around the annulus-cut cog, per arm.
usage: measure.py seed arm ..."""
import sys, json, numpy as np
sd = int(sys.argv[1]); c = np.load(f'ann_{sd}.npz'); cy, cx = float(c['cy']), float(c['cx'])
H, W = c['mask'].shape; yy, xx = np.mgrid[:H, :W]
d = np.hypot(np.minimum(abs(yy-cy), H-abs(yy-cy)), np.minimum(abs(xx-cx), W-abs(xx-cx)))
m0 = c['A'][:, d < 12].sum(); out = {}
for arm in sys.argv[2:]:
    X = np.load(f'{arm}{sd}_snaps.npz'); t = X['t']; X = X['X'].astype(np.float32)
    mat = X[:, :2][:, :, d < 12].sum((1, 2)) / m0; food = X[:, 2][:, d < 6].mean(1)
    dead = t[np.argmax(mat < 0.1)] if (mat < 0.1).any() else None
    out[arm] = {"cog_matter_end": round(float(mat[-1]), 3), "food_inside_end": round(float(food[-1]), 3), "t_cog_below_0.1": None if dead is None else float(dead),
                "series_every_100t": [(float(t[i]), round(float(mat[i]), 3), round(float(food[i]), 3)) for i in range(0, len(t), max(1, len(t) // 7))]}
    print(arm, out[arm]["cog_matter_end"], out[arm]["food_inside_end"], out[arm]["t_cog_below_0.1"])
json.dump(out, open(f'annulus_seed{sd}.json', 'w'), indent=1)
