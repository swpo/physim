"""test_blob_server.py — BLOB family gates (run with repo .venv python).

T1 tool loop: status/read/wait/move/dilate through the agent surface,
   budget ledgers, span hard-stop.
T2 replica parity: amp=0 control replica == cached A0 control branch (f16).
T3 inject mechanics: pricing, caps, locks, replica reads vs cached
   announced branch at amp used by A0 (via oracle check on truth_p3).
T4 BARRIER AUDIT: every agent-visible string (status/read/move/dilate/
   inject/submit responses + system prompt + tool docstrings) is grepped
   for leak words (coordinates, lattice names, field names, blob words).
T5 submit: shape rejection, revision, lock after inject.
"""
import asyncio
import json
import sys

import numpy as np

from physim import blobcore as B
from physim.blobstate import BlobToolState
from physim.servers import blob as S
from physim.taskset import BLOB_SYSTEM_PROMPT, _blob_task, PhysimConfig

WORLD, SEED = "p4g2_044", 928


def make_ts():
    ts = S.BlobToolset(S.BlobToolsetConfig())
    st = BlobToolState()
    st.world, st.seed = WORLD, SEED
    ts._inert_state = st            # inert-state path = direct-call testing
    return ts, st


def run(coro):
    return json.loads(asyncio.get_event_loop().run_until_complete(coro))


def t1():
    ts, st = make_ts()
    s0 = run(ts.status())
    assert s0["t"] == 0.0 and s0["phase"] == "exploration", s0
    assert s0["ports"] == 12 and s0["slots_per_device"] == [13, 19]
    assert s0["budget"] == {"sensor": 40000.0, "adjust": 1200.0,
                            "injection": 120.0}
    r = run(ts.read_streams(window=4, devices="all"))
    assert len(r["steps"]) == 4 and r["t"] == 20.0
    assert r["sensor_cost"] == 4 * 32 * 5.0
    v0 = np.asarray(r["steps"][0]["values"]["0"])
    assert v0.shape == (12, 13)
    w = run(ts.wait(steps=100))
    assert w["t"] == 520.0
    # R3-final fixed map: pure translation + a safe dilation step
    m = run(ts.adjust(device=1, u1=0.4, u2=-0.2, u3=0.0, steps=2))
    assert m["result"] == "ok" and m["steps_applied"] == 2
    assert abs(m["adjust_cost"] - 1.2) < 1e-9 and len(m["steps_read"]) == 2
    d = run(ts.adjust(device=1, u1=0.0, u2=0.0, u3=-0.6))
    assert d["result"] == "ok"                     # exp(-0.6)=0.55 > 0.5
    assert abs(d["adjust_cost"] - 0.6) < 1e-6
    # pose persisted in state (some translation and/or dilation happened)
    assert st.poses[1][2] != 1.0 or st.poses[1][:2] != list(
        B.get_secrets(WORLD, SEED)["devices"][1]["center"])
    # span hard-stop
    w2 = run(ts.wait(steps=10000))
    assert w2["t"] == B.T0 and w2["at_end_of_span"]
    r2 = run(ts.read_streams(window=1))
    assert "error" in r2
    # sensor budget ledger consistent
    assert abs(st.spent["sensor"] - (r["sensor_cost"] + m["sensor_cost"]
               + d["sensor_cost"])) < 1e-6
    # status reports the R2 surface
    s1 = run(ts.status())
    assert s1["n_actuator_channels"] == 3
    assert "adjust" in s1["budget"] and "motion" not in s1["budget"]
    print("T1 tool loop: PASS")


def t2():
    ts, st = make_ts()
    st.i_ctrl = B.N_STEPS_MAIN
    fr = B.replica_frames(WORLD, SEED, port=0, amp=0.0, dur=5.0, n_ctrl=50)
    brz, _ = B.get_branches(WORLD, SEED)
    ctrl = brz["control"]
    diff = np.abs(fr.astype(np.float16).astype(np.float32)
                  - ctrl.astype(np.float32))
    assert diff.max() == 0.0, f"control replica != cached branch ({diff.max()})"
    print("T2 replica parity (amp=0 vs cached control, f16): PASS bitwise")


