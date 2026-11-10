"""fetch_job -- copy a finished GPU job's files from origin/gpu-jobs into a scratch folder and results/<name>/.

    python -B fetch_job.py JOB_ID NAME SCRATCH_DIR [--repo /home/user/physim]

SCRATCH_DIR/NAME gets every file of jobs/JOB_ID/out (arrays included; not committed) plus status.json;
results/NAME gets status.json and the small JSON / text outputs (under 2 MB each). JSON outputs that hold pilot
truths, Lab episodes, posteriors or exam answers get the entry PILOT_NEVER_REUSE_AS_EXAM when the job did not
write it (the Mac's review of r5-vortexexam-003, point 2): a dict gets the key, a list of dicts gets it in every
element. Nothing else in the copies is changed; the originals stay on the gpu-jobs branch.
This is an analysis helper (it calls git); it is never part of a GPU job.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = "PILOT_NEVER_REUSE_AS_EXAM"
SMALL = 2_000_000


def git(repo, *a, binary=False):
    r = subprocess.run(["git", "-C", repo, *a], capture_output=True)
    if r.returncode:
        raise RuntimeError(f"git {' '.join(a)}: {r.stderr.decode()[:300]}")
    return r.stdout if binary else r.stdout.decode()


def mark(obj):
    if isinstance(obj, dict):
        return obj if obj.get(MARK) is True else {MARK: True, **obj}
    if isinstance(obj, list):
        return [mark(o) if isinstance(o, dict) else o for o in obj]
    return obj


def main():
    job, name, scratch = sys.argv[1:4]
    repo = sys.argv[sys.argv.index("--repo") + 1] if "--repo" in sys.argv else "/home/user/physim"
    ref = "origin/gpu-jobs"
    base = f"jobs/{job}"
    files = [f for f in git(repo, "ls-tree", "-r", "--name-only", ref, base).split("\n") if f]
    dst, res = os.path.join(scratch, name), os.path.join(HERE, "results", name)
    os.makedirs(dst, exist_ok=True)
    os.makedirs(res, exist_ok=True)
    listing = []
    for f in files:
        rel = f[len(base) + 1:]
        if not (rel == "status.json" or rel == "manifest.json" or rel.startswith("out/")):
            continue
        blob = git(repo, "show", f"{ref}:{f}", binary=True)
        out_rel = rel[4:] if rel.startswith("out/") else rel
        p = os.path.join(dst, out_rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(blob)
        listing.append([out_rel, len(blob)])
        if len(blob) <= SMALL and out_rel.endswith((".json", ".txt")):
            q = os.path.join(res, out_rel)
            os.makedirs(os.path.dirname(q), exist_ok=True)
            if out_rel.endswith(".json") and out_rel not in ("status.json", "manifest.json"):
                json.dump(mark(json.loads(blob)), open(q, "w"), indent=1)
            else:
                with open(q, "wb") as fh:
                    fh.write(blob)
    json.dump({MARK: True, "job_id": job, "gpu_jobs_commit": git(repo, "rev-parse", ref).strip(),
               "files_bytes": listing,
               "note": "files of origin/gpu-jobs:jobs/<job_id>/out; the JSON copies in this folder carry the pilot "
                       "marker (added by fetch_job.py where the job had not written it); arrays are not copied here"},
              open(os.path.join(res, "FILES.json"), "w"), indent=1)
    print(f"{job}: {len(listing)} files, {sum(n for _, n in listing) / 2 ** 20:.1f} MB -> {dst}; small files -> {res}")


if __name__ == "__main__":
    main()
