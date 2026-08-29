"""0.3.3 V1a smoke: 4-lane batch identity, stock vs devrec(async) vs
asyncapply — from the INSTALLED wheel, CPU-JAX (devrec kernel runs on
CPU backend: same code path, no GPU required)."""
import os
os.environ["JAX_PLATFORMS"] = "cpu"
import json
import numpy as np
from blobkit import worlds as W
from blobkit.soup import sim_gpu as SG


def run(mode):
    jobs = [(W.load(nm), 1 + i) for i, nm in
            enumerate(["m0", "pred", "m0", "pred"])]
    master = SG.init_soup_gpu_batch(jobs, L=64.0, dtype="f32")
    if mode == "devrec":
        from blobkit.soup import devrec_proto as DR
        DR.install(async_apply=True)
    elif mode == "async":
        from blobkit.soup import asyncapply_proto as AA
        AA.install()
    try:
        SG.advance_gpu_batch(master, 500.0)
    finally:
        if mode == "devrec":
            DR.uninstall()
        elif mode == "async":
            AA.uninstall(shutdown=False)
    return master["worlds"]


def cmp_lanes(A, B, tol=1e-12):
    ok, worst = True, 0.0
    for Sa, Sb in zip(A, B):
        ok &= (Sa["ts"] == Sb["ts"] and Sa["cts"] == Sb["cts"]
               and Sa["status"] == Sb["status"]
               and Sa["t_step"] == Sb["t_step"]
               and Sa["patches"] == Sb["patches"]
               and str(Sa["orgs"]) == str(Sb["orgs"])
               and sorted(Sa["snaps"]) == sorted(Sb["snaps"]))
        for a_i in Sa["blobs"]:
            for bla, blb in zip(Sa["blobs"][a_i], Sb["blobs"][a_i]):
                if len(bla) != len(blb):
                    ok = False
                    continue
                for ra, rb in zip(sorted(bla), sorted(blb)):
                    if ra[2] != rb[2] or ra[3] != rb[3]:
                        ok = False
                    for q in (0, 1):
                        err = abs(ra[q] - rb[q]) / max(abs(ra[q]), 1e-9)
                        worst = max(worst, err)
                        ok &= err <= tol
        for a_i in Sa["mass"]:
            for ma, mb in zip(Sa["mass"][a_i], Sb["mass"][a_i]):
                err = abs(ma - mb) / max(abs(ma), 1e-9)
                worst = max(worst, err)
                ok &= err <= tol
    return ok, worst


def main():
    import blobkit
    print("blobkit", blobkit.__version__, "locks",
          blobkit.verify_locks()["ok"])
    A = run("stock")
    B = run("async")
    okB, wB = cmp_lanes(A, B, tol=0.0)     # async must be BITWISE
    print(f"asyncapply vs stock: {'PASS' if okB and wB == 0 else 'FAIL'} "
          f"(worst {wB:.2e}, bitwise required)")
    C = run("devrec")
    okC, wC = cmp_lanes(A, C, tol=1e-12)
    from blobkit.soup import devrec_proto as DR
    st = DR.stats()
    print(f"devrec+async vs stock: {'PASS' if okC else 'FAIL'} "
          f"(worst {wC:.2e} tol 1e-12; dev points {st['points_dev']}, "
          f"fallbacks {st['lanes_fallback']})")
    print("V1a_033_SMOKE:", "PASS" if (okB and wB == 0 and okC) else "FAIL")


if __name__ == "__main__":
    main()
