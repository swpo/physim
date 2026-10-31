"""energy-score ratios with sampling uncertainty: per-truth-member ES (8 values per arm), ratio of means with a
bootstrap over truth members and forecast members (2000 resamples); plus the swapped null (truth ensemble as forecast,
native ensemble as truth). usage: score_extra.py TAG arms windows"""
import sys, json
import numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex")
from apparatus import OUT, energy_score

tag, arms, wins = sys.argv[1], sys.argv[2].split(","), [float(w) for w in sys.argv[3].split(",")]
E = {a: np.load(OUT / f"ens_s0_{tag}_{a}.npy") for a in ["native", "truth"] + arms}
nat = E["native"]; nm, nt_all, nf = nat.shape
scale = nat.reshape(-1, nf).std(axis=0) + 1e-6
every = 2.0
rng = np.random.default_rng(0)
groups = {"all": np.arange(nf), "dev0": np.arange(0, 26), "dev1": np.arange(26, 64), "global": np.arange(64, 68)}
res = {}
for win in wins:
    nt = int(round(win / every))
    for g, gi in groups.items():
        Z = {a: (X[:, :nt][:, :, gi] / scale[gi]).reshape(nm, -1) for a, X in E.items()}
        # pairwise distances forecast(native) members to all members of each truth set
        def es_mat(F, Tr):
            a = np.linalg.norm(F[:, None] - Tr[None], axis=2)          # (forecast k, truth j)
            b = np.linalg.norm(F[:, None] - F[None], axis=2)           # (k, k')
            return a, b
        out = {}
        aN, bN = es_mat(Z["native"], Z["truth"])
        def boot(aT, aN, bN):
            vals = []
            for _ in range(2000):
                fk = rng.integers(0, nm, nm); tj = rng.integers(0, nm, nm); tn = rng.integers(0, nm, nm)
                bb = 0.5 * bN[np.ix_(fk, fk)].mean()
                num = aT[np.ix_(fk, tj)].mean() - bb
                den = aN[np.ix_(fk, tn)].mean() - bb
                vals.append(num / den)
            return np.percentile(vals, [5, 50, 95])
        base = aN.mean() - 0.5 * bN.mean()
        for a in arms:
            aT = np.linalg.norm(Z["native"][:, None] - Z[a][None], axis=2)
            r = (aT.mean() - 0.5 * bN.mean()) / base
            lo, md, hi = boot(aT, aN, bN)
            out[a] = [round(float(r), 2), round(float(lo), 2), round(float(hi), 2)]
        # swapped null: truth ensemble as forecast vs native as truth, ratio to truth-vs-truth? use native-forecast base
        aS = np.linalg.norm(Z["truth"][:, None] - Z["native"][None], axis=2)
        bS = np.linalg.norm(Z["truth"][:, None] - Z["truth"][None], axis=2)
        out["swap_native_truth"] = round(float((aS.mean() - 0.5 * bS.mean()) / base), 2)
        res[f"w{win:g}_{g}"] = out
for k, v in res.items():
    print(k, v)
(OUT / f"detect_ci_s0_{tag}.json").write_text(json.dumps(res, indent=1))
