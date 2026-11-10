"""reference_agent -- scripted policies that go through exactly the agent's interface.

Run inside an agent workspace (cwd = workspace; `physim2` and TASK.md are there; the real world is reachable
only through physim2.Lab). Each policy writes submission/ (predict.py, ridge_family.py, model.npz) and submits.

  S     scripted science, a shrunk simulate-to-train (round4/sbi): N real episodes of exam shape -> design
        simulations at prior draws -> regression summaries -> synthetic-likelihood posterior -> training
        simulations at posterior draws -> ridge predictor
  D     data only: the ridge predictor fitted to the real episodes the tick budget allows (no simulator)
  P0    no hypothesis, no experiment: the ridge predictor trained on simulations at prior draws
  PM    the ridge predictor trained on simulations at the prior mean
  C     designer's ceiling: trained on simulations at the true parameters (--theta, evaluator only)
  null  the null agent: samples from the prior-predictive long-run law, ignoring history and program

usage: python reference_agent.py --policy S --sizes '{"n_lab": 8, "n_design": 256, "k_design": 2, "n_train": 512}'
"""
import argparse
import json
import os
import shutil
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.getcwd())
sys.path.insert(0, HERE)

import inference as INF  # noqa: E402
import physim2  # noqa: E402
import ridge_family as RF  # noqa: E402

T0 = time.time()
LOG = {"stages": {}, "member_ticks_simulated": 0}


def stage(name, t):
    LOG["stages"][name] = {"wall_s": round(time.time() - t, 2)}
    print(f"[{time.time() - T0:7.1f}s] {name}", flush=True)


