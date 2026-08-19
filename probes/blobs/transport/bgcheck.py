"""bgcheck: no-blob background integrity under tri field at dx=0.5, T=1500."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim

out = {}
for eps in (0.005, 0.0075, 0.01, 0.0125):
    r = sim.run(eps=eps, kind="tri", dx=0.5, stepper="imexfft", T=1500.0,
                spots=(), rec_tu=50.0)
    n1 = max(r["glob"]["n1"]); n2 = max(r["glob"]["n2"])
    a1 = max(r["glob"]["a1"]); a2 = max(r["glob"]["a2"])
    # also excess amplitude vs base at end
    N = r["N"]
    base2d = np.repeat(r["base1d"][:, :, None], N, axis=2)
    exc = np.abs(r["F"] - base2d).max()
    out[f"eps{eps}"] = dict(status=r["status"], n1=n1, n2=n2, a1=a1, a2=a2,
                            max_dev=float(exc))
    print(eps, out[f"eps{eps}"], flush=True)
    sim.append_result(dict(id=f"bgcheck_eps{eps}", kind="bgcheck", eps=eps,
                           **out[f"eps{eps}"]))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bgcheck.json"), "w"), indent=1)
print("DONE")