def t3():
    ts, st = make_ts()
    st.i_ctrl = B.N_STEPS_MAIN
    # cap enforcement
    e = run(ts.inject(port=4, amp=2.0, dur=10))
    assert "error" in e and "amp" in e["error"]
    e = run(ts.inject(port=4, amp=0.02, dur=10))
    assert "error" in e
    # pricing: amp 1.0 -> 1*(1+4*0.5)=3 per tu
    r = run(ts.inject(port=4, amp=1.0, dur=10, lags=[5, 50], devices=[1]))
    assert abs(r["injection_cost"] - 30.0) < 1e-6, r["injection_cost"]
    assert abs(r["sensor_cost"] - 2 * 19 * 5.0) < 1e-6
    assert r["locked_p1p2"] and st.locked_p1p2
    assert len(r["reads"]) == 2
    v = np.asarray(r["reads"][0]["values"]["1"])
    assert v.shape == (12, 19)
    # cheap amp: 0.3 -> 0.3 per tu
    r2 = run(ts.inject(port=4, amp=0.3, dur=10, lags=[5], devices=[1]))
    assert abs(r2["injection_cost"] - 3.0) < 1e-6
    # replica does respond: compare amp=1 vs control at same lag/port
    rc = run(ts.inject(port=4, amp=0.0, dur=5, lags=[5, 50], devices=[1]))
    a1 = np.asarray(r["reads"][0]["values"]["1"])
    a0 = np.asarray(rc["reads"][0]["values"]["1"])
    resp = np.abs(a1 - a0).max()
    assert resp > 1e-4, f"no detectable response at amp cap ({resp})"
    print(f"T3 inject mechanics: PASS (amp-1 response max {resp:.4f})")


# word-boundary patterns (re): geometry, domain, port names, secrets.
# "secret"/"undisclosed" as words are ALLOWED (the interface tells agents
# that structure exists without explaining it — spec A: "consistent, not
# explained"); disclosing WHICH structure is the leak.
LEAK_PATTERNS = [
    r"coordinate", r"\blattice\b", r"\bhex\b", r"hexagon", r"\bsquare\b",
    r"triangul", r"\bgrid\b", r"\btorus\b", r"periodic", r"\bwrap\b",
    r"\bring\b", r"\brings\b", r"node position", r"\(y, x\)",
    r"\by\s*=", r"\bx\s*=", r"center\s*=", r"\bnorth\b", r"\beast\b",
    r"\bblob", r"soliton", r"activator", r"inhibitor", r"\bfield\s*\d",
    r"genome", r"purwins", r"reaction[- ]diffusion", r"\bdiffusion\b",
    r"\bact\d", r"\bchan\d", r"p4g2", r"p6g8", r"p3g9",
    r"\bperm\b", r"permutation", r"rotation", r"\breflect",
    # R2 control-surface + emitter-location scrub (amendments A-C):
    r"co-locat", r"\bposition", r"\blocated\b", r"\bcenter\b",
    r"\borigin", r"\bmotion\b", r"\bmove\b", r"translat", r"dilat",
    r"spacing", r"\bzoom\b", r"\bscale\b", r"\bscaling\b",
    r"adjacen", r"\bpose\b", r"emitter",
]


def _leak_scan(text, label):
    import re
    low = text.lower()
    hits = [pat for pat in LEAK_PATTERNS if re.search(pat, low)]
    assert not hits, f"BARRIER LEAK in {label}: {hits}"


