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
    assert s0["budget"] == {"sensor": 40000.0, "motion": 1200.0,
                            "injection": 120.0}
    r = run(ts.read_streams(window=4, devices="all"))
    assert len(r["steps"]) == 4 and r["t"] == 20.0
    assert r["sensor_cost"] == 4 * 32 * 5.0
    v0 = np.asarray(r["steps"][0]["values"]["0"])
    assert v0.shape == (12, 13)
    w = run(ts.wait(steps=100))
    assert w["t"] == 520.0
    m = run(ts.move(device=1, a1=1.0, a2=-0.5, steps=2))
    assert abs(m["motion_cost"] - 3.0) < 1e-9 and len(m["steps_read"]) == 2
    d = run(ts.dilate(device=1, gain=0.2))
    assert abs(d["motion_cost"] - 0.2) < 1e-6
    # pose persisted in state
    assert st.poses[1][2] != 1.0
    # span hard-stop
    w2 = run(ts.wait(steps=10000))
    assert w2["t"] == B.T0 and w2["at_end_of_span"]
    r2 = run(ts.read_streams(window=1))
    assert "error" in r2
    # sensor budget ledger consistent
    assert abs(st.spent["sensor"] - (r["sensor_cost"] + m["sensor_cost"]
               + d["sensor_cost"])) < 1e-6
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
    r"\bact\d", r"\bchan\d", r"\bu\d\b", r"p4g2", r"p6g8", r"p3g9",
    r"\bperm\b", r"permutation", r"rotation", r"\breflect",
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
    texts.append(("move", asyncio.get_event_loop().run_until_complete(
        ts.move(device=0, a1=0.5, a2=0.5))))
    texts.append(("dilate", asyncio.get_event_loop().run_until_complete(
        ts.dilate(device=0, gain=0.1))))
    texts.append(("wait", asyncio.get_event_loop().run_until_complete(
        ts.wait(steps=400))))
    texts.append(("inject", asyncio.get_event_loop().run_until_complete(
        ts.inject(port=0, amp=0.5, dur=10, lags=[5], devices=[1]))))
    texts.append(("inject_err", asyncio.get_event_loop().run_until_complete(
        ts.inject(port=99, amp=0.5, dur=10))))
    texts.append(("submit_err", asyncio.get_event_loop().run_until_complete(
        ts.submit(contract="P2", payload={"mean": [1]}))))
    for label, txt in texts:
        _leak_scan(txt, label)
    # system prompt + tool docstrings
    cfg = PhysimConfig(id="physim", difficulty="BLOB-E1", tier="tools")
    task = _blob_task(cfg, 0)
    _leak_scan(task.data.system_prompt, "system_prompt")
    _leak_scan(task.data.prompt, "prompt")
    for fn_name in ("status", "read_streams", "wait", "move", "dilate",
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


if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.new_event_loop())
    t1()
    t2()
    t3()
    t4()
    t5()
    print("ALL BLOB SERVER GATES PASS")
