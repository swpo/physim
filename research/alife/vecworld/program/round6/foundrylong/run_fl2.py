"""run_fl2 -- study foundrylong (round 6), stage 2: can a hypothesis close the gap, and do experiments pay? (GPU job)

PILOT ONLY: every hidden world of this job is a public function of public seeds. These worlds, Lab data and items
must NEVER be reused as an exam. The noise secret (256 bits, os.urandom) is never written; it is new (stage 1's
items and Labs are not reused).

Declared in DECLARED.md (stage 2); details fixed in DEVIATIONS.md addendum 3 before the request. Order:
  hidden    per hidden world (the same 16): a Lab of 32 mix episodes and a Lab of 32 designed episodes (paired: the
            same initial states and free-tick noise), a new exam (96 items x 12 futures, 96 climatology runs), K, O,
            Kp, plug-ins (true weights, input-blind, another world), the ridge on each Lab
  stage 1   P0(1000) (3 seeds) and C(16384) seed 0, read from stage 1's public outputs (inputs/stage1/), scored again
  W mix     weight inference on the mix Lab: 32 screened prior worlds' weights scored by the fit loss on 8 episodes,
            the best 4 refined by Adam (fl_w.fit_batch: 16-tick forecast loss), seed 0 = the better of starts 1 and 3,
            seed 1 = the better of 2 and 4 (by the loss on all 32 episodes); W(true), W(prior)
  G* mix    FT(32) (cross-validated, 3 seeds), D(32) (3 seeds) on the mix Lab
  W, G* designed   the same on the designed Lab
  W+        simulate-to-train at the fitted weights (seed 0): 4,096 mix episodes, the C recipe at that size
Outputs under OUT: scores.npz, train_info.json, w_fits.npz, w_info.json, worlds.json, info.json, progress.txt.

usage: python -B run_fl2.py --out DIR [--size full|presmoke|smoke] [--max-hours H] [--full-hours H] [--cpu-ok]
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fl_lib as LL  # noqa: E402  (first: sets the pilot modules' episode constants)
import fl_w as W  # noqa: E402

FL, NN = LL.FL, LL.NN

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import tnca as TN  # noqa: E402
from vw.secret import Secret  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--size", default="full", choices=("full", "presmoke", "smoke"))
ap.add_argument("--max-hours", type=float, default=2.5)
ap.add_argument("--full-hours", type=float, default=None, help="presmoke: the time the full pass will have (speed guard)")
ap.add_argument("--cpu-ok", action="store_true")
args = ap.parse_args()
OUT = args.out
os.makedirs(OUT, exist_ok=True)
T0 = time.time()
T_END = T0 + args.max_hours * 3600

FULL = dict(burn=300, n_hidden=16, n_lab=32, lab_chunk=32, n_items=96, R=12, n_clim=96, m=24, m_plug=8, N=32,
            ft_lrs=[1.25e-5, 5e-5, 2e-4], ft_smax=400, ft_folds=4, d_steps=800, batch_lab=64, n_seeds=3, eval_small=50,
            chunk_steps=50, w_cands=32, w_pre_E=8, w_starts=4, w_steps=200, w_lr=(0.03, 0.01), w_eb=8, w_M=4, w_A=2, w_k=16,
            w_pool=16, w_respin=50, w_pair=2, w_eval_M=4, w_eval_pool=8,
            wp_n=4096, wp_steps=8000, wp_batch=128, wp_lock=8, eval_big=500, shape_test=False)
PRESMOKE = dict(FULL, n_hidden=2, ft_lrs=[5e-5, 2e-4], ft_smax=100, d_steps=100, n_seeds=2, w_cands=8, w_steps=10,
                wp_n=512, wp_steps=100, eval_big=50, shape_test=True)
SMOKE = dict(burn=3, n_hidden=2, n_lab=8, lab_chunk=4, n_items=4, R=3, n_clim=4, m=4, m_plug=3, N=8, ft_lrs=[2e-4, 8e-4],
             ft_smax=20, ft_folds=2, d_steps=20, batch_lab=16, n_seeds=2, eval_small=10, chunk_steps=10, w_cands=3, w_pre_E=2,
             w_starts=2, w_steps=2, w_lr=(0.03, 0.01), w_eb=2, w_M=2, w_A=1, w_k=4, w_pool=2, w_respin=1, w_pair=2, w_eval_M=2,
             w_eval_pool=2, wp_n=8, wp_steps=20, wp_batch=16, wp_lock=2, eval_big=10, shape_test=True)
CFG = {"full": FULL, "presmoke": PRESMOKE, "smoke": SMOKE}[args.size]
NN.Cfg.CHUNK = CFG["chunk_steps"]
if args.size == "smoke":
    NN.Cfg.EVAL_ROWS, NN.Cfg.EVAL_DRAWS = 16, 4
    LL.NV_H = 32
STRICT = args.size != "full"
FAILED, SKIPPED, CLOCK, INFO, WINFO, SPEED = [], [], {}, {}, {}, {}
NEX = sum(LL.ANCHORS)


def log(msg):
    line = f"{time.strftime('%H:%M:%S')} [{(time.time() - T0) / 60:6.1f} min] {msg}"
    print(line, flush=True)
    with open(os.path.join(OUT, "progress.txt"), "a") as f:
        f.write(line + "\n")


def jdump(name, obj):
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, np.bool_):
            return bool(o)
        return str(o)
    p = os.path.join(OUT, name)
    if isinstance(obj, dict):
        obj = {"PILOT_NEVER_REUSE_AS_EXAM": True, **obj}
    with open(p + ".tmp", "w") as f:
        json.dump(obj, f, indent=1, default=conv)
    os.replace(p + ".tmp", p)


def npz(name, **arrs):
    p = os.path.join(OUT, name)
    np.savez_compressed(p + ".tmp.npz", PILOT_NEVER_REUSE_AS_EXAM=np.array(True), **arrs)
    os.replace(p + ".tmp.npz", p)


def left():
    return T_END - time.time()


if not os.path.exists(os.path.join(OUT, "progress.txt")):
    with open(os.path.join(OUT, "progress.txt"), "w") as f:
        f.write("PILOT_NEVER_REUSE_AS_EXAM: the hidden worlds of this job are public pilot material\n")
backend = jax.default_backend()
log(f"run_fl2 size {args.size} max_hours {args.max_hours}; jax {jax.__version__} numpy {np.__version__} backend {backend} "
    f"devices {jax.devices()}; horizons {LL.HS}")
if backend != "gpu" and not args.cpu_ok:
    log("no GPU backend: refusing to run (use --cpu-ok for tests)")
    sys.exit(3)
PW = json.load(open(os.path.join(HERE, "inputs", "pilot_worlds.json")))
CN = json.load(open(os.path.join(HERE, "inputs", "code_norm.json")))
_s1w = os.path.join(HERE, "inputs", "stage1", "worlds.json")
S1W = json.load(open(_s1w)) if (os.path.exists(_s1w) or args.size != "smoke") else dict(train_labels=PW["train"])
SMU, SSD = np.asarray(CN["mean"], np.float32), np.asarray(CN["sd"], np.float32)
RUN = FL.Runner(2048 if args.size != "smoke" else 8, CFG["burn"])
SECRET = Secret()
KEY = jax.random.key(int.from_bytes(os.urandom(4), "little"))       # fit and prediction noise; not written


def theta_of_label(lab):
    s, i = lab[4:].split("-")
    return TN.draw_theta(int(s), int(i))


def np_theta(th):
    return {k: np.asarray(v, np.float64) for k, v in th.items()}


# ----------------------------------------------------------------------------- hidden worlds
def hidden_world(wi, hw, world, plug_label):
    th = hw["theta"]
    FL.set_params(world, th)
    sec = SECRET.child("world", "P", wi)
    rng = np.random.default_rng([20261112, 6, wi])
    t = time.time()
    labs = {"m": FL.run_lab(world, sec, CFG["n_lab"], CFG["lab_chunk"], rng),
            "d": W.run_lab_designed(world, sec, CFG["n_lab"], CFG["lab_chunk"])}
    ex = FL.build_exam(world, sec, CFG["n_items"], CFG["R"], CFG["n_clim"], f"P2-{wi}")
    hist, Ptest, klass = FL.item_arrays(ex)
    S = dict(FL.references(ex))
    S["Kp"] = FL.score_es(ex, FL.persistence_samples(hist))
    n, mp = ex.n, CFG["m_plug"]
    for nm, (thp, zero) in {"plugTrue": (th, False), "plugU0": (th, True), "plugPrior": (theta_of_label(plug_label), False)}.items():
        S[nm] = FL.score_es(ex, FL.plugin(ex, world, thp, mp, sec.keys(n * mp, "plug", nm), zero_program=zero))
    N = CFG["N"]
    for c, lab in labs.items():
        S[f"Dr{c}@{N}"] = FL.score_es(ex, FL.ridge_samples(FL.ridge_fit(lab["obs"][:N], lab["U"][:N]), hist, Ptest, CFG["m"], 7 + N))
    CLOCK["hidden_s"] = CLOCK.get("hidden_s", 0.0) + time.time() - t
    return dict(ex=ex, labs=labs, hist=hist, Ptest=Ptest, klass=klass, S=S, label=hw["label"], theta=th, plug_label=plug_label,
                D0=NN.item_dataset(hist, Ptest, SMU, SSD),
                lab_nats={c: dict(mean=float(lab["nats"].mean()), max=float(lab["nats"].max())) for c, lab in labs.items()})


def save_scores(HW):
    names = sorted(set().union(*[set(h["S"]) for h in HW]))
    names = [nm for nm in names if all(nm in h["S"] for h in HW)]
    npz("scores.npz", names=np.array(names), world=np.repeat(np.arange(len(HW)), CFG["n_items"]),
        item=np.tile(np.arange(CFG["n_items"]), len(HW)), klass=np.concatenate([h["klass"] for h in HW]),
        horizons=np.array(LL.HS), labels=np.array([h["label"] for h in HW]),
        **{"S__" + nm.replace("|", "__").replace("@", "_at_"): np.concatenate([h["S"][nm] for h in HW]) for nm in names})
    jdump("train_info.json", INFO)
    return names


def score_world_nets(HW, name, best, wids, seed):
    t = time.time()
    for k, i in enumerate(wids):
        h = HW[i]
        h["S"][f"{name}|s{seed}"] = FL.score_es(h["ex"], LL.samples_h(LL.tree_at(best, slice(None), k), h["D0"], CFG["m"], 800))
    CLOCK["scores_s"] = CLOCK.get("scores_s", 0.0) + time.time() - t


def quick(HW, names):
    base = sorted({n.split("|")[0] for n in names})
    L = {b: np.mean([np.concatenate([h["S"][n] for h in HW]) for n in names if n.split("|")[0] == b], 0).mean(0) for b in base}
    return {b: [round(float((L["K"][j] - L[b][j]) / (L["K"][j] - L["O"][j])), 3) for j in range(LL.NH)] for b in base if b not in ("K", "O")}


def load_stage1(n_hidden):
    """P0(1000) (3 seeds; leaves (NH, ...)) and C(16384) seed 0 per hidden world, from stage 1's public outputs."""
    d = os.path.join(HERE, "inputs", "stage1")
    if args.size == "smoke":
        return None, None
    z = dict(np.load(os.path.join(d, "params_p0w1000.npz")))
    seeds = sorted({k.split("/")[0] for k in z if k.startswith("s")})
    p0 = [LL.unflat_params({k[len(s) + 1:]: np.asarray(v, np.float32) for k, v in z.items() if k.startswith(s + "/")}) for s in seeds]
    cs = []
    for i in range(n_hidden):
        zc = dict(np.load(os.path.join(d, "cparams", f"c16384_w{i:02d}.npz")))
        cs.append(LL.unflat_params({k: np.asarray(v, np.float32) for k, v in zc.items() if k != "PILOT_NEVER_REUSE_AS_EXAM"}))
    return p0, cs


