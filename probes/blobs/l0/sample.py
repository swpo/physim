"""sample.py — L0 stage-1 LOCAL sampling run.

Usage: sample.py <n_candidates> [strategy] [seed0] [tag]
  strategy in {uniform, jitter, mix} (mix = alternate). Appends one record per
  candidate to results.json (SAVE-AS-YOU-GO), updates archive.json atomically.

Pipeline per candidate: sampler -> validate -> G0 funnel (all margins logged) ->
if funnel pass: assay battery (A1 all acts; A2/A3 on first persisting act) ->
descriptor -> MAP-Elites archive (exemplar = most negative g0a margin).
Timing per stage recorded (yield-curve deliverable).
"""
import sys, os, json, time
import fcntl
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "lib"))
import genome as G
import funnel as FU
import assays as AS
import sampler as SA

ARCHIVE = os.path.join(BASE, "archive.json")


def archive_update(desc, margin, genome, cand_id):
    """Atomic MAP-Elites insert; exemplar = most negative margin."""
    key = "|".join(map(str, desc))
    lockp = ARCHIVE + ".lock"
    with open(lockp, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            with open(ARCHIVE) as f:
                arch = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            arch = {}
        cell = arch.get(key)
        new_cell = dict(margin=margin, genome=G.genome_json(genome),
                        cand=cand_id, count=(cell["count"] + 1 if cell else 1))
        if cell is None or margin < cell["margin"]:
            pass                    # replace exemplar
        else:
            new_cell["margin"] = cell["margin"]
            new_cell["genome"] = cell["genome"]
            new_cell["cand"] = cell["cand"]
        arch[key] = new_cell
        tmp = ARCHIVE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(arch, f)
        os.replace(tmp, ARCHIVE)
    return key


def one_candidate(rng, strategy, cand_id, tag):
    rec = dict(kind="candidate", cand=cand_id, strategy=strategy, tag=tag)
    t0 = time.time()
    if strategy == "uniform":
        g, why = SA.sample_uniform(rng)
    else:
        g, why = SA.sample_jitter(rng)
    rec["gen_s"] = round(time.time() - t0, 4)
    rec["genome"] = G.genome_json(g)
    if why in ("no_real_root", "root_lost"):
        rec["stage"] = "fail_g0b"
        rec["why"] = why
        return rec
    probs = G.validate(g)
    if probs:
        rec["stage"] = "invalid"
        rec["why"] = probs
        return rec
    t0 = time.time()
    fr = FU.funnel(g)
    rec["funnel_s"] = round(time.time() - t0, 4)
    rec.update({k: fr[k] for k in fr if k != "stage"})
    rec["stage"] = fr["stage"]
    if why == "no_stable_root":
        rec["why"] = why            # documented: best root logged, g0a will fail
    if fr["stage"] != "pass":
        return rec
    t0 = time.time()
    desc, recs = AS.battery(g, fr)
    rec["assay_s"] = round(time.time() - t0, 2)
    rec["a1"] = recs["a1"]
    rec["a2"] = recs["a2"]
    rec["a3"] = recs["a3"]
    rec["desc"] = list(map(str, desc))
    rec["stage"] = "assayed"
    key = archive_update(desc, fr["g0a_margin"], g, cand_id)
    rec["cell"] = key
    return rec


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    strategy = sys.argv[2] if len(sys.argv) > 2 else "mix"
    seed0 = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    tag = sys.argv[4] if len(sys.argv) > 4 else "s1"
    for j in range(n):
        seed = seed0 + j
        rng = np.random.default_rng(seed)
        strat = strategy if strategy != "mix" else ("uniform" if j % 2 == 0 else "jitter")
        cand_id = f"{tag}_{strat[:3]}_{seed}"
        t0 = time.time()
        try:
            rec = one_candidate(rng, strat, cand_id, tag)
        except Exception as e:
            rec = dict(kind="candidate", cand=cand_id, strategy=strat, tag=tag,
                       stage="error", why=repr(e))
        rec["total_s"] = round(time.time() - t0, 2)
        G.append_result(rec)
        print(f"{cand_id} {rec['stage']} {rec.get('desc','')} {rec['total_s']}s",
              flush=True)


if __name__ == "__main__":
    main()
