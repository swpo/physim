"""Heredity prototype: body (m4) + CH membrane + global cap + bistable cargo activator h.
h: -h^3 + h + k1h (vacuum = lowest root), promoted by a body deposit (tilt kb), retained
by the membrane gate, and (when on) activating the body (kh) -> on-cells divide."""
import sys, json
from screen import *
import xgenome as X

def her(kb=0.15, kh=0.25, k1h=-0.2, Dh=0.3, beta=5.0, Kg=1.0, M=1.0, kc=0.0):
    g = load("m4")
    roots = np.roots([-1.0, 0.0, 1.0, k1h]); u0h = float(min(r.real for r in roots if abs(r.imag) < 1e-9))
    g["acts"].append(dict(lam=1.0, k1=k1h, Du=Dh, u0=u0h))
    ch = lambda tau, D, gg="id", **e: dict(tau=tau, D=D, g=gg, thr=0.0, sc=1.0, **e)
    g["chans"] = [g["chans"][0], g["chans"][1],
                  dict(tau=2.0, D=0.0, g="band", thr=0.0, sc=0.6, ch={"M": M, "k": 1.0, "h": 0.5}),
                  ch(10.0, 100.0), ch(1.0, 0.5), ch(1.0, 0.5)]
    #            v    w    m    glob  bdep  hdep
    g["W"] = [[1, 0], [1, 0], [2, 0], [1, 0], [1, 0], [0, 1]]
    g["K"] = [[1.0, 1.5, 0.0, Kg, 0.0, -kh],
              [0.0, 0.0, 0.0, 0.0, -kb, 0.0]]
    g["perm"] = [[1, 2, beta]]
    if kc:   # xcell-div division drive: gated diffusive cargo produced by the body
        g["chans"].append(ch(5.0, 4.0)); g["W"].append([1, 0])
        g["K"][0].append(-kc); g["K"][1].append(0.0)
        g["perm"].append([2 + 6, 2, beta])
    return g

def ic(g, N, seed, n=8, frac_on=0.5, dx=0.5):
    F = soup(g, N, seed, n=n, acts=[0])
    rng = np.random.default_rng(seed + 100)
    # re-find poke centres: local maxima of body
    from scipy import ndimage
    z = F[0] - g["acts"][0]["u0"]
    lab, k = ndimage.label(z > 0.5)
    cs = ndimage.center_of_mass(z, lab, range(1, k + 1))
    on = rng.permutation(k)[:int(round(frac_on * k))]
    for j in on:
        X.poke(F, 1, cs[j][0] * dx, cs[j][1] * dx, 2.2, 2.5, dx)
    return F

if __name__ == "__main__":
    args = json.loads(sys.argv[1]); T = float(sys.argv[2]) if len(sys.argv) > 2 else 300
    g = her(**args)
    N = 128
    sn, ts, w = run(g, N=N, T=T, F=ic(g, N, 0))
    u0 = g["acts"][0]["u0"]; u0h = g["acts"][1]["u0"]
    nb = [blobs(s[0], u0)[0] for s in sn]
    from scipy import ndimage
    non = []
    for s in sn:
        lab, k = ndimage.label(s[0] - u0 > 0.45 * (np.sqrt(2) - u0))
        hm = ndimage.maximum(s[1] - u0h, lab, range(1, k + 1)) if k else []
        non.append(int(np.sum(np.array(hm) > 1.0)))
    tag = "her_" + "_".join(f"{k}{v}" for k, v in args.items())
    line = f"{tag}: wall {w:.0f}s cells {nb} h-on cells {non}"
    print(line); open("screens/log.txt", "a").write(line + "\n")
    strip(sn, ts, ["u", "h", "v", "w", "m", "glob", "bdep", "hdep"], f"screens/{tag}.png", line)
