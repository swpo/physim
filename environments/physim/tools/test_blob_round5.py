'''test_blob_round5.py — BLOB round-5 gates (v2.1, spec PART 6 + brief).

G-R1 reveal-leak: byte-identical pre-reveal tool outputs under an instance
     salt redraw ("r5_instances_v1" vs a test salt); the redraw is proved
     REAL by differing reveal menus. Plus the text audit: the economy
     vocabulary ('budget','cost','price','spend','remaining','afford',
     'left') is absent from EVERY agent-visible round-5 string, and the v1
     barrier patterns hold (minus wording the normative syllabus itself
     uses: 'emitter', 'grid values').
G-R2 post-reveal isolation: after probe_ready every world tool returns the
     generic phase error; probe_status/probe_submit stay alive;
     resubmission works; world meters stop accruing.
G-R3 replay==live at anchor (A0 pattern): a fork's window=0 read equals the
     base-record read bitwise at the anchor, and a full f32 re-simulation
     from t=0 agrees with the f16 record at A0 tolerance (also gated at
     truth build: the anchors pass asserts bitwise state equality at the
     1700 snapshot; its parity_max is re-checked here).
G-R4 caps: synthetic saturation (shrunken CAPS5) triggers the generic
     "instrument saturated" refusal and logs cap_hits; the normal smoke
     runs show ZERO cap hits (checked from the floor tables in G-R5).
G-R5 scripted-actor smoke floor tables exist for both worlds x 3 seeds
     (produced by tools/smoke_blob2v2.py --all), every per-rollout smoke
     gate passed, zero cap hits anywhere.
G-R6 determinism: same (world, seed) -> identical instance menu (fresh
     redraw) + identical truth-array hashes across two independent builds
     (second build under --cache-dir, e.g. /tmp/r5_verify).

Run (repo root, after truth build + smokes):
  .venv/bin/python environments/physim/tools/test_blob_round5.py
  ... --verify-cache /tmp/r5_verify     # enables the G-R6 second-build half
'''
import argparse
import asyncio
import copy
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "environments", "physim"))

from physim import blobcore as B                      # noqa: E402
from physim import blobround5 as R5                   # noqa: E402
from physim.blobstate import BlobToolState            # noqa: E402
from physim.servers import blob as S                  # noqa: E402
from physim.taskset import _blob5_task, PhysimConfig  # noqa: E402

E1 = ("p4g2_044", 928, "E1")
E2 = ("p6g8_033", 942, "E2")
TEST_SALT = "r5_instances_TESTREDRAW"


def make_ts(world, seed, menu, nonce="gatenonce01"):
    ts = S.BlobToolset(S.BlobToolsetConfig())
    st = BlobToolState()
    st.world, st.seed, st.round5 = world, seed, menu
    st.r5_nonce = nonce
    ts._inert_state = st
    return ts, st


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def jrun(coro):
    return json.loads(run(coro))


# ------------------------------------------------------------------- G-R1
ECONOMY_PATTERNS = [r"\bbudget", r"\bcost", r"\bpric", r"\bspend",
                    r"\bspent\b", r"\bremaining\b", r"\bafford",
                    r"\bleft\b", r"\breplica", r"\block"]
# v1 barrier list (test_blob_round2), minus wording the normative spec-2.3
# syllabus itself uses: 'emitter' (L4 text) and 'grid' ("grid values",
# "base grid time" — parameter grids, not world geometry).
LEAK_PATTERNS = [
    r"coordinate", r"\blattice\b", r"\bhex\b", r"hexagon", r"\bsquare\b",
    r"triangul", r"\btorus\b", r"periodic", r"\bwrap\b", r"\bring\b",
    r"\brings\b", r"\bnorth\b", r"\beast\b", r"\bblob", r"soliton",
    r"activator", r"inhibitor", r"\bfield\s*\d", r"genome", r"purwins",
    r"reaction[- ]diffusion", r"\bdiffusion\b", r"\bact\d", r"\bchan\d",
    r"p4g2", r"p6g8", r"p3g9", r"\bperm\b", r"permutation", r"rotation",
    r"\breflect", r"co-locat", r"\bposition", r"\blocated\b", r"\bcenter\b",
    r"\borigin", r"\bmotion\b", r"\bmove\b", r"translat", r"dilat",
    r"spacing", r"\bzoom\b", r"\bscale\b", r"\bscaling\b", r"adjacen",
    r"\bpose\b", r"\bmidpoint\b", r"\bnear\b", r"\bdistance\b",
]


