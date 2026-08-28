"""verify_v03/relock.py — regenerate _locks.json for 0.3.0.
Adds assay_batch.py + data/fleet/pod_worker_batch.py + data/fleet/pod_gen_batch.py;
re-locks deploy_tools.py (0.3 edits). All other hashes must be UNCHANGED
(asserted; any other drift aborts)."""
import hashlib, json, os, sys, time

PKG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "blobkit")
PKG = os.path.abspath(PKG)
LOCKS = os.path.join(PKG, "_locks.json")

NEW_FILES = ["assay_batch.py", "data/fleet/pod_worker_batch.py",
             "data/fleet/pod_gen_batch.py"]
RELOCKED = ["deploy_tools.py",          # 0.3 edits (gpu_batch emission)
            "data/fleet/pod_lib.py"]    # F3: gpu_batch->gpu single-world map
ALSO = ["__init__.py"]                  # version bump — NOT in lock table
                                        # (it does the checking), just listed

def sha(p):
    h = hashlib.sha256()
    h.update(open(p, "rb").read())
    return h.hexdigest()

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
               version="0.3.0", files=dict(sorted(files.items())))
    json.dump(out, open(LOCKS, "w"), indent=1)
    print(f"locked {len(files)} files (was {len(old['files'])}); "
          f"relocked {RELOCKED}; added {NEW_FILES}")

if __name__ == "__main__":
    main()
