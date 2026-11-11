"""screen -- the round-5 screen and the passive-against-designed-input comparison for one candidate hidden level.

    python -B screen.py CAND LAM [size] [members] [R] [nats] [seed] [key=value ...]
        CAND   kpool | lpool | dorm | bound | public (public = the public world as the hidden world: noise floor)
        LAM    the dial
        size 64, members 8, R 6 replicate futures, nats 300 per item, seed 1; key=value overrides hidden numbers
        (rho, k_off, k_on, s_c, w_c, k_a, k_d); tag=... names the output file.

DESIGN-STAGE CHECK at tiny size, CPU. Hidden numbers are illustrative PILOT values: never to be reused as an exam.

What is run. M members of the HIDDEN world form cells for T0 = 150 ticks without input (the hidden field starts
at 0 and equilibrates). From each member's hidden state x at T0, four items, one per program class, each of H = 32
ticks at the same nats:
    none     no input (passive)
    blind    random 2-bump pushes of random sign on random ticks of the first 20 (the exam mix's blind class)
    feed     aimed: + on the bumps within 8 px of the largest cell for the first 10 ticks
    starve   aimed: - on the same bumps for the first 10 ticks
For every item: R futures of the hidden world from x with fresh channel noise (the truths; leave-one-out they are
the oracle O) and R futures of the PUBLIC law from the projected state Psi(x) (hidden field dropped) with fresh
noise (the public-law simulator given the state: round 5's `plugPM` with the law in place of the parameters).
Both start the tracker memory from the state (Designer.from_states), so slot identities play no part; the scored
views are permutation-invariant:
    pop      (N, mean size) of the cell list                      (level 2 without its 50-tick rate window)
    raster   cell mass and catalyst mass per 16-px block          (the level-1 view scored in round5/vortexexam)
Scores: fair energy score (vw.scoring) at h = 4, 8, 16, 32 ticks, coordinates divided by their SD over all truths
of the run (floored at a tenth of the median SD); K = the pool of the other members' `none` truths at the same
horizon. With plug_<name>=value the comparison simulator is instead the hidden law with those wrong values, run
from the full hidden state (how much the hidden VALUES matter once the form is known).
    screen gap = (L(public law | state) - L(O)) / (L(K) - L(O)), L summed over the four horizons,
per view and program class; bootstrap SE over members. Also: the same gap for an oracle that ignores the program
(does the input matter), and the mean shift truth - public of the target cell's mass and of the mean size in units
of the oracle's replicate SD (how many replicates a pump-probe needs to see the defect).
Writes results/screen_<tag>.json.
"""
import json
import os
import sys
import time

import numpy as np

import sublevel as SL
from sublevel import MJ, MW
from vw.scoring import energy_fair, energy_loo

T0, H, HS, T_BLIND, T_AIM = 150, 32, (4, 8, 16, 32), 20, 10
CLASSES = ("none", "blind", "feed", "starve")


def parse(argv):
    cand = argv[1]
    lam = float(argv[2])
    pos = [a for a in argv[3:] if "=" not in a]
    kv = dict(a.split("=", 1) for a in argv[3:] if "=" in a)
    size = int(pos[0]) if len(pos) > 0 else 64
    M = int(pos[1]) if len(pos) > 1 else 8
    R = int(pos[2]) if len(pos) > 2 else 6
    nats = float(pos[3]) if len(pos) > 3 else 300.0
    seed = int(pos[4]) if len(pos) > 4 else 1
    tag = kv.pop("tag", f"{cand}_lam{lam:g}")
    plug = {k[5:]: float(kv.pop(k)) for k in list(kv) if k.startswith("plug_")}
    return cand, lam, size, M, R, nats, seed, {k: float(v) for k, v in kv.items()}, tag, plug