# ----------------------------------------------------------------------------- W
def w_condition(HW, c):
    """Weight inference on Lab c ('m' mix, 'd' designed) of every hidden world."""
    nH, N = len(HW), CFG["N"]
    Y = np.stack([h["labs"][c]["obs"][:N] for h in HW]).astype(np.float64)
    U = np.stack([h["labs"][c]["U"][:N] for h in HW]).astype(np.float64)
    dens = np.stack([np.asarray(W.dens_of(y)) for y in Y])
    sc = np.stack([W.lab_scale(y) for y in Y])
    cand = PW["train"][: CFG["w_cands"]]
    Zc = jnp.stack([W.to_z(theta_of_label(l)) for l in cand])
    t = time.time()
    pre = np.zeros((nH, len(cand)))
    for i in range(nH):
        r = lambda a: np.repeat(a[i:i + 1], len(cand), 0)
        pre[i] = W.eval_batch(Zc, r(dens), r(Y), r(U), r(sc), jax.random.fold_in(KEY, 10 + i), M=CFG["w_eval_M"], k=CFG["w_k"],
                              pool=CFG["w_eval_pool"], burn=CFG["burn"], E_max=CFG["w_pre_E"])
    order = np.argsort(pre, 1)[:, : CFG["w_starts"]]                          # (nH, S)
    CLOCK[f"w{c}_prescreen_s"] = time.time() - t
    log(f"W{c}: prescreen of {len(cand)} prior worlds' weights ({time.time() - t:.0f}s); best loss median {np.median(pre.min(1)):.4f}")
    S_, P_ = CFG["w_starts"], CFG["w_pair"]
    Zfit = np.zeros((nH, S_, W.NZ))
    ev = np.zeros((nH, S_))
    traces = []
    for g0 in range(0, nH, P_):
        g = list(range(g0, min(nH, g0 + P_)))
        rep = lambda a: np.concatenate([np.repeat(a[i:i + 1], S_, 0) for i in g])
        Z0 = jnp.concatenate([Zc[order[i]] for i in g])
        t1 = time.time()
        Z, tr = W.fit_batch(Z0, rep(dens), rep(Y), rep(U), rep(sc), jax.random.fold_in(KEY, 100 + g0), steps=CFG["w_steps"],
                            lr=CFG["w_lr"], eb=CFG["w_eb"], M=CFG["w_M"], A=CFG["w_A"], k=CFG["w_k"], pool=CFG["w_pool"],
                            burn=CFG["burn"], respin=CFG["w_respin"], log=log, tag=f" W{c} w{g0}",
                            t_max=None if args.size != "full" else max(60.0, left() - 600.0))
        e = W.eval_batch(Z, rep(dens), rep(Y), rep(U), rep(sc), jax.random.fold_in(KEY, 200 + g0), M=CFG["w_eval_M"], k=CFG["w_k"],
                         pool=CFG["w_eval_pool"], burn=CFG["burn"])
        Zfit[g] = np.asarray(Z).reshape(len(g), S_, W.NZ)
        ev[g] = e.reshape(len(g), S_)
        traces.append(tr)
        SPEED.setdefault(f"w{c}_fit", []).append(dict(steps=int(tr.shape[0]), B=int(Z0.shape[0]), seconds=time.time() - t1))
    CLOCK[f"w{c}_fit_s"] = time.time() - t
    # seeds: seed s is the better (all-episode fit loss) of starts s, s + 2, ...
    nseed = min(2, S_)
    pick = np.stack([np.array([s + 2 * np.argmin(ev[i, s::2]) for i in range(nH)]) for s in range(nseed)], 1)   # (nH, nseed)
    fitted = []
    for i, h in enumerate(HW):
        fitted.append([])
        for s in range(nseed):
            th = np_theta(W.from_z(jnp.asarray(Zfit[i, pick[i, s]]), dens[i]))
            fitted[i].append(th)
            t2 = time.time()
            Sm = W.predict_items(jax.tree_util.tree_map(jnp.asarray, th), h["hist"], h["Ptest"], jax.random.fold_in(KEY, 300 + 10 * i + s),
                                 m=CFG["m"], burn=CFG["burn"], queries=LL.HS)
            h["S"][f"W{c}|s{s}"] = FL.score_es(h["ex"], Sm)
            CLOCK["w_predict_s"] = CLOCK.get("w_predict_s", 0.0) + time.time() - t2
    zt = np.stack([np.asarray(W.to_z(h["theta"])) for h in HW])
    WINFO[c] = dict(candidates=cand, prescreen_loss=pre, starts=order, eval_loss=ev, pick=pick, dens=dens,
                    z_dist_net_rms=np.sqrt(((Zfit[:, :, : W.NZ_NET] - zt[:, None, : W.NZ_NET]) ** 2).mean(-1)),
                    z_box_err=Zfit[:, :, W.NZ_NET:] - zt[:, None, W.NZ_NET:],
                    trace_median=np.concatenate([np.median(tr, 1, keepdims=True) for tr in traces], 1) if traces else None)
    WINFO[c]["z_fit"] = Zfit
    WINFO[c]["fitted_seed0"] = [np_theta(f[0]) for f in fitted]
    npz("w_fits.npz", z_true=zt, **{f"z_fit_{cc}": WINFO[cc]["z_fit"] for cc in WINFO})
    jdump("w_info.json", {cc: {k: v for k, v in WINFO[cc].items() if k not in ("z_fit", "fitted_seed0")} for cc in WINFO})
    return fitted


