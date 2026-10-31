"""Reviewer analysis from the saved arms only (no simulation)."""
import json, sys
import numpy as np
RR = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/rods_runner/out"
G = ("device0", "device1", "global")
L = lambda p, r, a: dict(np.load(f"{RR}/{p}_{r}_{a}.npz"))
def es(x, y):   # independent implementation: ordered pairs incl. self, rms distance (norm / sqrt(d))
    d = x.shape[1]
    xy = np.sqrt(((x[:, None] - y[None]) ** 2).sum(-1)).mean() / np.sqrt(d)
    xx = np.sqrt(((x[:, None] - x[None]) ** 2).sum(-1)).mean() / np.sqrt(d)
    return xy - 0.5 * xx
nat = L("sham", "pred", "native")
sc = {g: nat[g].std(axis=(0, 1, 3)) + 1e-9 for g in G}
def flat(a, g, w, scale=None):
    s = sc[g] if scale is None else scale
    return (a[:, :w] / s[None, None, :, None]).reshape(len(a), -1)
out = {}
# (a) independent re-score of a few cells
cells = {}
for prog, arm, g, w in [("sham", "mar0", "device0", 10), ("surf", "dthalf", "device0", 10), ("surf", "dthalf", "global", 50),
                        ("cargo", "native", "device0", 10)]:
    tr = L(prog, "truth", "native"); p = L(prog, "pred", arm); n = L(prog, "pred", "native")
    cells[f"{prog}/{arm}/{g}/{w}"] = dict(es=round(es(flat(p[g], g, w), flat(tr[g], g, w)), 4),
                                         ratio=round(es(flat(p[g], g, w), flat(tr[g], g, w)) / es(flat(n[g], g, w), flat(tr[g], g, w)), 3))
p = L("cargo", "pred", "native"); tr = L("cargo", "truth", "native"); sh = L("sham", "pred", "native")
cells["cargo/ignore/device0/10"] = round(es(flat(sh["device0"], "device0", 10), flat(tr["device0"], "device0", 10)) /
                                         es(flat(p["device0"], "device0", 10), flat(tr["device0"], "device0", 10)), 3)
out["rescore"] = cells
# (b) permutation null from the 16 native members of the surf program vs the dthalf arm, sizes 5 / 5 / 6
rng = np.random.default_rng(1)
pool = {g: np.concatenate([L("surf", "pred", "native")[g], L("surf", "truth", "native")[g]]) for g in G}
dth = L("surf", "pred", "dthalf")
k0 = L("surf", "pred", "kappa0")
perm = {}
for w in (10, 25, 50):
    for g in G:
        P = flat(pool[g], g, w); D = flat(dth[g], g, w)
        nul, rd = [], []
        for _ in range(400):
            idx = rng.permutation(16); A, B, T = idx[:5], idx[5:10], idx[10:]
            nul.append(es(P[A], P[T]) / es(P[B], P[T]))
            Dsub = rng.choice(8, 5, replace=False)
            rd.append(es(D[Dsub], P[T]) / es(P[B], P[T]))
        perm[f"{w}tu/{g}"] = dict(null_5_95=[round(float(np.percentile(nul, 5)), 2), round(float(np.percentile(nul, 95)), 2)],
                                  dthalf_median=round(float(np.median(rd)), 2),
                                  dthalf_5_95=[round(float(np.percentile(rd, 5)), 2), round(float(np.percentile(rd, 95)), 2)],
                                  frac_dthalf_above_null95=round(float(np.mean(np.array(rd) > np.percentile(nul, 95))), 2))
out["perm_null_surf_5v5v6"] = perm
# (c) bias vs spread of the dthalf ensemble against the 16 native members, per readout time
bs = {}
for g in G:
    for t in (1, 2, 5, 10, 25, 50):
        N = pool[g][:, t - 1] / sc[g][None, :, None]; D = dth[g][:, t - 1] / sc[g][None, :, None]
        Np, Nt = N[:8], N[8:]
        sd = N.std(axis=0, ddof=1) + 1e-12
        keep = sd > 1e-6 * sd.max()
        z_d = ((D.mean(0) - N.mean(0)) / sd)[keep]
        z_n = ((Np.mean(0) - Nt.mean(0)) / sd)[keep]
        bs[f"{g}/t{t}"] = dict(rms_z_mean_dthalf_vs_native16=round(float(np.sqrt((z_d ** 2).mean())), 2),
                               expected_if_null=round(float(np.sqrt(1 / 8 + 1 / 16)), 2),
                               rms_z_mean_pred8_vs_truth8=round(float(np.sqrt((z_n ** 2).mean())), 2),
                               expected_pred_truth=0.5,
                               spread_ratio_dthalf_over_native=round(float(np.median((D.std(axis=0, ddof=1) + 1e-12)[keep] / sd[keep])), 2))
out["bias_spread_dthalf"] = bs
# (d) global group: pooled scale vs slot-level gap, and re-score with per-slot scales
gl = nat["global"]
out["global_scale_check"] = {f: dict(pooled=round(float(sc["global"][i]), 5),
                                     within_mean_slot_sd=round(float(gl[:, :, i, 0].std()), 6),
                                     within_var_slot_sd=round(float(gl[:, :, i, 1].std()), 6))
                             for i, f in enumerate(("phi", "q1", "q2", "s", "c", "om"))}
slot_sc = gl.std(axis=(0, 1)) + 1e-9   # (fields, slots)
slot_sc[5, 0] = 1.0                     # om mean is identically 0
def flat_slot(a, w):
    return (a[:, :w] / slot_sc[None, None]).reshape(len(a), -1)
rs = {}
for prog, arms in (("sham", ("mar0", "passive", "kappa0", "chis0")), ("surf", ("mar0", "passive", "kappa0", "chis0", "dthalf"))):
    tr = L(prog, "truth", "native"); n = L(prog, "pred", "native")
    for w in (10, 25, 50):
        base = es(flat_slot(n["global"], w), flat_slot(tr["global"], w))
        rs[f"{prog}/{w}tu"] = {a: round(es(flat_slot(L(prog, "pred", a)["global"], w), flat_slot(tr["global"], w)) / base, 2) for a in arms}
    base = es(flat_slot(n["global"], 50), flat_slot(tr["global"], 50))
    rs[f"{prog}/50tu"]["ignore_actions"] = (round(es(flat_slot(L("sham", "pred", "native")["global"], 50), flat_slot(tr["global"], 50)) / base, 2)
                                            if prog == "surf" else None)
out["global_rescored_per_slot_scales"] = rs
print(json.dumps(out, indent=1))
json.dump(out, open("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/rods_runner_review/analyse.json", "w"), indent=1)
