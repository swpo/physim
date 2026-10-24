"""Radial profiles (mean over all cells) of body u, membrane m, cargo c: gate on/off, CH on/off."""
import json
from screen import *
from scipy import ndimage
import muts
cases = [("beta=5, CH on (xcell-a)", dict(beta=5.0)), ("beta=0 (no gate)", dict(beta=0.0)),
         ("beta=5, CH off (M=0)", dict(beta=5.0, M=0.0))]
fig, axs = plt.subplots(1, 3, figsize=(11, 3.2), sharey=True)
out = {}
for ax, (lab, kw) in zip(axs, cases):
    g = muts.cell(**kw)
    sn, ts, w = run(g, N=128, T=150, seed=0, nsnap=2)
    F = sn[-1]; u0 = g["acts"][0]["u0"]; z = F[0] - u0
    L, n = ndimage.label(z > 0.45 * (np.sqrt(2) - u0))
    prof = {k: np.zeros(30) for k in ("u", "m", "c")}; cnt = np.zeros(30)
    yy, xx = np.mgrid[:128, :128]
    for j in range(1, n + 1):
        cy, cx = ndimage.center_of_mass(L == j)
        dy = (yy - cy + 64) % 128 - 64; dx = (xx - cx + 64) % 128 - 64
        r = np.hypot(dy, dx).astype(int)
        sel = r < 30
        for k, f in (("u", z), ("m", F[3]), ("c", F[4])):
            prof[k] += np.bincount(r[sel], f[sel], 30)
        cnt += np.bincount(r[sel], minlength=30)
    for k in prof: prof[k] /= np.maximum(cnt, 1)
    r = np.arange(30) * 0.5
    ax.plot(r, prof["u"] / prof["u"].max(), label="body u (norm)", c="tab:blue")
    ax.plot(r, prof["m"], label="membrane m", c="tab:orange")
    ax.plot(r, prof["c"], label="cargo c", c="tab:purple")
    ax.set_title(f"{lab}: {n} cells", fontsize=9); ax.set_xlabel("distance from cell centre (units)")
    out[lab] = {k: prof[k].round(3).tolist() for k in prof}
axs[0].legend(fontsize=8)
fig.tight_layout(); fig.savefig("screens/profiles_containment.png", dpi=70)
json.dump(out, open("screens/profiles_containment.json", "w"))
for lab in out:
    c = np.array(out[lab]["c"]); m = np.array(out[lab]["m"])
    print(lab, "cargo centre", c[0], "cargo r=8", c[16], "m peak", m.max(), "at r", m.argmax() * 0.5, "m FWHM px", (m > m.max() / 2).sum())
