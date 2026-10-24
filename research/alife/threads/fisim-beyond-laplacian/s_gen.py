"""Generic screen: python s_gen.py module fn '{args}' T [nsnap] [noise]. Counts bodies at nsnap times."""
import sys, json, importlib
from screen import *
mod, fn = sys.argv[1], sys.argv[2]; args = json.loads(sys.argv[3]); T = float(sys.argv[4])
nsnap = int(sys.argv[5]) if len(sys.argv) > 5 else 10; noise = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
M = importlib.import_module(mod); g = getattr(M, fn)(**args)
F = M.ic(g, 128, 0) if hasattr(M, "ic") and mod == "s_her" else None
sn, ts, w = run(g, N=128, T=T, seed=0, nsnap=nsnap, F=F, noise=noise)
u0 = g["acts"][0]["u0"]
tag = f"{fn}_" + "_".join(f"{k}{v}" for k, v in args.items()) + (f"_n{noise}" if noise else "") + f"_T{T:.0f}"
cnt = [blobs(s[0], u0)[0] for s in sn]
line = f"{tag}: wall {w:.0f}s cells {cnt}"
print(line); open("screens/log.txt", "a").write(line + "\n")
idx = np.linspace(0, len(sn) - 1, 8).round().astype(int)
na = len(g["acts"])
strip(sn[idx][:, [0] + list(range(na, sn.shape[1]))], [ts[i] for i in idx], ["u"] + [f"x{c}" for c in range(sn.shape[1] - na)], f"screens/{tag}.png", line)
