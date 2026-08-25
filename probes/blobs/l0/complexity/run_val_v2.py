"""run_val_v2.py — validation battery driver (waves; called with a wave name).
Runs assay_v2 on GT worlds / champion genomes, saves npz + results rows.
Usage: python3 run_val_v2.py <spec> where spec lines = world:seed[:workers]
"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))

SPECS = dict(
    A=[("m0", 1), ("m0", 2), ("m4", 1), ("m4", 2), ("xv", 1), ("xv", 2)],
    B=[("bf", 1), ("bf", 2), ("coex", 1), ("coex", 2), ("mv3", 1), ("mv3", 2)],
    C=[("pred", 1), ("pred", 2),
       ("genomes_v2/ds6_000.json", 1), ("genomes_v2/ds6_000.json", 2)],
    D=[("genomes_v2/ds3_014.json", 1), ("genomes_v2/ds3_014.json", 2),
       ("genomes_v2/ds3_017.json", 1), ("genomes_v2/ds3_017.json", 2)],
    S3=[("m0", 3), ("m4", 3), ("xv", 3), ("bf", 3), ("coex", 3),
        ("mv3", 3), ("pred", 3)],
    DS3=[("genomes_v2/ds3_014.json", 3), ("genomes_v2/ds3_017.json", 3),
         ("genomes_v2/ds6_000.json", 3)],
)


def tag_of(w):
    if w.endswith(".json"):
        return os.path.basename(w)[:-5]
    return w


def main():
    wave = sys.argv[1]
    procs = []
    for w, seed in SPECS[wave]:
        tag = tag_of(w)
        npz = os.path.join(HERE, "runs_v2", f"v2_{tag}_s{seed}.npz")
        log = os.path.join(HERE, "logs_v2", f"val_{tag}_s{seed}.log")
        cmd = ["python3", os.path.join(HERE, "assay_v2.py"), w,
               "--seed", str(seed), "--workers", "2",
               "--tag", f"{tag}", "--save-npz", npz]
        procs.append((tag, seed, subprocess.Popen(
            cmd, stdout=open(log, "w"), stderr=subprocess.STDOUT, cwd=HERE)))
    for tag, seed, p in procs:
        rc = p.wait()
        print(f"{tag} s{seed} rc={rc}", flush=True)


if __name__ == "__main__":
    main()
