"""e4_x64step.py — does global JAX_ENABLE_X64 change f32 stepper bits?

devrec needs f64 accumulators (global x64 flag is the robust way in jax
0.4.38); the SIM must remain bit-identical under the flag or every devrec
gate is confounded. One experiment: advance the same batch 500 steps with
x64 OFF vs ON (two subprocess runs), hash the pulled state.

Run: ~/gv/bin/python e4_x64step.py   (self-spawns the two variants)
"""
import hashlib, json, os, subprocess, sys, time

VARIANT = os.environ.get("E4_VARIANT")

if VARIANT:
    if VARIANT == "on":
        os.environ["JAX_ENABLE_X64"] = "1"
    import numpy as np
    import jax
    if VARIANT == "on":
        jax.config.update("jax_enable_x64", True)
    from blobkit import worlds as W
    from blobkit.soup import sim_gpu as SG

    jobs = [(W.load(n), 1 + i) for i, n in
            enumerate(["m0", "pred", "coex", "ds3_014"])]
    master = SG.init_soup_gpu_batch(jobs, L=64.0, dtype="f32")
    SG.advance_gpu_batch(master, 250.0)          # 12500 steps, noise on
    h = hashlib.sha256()
    for S in master["worlds"]:
        F = np.asarray(SG._pull(S["_gpu"])[S["_gpu"]["gens"].index(S["g"])]
                       if False else SG._pull(S["_gpu"])[0])
    # simpler: hash the full batch tensor
    Fh = np.asarray(master["worlds"][0]["_gpu"]["F"])
    h.update(Fh.tobytes())
    rec_h = hashlib.sha256()
    for S in master["worlds"]:
        rec_h.update(json.dumps(
            [S["ts"], {k: v for k, v in S["mass"].items()}],
            default=str).encode())
    print(json.dumps(dict(variant=VARIANT, dtype=str(Fh.dtype),
                          state_sha=h.hexdigest()[:16],
                          rec_sha=rec_h.hexdigest()[:16])))
    sys.exit(0)

OUT = os.path.expanduser("~/perf/results/experiments.jsonl")
res = {}
for v in ("off", "on"):
    env = dict(os.environ, E4_VARIANT=v)
    p = subprocess.run([sys.executable, __file__], env=env,
                       capture_output=True, text=True, timeout=600)
    line = [l for l in p.stdout.strip().split("\n") if l.startswith("{")][-1]
    res[v] = json.loads(line)
    print(v, res[v], flush=True)
row = dict(question="E4 x64 flag vs f32 stepper bits",
           state_match=res["off"]["state_sha"] == res["on"]["state_sha"],
           rec_match=res["off"]["rec_sha"] == res["on"]["rec_sha"],
           detail=res,
           ts=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
row["verdict"] = ("BIT-IDENTICAL (x64 flip safe)"
                  if row["state_match"] and row["rec_match"]
                  else "DIVERGES — scope x64 to kernel only")
with open(OUT, "a") as f:
    f.write(json.dumps(row) + "\n")
print("[row]", json.dumps(row)[:300])
