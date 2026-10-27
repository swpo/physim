"""Within-rod bimodality: for every split-born rod with >= NMIN speed frames, the bimodality coefficient (BC) and the
KDE mode count of its own log speed series, against 200 phase-randomized surrogates of the same series (same power
spectrum, Gaussian marginals). Reports the fraction of rods above their surrogates' 95th percentile (5% expected by chance).
usage: perrod_bimod.py rods.json [...]"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/marangoni-bistability")
import numpy as np, states as S
from scipy import stats
NMIN = 80
R, trk = S.load(sys.argv[1:])
rng = np.random.default_rng(5)
hits = 0; n = 0; bcs = []; pv = []
for t in trk:
    x = np.log10(np.maximum(t["spL"], 1e-4))
    if len(x) < NMIN: continue
    n += 1; b = S.bimod_coef(x); bcs.append(b)
    X = np.fft.rfft(x - x.mean()); sur = []
    for _ in range(100):
        ph = np.exp(1j * rng.uniform(0, 2 * np.pi, len(X))); ph[0] = 1
        if len(x) % 2 == 0: ph[-1] = 1
        y = np.fft.irfft(X * ph, len(x)) + x.mean(); sur.append(S.bimod_coef(y))
    p = (np.sum(np.array(sur) >= b) + 1) / 101; pv.append(p)
    hits += p < 0.05
print(f"rods with >= {NMIN} frames: {n}; BC median {np.median(bcs):.3f}, BC > 0.555 in {np.sum(np.array(bcs) > 0.555)}; "
      f"above surrogate 95th pct: {hits} of {n} (expected by chance {0.05 * n:.1f}); binomial p {stats.binomtest(hits, n, 0.05, 'greater').pvalue:.3g}")


def nmodes(x, h, grid):
    y = stats.gaussian_kde(x, bw_method=h / x.std(ddof=1))(grid)
    return int(np.sum((y[1:-1] > y[:-2]) & (y[1:-1] > y[2:])))


def hcrit(x, grid):
    lo, hi = 1e-3, 2.0
    if nmodes(x, lo, grid) <= 1: return lo
    for _ in range(14):
        mid = np.sqrt(lo * hi)
        if nmodes(x, mid, grid) > 1: lo = mid
        else: hi = mid
    return hi


grid = np.linspace(-3.5, 0, 160)
rng = np.random.default_rng(6)
flag = []; nh = 0; n = 0
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
for t in trk:
    x = np.log10(np.maximum(t["spL"], 1e-4))
    if len(x) < NMIN: continue
    n += 1; hc = hcrit(x, grid)
    X = np.fft.rfft(x - x.mean()); sur = []
    for _ in range(40):
        ph = np.exp(1j * rng.uniform(0, 2 * np.pi, len(X))); ph[0] = 1
        if len(x) % 2 == 0: ph[-1] = 1
        sur.append(hcrit(np.fft.irfft(X * ph, len(x)) + x.mean(), grid))
    p = (np.sum(np.array(sur) >= hc) + 1) / 41
    nh += p < 0.05
    flag.append((p, hc, t))
print(f"Silverman critical bandwidth above surrogate 95th pct: {nh} of {n} (chance {0.05 * n:.1f}); binomial p {stats.binomtest(nh, n, 0.05, 'greater').pvalue:.3g}")
flag.sort(key=lambda z: z[0])
fig, axs = plt.subplots(3, 4, figsize=(16, 8.5), sharey=True)
for ax, (p, hc, t) in zip(axs.flat, flag[:12]):
    tt = (t["f"]) * 2.5
    ax.semilogy(tt, t["spL"], lw=1); ax.set_title(f"run{t['run']} #{t['id']} {t['fate']} p={p:.2f} hcrit={hc:.2f}", fontsize=8)
    ax.axhline(0.0077, color="0.6", ls=":"); ax.axhline(0.0108, color="0.6", ls=":")
fig.suptitle("12 split-born rods with the strongest within-rod multimodality (Silverman test vs phase-randomized surrogates); dotted: 40/60% thresholds")
fig.supxlabel("t"); fig.supylabel("speed (own lengths per t)")
fig.tight_layout(); fig.savefig(sys.argv[1].rsplit("/", 3)[0] + "/../../out/fig_a_flagged_traces.png" if False else "out/fig_a_flagged_traces.png", dpi=85)