def w_reference(HW):
    """The W predictor at the true weights and at another screened world's weights (the plugPrior world)."""
    for i, h in enumerate(HW):
        for nm, th in (("Wtrue", h["theta"]), ("Wprior", theta_of_label(h["plug_label"]))):
            Sm = W.predict_items(jax.tree_util.tree_map(jnp.asarray, th), h["hist"], h["Ptest"], jax.random.fold_in(KEY, 500 + 10 * i + len(nm)),
                                 m=CFG["m"], burn=CFG["burn"], queries=LL.HS)
            h["S"][f"{nm}|s0"] = FL.score_es(h["ex"], Sm)


def w_plus(HW, c):
    """Simulate-to-train at W's fitted weights (seed 0): wp_n mix episodes per world, the C recipe at that size."""
    nH, n = len(HW), CFG["wp_n"]
    ths = WINFO[c]["fitted_seed0"]
    t = time.time()
    TH = FL.stack_thetas([th for th in ths for _ in range(n)])
    rng = np.random.default_rng([7000, 17])
    cls = [x for _ in ths for x in FL.mix_classes(n, rng)]
    obs, U, _ = RUN.episodes(TH, 7000 + (c == "d"), classes=cls, prog_seed=7001, log=log, tag=f" W+{c}")
    CLOCK[f"wp{c}_sim_s"] = time.time() - t
    Lk = CFG["wp_lock"]
    for s0 in range(0, nH, Lk):
        grp = list(range(s0, min(nH, s0 + Lk)))
        dss = [LL.make_ds(obs[j * n:(j + 1) * n], U[j * n:(j + 1) * n], SMU, SSD, seed=j) for j in grp]
        best, inf = LL.train(dss, CFG["wp_steps"], [400 + 2 * j for j in grp], batch=CFG["wp_batch"], eval_every=CFG["eval_big"],
                             log=log, tag=f" W+{c} w{grp[0]}-{grp[-1]}", deadline=T_END, pad=(n, NEX * n, 3 * LL.NV_H))
        INFO[f"Wp{c}|s0|w{grp[0]}"] = dict(inf, worlds=grp)
        score_world_nets(HW, f"Wp{c}", best, grp, 0)
        del dss
    del obs, U


