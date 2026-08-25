"""tests/gate_anchor.py — Gate ANCHOR: bond statics incl. the A5-dt trap.
A1: A4s pair dt=0.02  T=2000 -> d* = 15.40 +- 0.5%, 2 blobs throughout.
A2: A5  pair dt=0.005 T=3000 -> d* = 15.70 +- 0.5%.
A3: A5  pair dt=0.02  T<=4000 -> REPLICATES (the artifact must reproduce).
GPU f32 (production dtype). Writes results/gate_anchor.json.
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..")))
from blobgpu.anchors import run_pair

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "results", "gate_anchor.json"))


def main():
    import jax
    rows, fails = [], []

    r = run_pair(2.5, 1.6, "stamp_A4_dx05.npz", dt=0.02, T=2000.0, dtype="f32")
    ok = (r["status"] == "ok" and r["d_final"] is not None
          and abs(r["d_final"] - 15.40) <= 0.005 * 15.40)
    rows.append(dict(gate="A1_A4s_dt02", status=r["status"],
                     d_final=r["d_final"], target=15.40,
                     verdict="PASS" if ok else "FAIL"))
    print(f"A1 A4s dt=0.02: {r['status']} d*={r['d_final']} [{rows[-1]['verdict']}]",
          flush=True)
    if not ok:
        fails.append("A1")

    r = run_pair(2.5, 2.0, "stamp_P7s_dx05.npz", dt=0.005, T=3000.0, dtype="f32")
    ok = (r["status"] == "ok" and r["d_final"] is not None
          and abs(r["d_final"] - 15.70) <= 0.005 * 15.70)
    rows.append(dict(gate="A2_A5_dt005", status=r["status"],
                     d_final=r["d_final"], target=15.70,
                     verdict="PASS" if ok else "FAIL"))
    print(f"A2 A5 dt=0.005: {r['status']} d*={r['d_final']} [{rows[-1]['verdict']}]",
          flush=True)
    if not ok:
        fails.append("A2")

    r = run_pair(2.5, 2.0, "stamp_P7s_dx05.npz", dt=0.02, T=4000.0, dtype="f32")
    ok = (r["status"] == "replicated")
    rows.append(dict(gate="A3_A5_dt02_trap", status=r["status"],
                     t_repl=(r["t"][-1] if ok else None),
                     sep_tail=[s for s in r["sep"][-6:]],
                     verdict="PASS" if ok else "FAIL"))
    print(f"A3 A5 dt=0.02 trap: {r['status']} at t={r['t'][-1]} "
          f"[{rows[-1]['verdict']}]", flush=True)
    if not ok:
        fails.append("A3")

    out = dict(kind="gate_anchor", backend=str(jax.devices()[0]),
               ts=time.strftime("%Y-%m-%d %H:%M:%S"), rows=rows,
               verdict="PASS" if not fails else f"FAIL {fails}")
    hist = json.load(open(OUT)) if os.path.exists(OUT) else []
    hist.append(out)
    json.dump(hist, open(OUT, "w"), indent=1)
    print("GATE-ANCHOR:", out["verdict"])
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