def _scan(text, label, patterns, what):
    low = str(text).lower()
    # the episode tag "BLOB2v2-Ex" is spec-2.3 normative wording (the
    # syllabus header); it is the only permitted "blob" token.
    low = low.replace("blob2v2-e1", "").replace("blob2v2-e2", "")
    hits = [p for p in patterns if re.search(p, low)]
    assert not hits, f"{what} in {label}: {hits}"


def _prereveal_transcript(world, seed, menu):
    '''A fixed pre-reveal tool program covering every world tool + error
    paths; returns the exact byte sequence of responses.'''
    ts, st = make_ts(world, seed, menu)
    outs = []

    async def drive():
        outs.append(await ts.status5())
        outs.append(await ts.read5(ctx="base", window=4, devices="all"))
        outs.append(await ts.read5(ctx="base", window=0, ports=[0, 1]))
        outs.append(await ts.wait5(ctx="base", steps=20))
        outs.append(await ts.adjust5(device=1, u1=0.4, u2=-0.2, u3=0.1,
                                     ctx="base", steps=2))
        f = json.loads(await ts.fork5(t=750.0))
        fid = f["fork"]
        outs.append(json.dumps(f))
        outs.append(await ts.read5(ctx=fid, window=2, devices=[1]))
        outs.append(await ts.inject5(ctx=fid, port=2, amp=0.6, dur=7.5))
        outs.append(await ts.read5(ctx=fid, window=3, devices=[1]))
        outs.append(await ts.adjust5(device=0, u1=0.2, u2=0.0, u3=0.0,
                                     ctx=fid, steps=1))
        outs.append(await ts.wait5(ctx=fid, steps=2))
        f2 = json.loads(await ts.fork5(fork=fid))
        outs.append(json.dumps(f2))
        outs.append(await ts.reset5(fork=f2["fork"]))
        outs.append(await ts.inject5(ctx=fid, port=0, amp=2.0, dur=5))
        outs.append(await ts.inject5(ctx="base", port=0, amp=0.5, dur=5))
        outs.append(await ts.read5(ctx="nosuch", window=1))
        outs.append(await ts.submit5(instance="L1", payload={"mean": 0}))
        outs.append(await ts.status5())
    run(drive())
    return "\x1e".join(outs), ts, st


def g_r1():
    n_surface = 0
    for world, seed, menu in (E1, E2):
        base_salt = R5.ACTIVE_SALT
        try:
            R5.ACTIVE_SALT = R5.INSTANCE_SALT
            t_v1, _, _ = _prereveal_transcript(world, seed, menu)
            menu_a = R5.reveal_menu5(world, seed, menu, R5.INSTANCE_SALT)
            R5.ACTIVE_SALT = TEST_SALT
            t_v2, ts2, _ = _prereveal_transcript(world, seed, menu)
            menu_b = R5.reveal_menu5(world, seed, menu, TEST_SALT)
        finally:
            R5.ACTIVE_SALT = base_salt
        assert t_v1 == t_v2, \
            f"pre-reveal surface depends on the instance salt ({menu})"
        assert json.dumps(menu_a) != json.dumps(menu_b), \
            "test salt failed to redraw instances (vacuous gate)"
        # text audit over the whole pre-reveal transcript + reveal menu +
        # system prompt + docstrings
        _scan(t_v1, f"pre-reveal transcript[{menu}]", ECONOMY_PATTERNS,
              "ECONOMY VOCAB")
        _scan(t_v1, f"pre-reveal transcript[{menu}]", LEAK_PATTERNS,
              "BARRIER LEAK")
        _scan(json.dumps(menu_a), f"reveal menu[{menu}]", ECONOMY_PATTERNS,
              "ECONOMY VOCAB")
        _scan(json.dumps(menu_a), f"reveal menu[{menu}]", LEAK_PATTERNS,
              "BARRIER LEAK")
        n_surface += 2
        d = "BLOB2v2-E1" if menu == "E1" else "BLOB2v2-E2"
        task = _blob5_task(PhysimConfig(id="physim", difficulty=d,
                                        tier="tools"), 0)
        for label, txt in (("system_prompt", task.data.system_prompt),
                           ("prompt", task.data.prompt)):
            _scan(txt, f"{label}[{menu}]", ECONOMY_PATTERNS,
                  "ECONOMY VOCAB")
            _scan(txt, f"{label}[{menu}]", LEAK_PATTERNS, "BARRIER LEAK")
            n_surface += 1
        # post-ready + submit responses (phase B surface)
        outs = []

        async def phase_b(ts2=ts2):
            outs.append(await ts2.ready5())
            shp = R5.payload_shapes5(world, seed, menu, TEST_SALT)["L2"]
            outs.append(await ts2.submit5(
                instance="L2", payload=json.dumps(
                    dict(mean=np.zeros(shp).tolist(), sigma=1.0))))
            outs.append(await ts2.submit5(instance="L1",
                                          payload={"mean": [1]}))
            outs.append(await ts2.status5())
            outs.append(await ts2.read5(ctx="base", window=1))
        run(phase_b())
        _scan("\x1e".join(outs), f"phase-B transcript[{menu}]",
              ECONOMY_PATTERNS, "ECONOMY VOCAB")
        n_surface += 1
    for fn_name in ("status5", "read5", "wait5", "adjust5", "fork5",
                    "reset5", "inject5", "ready5", "submit5"):
        doc = getattr(S.BlobToolset, fn_name).__doc__ or ""
        _scan(doc, f"docstring:{fn_name}", ECONOMY_PATTERNS,
              "ECONOMY VOCAB")
        _scan(doc, f"docstring:{fn_name}", LEAK_PATTERNS, "BARRIER LEAK")
        n_surface += 1
    print(f"G-R1 reveal-leak + text audit: PASS ({n_surface} surfaces, "
          "byte-identical pre-reveal transcripts under salt redraw)")