# ----------------------------------------------------------------------------- G*: FT, D on each Lab
def do_ft(HW, c, init_k):
    N, nH = CFG["N"], len(HW)
    for s in range(CFG["n_seeds"]):
        name = f"FT{c}@{N}|s{s}"
        best, inf = LL.ft_cv([h["labs"][c]["obs"] for h in HW], [h["labs"][c]["U"] for h in HW], N, [init_k[s]] * nH, SMU, SSD,
                             [600 + 2 * i + s for i in range(nH)], CFG["ft_lrs"], CFG["ft_smax"], folds=CFG["ft_folds"],
                             batch=CFG["batch_lab"], eval_every=CFG["eval_small"], pad=LAB_PAD, log=log, tag=f" {name}", deadline=T_END)
        INFO[name] = inf
        score_world_nets(HW, f"FT{c}@{N}", best, list(range(nH)), s)


def do_d(HW, c):
    N, nH = CFG["N"], len(HW)
    for s in range(CFG["n_seeds"]):
        dss = [LL.make_ds(h["labs"][c]["obs"][:N], h["labs"][c]["U"][:N], SMU, SSD, seed=N + i) for i, h in enumerate(HW)]
        for g0 in range(0, nH, 16):
            grp = list(range(g0, min(nH, g0 + 16)))
            best, inf = LL.train(dss[g0:g0 + 16], CFG["d_steps"], [700 + 2 * i + s for i in grp], batch=CFG["batch_lab"],
                                 eval_every=CFG["eval_small"], pad=LAB_PAD, deadline=T_END)
            INFO[f"D{c}@{N}|s{s}|w{g0}"] = dict(inf, worlds=grp)
            score_world_nets(HW, f"D{c}@{N}", best, grp, s)


