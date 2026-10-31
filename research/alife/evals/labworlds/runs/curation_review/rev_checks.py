"""Review checks: NN-rotation duplication, IC isotropy rotated vs unrotated, synthetic-ellipse A4 bias of analyze.elongation."""
import json, sys
import numpy as np
from scipy import ndimage
sys.path.insert(0, "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/curation")
import cc, analyze as A
from labkit import run as R
out = {}
# 1. nearest-neighbour 45-degree remap: how often is each source pixel used?
idx = np.arange(128 * 128, dtype=float).reshape(128, 128)
used = np.bincount(cc.rot_nn(idx).astype(int).ravel(), minlength=128 * 128)
out["nn_rot_source_use_frac"] = {str(k): round(float((used == k).mean()), 3) for k in range(4)}
# 2. IC isotropy: A4 of |grad phi|-weighted gradient direction and of the power spectrum, 16 seeds each way
W = cc.load("pm")
def ica4(rot):
    g4, s4 = [], []
    for s in range(100, 116):
        phi = cc.ic("pm", s, rot, W=W)["phi"]
        gy, gx = np.gradient(phi)
        w = np.hypot(gy, gx); th = np.arctan2(gy, gx)
        g4.append(float((w * np.cos(4 * th)).sum() / w.sum()))
        F = np.abs(np.fft.fft2(phi - phi.mean())) ** 2
        ky, kx = np.meshgrid(np.fft.fftfreq(128), np.fft.fftfreq(128), indexing="ij")
        k = np.hypot(ky, kx); m = (k > 0.01) & (k < 0.08)
        s4.append(float((F[m] * np.cos(4 * np.arctan2(ky[m], kx[m]))).sum() / F[m].sum()))
    return dict(grad_A4=[round(np.mean(g4), 4), round(np.std(g4) / 4, 4)], spec_A4=[round(np.mean(s4), 4), round(np.std(s4) / 4, 4)])
out["ic_isotropy"] = {"rot0": ica4(0), "rot45": ica4(45)}
# interior correspondence: rotated IC vs ndimage.rotate of the unrotated IC (central disc r<40)
p0 = cc.ic("pm", 11, 0, W=W)["phi"]; p45 = cc.ic("pm", 11, 45, W=W)["phi"]
pr = ndimage.rotate(p0, -45, reshape=False, order=1, mode="wrap")
pr2 = ndimage.rotate(p0, 45, reshape=False, order=1, mode="wrap")
yy, xx = np.indices(p0.shape); disc = np.hypot(yy - 63.5, xx - 63.5) < 40
out["interior_corr_rot_vs_rotated_unrot"] = [round(float(np.corrcoef(p45[disc], pr[disc])[0, 1]), 3), round(float(np.corrcoef(p45[disc], pr2[disc])[0, 1]), 3)]
# 3. pm body sizes (final frame of the re-run) and a synthetic-ellipse control of analyze.elongation
z = np.load(sys.argv[1]); rec = z["rec"][:, 0]
mn, thr, lo, hi = R._normalize_matter(rec, W.META, True, None)
comps, links = R._segment_frames(mn[-40:], thr, R._default_min_area(128, 128), True, keep_labels=True)
el_area = []
for c in comps[::5]:
    for i in range(c["n"]):
        if c["area"][i] >= 20:
            el_area.append(int(c["area"][i]))
el_area = np.array(el_area)
out["pm_body_area_px"] = [int(np.percentile(el_area, q)) for q in (10, 50, 90)]
rng = np.random.default_rng(5)
def synth(n_frames, areas, soft):
    th_all = []
    for f in range(n_frames):
        img = np.zeros((128, 128))
        yy, xx = np.indices(img.shape)
        for gy in range(4):
            for gx in range(4):
                ar = rng.choice(areas); asp = rng.uniform(1.0, 2.6); phi0 = rng.uniform(0, np.pi)
                a = np.sqrt(ar * asp / np.pi); b = a / asp
                cy, cx = 16 + 32 * gy + rng.uniform(-1, 1), 16 + 32 * gx + rng.uniform(-1, 1)
                dy, dx = yy - cy, xx - cx
                u = dx * np.cos(phi0) + dy * np.sin(phi0); v = -dx * np.sin(phi0) + dy * np.cos(phi0)
                img = np.maximum(img, ((u / a) ** 2 + (v / b) ** 2 <= 1).astype(float))
        if soft:
            img = ndimage.gaussian_filter(img, soft, mode="wrap")
        lab, n = ndimage.label(img > 0.5)
        idxs = range(1, n + 1)
        area = ndimage.sum(np.ones_like(img), lab, idxs)
        cyx = ndimage.center_of_mass(np.ones_like(img), lab, idxs)
        seg = dict(lab=lab, n=n, area=area, cy=[c[0] for c in cyx], cx=[c[1] for c in cyx])
        th_all += [t for t, asp in A.elongation(seg) if asp > 1.5]
    return A.a4(th_all)
out["synthetic_A4_pm_areas_hard"] = synth(200, el_area, 0)
out["synthetic_A4_pm_areas_soft1.5"] = synth(200, el_area, 1.5)
small = el_area[el_area < np.percentile(el_area, 30)]
out["synthetic_A4_smallest30pct_hard"] = synth(200, small, 0)
print(json.dumps(out, indent=1))
