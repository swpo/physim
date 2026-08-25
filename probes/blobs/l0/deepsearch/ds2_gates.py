"""ds2_gates.py — validation gates for the v2 operator alphabet.

G1 vacuum-exact: every new op's child keeps the vacuum an exact fixed point
   (noise=0 sim from state_vacuum stays put; iso-background trick preserved).
G2 fossil-vertex reconstruction: delete_bilin(ref_BFIELD) then re-adding
   [0,2,1,1.0] restores BIT-EXACT dynamics vs the untouched reference, and
   the deleted genome DIFFERS (miniature of the ds3_014 ablation).
G3 mint reachability: mint_bilin CAN mint the BFIELD fossil vertex class
   (act0, chans {1,2}) under the biased pick (creation rate > 0 — the T1 fix).
G4 dup_act split algebra: dup_act(iso, split, sigma=0) == merge_share_chan(
   iso, iso) up to field permutation (speciation == self-merge, exactly).
G5 merge bilin preservation: all 3 merge modes with bilin-carrying parents
   keep the coef multiset + valid indices + vtag concat (v1 V1/V2 exactness
   gates re-run too).
G6 add_chan wiring: shapes, one W=1 edge, K entry, funnel runs, vacuum-exact.
Logged to results_v2.json as kind="val_gate_v2".
"""
import copy, json, os, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ds_lib as DL
import ds2_lib as D2
import ds2_ops as OPS2
import genome as G
import operators_lib as OP
import funnel as FU

RES = []


def check(name, ok, note=""):
    RES.append(dict(gate=name, passed=bool(ok), note=note))
    print(("PASS " if ok else "FAIL ") + name + (f"  [{note}]" if note else ""),
          flush=True)
    return ok


def sim_fields(g, T=30.0, poke=None, seed=0):
    """Deterministic short sim, returns final field stack (na+nc,N,N)."""
    N = int(round(96.0 / 0.5))
    F = G.state_vacuum(g, N)
    if poke:
        F = G.poke(F, g, 0, 40.0, 40.0, 2.0, 3.0, 0.5)
    out = G.run_genome(g, F=F, T=T, noise=0.0, seed=seed, save_fields=True,
                       stop_all_dead=False)
    return out["fields"]


def vacuum_exact(g, T=20.0):
    N = int(round(96.0 / 0.5))
    F0 = G.state_vacuum(g, N)
    out = G.run_genome(g, F=F0.copy(), T=T, noise=0.0, save_fields=True,
                       stop_all_dead=False)
    return float(np.abs(out["fields"] - F0).max())