LAB_PAD = (CFG["n_lab"], NEX * CFG["n_lab"], 3 * NN.Cfg.EVAL_ROWS if args.size != "smoke" else NN.Cfg.EVAL_ROWS * 4)


def write_info(done=False, extra=None):
    jdump("info.json", dict(size=args.size, finished=bool(done), config={k: v for k, v in CFG.items()},
                            platform=dict(jax=jax.__version__, numpy=np.__version__, python=platform.python_version(), backend=backend,
                                          devices=[str(d) for d in jax.devices()]),
                            member_ticks_runner=RUN.member_ticks, speed=SPEED, hours=(time.time() - T0) / 3600, failed=FAILED,
                            skipped=SKIPPED, clock=CLOCK, secret_commitment=SECRET.commitment(), **(extra or {})))


def speed_guard():
    """Presmoke: project the full pass from the measured fit speed and stage 1's timings; exit 4 if too slow."""
    F = FULL
    fs = [r for k in SPEED if k.startswith("w") for r in SPEED[k]]
    per_step_B = sum(r["seconds"] for r in fs) / max(sum(r["steps"] * r["B"] for r in fs), 1)   # s per step per fit
    nfits = 2 * F["n_hidden"] * F["w_starts"]
    w_s = per_step_B * F["w_steps"] * nfits * 1.15 + 2 * CLOCK.get("wm_prescreen_s", 60) * (F["n_hidden"] / CFG["n_hidden"]) * (F["w_cands"] / CFG["w_cands"])
    pred_s = CLOCK.get("w_predict_s", 30) * (F["n_hidden"] / CFG["n_hidden"]) * 1.5
    rest_s = 2 * 375 + 2 * 300 + 2 * (F["n_hidden"] * F["wp_n"] * 348 / 30000.0 + 450) + 900   # FT, D, W+ (sim + nets), data and scores
    total_h = (w_s + pred_s + rest_s) / 3600
    have = None if args.full_hours is None else args.full_hours - (time.time() - T0) / 3600
    ok = have is None or total_h <= 1.25 * have
    res = dict(seconds_per_fit_step=per_step_B, projected_w_hours=w_s / 3600, projected_hours_total=total_h, hours_available=have, speed_ok=ok)
    jdump("shape_test.json", res)
    log(f"speed guard: {per_step_B:.3f} s per fit step per fit; projected {total_h:.2f} h (W {w_s / 3600:.2f}); available {have}; ok {ok}")
    if not ok:
        log("TOO SLOW: stopping before the full pass")
        sys.exit(4)


