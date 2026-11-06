"""Supplement: the coarse 'patchnet' trained 4x longer (it was still improving at the 300-epoch cap).

usage: python -B patch_long.py [EPOCHS]   -> results/closure_coarse_patchlong_items.npz

Same folds, items, standardisation, baseline and early stopping as closure_lib.make_patch_extra;
only the epoch cap (default 1200) and the patience (60) change. finalize.py adds it to the coarse
best-of set (per-item errors) and recomputes the ceiling, its SE and the selection check.
"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/fresh/closure/scripts")
import closure_lib as CL  # noqa: E402

AN = CL.AN
AN.HORIZONS = [1, 2, 4, 8, 16, 32]
EPOCHS = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:8.1f}s]", *a, flush=True)


D, cat, metas = CL.load_data()
Ys, Bs = D["Yc"], D["Bc"]
J = len(Ys)
allY = np.concatenate(Ys)
sd = allY.std(0)
eff = sd > 1e-6 * max(sd.max(), 1e-12)
sd = np.where(eff, sd, 1.0)
neff = int(eff.sum())
Ys = [Y[:, eff] / sd[eff] for Y in Ys]
Bs = [B[..., eff] / sd[eff] for B in Bs]
items = [(jj, i, int(t)) for jj in range(J) for i, t in enumerate(D["st_tick"][jj])]
HZ = AN.HORIZONS
FUT = np.stack([np.stack([np.stack([Ys[jj][t + h] for h in HZ])] + [np.stack([Bs[jj][i, r, h - 1] for h in HZ])
                                                                    for r in range(Bs[jj].shape[1])]) for jj, i, t in items])
R = FUT.shape[1]
orac = ((FUT - FUT.mean(1, keepdims=True)) ** 2).sum((1, 3)) / (R - 1) / neff
pred = np.zeros((len(items), len(HZ), neff))
info = []
hook = CL.make_patch_extra(D, log=log, info_store=info, epochs=EPOCHS, patience=60, seeds=(0, 1))
fold_of = {jj: D["j"][jj] % AN.NFOLD for jj in range(J)}
for f in range(AN.NFOLD):
    tr_j = [jj for jj in range(J) if fold_of[jj] != f]
    va_j = [jj for jj in tr_j if fold_of[jj] == (f + 1) % AN.NFOLD]
    fit_j = [jj for jj in tr_j if jj not in va_j]
    te = [n for n, it in enumerate(items) if fold_of[it[0]] == f]
    pred[te] = hook(f, Ys, tr_j, fit_j, va_j, [items[n] for n in te])["patchnet"]
err = ((FUT - pred[:, None]) ** 2).sum(3).mean(1) / neff
import os  # noqa: E402
orac_diff = None
if os.path.exists(f"{CL.RES}/closure_coarse_items.npz"):     # the main run may finish later; finalize checks again
    main = np.load(f"{CL.RES}/closure_coarse_items.npz")
    assert np.array_equal(main["items"], np.array(items)), "item order differs from the main run"
    orac_diff = float(np.abs(main["orac"] - orac.astype(np.float32)).max())
    log("items match the main run; max |orac - main orac| =", orac_diff)
log("patchnet_long V", np.round(err.mean(0), 4).tolist())
np.savez_compressed(f"{CL.RES}/closure_coarse_patchlong_items.npz", err=err.astype(np.float32), items=np.array(items),
                    orac=orac.astype(np.float32),
                    name="patchnet_long", epochs=EPOCHS)
json.dump(CL.jsonable({"epochs_cap": EPOCHS, "patience": 60, "info": info, "V": err.mean(0), "orac_check": orac_diff,
                       "seconds": time.time() - T0}),
          open(f"{CL.RES}/closure_coarse_patchlong.json", "w"), indent=1)
log("saved")
