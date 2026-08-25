"""Diagnostic: CPU mv3 seed distribution (seeds 4-8), locked pipeline verbatim.
This does NOT touch the gate definition: it characterizes the CPU's own
seed-noise distribution that the 3-seed band was estimated from."""
import sys, os, json, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/l0/complexity")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/l0/stage2/lib")
import soup_sim, worlds, metrics_v1 as M

seed = int(sys.argv[1])
g = worlds.WORLDS["mv3"]()
rec = soup_sim.run_soup(g, L=128.0, T=5000.0, seed=seed, dtype="f32",
                        kicks=worlds.KICKS.get(g["id"]), workers=2)
pth = os.path.join("/Users/spoho/Documents/prime/test/physim/probes/blobs/gpu/results/parity_runs",
                   f"cpu_mv3_s{seed}.npz")
soup_sim.save_run(rec, pth)
out = M.full_battery(rec)
print(json.dumps(dict(seed=seed, interest=out["interest"],
                      C={k: round(v, 3) for k, v in out["C"].items()},
                      n_end=out["D"]["d1"]["n_end"], model=out["D"]["d1"]["model"],
                      slow=out["D"]["d2"].get("slow"))))