def main():
    hidden = [dict(label=h["label"], theta=theta_of_label(h["label"])) for h in PW["hidden"][: CFG["n_hidden"]]]
    nH = len(hidden)
    train_labels = S1W["train_labels"]
    world = FL.build_world(hidden[0]["theta"], CFG["burn"])
    HW = []
    t = time.time()
    for wi, hw in enumerate(hidden):
        HW.append(hidden_world(wi, hw, world, train_labels[wi % len(train_labels)]))
    log(f"hidden worlds: {nH} x (2 Labs + exam + plug-ins + ridges) ({time.time() - t:.0f}s); designed Lab nats "
        f"{[h['lab_nats']['d']['mean'] for h in HW][:2]}")
    jdump("worlds.json", dict(hidden=[dict(label=h["label"], lab_nats=h["lab_nats"], plug_prior=h["plug_label"],
                                           lab_cls_mix="".join(h["labs"]["m"]["cls"])) for h in HW]))
    names = save_scores(HW)
    log(f"references: {quick(HW, names)}")
    p0, cs = load_stage1(nH)
    init_k = None

    def stage1_nets():
        nonlocal init_k
        for s, p in enumerate(p0):
            for h in HW:
                h["S"][f"P0w1000|s{s}"] = FL.score_es(h["ex"], LL.samples_h(p, h["D0"], CFG["m"], 800))
        for i, h in enumerate(HW):
            h["S"]["C16384|s0"] = FL.score_es(h["ex"], LL.samples_h(cs[i], h["D0"], CFG["m"], 800))
        init_k = [LL.tree_at(p, 1) for p in p0]                    # the parameters that were best at 16 ticks
    if args.size == "smoke":                                     # no stage-1 parameters on a CPU test: a tiny P0 instead
        def stage1_nets():
            nonlocal init_k
            ds = LL.make_ds(np.concatenate([h["labs"]["m"]["obs"] for h in HW]), np.concatenate([h["labs"]["m"]["U"] for h in HW]), SMU, SSD, seed=0)
            best, _ = LL.train(ds, 20, [0, 1], batch=16, eval_every=10)
            for s in range(2):
                for h in HW:
                    h["S"][f"P0w1000|s{s}"] = FL.score_es(h["ex"], LL.samples_h(LL.tree_at(best, slice(None), s), h["D0"], CFG["m"], 800))
                for h in HW:
                    h["S"]["C16384|s0"] = h["S"]["P0w1000|s0"]
            init_k = [LL.tree_at(best, 1, s) for s in range(2)]
    plan = [("stage-1 nets", stage1_nets), ("W mix", lambda: w_condition(HW, "m")), ("W references", lambda: w_reference(HW)),
            ("FT mix", lambda: do_ft(HW, "m", init_k)), ("D mix", lambda: do_d(HW, "m")),
            ("W designed", lambda: w_condition(HW, "d")), ("FT designed", lambda: do_ft(HW, "d", init_k)), ("D designed", lambda: do_d(HW, "d")),
            ("W+ mix", lambda: w_plus(HW, "m")), ("W+ designed", lambda: w_plus(HW, "d"))]
    for what, fn in plan:
        if left() < 240 and args.size == "full":
            SKIPPED.append(f"{what} (time left {left():.0f}s)")
            log("SKIP " + SKIPPED[-1])
            continue
        t = time.time()
        try:
            fn()
        except Exception:
            FAILED.append(what)
            log("FAILED " + what + "\n" + traceback.format_exc())
        CLOCK[f"{what}_s"] = time.time() - t
        names = save_scores(HW)
        write_info()
        log(f"{what} done ({time.time() - t:.0f}s); skill by horizon {LL.HS}: {quick(HW, names)}")
        if what == "W mix" and CFG["shape_test"]:
            speed_guard()
    stopped = [k for k, v in INFO.items() if isinstance(v, dict) and v.get("stopped_early")]
    if stopped:
        SKIPPED.append(f"stopped early by the deadline: {stopped}")
    write_info(done=True)
    log(f"done: {(time.time() - T0) / 3600:.2f} h; failed {FAILED}; skipped {SKIPPED}")
    sys.exit(1 if (FAILED or (STRICT and SKIPPED)) else 0)


if __name__ == "__main__":
    main()
