"""check_cardlib -- the card's estimators against a world whose answers are known in closed form (numpy only).

World: independent AR(1) numbers on a 2 x 8 x 8 grid, z(t+1) = a z(t) + sqrt(1 - a^2) xi, unit variance, plus a
common function of the tick g(t) = A sin(2 pi t / 200). The hidden part is a; a neighbour at eps is a + 0.1 eps.
An input adds c to a fixed set of blocks during the first T_in ticks of a branch (aimed: 4 blocks, blind: the same
norm on 4 other blocks). Expected, per horizon h (in units of the AR variance; the card standardises by the total
variance 1 + A^2 / 2, which the expectations below include):
    predictable fraction   PF(h) = 1 - (1 - a^(2h)) / V_clim            closure ceiling = 1 (the law is linear)
    plug-in loss           PL(eps, h) = (a'^h - a^h)^2 E z^2   (paired estimator: tight; unpaired: within its noise)
    actions                D(h) = MS(h) = mean over cells of (sum_i a^(h-1-i) c)^2 , i < min(h, T_in)
    response difference    RD(h) = the same with (a'^k - a^k)
    tick share             (A^2 / 2) / (1 + A^2 / 2)
Run: python -B check_cardlib.py  -> results/check_cardlib.json, exit 1 on a failed check.
"""
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402

import cardlib as CL  # noqa: E402


