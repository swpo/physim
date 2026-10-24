"""Write a self-contained world.py for a random-screen rule (noise initial condition).

python make_rule_world.py SCREEN.json IDX WORLD_ID [--R 10] [--size 128] [--food JSON] [--noise 0.6]
"""
import argparse
import json
from pathlib import Path

from make_chan_world import TEMPLATE, HERE

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("screen")
    ap.add_argument("idx", type=int)
    ap.add_argument("wid")
    ap.add_argument("--R", type=float, default=10)
    ap.add_argument("--size", type=int, default=128)
    ap.add_argument("--spf", type=int, default=5)
    ap.add_argument("--noise", type=float, default=0.6)
    ap.add_argument("--food", default=None)
    ap.add_argument("--mutation", default=None)
    ap.add_argument("--parent", default=None)
    a = ap.parse_args()
    row = [r for r in json.load(open(a.screen)) if r["i"] == a.idx][0]
    rule = [dict(b=k["b"], m=k["m"], s=k["s"], h=k["h"], r=k["r"], c=[k["c0"], k["c1"]]) for k in row["rule"]]
    rule_src = "[\n" + "".join(f"    {json.dumps(k)},\n" for k in rule) + "]"
    doc = (f"Random multi-channel Lenia rule from screen {Path(a.screen).name} (family '{row['fam']}', rule {a.idx}).\n\n"
           f"{row['C']} channels, {len(rule)} kernels, R={a.R}. Spontaneous: starts from uniform noise in a patch "
           f"covering {a.noise:.0%} of the grid side (no planted creature).")
    out = HERE.parent / "worlds" / a.wid
    out.mkdir(parents=True, exist_ok=True)
    src = TEMPLATE.format(doc=doc, engine=(HERE / "engine_src.py").read_text(), name=a.wid,
                          parent=a.parent or f"screen:{row['fam']}#{a.idx}",
                          mutation=a.mutation or f"random '{row['fam']}' channel/kernel graph",
                          food=json.loads(a.food) if a.food else None, size=a.size, spf=a.spf, dt=0.1,
                          C=row["C"], R=a.R, T=10, rule=rule_src, cells="None", n=0)
    src = src.replace("NOISE = 0.6", f"NOISE = {a.noise}")
    (out / "world.py").write_text(src)
    print(out / "world.py")
