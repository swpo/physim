"""Checker: (1) the unmodified VW-0 estimator analyze.closure (MLP off) on the saved VW-1 data must
reproduce closure_objects.json's V for every non-learned predictor; (2) re-train slotnet on fold 0
(same code, seeds, epochs) and compare with the saved per-item errors / tau-1 predictions."""
import json, sys, time
import numpy as np
sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/fresh/closure/scripts")
import closure_lib as CL
AN = CL.AN
AN.HORIZONS = [1, 2, 4, 8, 16, 32]
RES = CL.RES
T0 = time.time()
D, cat, metas = CL.load_data()
js = json.load(open(f"{RES}/closure_objects.json"))
it = np.load(f"{RES}/closure_objects_items.npz")
names = [str(x) for x in it["names"]]
out = {}
ref = AN.closure(D, "objects", K=12, mlp=False)[0]
out["analyze_closure_V_maxabs_vs_json"] = {nm: float(np.abs(np.asarray(ref["V"][nm]) - np.asarray(js["V"][nm])).max())
                                          for nm in ref["V"] if nm != "mlp" and nm in js["V"]}
out["analyze_closure_Voracle_maxabs"] = float(np.abs(np.asarray(ref["V_oracle"]) - np.asarray(js["V_oracle"])).max())
out["analyze_closure_s"] = time.time() - T0
print(out, flush=True)
Ys0 = D["Yo"]; J = len(Ys0)
allY = np.concatenate(Ys0); sd = allY.std(0); eff = sd > 1e-6 * max(sd.max(), 1e-12); sd = np.where(eff, sd, 1.0)
Ys = [Y[:, eff] / sd[eff] for Y in Ys0]
items = [tuple(x) for x in it["items"]]
fold_of = {jj: jj % AN.NFOLD for jj in range(J)}
f = 0
tr_j = [jj for jj in range(J) if fold_of[jj] != f]
va_j = [jj for jj in tr_j if fold_of[jj] == (f + 1) % AN.NFOLD]
fit_j = [jj for jj in tr_j if jj not in va_j]
te = [n for n, x in enumerate(items) if fold_of[x[0]] == f]
t1 = time.time()
P = CL.make_slot_extra(D, epochs=300, seeds=(0, 1))(f, Ys, tr_j, fit_j, va_j, [items[n] for n in te])["slotnet"]
out["slotnet_fold0_s"] = time.time() - t1
P1 = it["P1"][names.index("slotnet")][te].astype(float)
out["slotnet_fold0_tau1_pred_maxabs_vs_saved"] = float(np.abs(P[:, 0] - P1).max())
Bs = [B[..., eff] / sd[eff] for B in D["Bo"]]
FUT = np.stack([np.concatenate([np.stack([Ys[j][t + h] for h in AN.HORIZONS])[None],
                                np.stack([Bs[j][i, :, h - 1] for h in AN.HORIZONS], 1)], 0) for j, i, t in (items[n] for n in te)])
e = ((FUT - P[:, None]) ** 2).sum(3).mean(1) / FUT.shape[3]
es = it["err"][names.index("slotnet")][te].astype(float)
out["slotnet_fold0_err_maxabs_vs_saved"] = float(np.abs(e - es).max())
out["slotnet_fold0_V_mine"] = e.mean(0).tolist(); out["slotnet_fold0_V_saved"] = es.mean(0).tolist()
out["total_s"] = time.time() - T0
json.dump(out, open("/home/user/evalwork/vecworld/vw1/fresh/closure/check/e2e_analysis.json", "w"), indent=1)
print(json.dumps(out, indent=1))