def programs(cfg, L1_t0, K, nats, rng):
    """(M, C, H, m) dense programs and the target slot per member."""
    M = L1_t0.shape[0]
    T = L1_t0[:, :K * 12].reshape(M, K, 12)
    cen = MJ.bump_centres(cfg)
    s2 = 2 * cfg.sigma_a ** 2
    P = np.zeros((M, len(CLASSES), H, cfg.m))
    tgt = []
    for i in range(M):
        pres = T[i, :, 0] > 0.5
        k = int(np.argmax(np.where(pres, T[i, :, 1], -1)))
        cx = (np.arctan2(T[i, k, 4], T[i, k, 3]) * cfg.W / (2 * np.pi)) % cfg.W
        cy = (np.arctan2(T[i, k, 6], T[i, k, 5]) * cfg.H / (2 * np.pi)) % cfg.H
        dd = np.hypot((cen[:, 0] - cy + cfg.H / 2) % cfg.H - cfg.H / 2, (cen[:, 1] - cx + cfg.W / 2) % cfg.W - cfg.W / 2)
        sel = np.flatnonzero(dd <= 8.0)
        if sel.size < 2:
            sel = np.argsort(dd)[:2]
        amp = np.sqrt(s2 * nats / (T_AIM * sel.size))                    # T_AIM * n_b * amp^2 / (2 sigma^2) = nats
        P[i, 2, :T_AIM][:, sel] = amp
        P[i, 3, :T_AIM][:, sel] = -amp
        left, cap = nats, nats / 5.0
        for t in range(T_BLIND):                                         # blind: as vw.harness.blind_random(k=2, rate 0.5)
            if rng.random() >= 0.5 or left <= 1e-9:
                continue
            idx = rng.choice(cfg.m, size=2, replace=False)
            v = rng.standard_normal(2)
            c = min(rng.uniform(0, cap), left)
            v *= np.sqrt(c * s2 / (v ** 2).sum())
            P[i, 1, t, idx] = v
            left -= c
        tgt.append({"slot": k, "mass_t0": float(T[i, k, 1]), "cy": float(cy), "cx": float(cx), "bumps": sel.tolist(),
                    "amp": float(amp), "blind_nats": float(nats - left)})
    return P, tgt


def target_mass(L1, K, tgt, size):
    """Mass of the cell nearest to the target's start position (fresh tracker memory, so slots are re-numbered):
    (...,) from level-1 vectors (..., K*12+5); 0 if no cell within 12 px."""
    T = L1[..., :K * 12].reshape(L1.shape[:-1] + (K, 12))
    pres = T[..., 0] > 0.5
    cx = (np.arctan2(T[..., 4], T[..., 3]) * size / (2 * np.pi)) % size
    cy = (np.arctan2(T[..., 6], T[..., 5]) * size / (2 * np.pi)) % size
    d = np.hypot((cy - tgt["cy"] + size / 2) % size - size / 2, (cx - tgt["cx"] + size / 2) % size - size / 2)
    d = np.where(pres, d, 1e9)
    j = d.argmin(-1)
    m = np.take_along_axis(T[..., 1], j[..., None], -1)[..., 0]
    return np.where(d.min(-1) <= 12.0, m, 0.0)


