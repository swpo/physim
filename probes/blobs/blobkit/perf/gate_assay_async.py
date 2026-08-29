"""gate_assay_async.py — t2-level identity: run_assay_batch STOCK vs
ASYNCAPPLY (multi-rung, criteria decisions + battery outputs must match).
MUST be run as a script from perf/ (spawn workers re-import __main__)."""
import os
os.environ["JAX_PLATFORMS"] = os.environ.get("JAX_PLATFORMS", "cpu")
import json


def run(proto):
    from blobkit import worlds as W
    from blobkit.assay_batch import run_assay_batch
    jobs = [dict(genome=W.load("m0"), seed=1, t0=1250.0, cap=2500.0),
            dict(genome=W.load("pred"), seed=2, t0=1250.0, cap=2500.0)]
    if proto:
        import proto_asyncapply as AA
        AA.install()
    try:
        outs = run_assay_batch(jobs, L=64.0, t0=1250.0, cap=2500.0,
                               results_path=None, verbose=False,
                               battery_procs=2, B_pad=(1, 2, 4))
    finally:
        if proto:
            AA.uninstall()
    return outs


def main():
    A = run(False)
    B = run(True)
    ok = True
    for i, (a, b) in enumerate(zip(A, B)):
        wa = dict(a["horizon"]); wb = dict(b["horizon"])
        wa.pop("wall_total"); wb.pop("wall_total")
        same = (a["interest"] == b["interest"]
                and json.dumps(a["C"], sort_keys=True, default=str)
                    == json.dumps(b["C"], sort_keys=True, default=str)
                and a["flags"] == b["flags"]
                and json.dumps(wa, sort_keys=True, default=str)
                    == json.dumps(wb, sort_keys=True, default=str))
        ok &= same
        print(f"lane{i}: {'PASS' if same else 'FAIL'} "
              f"interest {a['interest']}=={b['interest']} "
              f"T_used {wa['T_used']}=={wb['T_used']} "
              f"why {wa['why_stopped']}=={wb['why_stopped']} "
              f"n_ext {wa['n_extensions']}=={wb['n_extensions']}")
    print("assay-level identity:", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    main()