def main():
    rng = np.random.default_rng(606)
    a, A_t, Q, G = 0.9, 0.5, 2, 8
    sz = CL.Sizes(M=24, M_fit=12, T=400, n_snap=4, R=6, R2=2, n_dir=2, n_boot=50)
    lay = sz.layout()
    s = np.sqrt(1 - a * a)
    g = lambda t: A_t * np.sin(2 * np.pi * np.asarray(t) / 200.0)
    T, M = sz.T, sz.M
    x = np.zeros((T + 1, M, Q, G, G))
    x[0] = rng.normal(size=(M, Q, G, G))
    for t in range(T):
        x[t + 1] = a * x[t] + s * rng.normal(size=(M, Q, G, G))
    Y = x + g(np.arange(T + 1))[:, None, None, None, None]
    seg = T // sz.n_snap
    ts = [(i + 1) * seg for i in range(sz.n_snap)]
    xs = np.concatenate([x[t, sz.M_fit:] for t in ts], 0)                     # (NS, Q, G, G)
    t0 = np.repeat(ts, sz.M_test)
    aa = np.full(sz.Bb, a)
    nb = lambda e: a + 0.1 * e
    for (e, d), idx in lay["nb"].items():
        aa[idx] = nb(e)
    aa[lay["xb"]] = aa[lay["xa"]] = nb(sz.x_eps)
    c = np.zeros((sz.Bb, Q, G, G))
    amp = {}
    for (kind, nats), idx in lay["act"].items():
        amp[(kind, nats)] = np.sqrt(nats / 200.0) * 0.5
        blocks = (slice(0, 2), slice(0, 2)) if kind == "aimed" else (slice(4, 6), slice(4, 6))
        c[(idx, slice(None)) + blocks] = amp[(kind, nats)]
        if (kind, nats) == tuple(sz.x_arm):
            c[(lay["xa"], slice(None), slice(0, 2), slice(0, 2))] = amp[(kind, nats)]
    # branches: common noise for the neighbour arms (replicas 0 .. R2 - 1), the action arms and the x arms
    kid = np.arange(sz.Bb)
    for idx in lay["nb"].values():
        kid[idx] = np.arange(sz.R2)
    for idx in list(lay["act"].values()) + [lay["xb"], lay["xa"]]:
        kid[idx] = np.arange(sz.R_u)
    YA = np.zeros((sz.NS, sz.HB, sz.Bb, Q, G, G))
    cur = np.broadcast_to(xs[:, None], (sz.NS, sz.Bb, Q, G, G)).copy()
    for h in range(sz.HB):
        xi = rng.normal(size=(sz.NS, sz.Bb, Q, G, G))
        xi = xi[:, kid]
        sa = np.full(sz.Bb, s)[None, :, None, None, None]         # the noise amplitude is not part of the hidden part
        cur = aa[None, :, None, None, None] * cur + sa * xi + (c[None] if h < sz.T_in else 0.0)
        YA[:, h] = cur + g(t0 + h + 1)[:, None, None, None, None]
    out = CL.grid_card(Y.astype(np.float32), YA.astype(np.float32), sz, ts, np.arange(sz.M_fit), seed=1)
    vtot = 1 + A_t ** 2 / 2
    hz = np.array(sz.hz)
    exp = {}
    exp["v_orc"] = (1 - a ** (2 * hz)) / vtot
    exp["tick_share"] = (A_t ** 2 / 2) / vtot
    exp["pl"] = {str(e): (nb(e) ** hz - a ** hz) ** 2 / vtot for e in sz.eps}

    def resp(al, h, cc):
        return sum(al ** (h - 1 - i) for i in range(min(h, sz.T_in))) * cc
    frac = 4.0 / (G * G)
    exp["D"] = {f"{k}_{int(n)}": np.array([resp(a, h, amp[(k, n)]) ** 2 * frac for h in hz]) / vtot for (k, n) in lay["act"]}
    xa = amp[tuple(sz.x_arm)]
    exp["RD"] = np.array([(resp(nb(sz.x_eps), h, xa) - resp(a, h, xa)) ** 2 * frac for h in hz]) / vtot
    checks = []

    def chk(name, got, want, rtol, atol):
        got, want = np.asarray(got, float), np.asarray(want, float)
        ok = bool(np.all(np.abs(got - want) <= atol + rtol * np.abs(want)))
        checks.append(dict(name=name, ok=ok, got=np.round(got, 5).tolist(), want=np.round(want, 5).tolist(), rtol=rtol, atol=atol))
        print(("ok   " if ok else "FAIL ") + name, np.round(got, 4), np.round(want, 4))
    chk("oracle variance V_orc(h)", out["v_orc"], exp["v_orc"], 0.05, 0.002)
    chk("typical-state V_orc(h) (median over states)", out["v_orc_med"], exp["v_orc"], 0.06, 0.002)
    chk("closure ceiling at 1 and 2 ticks (the linear law is exact; the tick function costs a little)", out["ceil"][:2], np.ones(2), 0.0, 0.02)
    chk("tick share", out["tick_share"], exp["tick_share"], 0.15, 0.01)
    for e in sz.eps:
        chk(f"plug-in loss PL(eps = {e}, h), paired", out["pl"][str(e)]["pl"], exp["pl"][str(e)], 0.1, 2e-5)
        chk(f"plug-in loss PL(eps = {e}, h), unpaired (round 5's form)", out["pl"][str(e)]["pl_unpaired"], exp["pl"][str(e)], 0.25, 0.03)
    for k, v in exp["D"].items():
        chk(f"paired displacement D, arm {k}", out["act"][k]["D"], v, 0.05, 1e-4)
        chk(f"predictable shift MS, arm {k}", out["act"][k]["MS"], v, 0.05, 1e-4)
    chk("response difference RD(h)", out["xresp"]["RD"], exp["RD"], 0.1, 1e-4)
    chk("member share is small for an ergodic level", out["member_share"], 0.0, 0.0, 0.08)
    res = dict(passed=bool(all(c["ok"] for c in checks)), a=a, A_tick=A_t, sizes=dict(M=sz.M, T=sz.T, NS=sz.NS, R=sz.R), checks=checks)
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    json.dump(res, open(os.path.join(HERE, "results", "check_cardlib.json"), "w"), indent=1)
    print("PASSED" if res["passed"] else "FAILED")
    sys.exit(0 if res["passed"] else 1)


if __name__ == "__main__":
    main()
