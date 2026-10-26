"""Sweep runner: python sweep_run.py TAG T PARAMS_JSON SEEDS... -> runs/TAG_sSEED.json (cohort measure vs RB shadow, top-20 overlap)."""
import sys, os, time, json, numpy as np
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '20261026T0009-c30-hash-chemistry-o-calibration')
sys.path.insert(0, W); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import world, o_measure as om
tag, T = sys.argv[1], int(sys.argv[2]); p = json.loads(sys.argv[3]); seeds = [int(s) for s in sys.argv[4:]]
for s in seeds:
    t0 = time.time(); S = world.init(s, p=dict(p, maxev=420 * T + 10**6)); tops = []
    for t in range(T):
        world.step(S)
        if (t + 1) % 1000 == 0 and S["n"]:
            c = np.bincount(S["ty"][:S["n"]], minlength=1001); tops.append(round(float(c.max() / S["n"]), 2))
    L = world.logs(S)
    if L["pop"][-1] == 0:
        print(tag, s, "extinct", int(np.argmax(L["pop"] == 0)), flush=True); continue
    sh = om.shadow(L, seed=1)
    a = om.stats(L, T, win=1000); b = om.stats(sh | {"mut_n": L["mut_n"]}, T, win=1000)
    res = dict(tag=tag, seed=s, p=p, pop_end=int(L["pop"][-1]), pop_mean=float(L["pop"][T//2:].mean()), uniq=int(a["cum_unique"][-1]), sh_uniq=int(b["cum_unique"][-1]),
               cohort=a["cohort_new"].tolist(), sh_cohort=b["cohort_new"].tolist(), ov=[round(v, 2) for v in a["top_overlap_first"]],
               ovp=[round(v, 2) for v in a["top_overlap_prev"]], msize=[round(float(v), 2) for v in a["mean_size"]], toptype_share=tops, secs=round(time.time() - t0))
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs", f"{tag}_s{s}.json"), "w"))  # (c32) path fixed
    print(tag, s, f"{res['secs']}s pop={res['pop_mean']:.0f} late_cohort={sum(res['cohort'][2:])} sh={sum(res['sh_cohort'][2:])} ov_end={res['ov'][-1]} top={tops[::4]}", flush=True)