# ------------------------------------------------------------------- G-R2
def g_r2():
    world, seed, menu = E1
    ts, st = make_ts(world, seed, menu)

    async def drive():
        await ts.read5(ctx="base", window=2)
        f = json.loads(await ts.fork5(t=500.0))
        await ts.read5(ctx=f["fork"], window=1, devices=[0])
        rr = json.loads(await ts.ready5())
        assert rr["phase"] == "revealed" and len(rr["instances"]) == 6
        meters_at_ready = copy.deepcopy(st.r5_meters)
        world_tools = [
            ("read", ts.read5(ctx="base", window=1)),
            ("read0", ts.read5(ctx="base", window=0)),
            ("wait", ts.wait5(ctx="base", steps=1)),
            ("adjust", ts.adjust5(device=0, u1=0.1, u2=0, u3=0,
                                  ctx="base")),
            ("fork", ts.fork5(t=100.0)),
            ("fork2", ts.fork5(fork=f["fork"])),
            ("reset", ts.reset5(fork=f["fork"])),
            ("inject", ts.inject5(ctx=f["fork"], port=0, amp=0.5, dur=5)),
            ("ready2", ts.ready5()),
        ]
        for name, coro in world_tools:
            out = json.loads(await coro)
            assert out.get("error") == "not available in the current " \
                "phase", (name, out)
        assert st.r5_meters == meters_at_ready, "meters accrued in phase B"
        s = json.loads(await ts.status5())
        assert s["phase"] == "revealed" and "instances" in s
        shp = R5.payload_shapes5(world, seed, menu)["L3E"]
        p1 = json.dumps(dict(mean=np.zeros(shp).tolist(), sigma=1.0))
        r1 = json.loads(await ts.submit5(instance="L3E", payload=p1))
        assert r1.get("ok"), r1
        p2 = json.dumps(dict(mean=(np.zeros(shp) + 2).tolist(), sigma=2.0))
        r2 = json.loads(await ts.submit5(instance="L3E@i1", payload=p2))
        assert r2.get("ok"), r2
        assert json.loads(st.r5_subs["L3E"])["mean"][0] == 2.0, \
            "resubmission must replace"
        s2 = json.loads(await ts.status5())
        assert s2["submitted"]["L3E@i1"] is True
    run(drive())
    print("G-R2 post-reveal isolation: PASS (9 world tools refused "
          "generically; status/submit/resubmit alive; meters frozen)")


