"""tools/extract_worlds.py — one-time extraction of every registry genome
from the SOURCE TREE into blobkit/blobkit/data/worlds/<name>.json.

Run from anywhere on a machine with the physim tree:
    python3 tools/extract_worlds.py [--tree /path/to/physim/probes/blobs]

Ground truths (m0..mv3) are built by the CURRENT complexity/worlds.py builders
(incl. machinev3.lib.build_world for mv3) and dumped through genome_json ->
json round-trip (exactly the gpu/data/gt_worlds.json freeze convention).
Champions/parts are byte-decoded from their canonical JSON files (see PROV).
"""
import argparse, copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
OUT = os.path.join(KIT, "blobkit", "data", "worlds")

DEFAULT_TREE = "/Users/spoho/Documents/prime/test/physim/probes/blobs"

# champions + parts: canonical source files, relative to the blobs tree
PROV = {
    "ds3_014":      "l0/complexity/genomes_v2/ds3_014.json",
    "ds3_017":      "l0/complexity/genomes_v2/ds3_017.json",
    "ds6_000":      "l0/complexity/genomes_v2/ds6_000.json",
    "g0_jit_11":    "l0/deepsearch/deploy/seeds/g0_jit_11.json",
    "engine_10748": "l0/stage3/engine_10748.json",
    "rail_111_17":  "l0/deepsearch/seeds/rail_111_17.json",
    "s2_128_26":    "l0/deepsearch/seeds/s2_128_26.json",
    "s2_118_41":    "l0/deepsearch/seeds/s2_118_41.json",
}
GT = ["m0", "m4", "xv", "bf", "pred", "coex", "mv3"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", default=DEFAULT_TREE)
    a = ap.parse_args()
    blobs = os.path.abspath(a.tree)
    os.makedirs(OUT, exist_ok=True)

    sys.path.insert(0, os.path.join(blobs, "l0", "complexity"))
    sys.path.insert(0, os.path.join(blobs, "l0", "stage2", "lib"))
    import worlds as W          # the CURRENT tree worlds.py
    import genome as G

    manifest = {}
    for n in GT:
        g = json.loads(json.dumps(G.genome_json(W.WORLDS[n]())))
        p = os.path.join(OUT, n + ".json")
        with open(p, "w") as f:
            json.dump(g, f, indent=1, sort_keys=True)
        manifest[n] = dict(source="built:complexity/worlds.py:" + n,
                           id=g.get("id"))
        print("built", n, "->", p)

    for n, rel in PROV.items():
        src = os.path.join(blobs, rel)
        g = json.load(open(src))
        p = os.path.join(OUT, n + ".json")
        with open(p, "w") as f:
            json.dump(g, f, indent=1, sort_keys=True)
        manifest[n] = dict(source=rel, id=g.get("id"))
        print("copied", n, "<-", rel)

    with open(os.path.join(OUT, "_extraction.json"), "w") as f:
        json.dump(dict(kicks=W.KICKS, worlds=manifest), f, indent=1,
                  sort_keys=True)
    print("done:", len(GT) + len(PROV), "worlds ->", OUT)


if __name__ == "__main__":
    main()
