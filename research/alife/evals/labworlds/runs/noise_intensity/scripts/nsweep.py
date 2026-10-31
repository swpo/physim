"""Intensity-scaled correlated noise (ell = 2 world units): control separation and behaviour per level.

Worlds: phase_membrane (runner_demo.py / labeval declaration) and fed vortices (vortex_demo.py / labeval),
with every noisy field's sd read as an intensity (LabWorld.noise_intensity) and ell = 2 on every noisy field.

  time   --world W --level X            CPU-s of one 50-tu member (pulse program)
  score  --world W --level X            8-member ensembles on the world's pulse program: three natives (T, A, B),
                                        the mechanism ablation (X) and the action-free predictor (I, sham program)
  null   --world W --level X            8-member dt-halved native on the pulse program (numerics penalty)
  det    --world W                      zero-noise deterministic native at dt and dt/2 (1 member each)
  behav  --world W --level X --seed S   a labkit pack (labkit.run.run_pack) of the noisy world from init(S)
Groups and scales are the frozen labeval suites' (white-noise calibration), the same at every level.
Member seeds are the same at every level (common random numbers across levels).
"""
import argparse, dataclasses, json, os, sys, time
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np

ENV = "/home/user/swpo/residency-environments/environments/physim"
sys.path.insert(0, ENV)
sys.path.insert(0, "/home/user/swpo/residency-environments/scripts/physim/labworlds")
import labeval as LE  # noqa: E402
from physim import labworld as LW  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out"
SUITE = Path("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/suite")
ELL = 2.0
MEMBERS = 8
SEED0 = 600000
WORLD = {
    "pm": dict(spec=LE.phase_membrane, suite="pm", ablation="chi0",
               pulse=[dict(t=0, kind="inject", device=0, port=1, amp=3.0, dur=10.0)], program="pulse_d0_K"),
    "fv": dict(spec=LE.fed_vortices, suite="fv", ablation="adv0",
               pulse=[dict(t=0, kind="inject", device=0, port=0, amp=3.0, dur=10.0)], program="pulse_d0_om"),
}
ENSEMBLES = {"T": ("native", "pulse", 1), "A": ("native", "pulse", 2), "B": ("native", "pulse", 3),
             "X": ("ablation", "pulse", 4), "I": ("native", "sham", 5)}


def make_spec(world, level, ell=ELL):
    s = WORLD[world]["spec"]()
    w = s.world
    noise = {f: (kind, float(level)) for f, (kind, _) in w.noise.items()}
    s.world = dataclasses.replace(w, noise=noise, noise_corr={f: ell for f in w.noise} if ell else {},
                                  noise_intensity=tuple(w.noise))
    return s


def ldir(world, level):
    d = OUT / "score" / world / f"L{level:g}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def ensemble(spec, variant, actions, seed, path, members=MEMBERS):
    meta = dict(variant=variant, actions=actions, seed=seed, members=members,
                declaration=LE._jsonable(spec.world.declaration()))
    return LE.cached(path, lambda: LE.make_oracle(spec, variant).sample_truth(actions, LE.queries(), members,
                                                                              truth_seed=seed), meta=meta)


def cmd_time(a):
    spec = make_spec(a.world, a.level)
    o = LE.make_oracle(spec, "native")
    t0 = time.process_time()
    o.sample_truth(WORLD[a.world]["pulse"], LE.queries(), 1, truth_seed=1)
    print(f"{a.world} level {a.level}: {time.process_time() - t0:.2f} cpu-s per 50-tu member", flush=True)


def cmd_score(a):
    spec, W = make_spec(a.world, a.level), WORLD[a.world]
    d = ldir(a.world, a.level)
    for name, (kind, prog, k) in ENSEMBLES.items():
        variant = W["ablation"] if kind == "ablation" else "native"
        ensemble(spec, variant, W["pulse"] if prog == "pulse" else [], SEED0 + k, d / f"{name}.npz")


def cmd_null(a):
    spec, W = make_spec(a.world, a.level), WORLD[a.world]
    ensemble(spec, "numerical_null", W["pulse"], SEED0 + 6, ldir(a.world, a.level) / "N.npz")


def cmd_det(a):
    spec, W = make_spec(a.world, 0.0, ell=None), WORLD[a.world]
    d = OUT / "score" / a.world / "det"
    d.mkdir(parents=True, exist_ok=True)
    for name, variant in (("det_dt", "native"), ("det_dt2", "numerical_null")):
        ensemble(spec, variant, W["pulse"], SEED0 + 9, d / f"{name}.npz", members=1)


def cmd_behav(a):
    """Simulate with labkit.run.simulate (this Python); behav_analyse.py (the lab's Python: gudhi) writes the pack."""
    import pickle
    sys.path.insert(0, LE.LAB)
    from labkit import run as LR
    from labkit.world import load_world
    spec = make_spec(a.world, a.level)
    w = spec.world
    noisy = dict(path=w.path, fields=list(w.fields), native_dt=w.native_dt, noise=w.noise, noise_corr=w.noise_corr,
                 noise_intensity=list(w.noise_intensity), overrides=w.overrides, dx=w.dx, sys_path=list(w.sys_path),
                 noise_seed=4242)
    os.environ["NOISY_SPEC"] = json.dumps(noisy)
    frames, spf = {"pm": (160, 50), "fv": (150, 150)}[a.world]
    out = OUT / "behav" / a.world / f"L{a.level:g}_s{a.seed}"
    out.mkdir(parents=True, exist_ok=True)
    W = load_world(str(HERE / "noisy_world.py"))
    t0 = time.process_time()
    rec = LR.simulate(W, a.seed, frames, spf, tuple(W.META["size"]), log=lambda *x: None,
                      K=LR._lineage_k(W.META, None)[0], periodic=W.META.get("periodic", True),
                      threshold=W.META.get("threshold"))
    cpu = time.process_time() - t0
    with open(out / "rec.pkl", "wb") as fh:
        pickle.dump(dict(rec=rec, meta=W.META, seed=a.seed, frames=frames, spf=spf, cpu_s=cpu, noisy_spec=noisy,
                         world=a.world, level=a.level), fh)
    print(f"{a.world} L{a.level:g} s{a.seed}: {rec['status']}, {cpu:.0f} cpu-s", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["time", "score", "null", "det", "behav"])
    ap.add_argument("--world", choices=sorted(WORLD), required=True)
    ap.add_argument("--level", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    {"time": cmd_time, "score": cmd_score, "null": cmd_null, "det": cmd_det, "behav": cmd_behav}[a.cmd](a)