# ------------------------------------------------------------------- G-R3
def g_r3(full=True):
    world, seed, menu = E1
    ts, st = make_ts(world, seed, menu)

    async def drive():
        outs = {}
        for t_anchor in (700.0, 1800.0):
            f = json.loads(await ts.fork5(t=t_anchor))
            r = json.loads(await ts.read5(ctx=f["fork"], window=0))
            outs[t_anchor] = {d: np.asarray(r["steps"][0]["values"][d])
                              for d in ("0", "1")}
        return outs
    fork_reads = run(drive())
    devs = [B.make_device(world, seed, i) for i in (0, 1)]
    for t_anchor, vals in fork_reads.items():
        i = int(round(t_anchor / B.CTRL_TU))
        for d in (0, 1):
            rep = np.round(B.sample_at(world, seed, i, devs[d]), 5)
            assert np.array_equal(vals[str(d)], rep), \
                f"fork spawn read != base record at t={t_anchor}"
    # A0 tolerance vs a full f32 re-simulation: the truth build already
    # asserted bitwise equality at the 1700 snapshot and recorded the
    # replay==live parity over 4 grid checkpoints; re-check that number.
    z = np.load(R5._anchors_path(world, seed), allow_pickle=False)
    meta = json.loads(str(z["meta"]))
    assert meta["parity_max"] <= 2e-3, meta["parity_max"]
    par = []
    if full:
        # independent 300tu live re-sim from t=0 (fresh init_soup state)
        from blobkit.soup import sim_cpu
        g = B.load_genome(world)
        c = B.get_cached(world, seed)
        Ssim = sim_cpu.init_soup(g, L=c.meta["L"], seed=seed, dtype="f32",
                                 workers=3)
        perm = np.asarray(B.get_secrets(world, seed)["port_perm"], int)
        for i_chk in (30, 60):
            B.agdev.step_chunk(Ssim, (i_chk - (0 if i_chk == 30 else 30))
                               * R5.SPC)
            live = devs[0].sample(
                np.asarray(Ssim["F"], np.float32)[perm], c.meta["dx"])
            rep = B.sample_at(world, seed, i_chk, devs[0])
            par.append(float(np.abs(live - rep).max()))
        assert max(par) <= 2e-3, par
    print("G-R3 replay==live at anchor: PASS (fork window-0 reads bitwise "
          f"vs record; build parity_max {meta['parity_max']:.2e}"
          + (f"; fresh re-sim parity {max(par):.2e}" if par else ""))


# ------------------------------------------------------------------- G-R4
def g_r4():
    world, seed, menu = E1
    tiny = dict(sensor=200.0, adjust=1.0, injection=2.0, fork_spawns=2,
                open_forks=1, sim_tu=10.0)
    real = R5.CAPS5
    hits_expected = []
    try:
        R5.CAPS5 = tiny
        ts, st = make_ts(world, seed, menu)

        async def drive():
            f = json.loads(await ts.fork5(t=500.0))          # spawn 1
            fid = f["fork"]
            out = json.loads(await ts.fork5(t=600.0))        # open cap (1)
            assert out.get("error") == R5.CAP_MSG, out
            hits_expected.append("open_forks")
            out = json.loads(await ts.read5(ctx=fid, window=3,
                                            devices=[0]))    # sim 15tu
            assert out.get("error") == R5.CAP_MSG, out
            hits_expected.append("sim_tu")
            out = json.loads(await ts.read5(ctx="base", window=2))
            assert out.get("error") == R5.CAP_MSG, out       # sensor 320
            hits_expected.append("sensor")
            out = json.loads(await ts.adjust5(device=0, u1=1.0, u2=0.5,
                                              u3=0.0, ctx="base"))
            assert out.get("error") == R5.CAP_MSG, out       # adjust 1.5
            hits_expected.append("adjust")
            out = json.loads(await ts.inject5(ctx=fid, port=0, amp=1.0,
                                              dur=10))       # 30 amp-tu
            assert out.get("error") == R5.CAP_MSG, out
            hits_expected.append("injection")
            await ts.reset5(fork=fid)
            json.loads(await ts.fork5(t=700.0))              # spawn 2
            out = json.loads(await ts.fork5(t=800.0))        # spawn cap
            assert out.get("error") == R5.CAP_MSG, out
            hits_expected.append("fork_spawns")
        run(drive())
        for k in hits_expected:
            assert st.r5_cap_hits[k] >= 1, (k, st.r5_cap_hits)
    finally:
        R5.CAPS5 = real
    # generic wording: no numbers, no meter names, no coaching
    assert R5.CAP_MSG == "instrument saturated"
    print("G-R4 caps: PASS (6 synthetic saturations -> generic refusal, "
          "all logged; zero hits in normal smokes checked in G-R5)")


