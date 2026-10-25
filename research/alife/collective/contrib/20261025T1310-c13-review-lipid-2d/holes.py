"""Count solvent regions enclosed by lipid in a final configuration: splat all beads on a grid (0.5 sigma pixels),
blur 0.5 sigma, threshold, label the background with periodic wrap; enclosed = every background component except
the largest, with area >= 8 sigma^2 (more than a few lipids' worth of solvent). usage: holes.py L x_tag.npy ..."""
import sys, numpy as np
from scipy import ndimage
L = float(sys.argv[1])
for f in sys.argv[2:]:
    x = np.load(f); n = int(round(L / 0.5)); g = np.zeros((n, n))
    ix = (x / L * n).astype(int) % n; np.add.at(g, (ix[:, 1], ix[:, 0]), 1)
    g = ndimage.gaussian_filter(g, 1.0, mode="wrap"); lip = g > 0.15
    bg = np.tile(~lip, (3, 3)); lab, k = ndimage.label(bg)
    c = lab[n:2 * n, n:2 * n]; ids, cnt = np.unique(c[c > 0], return_counts=True)
    # a component that is enclosed does not extend beyond the tile; the outside wraps and is large
    sizes = ndimage.sum(bg, lab, ids); enclosed = [(i, a) for i, a, s in zip(ids, cnt, sizes) if s == a and a * 0.25 >= 8]
    print(f"{f}: lipid area fraction {lip.mean():.2f}; enclosed solvent regions >= 8 sigma^2: {len(enclosed)} (areas sigma^2: {[round(a*0.25) for _, a in enclosed][:10]})")
