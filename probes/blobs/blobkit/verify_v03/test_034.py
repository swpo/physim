"""test_034.py — 0.3.4 battery-timeout containment gates (installed wheel).

T1 IDENTITY: normal worlds under the default guard == 0.3.3 reference
   (subsample must NEVER engage below timeout; ref_033.json captured on
   the 0.3.3 wheel pre-upgrade).
T2 LADDER: synthetic dense record (many blobs x many frames, build_tracks
   >> timeout) -> timeout fires -> subsampled retry SCORES the lane with
   battery_mode="subsampled".
T3 DOUBLE-TIMEOUT: absurdly low timeout -> battery_timeout error, worker
   returns contained (out=None, err set), process survives.
T4 WORKER PATH: battery_worker (the pool entry) on normal input returns
   (out, crit, None) identical decision inputs vs direct battery.
"""
import json, os, sys, time
import numpy as np

import blobkit
from blobkit import worlds as W
from blobkit import metrics_v2 as MV2
from blobkit import _batteryproc as BP
from blobkit.soup import sim_cpu as SC
from blobkit.assay_v2 import horizon_criteria

REF = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "ref_033.json")))


def battery_pair(name, T=500.0):
    g = W.load(name)
    S = SC.init_soup(g, L=64.0, seed=1, workers=2)
    SC.advance(S, T)
    rec = SC.snapshot_rec(S)
    return rec, g


def t1_identity():
    ok = True
    for name in ("m0", "pred"):
        rec, g = battery_pair(name)
        out, err = BP.guarded_battery(rec, g)
        assert err is None, err
        crit = horizon_criteria(rec, g, D=out["D"])
        ref = REF[name]
        same = (out["interest"] == ref["interest"]
                and out["C"] == ref["C"]
                and out["flags"] == ref["flags"]
                and {k: crit[k] for k in ("a_mem", "b_org", "c_acf")}
                    == ref["crit"]
                and "battery_mode" not in out)
        ok &= same
        print(f"[T1 {name}] {'PASS' if same else 'FAIL'} "
              f"interest={out['interest']} (ref {ref['interest']}) "
              f"mode={'full' if 'battery_mode' not in out else out['battery_mode']}")
    return ok


def dense_record(n_frames=400, n_blobs=260, L=128.0, seed=0):
    """Synthetic record: n_blobs jittering blobs per frame, one act.
    build_tracks cost ~ frames x blobs^2 x numpy-min_image => minutes."""
    rng = np.random.default_rng(seed)
    base = rng.uniform(0, L, (n_blobs, 2))
    blobs0 = []
    for k in range(n_frames):
        pos = (base + rng.normal(0, 0.8, base.shape)) % L
        blobs0.append([[float(y), float(x), 4.0, 1.2] for y, x in pos])
    ts = np.arange(1, n_frames + 1) * 5.0
    cts = ts[::5]
    na = 1
    rec = dict(world="dense_synth", seed=seed, L=L, T=float(ts[-1]),
               dtype="f32", status="ok", wall_s=0.0, na=na, nc=2,
               memch=[], thr=[0.6], thr_lo=[0.45], taus=[8.0, 40.0],
               t=ts, blobs={0: blobs0},
               mass={0: [float(n_blobs) * 4.0] * n_frames},
               ct=cts,
               patches={0: [dict(n=n_blobs, sizes=[4.0] * n_blobs,
                                 cover=0.2)] * len(cts)},
               orgs={0: [dict(n=n_blobs, sizes=[4.0] * n_blobs, cover=0.2,
                              spans=[2.0, 2.0, 2.0])] * len(cts)},
               memf={}, snaps={}, species_seeded=[0], seed_pts=[])
    return rec


def t2_ladder():
    rec = dense_record()
    g = W.load("m0")
    # sanity: full build_tracks on this record would take minutes; timeout
    # at 20s forces the ladder fast. Stride 4 cuts frames 4x => ~16x less
    # matching work per frame-pair (and fewer pairs).
    os.environ["BLOBKIT_BATTERY_TIMEOUT"] = "20"
    os.environ["BLOBKIT_BATTERY_SUBSAMPLE"] = "4"
    t0 = time.time()
    out, err = BP.guarded_battery(rec, g)
    wall = time.time() - t0
    okA = err is None and out is not None \
        and out.get("battery_mode") == "subsampled" \
        and np.isfinite(out.get("interest", np.nan))
    print(f"[T2 ladder] {'PASS' if okA else 'FAIL'} wall={wall:.0f}s "
          f"mode={out.get('battery_mode') if out else None} "
          f"interest={out.get('interest') if out else None} err={err}")
    # T3: absurd timeout -> double-timeout containment
    os.environ["BLOBKIT_BATTERY_TIMEOUT"] = "2"
    t0 = time.time()
    out2, err2 = BP.guarded_battery(dense_record(n_frames=600, n_blobs=380),
                                    g)
    wall2 = time.time() - t0
    okB = out2 is None and err2 is not None and "battery_timeout" in err2 \
        and wall2 < 30
    print(f"[T3 double-timeout] {'PASS' if okB else 'FAIL'} wall={wall2:.0f}s "
          f"err={err2}")
    os.environ["BLOBKIT_BATTERY_TIMEOUT"] = "300"
    return okA and okB


def t4_worker():
    rec, g = battery_pair("pred")
    out, crit, err = BP.battery_worker((rec, g))
    ref = REF["pred"]
    ok = (err is None and out["interest"] == ref["interest"]
          and {k: crit[k] for k in ("a_mem", "b_org", "c_acf")}
              == ref["crit"])
    print(f"[T4 worker] {'PASS' if ok else 'FAIL'}")
    return ok


def main():
    print("blobkit", blobkit.__version__, "locks",
          blobkit.verify_locks()["ok"])
    r1 = t1_identity()
    r2 = t2_ladder()
    r4 = t4_worker()
    print("V1a_034:", "PASS" if (r1 and r2 and r4) else "FAIL")


if __name__ == "__main__":
    main()
