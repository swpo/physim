"""verify_v03/relock_031.py — 0.3.1 lock refresh: assay_batch.py re-locked
(spawn-pool hardening), _batteryproc.py added. Everything else unchanged."""
import hashlib, json, os, sys, time

PKG = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "..", "blobkit"))
LOCKS = os.path.join(PKG, "_locks.json")
NEW_FILES = ["_batteryproc.py"]
RELOCKED = ["assay_batch.py"]

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
    for rel in NEW_FILES:
        files[rel] = sha(os.path.join(PKG, rel))
    out = dict(locked_at=time.strftime("%Y-%m-%d %H:%M:%S"),
               version="0.3.1", files=dict(sorted(files.items())))
    json.dump(out, open(LOCKS, "w"), indent=1)
    print(f"locked {len(files)} files; relocked {RELOCKED}; added {NEW_FILES}")

if __name__ == "__main__":
    main()
