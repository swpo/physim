"""Share of the amphiphile source made inside bodies (e > 0.5) vs in the bath, original world (SRC_TRACK=1 only counts).
usage: share.py SEED T"""
import os, sys, json, importlib.util
os.environ["WORLD_P"] = json.dumps({"SRC_TRACK": 1})
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py")); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, T = int(sys.argv[1]), float(sys.argv[2]); s = w.init(seed, w.META["size"]); nxt = T / 4; last = (0.0, 0.0)
while s["t"] < T - 1e-9:
    w.step(s)
    if s["t"] >= nxt - 1e-9:
        i, o = s.get("src_in", 0.0), s.get("src_out", 0.0)
        print("t=%.0f cumulative body share %.3f, share in the last window %.3f" % (s["t"], i / max(i + o, 1e-12), (i - last[0]) / max(i + o - last[0] - last[1], 1e-12)), flush=True)
        last = (i, o); nxt += T / 4
