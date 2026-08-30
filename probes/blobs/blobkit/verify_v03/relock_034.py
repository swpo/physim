"""verify_v03/relock_034.py — 0.3.4: per-lane battery timeout containment.
RE-LOCK _batteryproc.py (SIGALRM guard + timeout->subsample->error ladder +
strided build_tracks), assay_batch.py (finalize via guarded_battery + row
battery_mode flag), data/fleet/pod_worker_batch.py (row battery_mode flag).
Wedge: isl6 battery worker 4h+ ACTIVE+GIL in metrics_v1.build_tracks
(O(frames x blobs^2) greedy matching on a dense long-T world)."""
import hashlib, json, os, sys, time

PKG = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "..", "blobkit"))
LOCKS = os.path.join(PKG, "_locks.json")
RELOCKED = ["_batteryproc.py", "assay_batch.py",
            "data/fleet/pod_worker_batch.py"]

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def main():
    old = json.load(open(LOCKS))
    drift = []
    for rel, want in old["files"].items():
        got = sha(os.path.join(PKG, rel))
        if got != want and rel not in RELOCKED:
            drift.append((rel, want[:12], got[:12]))
    if drift:
        print("UNEXPECTED DRIFT (abort):", drift)
        sys.exit(1)
    files = dict(old["files"])
    for rel in RELOCKED:
        files[rel] = sha(os.path.join(PKG, rel))
    out = dict(locked_at=time.strftime("%Y-%m-%d %H:%M:%S"),
               version="0.3.4", files=dict(sorted(files.items())))
    json.dump(out, open(LOCKS, "w"), indent=1)
    print(f"locked {len(files)} files; relocked {RELOCKED}")

if __name__ == "__main__":
    main()
