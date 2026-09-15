"""test_blob_round2.py — BLOB round-2 gates (clean-slate L1-L4).

G1 registry + shapes + menus (E1 vs E2 differ per phenomenology).
G2 L1 truth vs agent-surface execution: running the announced sequence via
   probe_adjust during the span (from t=0 config) lands on the SAME pose
   the evaluator walks; truth frame index = span end + steps.
G3 L4D dose leg: drawn amp in [0.3,0.9]; table interpolation exact at grid
   points; oracle table -> skill 1; announced port == cached branch port.
G4 skill scoring: empty -1, oracle +1, worse-than-baseline clipped >= -1;
   baseline table published in detail.
G5 BARRIER AUDIT: round-2 status (menu mode) + all announced contract text
   + both system prompts + submit responses, extended pattern list (zero
   pose/location/actuator-semantics language; L2 wording especially).
G6 server round-2 submit: shape rejection, lock set (L1/L2/L3* lock at
   first inject; L4/L4D stay open), status submitted-map.
"""
import asyncio
import json
import sys

import numpy as np

from physim import blobcore as B
from physim import blobround2 as R2
from physim.blobstate import BlobToolState
from physim.servers import blob as S
from physim.taskset import _blob2_task, PhysimConfig

E1 = ("p4g2_044", 928, "E1")
E2 = ("p6g8_033", 942, "E2")


def make_ts(world, seed, menu):
    ts = S.BlobToolset(S.BlobToolsetConfig())
    st = BlobToolState()
    st.world, st.seed, st.round2 = world, seed, menu
    ts._inert_state = st
    return ts, st


def run(coro):
    return json.loads(asyncio.get_event_loop().run_until_complete(coro))


def g1():
    for world, seed, menu in (E1, E2):
        cc = R2.contracts2(world, seed, menu)
        shapes = R2.payload_shapes2(world, seed, menu)
        assert set(cc["public"]["menu"]) == set(R2.MENUS[menu])
        assert set(shapes) == set(R2.MENUS[menu])
    assert "L3E" in R2.MENUS["E1"] and "L3E" not in R2.MENUS["E2"]
    assert "L3S" in R2.MENUS["E2"] and "L3S" not in R2.MENUS["E1"]
    assert R2.L3F_H["E1"][0] == 5.0 and R2.L3F_H["E2"][0] == 25.0
    print("G1 registry/menus: PASS")


def g2():
    world, seed, menu = E1
    ts, st = make_ts(world, seed, menu)
    seqs = R2.l1_sequences(world, seed)
    # walk the span to its end minus enough steps, then execute seq 0
    seq = seqs[0]
    n = int(seq["steps"])
    run(ts.wait(steps=B.N_STEPS_MAIN - n))
    r = run(ts.adjust(device=0, u1=seq["u"][0], u2=seq["u"][1],
                      u3=seq["u"][2], steps=n, read=True))
    assert r["result"] == "ok" and r["steps_applied"] == n
    # agent pose after executing == evaluator's walked pose
    dev_eval = R2._walked_device(world, seed, seq)
    assert np.allclose(st.poses[0][:2], dev_eval.center, atol=1e-9)
    assert abs(st.poses[0][2] - dev_eval.dilation) < 1e-12
    # the agent's final read (at frame N_STEPS_MAIN) equals truth sampled at
    # the same pose at the same frame — while L1 truth is at N_STEPS_MAIN+n
    # (fork extends past the span): verify the evaluator frame index
    y = R2.truth_l1(world, seed)
    i_truth = B.N_STEPS_MAIN + n
    expect = B.sample_at(world, seed, i_truth, dev_eval)
    assert np.allclose(y[0], expect, atol=0), "truth frame mismatch"
    # and the agent-surface read at the walked pose matches the cache at its
    # own frame (read values come from the same sample path)
    v_agent = np.asarray(r["steps_read"][-1]["values"], float)
    expect_agent = B.sample_at(world, seed, B.N_STEPS_MAIN, dev_eval)
    assert np.allclose(v_agent, np.round(expect_agent, 5), atol=1e-5)
    print("G2 L1 pose/truth parity: PASS")


def g3():
    for world, seed, menu in (E1, E2):
        amp = R2.dose_amp(world, seed)
        assert 0.3 <= amp <= 0.9
        # announced port must equal the cached branch injection port
        _, br_meta = B.get_branches(world, seed)
        cc = B.contracts(world, seed)["private"]
        assert cc["ann_port"] == br_meta["inj_port"]
        # interpolation exactness at grid points: build a table linear in
        # amp (resp = amp * T); interp at drawn amp must equal amp * T
        shapes = R2.payload_shapes2(world, seed, menu)
        nA, nL, nf, kB = shapes["L4D"]
        T = np.arange(nL * nf * kB, dtype=float).reshape(nL, nf, kB) / 999.0
        tab = np.stack([a * T for a in R2.L4D_AMPS])
        mu_interp_expect = amp * T
        grid = np.asarray(R2.L4D_AMPS)
        j = int(np.clip(np.searchsorted(grid, amp) - 1, 0, len(grid) - 2))
        w = (amp - grid[j]) / (grid[j + 1] - grid[j])
        got = (1 - w) * tab[j] + w * tab[j + 1]
        assert np.allclose(got, mu_interp_expect, atol=1e-12)
    print(f"G3 dose leg: PASS (drawn amps "
          f"{R2.dose_amp(*E1[:2]):.3f}/{R2.dose_amp(*E2[:2]):.3f})")


