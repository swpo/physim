import sys, time, numpy as np
sys.path.insert(0, "."); import importlib; w = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "world")
s = w.init(0, w.META["size"]); t0 = time.time()
for k in range(int(70 / w.META["dt"]) + 1):
    if k % 250 == 0:
        h = s.get("nsub_hist", {}); tot = sum(h.values()) or 1
        print(round(k * w.META["dt"]), w.stats(s), "mean nsub %.1f max %s" % (sum(a * b for a, b in h.items()) / tot, max(h) if h else 0), "vmax %.2f" % np.abs(s["v"]).max(), round(time.time() - t0), flush=True)
        s["nsub_hist"] = {}
    s = w.step(s)
np.savez("snap_%s.npz" % (sys.argv[1] if len(sys.argv) > 1 else "world"), x=s["x"], t=s["t"], bA=s["bA"], bB=s["bB"])