def main():
    cand, lam, size, M, R, nats, seed, hid, tag, plug = parse(sys.argv)
    cfg = SL.small_cfg(size)
    t_cpu = time.process_time()
    spec_p, parts = SL.build(cfg)
    wp = MW.MapWorld(spec_p, world_seed=1)          # another designer seed: the public futures get their own noise keys
    dp = wp.designer
    if cand == "public":
        wh, ek = MW.MapWorld(spec_p, world_seed=0), None
        dh = wh.designer
    else:
        spec_h, _ = SL.build(cfg, cand, hidden=dict(hid, lam=lam))
        wh = MW.MapWorld(spec_h, world_seed=0)
        dh, ek = wh.designer, SL.EXTRA[cand]
    K = parts["tracker"].K
    rng = np.random.default_rng(seed)

    ens = dh.ensemble(M, seed=(77, seed))
    ens, rec0 = dh.rollout(ens, None, T=T0, rec=("L1",))
    x = {k: np.asarray(v) for k, v in ens.x.items()}
    P, tgt = programs(cfg, rec0["L1"][:, -1], K, nats, rng)
    C = len(CLASSES)
    B = M * C * R
    rep = lambda a: np.repeat(np.repeat(a, C, axis=0), R, axis=0)          # noqa: E731  member-major, class, replicate
    Pd = np.repeat(P.reshape(M * C, H, cfg.m), R, axis=0)                  # (B, H, m)
    xh = {k: rep(v) for k, v in x.items()}
    _, rt = dh.rollout(dh.from_states(xh), Pd, T=H, rec=("L1",))
    if plug:                                    # plug_<name>=value: the comparison simulator is the HIDDEN law with
        spec_q, _ = SL.build(cfg, cand, hidden=dict(hid, lam=lam, **plug))   # these wrong values, run from the full state
        dq = MW.MapWorld(spec_q, world_seed=1).designer
        _, rq = dq.rollout(dq.from_states(xh), Pd, T=H, rec=("L1",))
    else:
        xp = {k: rep(x[k]) for k in MJ.FIELDS}
        _, rq = dp.rollout(dp.from_states(xp), Pd, T=H, rec=("L1",))
    cpu_sim = time.process_time() - t_cpu

    def views(r):
        L1 = r["L1"][:, list(HS)]                                          # (B, nh, d1)
        ras, pop = SL.list_views(L1, K, size)
        return (ras.reshape(M, C, R, len(HS), -1), pop.reshape(M, C, R, len(HS), -1),
                L1.reshape(M, C, R, len(HS), -1))
    ras_t, pop_t, L1_t = views(rt)
    ras_q, pop_q, L1_q = views(rq)

    out = {"PILOT_NEVER_REUSE_AS_EXAM": True, "cand": cand, "lam": lam, "hidden_overrides": hid,
           "comparison_simulator": ("public law from the projected state" if not plug else
                                    {"hidden law from the full state with wrong values": plug}),
           "hidden_values_pilot": None if cand == "public" else {k: float(v) for k, v in {**SL.HID0, **hid, "lam": lam}.items()},
           "size": size, "members": M, "R": R, "nats_per_item": nats, "seed": seed, "T0": T0, "H": H, "horizons": list(HS),
           "classes": list(CLASSES), "targets": tgt, "cpu_s_sim_incl_compile": cpu_sim,
           "member_ticks": int(M * T0 + 2 * B * H)}
    inside = x["phi"] > 0.5
    pop0 = SL.list_views(rec0["L1"][:, -1], K, size)[1]
    st = {"cells_at_T0": [int(v) for v in pop0[:, 0]], "mean_size_at_T0": [float(v) for v in pop0[:, 1]],
          "phi_area_at_T0": [int(v) for v in inside.reshape(M, -1).sum(1)],
          "S_inside_q01_q50": [float(np.quantile(x["S"][inside], q)) for q in (0.01, 0.5)] if inside.any() else None}
    if ek is not None and inside.any():
        e = x[ek]
        st["hidden_field_mean_inside"] = float(e[inside].mean())
        st["hidden_over_K_inside"] = float(e[inside].sum() / max(x["K"][inside].sum(), 1e-12))
        st["hidden_over_S_all"] = float(e.sum() / x["S"].sum())
    out["state_at_T0"] = st

    res = {}
    for vname, Yt, Yq in (("pop", pop_t, pop_q), ("raster", ras_t, ras_q)):
        d = Yt.shape[-1]
        pool = Yt[:, 0]                                                    # none truths (M, R, nh, d)
        sc = Yt.reshape(M * C * R, len(HS), d).std(0)                      # (nh, d): SD over all truths of the run
        pos = sc[sc > 1e-9]
        sc = np.maximum(sc, 0.1 * np.median(pos)) if pos.size else np.ones_like(sc)   # floor: blocks that are rarely occupied
        esO = np.zeros((M, C, len(HS)))
        esQ, esK, esI = np.zeros_like(esO), np.zeros_like(esO), np.zeros_like(esO)
        for j in range(len(HS)):
            s = sc[j]
            esO[:, :, j] = energy_loo(Yt[:, :, :, j], s)
            esQ[:, :, j] = energy_fair(Yq[:, :, :, j], Yt[:, :, :, j], s)
            for i in range(M):
                others = np.delete(pool[:, :, j], i, axis=0).reshape((M - 1) * R, d)
                esK[i, :, j] = energy_fair(np.broadcast_to(others, (C,) + others.shape), Yt[i, :, :, j], s)
                esI[i, :, j] = energy_fair(np.broadcast_to(Yq[i, 0, :, j], (C, R, d)), Yt[i, :, :, j], s)
        # esI: the public-law simulator given the state but ignoring the program (its `none` futures)

        def gap(idx, cls, num):
            a = num[idx][:, cls].sum(-1).mean()
            o = esO[idx][:, cls].sum(-1).mean()
            k = esK[idx][:, cls].sum(-1).mean()
            return (a - o) / (k - o)

        rb = np.random.default_rng(12345)
        boots = rb.integers(0, M, size=(400, M))
        r = {}
        for name, cls in [(c, [ci]) for ci, c in enumerate(CLASSES)] + [("mix", list(range(C))), ("inputs", [1, 2, 3])]:
            g = gap(np.arange(M), cls, esQ)
            gb = np.array([gap(b, cls, esQ) for b in boots])
            gi = gap(np.arange(M), cls, esI)
            r[name] = {"screen_gap": float(g), "se_members": float(gb.std(ddof=1)),
                       "gap_if_program_ignored": float(gi),
                       "L_O": float(esO[:, cls].sum(-1).mean()), "L_public": float(esQ[:, cls].sum(-1).mean()),
                       "L_K": float(esK[:, cls].sum(-1).mean()),
                       "gap_by_horizon": [float((esQ[:, cls, j].mean() - esO[:, cls, j].mean()) /
                                                (esK[:, cls, j].mean() - esO[:, cls, j].mean())) for j in range(len(HS))]}
        res[vname] = r
    out["screen"] = res

    # mean shift truth - public, in oracle replicate SDs: target-cell mass and mean size
    shift = {}
    tm_t = np.stack([target_mass(L1_t[i], K, tgt[i], size) for i in range(M)])     # (M, C, R, nh)
    tm_q = np.stack([target_mass(L1_q[i], K, tgt[i], size) for i in range(M)])
    for name, a, b in (("target_mass", tm_t, tm_q), ("mean_size", pop_t[..., 1], pop_q[..., 1]), ("N", pop_t[..., 0], pop_q[..., 0])):
        dlt = a.mean(2) - b.mean(2)                                        # (M, C, nh)
        sd = np.sqrt(a.var(2, ddof=1).mean(0))                             # (C, nh) oracle replicate SD
        shift[name] = {c: {"mean_shift": dlt[:, ci].mean(0).tolist(),
                           "z_members": (dlt[:, ci].mean(0) / np.maximum(dlt[:, ci].std(0, ddof=1) / np.sqrt(M), 1e-12)).tolist(),
                           "oracle_sd": sd[ci].tolist(),
                           "shift_over_oracle_sd": (dlt[:, ci].mean(0) / np.maximum(sd[ci], 1e-12)).tolist()}
                       for ci, c in enumerate(CLASSES)}
    out["shift_truth_minus_public"] = shift
    out["cpu_s_total"] = time.process_time() - t_cpu
    os.makedirs(os.path.join(SL.HERE, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(SL.HERE, "results", f"screen_{tag}.json"), "w"), indent=1)
    print(tag, "cpu_s", round(out["cpu_s_total"], 1), "member_ticks", out["member_ticks"], "state", st)
    for v in res:
        print(" ", v, {c: (round(res[v][c]["screen_gap"], 3), round(res[v][c]["se_members"], 3)) for c in res[v]},
              "| ignore-program:", {c: round(res[v][c]["gap_if_program_ignored"], 3) for c in ("blind", "feed", "starve")})
    print("  target_mass shift/oracle SD at h =", HS, {c: np.round(shift["target_mass"][c]["shift_over_oracle_sd"], 2).tolist() for c in CLASSES})


if __name__ == "__main__":
    main()