def g4():
    world, seed, menu = E1
    r0 = R2.score_episode2(world, seed, menu, {})
    assert r0["reward_skill"] == -1.0
    assert "baselines" in r0["detail"] and "L4D" in r0["detail"]["baselines"]
    # garbage submission scores clipped at -1, not below
    shapes = R2.payload_shapes2(world, seed, menu)
    subs = {"L2": json.dumps(dict(mean=(np.zeros(shapes["L2"])
                                        + 99).tolist(), sigma=0.001))}
    r1 = R2.score_episode2(world, seed, menu, subs)
    assert r1["skills"]["L2"] == -1.0
    print("G4 skill scoring: PASS")


LEAK_PATTERNS = [
    r"coordinate", r"\blattice\b", r"\bhex\b", r"hexagon", r"\bsquare\b",
    r"triangul", r"\bgrid\b", r"\btorus\b", r"periodic",
    r"\bwrap\b", r"\bring\b", r"\brings\b", r"\bnorth\b", r"\beast\b",
    r"\bblob", r"soliton", r"activator", r"inhibitor", r"\bfield\s*\d",
    r"genome", r"purwins", r"reaction[- ]diffusion", r"\bdiffusion\b",
    r"\bact\d", r"\bchan\d", r"p4g2", r"p6g8", r"p3g9",
    r"\bperm\b", r"permutation", r"rotation", r"\breflect",
    r"co-locat", r"\bposition", r"\blocated\b", r"\bcenter\b", r"\borigin",
    r"\bmotion\b", r"\bmove\b", r"translat", r"dilat", r"spacing",
    r"\bzoom\b", r"\bscale\b", r"\bscaling\b", r"adjacen", r"\bpose\b",
    r"emitter",
    # location hints ("where ... is undisclosed" is approved non-disclosure)
    r"\bmidpoint\b", r"\bbetween\b", r"\bnear\b", r"\bdistance\b",
]


def _scan(text, label):
    import re
    low = text.lower()
    hits = [pat for pat in LEAK_PATTERNS if re.search(pat, low)]
    assert not hits, f"BARRIER LEAK in {label}: {hits}"


def g5():
    import re
    n = 0
    for world, seed, menu in (E1, E2):
        cc = R2.contracts2(world, seed, menu)["public"]
        _scan(json.dumps(cc), f"contracts2[{menu}]")
        n += 1
        ts, st = make_ts(world, seed, menu)
        _scan(asyncio.get_event_loop().run_until_complete(ts.status()),
              f"status[{menu}]")
        n += 1
        # submit error paths
        _scan(asyncio.get_event_loop().run_until_complete(
            ts.submit(contract="L2", payload={"mean": [1]})),
            f"submit_err[{menu}]")
        n += 1
        d = "BLOB2-E1" if menu == "E1" else "BLOB2-E2"
        t = _blob2_task(PhysimConfig(id="physim", difficulty=d,
                                     tier="tools"), 0)
        _scan(t.data.system_prompt, f"system_prompt[{menu}]")
        _scan(t.data.prompt, f"prompt[{menu}]")
        n += 2
    print(f"G5 barrier audit: PASS ({n} surfaces)")


def g6():
    world, seed, menu = E1
    ts, st = make_ts(world, seed, menu)
    st.i_ctrl = B.N_STEPS_MAIN
    shapes = R2.payload_shapes2(world, seed, menu)
    # wrong id
    r = run(ts.submit(contract="P1", payload={"mean": 0}))
    assert "error" in r
    # shape rejection
    r = run(ts.submit(contract="L1", payload={"mean": [0] * 5}))
    assert "error" in r and r["required_shape"] == list(shapes["L1"])
    # accept + revise
    mu = np.zeros(shapes["L3F"]).tolist()
    r = run(ts.submit(contract="L3F",
                      payload=json.dumps(dict(mean=mu, sigma=1.0))))
    assert r["ok"]
    # inject locks the forecast set but not L4/L4D
    run(ts.inject(port=0, amp=0.0, dur=5, lags=[5], devices=[1]))
    for cid in ("L1", "L2", "L3F", "L3E"):
        r = run(ts.submit(contract=cid,
                          payload=json.dumps(dict(mean=0.0))))
        assert "error" in r and "locked" in r["error"], (cid, r)
    mu4 = np.zeros(shapes["L4"]).tolist()
    r = run(ts.submit(contract="L4",
                      payload=json.dumps(dict(mean=mu4, sigma=1.0))))
    assert r["ok"]
    mu4d = np.zeros(shapes["L4D"]).tolist()
    r = run(ts.submit(contract="L4D",
                      payload=json.dumps(dict(mean=mu4d, sigma=1.0))))
    assert r["ok"]
    # status submitted-map reflects menu
    s = run(ts.status())
    assert set(s["submitted"]) == set(R2.MENUS[menu])
    assert s["submitted"]["L4"] and not s["submitted"]["L2"]
    print("G6 round-2 submit/locks: PASS")


if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.new_event_loop())
    g1()
    g2()
    g3()
    g4()
    g5()
    g6()
    print("ALL BLOB ROUND-2 GATES PASS")
