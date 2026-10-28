"""Claim capability measures on one labkit pack dir (frames.npz + metrics.json), using c34's own scripts.
usage: measure.py PACKDIR [dx]  -> prints one JSON line and writes PACKDIR/claim_measures.json"""
import json, re, subprocess, sys
from pathlib import Path

C34 = Path("/home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni")
PY = "/home/user/physim/research/alife/.labenv/bin/python"
d = Path(sys.argv[1])
dx = sys.argv[2] if len(sys.argv) > 2 else "1"
fr = d / "frames.npz"
m = json.loads((d / "metrics.json").read_text())
S = m["summary"]
out = dict(pack=str(d), status=m["status"], wall=round(m["wall_seconds"], 1), frames=S.get("frames"),
           components_final=S.get("components_final"), components_mean=round(S.get("components_mean") or 0, 1),
           persistent_splits=S.get("persistent_splits"), splits=S.get("splits"), max_generation=S.get("max_generation"),
           merge_split_ratio=S.get("merge_split_ratio"), moving_tracks=S.get("moving_tracks"),
           max_body_lengths=None if S.get("max_body_lengths") is None else round(S["max_body_lengths"], 2))


def run(script, *a):
    r = subprocess.run([PY, str(C34 / script), str(fr), *a], capture_output=True, text=True, cwd=str(C34))
    return r.stdout + r.stderr


if m["status"] == "ok" and fr.exists():
    t = run("swimdivide.py", str(C34 / "world.py"))
    g = re.search(r"then divide: (\d+); by rod length >= 3: (\d+)", t)
    out["swim_divide_3bl"] = int(g.group(1)) if g else None
    out["swim_divide_3rod"] = int(g.group(2)) if g else None
    bl = [json.loads(x)["bl_labkit"] for x in re.findall(r"^\s+(\{.*\})$", t, re.M)]
    out["best_bl"] = max(bl) if bl else 0.0
    g = re.search(r"(\d+) end in a split", t)
    out["dividing_tracks"] = int(g.group(1)) if g else None
    t = run("sd_individuals.py", "2,3", dx)
    g = re.search(r"ch2: body-frames (\d+), both >= 1.5: ([\d.na]+), median rim/core ([\d.na]+), median rim/out ([\d.na]+)", t)
    if g:
        out.update(ring_bodyframes=int(g.group(1)), ring_frac=float(g.group(2)), ring_rimcore=float(g.group(3)),
                   ring_rimout=float(g.group(4)))
    g = re.search(r"ch3: inside/outside \(d<=-1 vs 2<=d<=4\) median ([\d.na]+), fraction >= 2: ([\d.na]+)", t)
    if g:
        out.update(cargo_inout=float(g.group(1)), cargo_frac2=float(g.group(2)))
    t = run("inherit.py", str(C34 / "world.py"))
    g = re.search(r"5 frames after birth: n=(\d+), median in/out ([\d.na]+), fraction >= 2: ([\d.na]+)", t)
    if g:
        out.update(daughters_n=int(g.group(1)), daughters_inout=float(g.group(2)), daughters_frac2=float(g.group(3)))
    t = run("speedstats.py", str(C34 / "world.py"))
    v = [float(x) for x in re.findall(r"life phase [\d.]+: mean px/frame ([\d.na]+)", t)]
    out["speed_px_per_frame"] = round(sum(v) / len(v), 3) if v else None
(d / "claim_measures.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
