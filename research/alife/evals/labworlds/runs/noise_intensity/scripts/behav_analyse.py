"""Write a labkit pack from a simulated record (nsweep.py behav), with labkit's own analysis; run with the lab's
Python (gudhi). For the fed vortices also c53's splits.py sign measures. usage: behav_analyse.py PACK_DIR..."""
import json, pickle, sys
from pathlib import Path
from types import SimpleNamespace
import numpy as np

sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M  # noqa: E402


def signs(W, rec, A):
    mn, comps, tracks, events, lin = A["mn"], A["comps"], A["tracks"], A["events"], A["lineage"]
    RR, rf = A["render"], list(rec["render_f"])

    def sign(tid):
        t = tracks[tid]
        for k, ci in enumerate(t["comp"]):
            f = t["start"] + k
            if f in rf:
                return int(np.sign(RR[rf.index(f), 2][comps[f]["lab"] == ci + 1].sum()))
        return 0
    same = diff = unk = 0
    for e in lin["persistent_splits"]:
        sp, sc = sign(e["parent"]), [sign(c) for c in e["surviving_children"]]
        if sp == 0 or 0 in sc:
            unk += 1
        elif all(x == sp for x in sc):
            same += 1
        else:
            diff += 1
    mg = dict(same=0, opposite=0, unknown=0)
    for ev in events:
        if ev.get("type") != "merge":
            continue
        ss = [sign(p) for p in ev.get("parents", [])]
        mg["unknown" if 0 in ss or len(ss) < 2 else ("same" if len(set(ss)) == 1 else "opposite")] += 1
    return dict(daughters_same_sign=same, daughters_other_sign=diff, sign_unknown=unk, merges=mg)


def main(pack):
    pack = Path(pack)
    d = pickle.loads((pack / "rec.pkl").read_bytes())
    rec, W, spf = d["rec"], SimpleNamespace(META=d["meta"]), d["spf"]
    thr = W.META.get("threshold")
    A = LR.analyze(W, rec, spf, W.META.get("periodic", True), thr, None)
    written = LR.figures(W, rec, A, pack, spf, False)
    warn = LR.facts(W, rec, A, pack, d["seed"], spf, f"nsweep behav {d['world']} level {d['level']}", written)
    s = dict(A["summary"])
    lin = A["lineage"]
    s["splits_after_t"] = {str(t): sum(1 for e in lin["persistent_splits"] if e["frame"] * A["dt_frame"] > t)
                           for t in (100, 300, 1000, 3000)}
    if d["world"] == "fv":
        s["signs"] = signs(W, rec, A)
    out = dict(world=d["world"], level=d["level"], seed=d["seed"], status=rec["status"], cpu_s=d["cpu_s"],
               warnings=warn, summary=s, noisy_spec=d["noisy_spec"], series=A["series"]["n_comp"])
    (pack / "summary.json").write_text(json.dumps(LR._strict(out), indent=1, default=str))
    # frames.npz is not kept (disk is shared and nearly full); the pack regenerates from world, level and seed
    (pack / "rec.pkl").unlink()
    keys = ("components_final", "persistent_tracks", "splits", "persistent_splits", "max_generation", "merges",
            "nucleations", "splits_after_t", "signs")
    print(pack.name, rec["status"], json.dumps({k: s.get(k) for k in keys}), flush=True)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