def t4():
    ts, st = make_ts()
    # every tool response on a happy path + error paths
    texts = []
    texts.append(("status", asyncio.get_event_loop().run_until_complete(
        ts.status())))
    texts.append(("read", asyncio.get_event_loop().run_until_complete(
        ts.read_streams(window=2))))
    texts.append(("adjust", asyncio.get_event_loop().run_until_complete(
        ts.adjust(device=0, u1=0.5, u2=0.5, u3=-0.3))))
    texts.append(("adjust_err", asyncio.get_event_loop().run_until_complete(
        ts.adjust(device=7, u1=0.1, u2=0.0, u3=0.0))))
    texts.append(("wait", asyncio.get_event_loop().run_until_complete(
        ts.wait(steps=400))))
    texts.append(("inject", asyncio.get_event_loop().run_until_complete(
        ts.inject(port=0, amp=0.5, dur=10, lags=[5], devices=[1]))))
    texts.append(("inject_err", asyncio.get_event_loop().run_until_complete(
        ts.inject(port=99, amp=0.5, dur=10))))
    texts.append(("submit_err", asyncio.get_event_loop().run_until_complete(
        ts.submit(contract="P2", payload={"mean": [1]}))))
    # a rejected adjust (park device at the wall via evaluator state, then
    # command the dilation channel upward): the response must stay GENERIC
    ts2, st2 = make_ts()
    st2.poses = [[10.0, 10.0, 2.999], [40.0, 40.0, 1.0]]
    st2.spent = dict(sensor=0.0, adjust=0.0, injection=0.0)
    rej = asyncio.get_event_loop().run_until_complete(
        ts2.adjust(device=0, u1=0.0, u2=0.0, u3=1.0, steps=3))
    rj = json.loads(rej)
    assert rj.get("result") == "adjust_rejected", rj
    assert set(rj) <= {"t", "applied", "steps_requested", "steps_applied",
                       "result", "device", "adjust_cost", "sensor_cost",
                       "steps_read", "budget"}, rj
    texts.append(("adjust_rejected", rej))
    for label, txt in texts:
        _leak_scan(txt, label)
    # system prompt + tool docstrings
    cfg = PhysimConfig(id="physim", difficulty="BLOB-E1r3", tier="tools")
    task = _blob_task(cfg, 0)
    _leak_scan(task.data.system_prompt, "system_prompt")
    _leak_scan(task.data.prompt, "prompt")
    for fn_name in ("status", "read_streams", "wait", "adjust",
                    "inject", "submit"):
        fn = getattr(S.BlobToolset, fn_name)
        _leak_scan(fn.__doc__ or "", f"docstring:{fn_name}")
    # announced contracts JSON
    cc = json.dumps(B.contracts(WORLD, SEED)["public"])
    _leak_scan(cc, "contracts.public")
    print("T4 barrier audit: PASS "
          f"({len(texts)} responses + prompt + docstrings + contracts)")


def t5():
    ts, st = make_ts()
    st.i_ctrl = B.N_STEPS_MAIN
    shapes = B.payload_shapes(WORLD, SEED)
    bad = run(ts.submit(contract="P2", payload={"mean": [0] * 5}))
    assert "error" in bad and bad["required_shape"] == [16]
    ok = run(ts.submit(contract="P2",
                       payload={"mean": [5.0] * 16, "sigma": 2.0}))
    assert ok["ok"]
    ok2 = run(ts.submit(contract="P2",
                        payload={"mean": [6.0] * 16, "sigma": 2.0}))
    assert ok2["ok"] and json.loads(st.sub_p2)["mean"][0] == 6.0
    # P3 shape via string payload
    mu = np.zeros(shapes["P3"]).tolist()
    ok3 = run(ts.submit(contract="P3",
                        payload=json.dumps({"mean": mu, "sigma": 1.0})))
    assert ok3["ok"]
    # lock
    run(ts.inject(port=0, amp=0.0, dur=5, lags=[5], devices=[1]))
    lk = run(ts.submit(contract="P1", payload={"mean": 0}))
    assert "error" in lk and "locked" in lk["error"]
    lk2 = run(ts.submit(contract="P2", payload={"mean": [5.0] * 16}))
    assert "error" in lk2
    ok4 = run(ts.submit(contract="P3",
                        payload=json.dumps({"mean": mu, "sigma": 1.0})))
    assert ok4["ok"], "P3 must stay open after lock"
    print("T5 submit/locks: PASS")




