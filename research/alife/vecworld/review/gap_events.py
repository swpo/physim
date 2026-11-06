"""Where does the tau = 1 Phi_objects gap sit? AR(1) error (same as the best predictor) against the
base continuation, split by slots that have a tracker event (fusion/fission/fused/birth/death) at
t+1 in the base run vs slots that continue without one. Also: median A_sum of tracked-body cells."""
import glob, json, sys
import numpy as np
INT = "/home/user/evalwork/vecworld/integrate"
sys.path.insert(0, INT)
import lenia_world as LW
NF = LW.NF
fs = sorted(glob.glob(f"{INT}/data/A_gliders/base_*.npz"))
D = [np.load(f) for f in fs]
Ys = [d["Yo"] for d in D]
sd = np.concatenate(Ys).std(0); eff = sd > 1e-6 * sd.max(); sd = np.where(eff, sd, 1)
Z = [Y / sd for Y in Ys]
J = len(Z); fold = np.arange(J) % 4
err_ev, err_no, n_ev, n_no = [], [], 0, 0
grp = {"identity": [0, 1, 2], "position": [3, 4, 5, 6], "shape": [7, 8, 9], "velocity": [10, 11]}
acc = {k: {g: 0.0 for g in grp} for k in ("event", "none")}
cnt = {"event": 0, "none": 0}
for f in range(4):
    tr = [j for j in range(J) if fold[j] != f]
    mu = np.concatenate([Z[j] for j in tr]).mean(0)
    a = np.concatenate([Z[j][:-1] for j in tr]) - mu; b = np.concatenate([Z[j][1:] for j in tr]) - mu
    rho = (a * b).sum(0) / np.maximum((a * a).sum(0), 1e-12)
    for j in [j for j in range(J) if fold[j] == f]:
        for t in (D[j]["st_tick"] - int(D[j]["burn_in"])):
            p = mu + rho * (Z[j][t] - mu)
            e = ((Z[j][t + 1] - p) ** 2).reshape(-1, NF)          # (K, NF)
            ev = D[j]["tab"][t + 1][:, 3]                           # event code per slot at t+1
            wasp = Ys[j][t].reshape(-1, NF)[:, 0] > 0.5
            isp = Ys[j][t + 1].reshape(-1, NF)[:, 0] > 0.5
            for s in range(e.shape[0]):
                if not (wasp[s] or isp[s]):
                    continue
                k = "event" if (ev[s] != 0 or wasp[s] != isp[s]) else "none"
                cnt[k] += 1
                for g, idx in grp.items():
                    acc[k][g] += e[s, idx].sum()
tot = sum(acc[k][g] for k in acc for g in grp)
out = {"slot_ticks": cnt, "share_of_total_sq_error": {k: {g: round(acc[k][g] / tot, 3) for g in grp} for k in acc},
       "share_event_slots": round(sum(acc["event"].values()) / tot, 3)}
# median A_sum over tracked-body cells at the saved test states
S = []
for d in D[:6]:
    for i in range(3):
        h = d["st_h0"][i].reshape(2, -1).sum(0); body = d["st_m"][i][:16384] > 0
        S.append(h[body])
S = np.concatenate(S)
out["median_Asum_body_cells"] = float(np.median(S)); out["median_Asum_cells_gt_0.01"] = float(np.median(np.concatenate([d["st_h0"][i].reshape(2,-1).sum(0)[d["st_h0"][i].reshape(2,-1).sum(0) > 0.01] for d in D[:6] for i in range(3)])))
print(json.dumps(out, indent=1))
json.dump(out, open("/home/user/evalwork/vecworld_integrate_review/gap_events.json", "w"), indent=1)