def lab_episodes(lab, W, n, P, H, seed, tag):
    names = list(W.program_mix().names)
    obs, UU = [], []
    for i in range(n):
        o0 = lab.reset(f"{tag}-{i}")
        hist = np.concatenate([o0[None], lab.advance(P)], 0)
        U = W.draw_program(names[i % len(names)], np.random.default_rng([seed, 21, i]), hist, H)
        if np.any(U):
            o2 = lab.advance(U)
        else:
            o2 = lab.advance(H)
        obs.append(np.concatenate([hist, o2], 0))
        UU.append(np.concatenate([np.zeros((P, W.N_IN)), U], 0))
    return np.stack(obs), np.stack(UU)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", required=True, choices=["S", "D", "P0", "PM", "C", "null"])
    ap.add_argument("--sizes", default="{}")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="submission")
    ap.add_argument("--theta", default=None)
    ap.add_argument("--no-submit", action="store_true")
    a = ap.parse_args()
    sz = {"n_lab": 8, "n_design": 128, "k_design": 2, "n_train": 256, "chunk": 64}
    sz.update(json.loads(a.sizes))
    W = physim2.load_world()
    world = W.NAME
    lab = None if a.no_submit and a.policy not in ("S", "D") else physim2.Lab()
    if lab is not None:
        card = lab.card()
        P, queries = card["exam"]["prefix_P"], {int(l): v for l, v in card["exam"]["queries"].items()}
        cost = card["ticks"]["reset_cost"] + P + max(max(v) for v in queries.values())
        left = card["ticks"]["max_ticks"] - lab.usage()["ticks_used"]
    else:                                                   # evaluator-run reference without a laboratory
        P, queries = W.P_PREFIX, {int(l): list(v) for l, v in W.QUERIES.items()}
    H = max(max(v) for v in queries.values())
    scales = W.scales()
    rng = np.random.default_rng([a.seed, 1])
    d = len(W.THETA_NAMES)
    cen, hw = (W.PRIOR_LO + W.PRIOR_HI) / 2, (W.PRIOR_HI - W.PRIOR_LO) / 2
    sim = None

    def simulate(thetas, seed):
        nonlocal sim
        if sim is None:
            sim = W.Simulator(chunk=sz["chunk"])
        outs = [sim.episodes(thetas[s:s + sz["chunk"]], seed + s, P=P, H=H) for s in range(0, len(thetas), sz["chunk"])]
        LOG["member_ticks_simulated"] = int(sim.member_ticks)
        return np.concatenate([o["obs"] for o in outs]), np.concatenate([o["U"] for o in outs])

    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    if a.policy == "null":
        t = time.time()
        th = W.prior_sample(rng, sz["n_train"])
        sim = W.Simulator(chunk=sz["chunk"])
        obs = np.concatenate([sim.episodes(th[s:s + sz["chunk"]], a.seed + s, P=P, H=H,
                                           classes=np.array(["a"] * len(th[s:s + sz["chunk"]]))) ["obs"]
                              for s in range(0, len(th), sz["chunk"])])
        LOG["member_ticks_simulated"] = int(sim.member_ticks)
        pool = {f"level{l}": np.asarray(W.level(l, obs[:, [P + t_ for t_ in ts]]), np.float32) for l, ts in queries.items()}
        np.savez_compressed(os.path.join(out, "pool.npz"), **pool)
        open(os.path.join(out, "predict.py"), "w").write(NULL_PY)
        stage("null pool", t)
    else:
        obs_lab = None
        if a.policy in ("S", "D"):
            t = time.time()
            n_lab = min(int(sz["n_lab"]), left // cost) if a.policy == "S" else left // cost
            if a.policy == "D" and sz.get("n_lab_D"):
                n_lab = min(int(sz["n_lab_D"]), left // cost)
            obs_lab, U_lab = lab_episodes(lab, W, int(n_lab), P, H, a.seed, f"{a.policy}{a.seed}")
            LOG["lab_episodes"] = int(n_lab)
            stage("lab episodes", t)
        if a.policy == "D":
            Ytr, Utr = obs_lab, U_lab
        else:
            if a.policy == "S":
                t = time.time()
                ud = rng.uniform(-1, 1, (sz["n_design"], d))
                od, _ = simulate(np.repeat(cen + ud * hw, sz["k_design"], 0), 1000 * (a.seed + 1))
                F = INF.features(world, od, scales).reshape(sz["n_design"], sz["k_design"], -1)
                half = sz["n_design"] // 2                      # cross-fitting: summaries on one half, likelihood on the other
                proj = INF.Projection().fit(F[:half].reshape(half * sz["k_design"], -1), np.repeat(ud[:half], sz["k_design"], 0),
                                            groups=np.repeat(np.arange(half), sz["k_design"]))
                sl = INF.LinSL().fit(ud[half:], proj(F[half:]))
                sbar = proj(INF.features(world, obs_lab, scales)).mean(0)
                draws, diag = INF.posterior(sl, sbar, len(obs_lab), d, rng, n_out=sz["n_train"])
                LOG["posterior"] = {k: diag[k] for k in ("ess", "sd_over_prior_sd")}
                LOG["emulator_degree"], LOG["projection"] = sl.deg, {"lambda": proj.lam, "cv_r2": proj.cv_r2}
                np.save(os.path.join(os.getcwd(), "posterior_draws_u.npy"), draws)     # the agent's own notes
                thetas = cen + draws * hw
                stage("inference", t)
            elif a.policy == "P0":
                thetas = W.prior_sample(rng, sz["n_train"])
            elif a.policy == "PM":
                thetas = np.tile(cen, (sz["n_train"], 1))
            else:
                thetas = np.tile(np.array([float(v) for v in a.theta.split(",")]), (sz["n_train"], 1))
            t = time.time()
            Ytr, Utr = simulate(thetas, 5000 * (a.seed + 1))
            stage("training simulations", t)
        t = time.time()
        model = RF.fit(world, Ytr, Utr, queries, scales, seed=a.seed)
        LOG["ridge_lambdas"] = [float(v) for v in model["lams"]]
        np.savez_compressed(os.path.join(out, "model.npz"), **model)
        shutil.copy(os.path.join(HERE, "ridge_family.py"), os.path.join(out, "ridge_family.py"))
        open(os.path.join(out, "predict.py"), "w").write(RF.PREDICT_PY)
        LOG["train_episodes"] = int(len(Ytr))
        stage("fit", t)
    LOG["cpu_s"] = time.process_time()
    LOG["wall_s"] = time.time() - T0
    if lab is not None and not a.no_submit:
        LOG["validate"] = lab.validate(os.path.relpath(out, os.getcwd()))
        LOG["submit"] = lab.submit(os.path.relpath(out, os.getcwd()))
        LOG["usage"] = lab.usage()
    json.dump(LOG, open(os.path.join(os.getcwd(), f"agent_log_{a.policy}.json"), "w"), indent=1)
    print(json.dumps({k: LOG.get(k) for k in ("member_ticks_simulated", "lab_episodes", "train_episodes", "cpu_s", "submit")}))


NULL_PY = '''"""Null agent: samples from the prior-predictive long-run law (no history, no program)."""
import os

import numpy as np

_P = None


def predict(history, program, queries, n_samples, seed):
    global _P
    if _P is None:
        _P = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pool.npz"))
    rng = np.random.default_rng(seed)
    out = {}
    for l in queries:
        pool = _P[f"level{l}"]
        out[l] = pool[rng.integers(0, len(pool), n_samples)]
    return out
'''

if __name__ == "__main__":
    main()