def t6():
    """R3-final probe_adjust: fixed global map (u1->dx*1.5, u2->dy*1.5,
    u3->dlog) — pose math, wall rejection at BOTH bounds (u3 only), strain-
    charge equality, multi-step partial application, rejected-step stream
    absence, pure-translation never refused (even at a wall)."""
    M = np.asarray(B.get_secrets(WORLD, SEED)["adjust_mix"], float)
    assert np.allclose(M, [[0.0, 1.5, 0.0], [1.5, 0.0, 0.0],
                           [0.0, 0.0, 1.0]]), M

    # --- pose math
    ts, st = make_ts()
    sec = B.get_secrets(WORLD, SEED)
    c0 = np.asarray(sec["devices"][0]["center"], float)
    r = run(ts.adjust(device=0, u1=0.3, u2=-0.2, u3=0.1, read=False))
    assert r["result"] == "ok" and r["steps_applied"] == 1
    L = B.get_cached(WORLD, SEED).meta["L"]
    exp = (c0 + np.array([1.5 * -0.2, 1.5 * 0.3])) % L   # (dy, dx)
    assert np.allclose(st.poses[0][:2], exp, atol=1e-9)
    assert abs(st.poses[0][2] - float(np.exp(0.1))) < 1e-12
    assert abs(st.spent["adjust"] - 0.6) < 1e-9

    # --- UPPER wall via u3
    ts, st = make_ts()
    per = 0.5
    n_to_wall = int(np.ceil(np.log(3.0) / 0.5)) + 1      # dlog=0.5/step
    rr = run(ts.adjust(device=0, u1=0.0, u2=0.0, u3=0.5,
                       steps=n_to_wall, read=False))
    assert rr["result"] == "adjust_rejected", rr
    napp = rr["steps_applied"]
    assert 0 < napp < n_to_wall
    assert abs(st.spent["adjust"] - (napp + 1) * per) < 1e-9
    assert st.poses[0][2] <= 3.0 + 1e-9
    dil_wall = st.poses[0][2]
    # repeated push at the wall: 1 strain, no movement, no streams
    spent0 = st.spent["adjust"]
    r2_ = run(ts.adjust(device=0, u1=0.0, u2=0.0, u3=0.5, steps=5,
                        read=True))
    assert r2_["result"] == "adjust_rejected" and r2_["steps_applied"] == 0
    assert st.poses[0][2] == dil_wall
    assert r2_["steps_read"] == [] and r2_["sensor_cost"] == 0.0
    assert abs(st.spent["adjust"] - spent0 - per) < 1e-9
    # --- pure TRANSLATION at the wall: NEVER refused
    pos_before = list(st.poses[0][:2])
    r3_ = run(ts.adjust(device=0, u1=1.0, u2=-0.7, u3=0.0, steps=3,
                        read=False))
    assert r3_["result"] == "ok" and r3_["steps_applied"] == 3, r3_
    assert st.poses[0][2] == dil_wall
    assert st.poses[0][:2] != pos_before
    # --- strain equality: +u3 vs -u3 of equal magnitude
    spent1 = st.spent["adjust"]
    r4_ = run(ts.adjust(device=0, u1=0.0, u2=0.0, u3=-0.5, read=False))
    assert r4_["result"] == "ok"                    # off the wall: applies
    assert abs(st.spent["adjust"] - spent1 - per) < 1e-9
    # --- LOWER wall
    ts, st = make_ts()
    n_to_floor = int(np.ceil(np.log(1.0 / 0.5) / 0.5)) + 1
    r5_ = run(ts.adjust(device=0, u1=0.0, u2=0.0, u3=-0.5,
                        steps=n_to_floor + 3, read=False))
    assert r5_["result"] == "adjust_rejected"
    assert st.poses[0][2] >= 0.5 - 1e-9
    assert abs(st.spent["adjust"]
               - (r5_["steps_applied"] + 1) * per) < 1e-9
    print("T6 probe_adjust (R3-final fixed map): PASS "
          f"(wall at {dil_wall:.3f}, floor at {st.poses[0][2]:.3f})")


if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.new_event_loop())
    t1()
    t2()
    t3()
    t4()
    t5()
    t6()
    print("ALL BLOB SERVER GATES PASS")
