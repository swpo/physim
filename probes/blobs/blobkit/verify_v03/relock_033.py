"""verify_v03/relock_033.py — 0.3.3: ADD soup/devrec_proto.py +
soup/asyncapply_proto.py (gated record-path prototypes, perf thread 2.18x
claim row); RE-LOCK data/fleet/pod_worker_batch.py (island_config
record_mode/apply_mode install hook) + deploy_tools.py (template defaults
record_mode=device, apply_mode=async for gpu_batch bundles)."""
import hashlib, json, os, sys, time

PKG = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "..", "blobkit"))
LOCKS = os.path.join(PKG, "_locks.json")
NEW = ["soup/devrec_proto.py", "soup/asyncapply_proto.py"]
RELOCKED = ["data/fleet/pod_worker_batch.py", "deploy_tools.py"]

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
    for rel in RELOCKED + NEW:
        files[rel] = sha(os.path.join(PKG, rel))
    out = dict(locked_at=time.strftime("%Y-%m-%d %H:%M:%S"),
               version="0.3.3", files=dict(sorted(files.items())))
    json.dump(out, open(LOCKS, "w"), indent=1)
    print(f"locked {len(files)} files; new {NEW}; relocked {RELOCKED}")

if __name__ == "__main__":
    main()
