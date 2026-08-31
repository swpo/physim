"""test_adequacy.py — W3 gates (needs E1 cache built).
Run: <venv-python> probes/blobs/agentenv/test_adequacy.py"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adequacy as A
import device as D


def t1_secrets_shared_dev0():
    """r1/r2 share dev0 secrets (P3 injection anchor identical) — required
    for branch-cache reuse across rosters."""
    wk = A.world_key("p4g2_044", 928)
    s1 = D.world_secrets(wk, 12, A.ROSTERS["r1"], 128.0)
    s2 = D.world_secrets(wk, 12, A.ROSTERS["r2"], 128.0)
    assert s1["port_perm"] == s2["port_perm"]
    # injection anchor (dev0 center) + pose shared; node_perm may differ (k)
    for key in ("center", "secret_rot", "reflect", "motion_theta",
                "motion_reflect"):
        assert s1["devices"][0][key] == s2["devices"][0][key], key
    print("T1 dev0 anchor/pose + port perm shared across rosters: PASS")


def t2_read_plans():
    for tier, cfg in A.TIERS.items():
        plan = A.read_plan(cfg["duty"])
        n_A = len(plan["A"])
        n_E = len(plan["E"])
        used = n_A + n_E + (A.COST_B_FULL if (plan["do_B"] and cfg["duty"] >= 1)
                            else A.COST_B if plan["do_B"] else 0) \
            + (A.COST_C if plan["do_C"] else 0) \
            + int(plan["D_duty"] * (A.PH_D[1] - A.PH_D[0]))
        print(f"  {tier}: total={plan['total']} A={n_A} E={n_E} "
              f"do_B={plan['do_B']} do_C={plan['do_C']} "
              f"D_duty={plan['D_duty']:.2f} used~{used}")
        assert used <= plan["total"] * 1.15 + 2, (tier, used, plan["total"])
        assert n_E >= 4, "contract anchors must always be funded"
    print("T2 read plans within budget, anchors funded: PASS")


def t3_branch_parity():
    """Control branch == main run over the branch window (f16 tolerance)."""
    mp, bp = A.cache_paths("p4g2_044", 928)
    if not (os.path.exists(mp) and os.path.exists(bp)):
        print("T3 SKIPPED (cache not built)")
        return
    c = D.CachedRun(mp)
    z = np.load(bp, allow_pickle=False)
    ctrl = z["control"]
    i0 = int(round(A.T0 / A.CTRL_TU))
    errs = []
    for j in range(0, ctrl.shape[0], 10):
        f_main = c.fields_at(i0 + j)
        f_br = ctrl[j].astype(np.float32)
        errs.append(np.abs(f_main - f_br).max())
    err = max(errs)
    assert err < 2e-2, f"branch-control drift vs main: {err}"
    print(f"T3 control branch == main window (max err {err:.1e}): PASS")


def t4_smoke_cell():
    """One full cell on E1 x1 r1; sanity of result structure."""
    mp, bp = A.cache_paths("p4g2_044", 928)
    if not (os.path.exists(mp) and os.path.exists(bp)):
        print("T4 SKIPPED (cache not built)")
        return
    res = A.run_cell("p4g2_044", 928, "r1", "x1", verbose=False)
    assert res["r1"]["ok"], res["r1"]
    assert "p1" in res and "p2" in res and "p3" in res
    assert res["spend"]["sensor"] <= res["budget"]["sensor"] + 1e-6
    assert res["spend"]["motion"] <= res["budget"]["motion"] + 1e-6
    print(json.dumps({k: res[k] for k in ("r1", "r2", "r3", "home_err",
                                          "spend", "budget")},
                     indent=1, default=str)[:1200])
    print("T4 smoke cell E1/x1/r1: PASS")


if __name__ == "__main__":
    t1_secrets_shared_dev0()
    t2_read_plans()
    t3_branch_parity()
    t4_smoke_cell()
    print("\nALL W3 GATES PASS (cache-dependent ones may be SKIPPED)")