def main():
    rng = np.random.default_rng(7)

    # ---------------- G1 vacuum-exact for each op class
    bf = G.ref_BFIELD()
    iso = OP.ref_iso(0.75)
    for name, child in [
        ("mint_bilin", OPS2.mint_bilin(bf, rng, "vt")[0]),
        ("delete_bilin", OPS2.delete_bilin(bf, rng)[0]),
        ("add_chan", OPS2.add_chan(iso, rng)[0]),
        ("dup_act_shared", OPS2.dup_act(iso, rng, mode="shared")[0]),
        ("dup_act_split", OPS2.dup_act(iso, rng, mode="split")[0]),
    ]:
        dev = vacuum_exact(child) if child is not None else np.inf
        check(f"G1_vacuum_{name}", dev < 1e-5, f"max_dev={dev:.2e}")

    # ---------------- G2 fossil-vertex delete + restore
    noV, info = OPS2.delete_bilin(copy.deepcopy(bf), rng)
    check("G2a_delete_removes", len(noV["bilin"]) == 0
          and len(noV["vtags"]) == 0, str(info.get("term")))
    back = copy.deepcopy(noV)
    back["bilin"].append([0, 2, 1, 1.0])
    back["vtags"].append("re_minted")
    Fa = sim_fields(bf, T=40.0, poke=True)
    Fb = sim_fields(back, T=40.0, poke=True)
    Fc = sim_fields(noV, T=40.0, poke=True)
    check("G2b_restore_exact", float(np.abs(Fa - Fb).max()) < 1e-12,
          f"dev={float(np.abs(Fa - Fb).max()):.2e}")
    check("G2c_ablation_differs", float(np.abs(Fa - Fc).max()) > 1e-6,
          f"dev={float(np.abs(Fa - Fc).max()):.2e}")

    # ---------------- G3 mint reachability of the fossil class
    hit, tries = None, 0
    r3 = np.random.default_rng(11)
    for t in range(400):
        child, inf = OPS2.mint_bilin(copy.deepcopy(noV), r3, f"m{t}")
        tries += 1
        if child is None:
            continue
        b = child["bilin"][-1]
        if b[0] == 0 and {b[1], b[2]} == {1, 2}:
            hit = (t, b)
            break
    check("G3_mint_reaches_fossil_class", hit is not None,
          f"try={hit[0]} coef={hit[1][3]:.3f}" if hit else "not in 400")

    # ---------------- G4 dup_act split == self share_chan merge
    r0 = np.random.default_rng(0)
    dup, dinfo = OPS2.dup_act(copy.deepcopy(iso), r0, mode="split", src=0,
                              sigma=0.0, sigma_d=0.0)
    mrg, _ = OP.merge_share_chan(copy.deepcopy(iso), copy.deepcopy(iso))
    sys.path.insert(0, os.path.join(D2.L0, "evolve"))
    from val_gates_lib import eq_upto_perm
    ok4 = dup is not None and mrg is not None and eq_upto_perm(dup, mrg, 1e-9)
    check("G4_dup_split_eq_selfmerge", ok4, str(dinfo))

    # ---------------- G5 merges preserve bilin + vtags (and v1 exactness)
    bf2 = copy.deepcopy(bf)
    bf2["bilin"] = [[0, 2, 1, 1.0], [0, 0, 0, 0.37]]
    bf2["vtags"] = ["fdr_bf_0", "minted_x"]
    for mode in ("cross_edge", "slow_tanh", "share_chan"):
        ch, inf = OPS2.merge_v2(mode, bf2, bf, rng=np.random.default_rng(3))
        if ch is None:
            check(f"G5_{mode}", False, str(inf))
            continue
        ok = (sorted(round(b[3], 9) for b in ch["bilin"])
              == sorted([1.0, 0.37, 1.0]))
        ok &= len(ch["vtags"]) == 3 and "minted_x" in ch["vtags"]
        ok &= not G.validate(ch)
        check(f"G5_{mode}", ok, f'n_bilin={len(ch["bilin"])}')
    # share_chan bilin DYNAMICS preservation (remap correctness): merged
    # bf x iso — bilin chans (b,w of parent1) survive un-fused only if not
    # the fusion target; simulate to be sure indices still point at the
    # same physical channels: ablating the vertex must change dynamics.
    m5, _ = OPS2.merge_v2("share_chan", bf2, iso, rng=np.random.default_rng(5))
    if m5 is not None:
        m5n = copy.deepcopy(m5)
        m5n["bilin"] = [b for b in m5n["bilin"] if abs(b[3] - 1.0) > 1e-9]
        Fa = sim_fields(m5, T=30.0, poke=True)
        Fb = sim_fields(m5n, T=30.0, poke=True)
        check("G5_sharechan_vertex_live", float(np.abs(Fa - Fb).max()) > 1e-8,
              f"dev={float(np.abs(Fa - Fb).max()):.2e}")
    else:
        check("G5_sharechan_vertex_live", False, "merge failed")
    v1a, _ = OP.merge_share_chan(OP.ref_iso(0.0), OP.ref_iso(0.75))
    ok_v1a = eq_upto_perm(v1a, G.ref_VVW(), tol=2e-5)
    v1b, _ = OP.merge_cross_edge(G.ref_M4(5.7), G.ref_M4(2.5), eta=0.1)
    ok_v1b = eq_upto_perm(v1b, G.ref_XV(5.7, 2.5, 0.1, 0.1))
    check("G5_v1_exactness_kept", ok_v1a and ok_v1b,
          f"vvw={ok_v1a} xv={ok_v1b}")

    # ---------------- G6 add_chan wiring
    r6 = np.random.default_rng(21)
    ch6, inf6 = OPS2.add_chan(copy.deepcopy(bf), r6)
    W = np.asarray(ch6["W"], float); K = np.asarray(ch6["K"], float)
    ok6 = (W.shape == (4, 1) and K.shape == (1, 4)
           and W[3, inf6["act"]] == 1.0 and abs(K[inf6["act"], 3]) > 0)
    fu = FU.funnel(ch6)
    ok6 &= fu["stage"] in ("pass", "fail_g0a")
    check("G6_add_chan_wiring", ok6, f'{inf6} funnel={fu["stage"]}')

    n_pass = sum(r["passed"] for r in RES)
    DL.append_result(dict(kind="val_gate_v2", gates=RES,
                          passed=bool(n_pass == len(RES)),
                          n_pass=n_pass, n=len(RES)), D2.RESULTS2)
    print(f"\n{n_pass}/{len(RES)} gates pass")
    return n_pass == len(RES)


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