# ------------------------------------------------------------------- G-R5
def g_r5():
    rdir = os.path.join(B.AGENTENV, "results")
    rows = []
    for tag, seeds in (("E1", (928, 929, 930)), ("E2", (942, 943, 944))):
        for seed in seeds:
            p = os.path.join(rdir, f"smoke_blob2v2_{tag}_s{seed}.json")
            assert os.path.exists(p), \
                f"missing floor table {p}; run tools/smoke_blob2v2.py --all"
            rows.append((tag, seed, json.load(open(p))))
    bad = [(t, s) for t, s, r in rows if not r["smoke_pass"]]
    assert not bad, f"smoke gates failed: {bad}"
    caps = [(t, s) for t, s, r in rows
            if sum(r["cap_hits"].values()) != 0]
    assert not caps, f"cap hits in normal smokes: {caps}"
    for t, s, r in rows:
        print(f"  {t} s{s}: reward {r['reward_skill']:+.3f}  "
              + "  ".join(f"{k} {v:+.2f}" for k, v in r["skills"].items()))
    print("G-R5 scripted-actor floors: PASS (6/6 rollouts, all instances "
          "submitted, zero cap hits)")


# ------------------------------------------------------------------- G-R6
def g_r6(verify_cache=None):
    for world, seed, menu in (E1, E2):
        # instance-menu determinism: fresh redraws agree
        a = R5.instances5(world, seed, menu)
        R5.instances5.cache_clear()
        b = R5.instances5(world, seed, menu)
        assert json.dumps(a, sort_keys=True) == json.dumps(b,
                                                           sort_keys=True)
    pairs = [("p4g2_044", s, "E1") for s in (928, 929, 930)] + \
            [("p6g8_033", s, "E2") for s in (942, 943, 944)]
    n_arrays = 0
    for world, seed, menu in pairs:
        z = np.load(R5.truth_path(world, seed), allow_pickle=False)
        man = json.loads(str(z["manifest"]))
        # manifest hashes match the stored arrays (self-consistency)
        import hashlib
        for k, hexp in man["hashes"].items():
            h = hashlib.sha256(
                np.ascontiguousarray(z[k]).tobytes()).hexdigest()
            assert h == hexp, f"stored-array hash drift {world} s{seed} {k}"
            n_arrays += 1
        if verify_cache:
            p2 = R5.truth_path(world, seed, verify_cache)
            assert os.path.exists(p2), \
                f"missing second build {p2}; run build_blob5_truth.py " \
                f"all --cache-dir {verify_cache}"
            man2 = json.loads(str(np.load(p2,
                                          allow_pickle=False)["manifest"]))
            assert man["hashes"] == man2["hashes"], \
                f"TRUTH HASH MISMATCH across builds: {world} s{seed}"
            assert json.dumps(man["instances"], sort_keys=True) == \
                json.dumps(man2["instances"], sort_keys=True)
    extra = " + second-build hash equality" if verify_cache else \
        " (second build not supplied: self-consistency only)"
    print(f"G-R6 determinism: PASS (menus redraw-stable; {n_arrays} truth "
          f"arrays hash-consistent{extra})")


def brute_force_note():
    '''PART 6 step 4: per-tier hidden dimensions + effective cardinality
    (published with the floors; documents that domain-gridding is
    hopeless).'''
    note = {
        "anchor_t": "continuous-uniform [600, 2300], realized at sim-step "
                    "resolution dt=0.02 -> 85,000 distinguishable anchor "
                    "states per family draw, off the 5tu read grid w.p. 1",
        "L1": "anchor x sequence length {1,2,3} x continuous u in "
              "[-1,1]^3 per step -> R^3..R^9 continuum",
        "L2": "anchor continuum",
        "L3F": "anchor continuum x device {0,1}",
        "L3E/L3S": "anchor continuum",
        "L4": "anchor x port x amp [1.5,3.0] x dur [5,20] continuum; the "
              "whole amp domain sits above the apparatus AMP_CAP=1.0, so "
              "the graded protocol is never runnable even in Phase A",
        "L4D": "anchor x port x amp [0.30,0.90] x dur [5,20] continuum; "
               "runnable amps, but the instance is hidden until the world "
               "is closed",
    }
    path = os.path.join(B.AGENTENV, "results",
                        "smoke_blob2v2_bruteforce_note.json")
    json.dump(note, open(path, "w"), indent=1)
    print("brute-force-infeasibility note ->", path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-cache", default=None)
    ap.add_argument("--fast", action="store_true",
                    help="skip the fresh 300tu re-sim inside G-R3")
    a = ap.parse_args()
    asyncio.set_event_loop(asyncio.new_event_loop())
    g_r1()
    g_r2()
    g_r3(full=not a.fast)
    g_r4()
    g_r5()
    g_r6(a.verify_cache)
    brute_force_note()
    print("ALL BLOB ROUND-5 GATES PASS")
