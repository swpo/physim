"""aggregate_v2.py — collect assay_v2 rows from results.json into a table."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))

def rows(path=None):
    res = json.load(open(path or os.path.join(HERE, "results.json")))
    return [r for r in res if r.get("kind") == "assay_v2"]

def latest(rs):
    """Keep latest row per (tag, seed)."""
    out = {}
    for r in rs:
        out[(r["tag"], r["seed"])] = r
    return out

def table(sel=None):
    rs = latest(rows())
    print(f"{'tag':22s} {'s':>2s} {'int':>6s} {'T':>6s} {'why':10s} "
          f"{'wall':>6s} {'C1':>5s} {'C5':>5s} {'C6':>5s} {'C8':>5s} "
          f"{'nsi':>4s} {'stg':>3s} {'box':>3s}")
    for (tag, seed), r in sorted(rs.items()):
        if sel and sel not in tag:
            continue
        C = r["battery"]["C"]; s = r.get("summary", {})
        fl = r["battery"].get("flags") or {}
        print(f"{tag:22s} {seed:2d} {r['battery']['interest']:6.1f} "
              f"{r['T']:6.0f} {r['horizon']['why_stopped']:10s} "
              f"{r.get('wall_total', 0):6.0f} {C['C1_popdyn']:5.2f} "
              f"{C['C5_memory']:5.2f} {C['C6_ecology']:5.2f} "
              f"{C['C8_succession']:5.2f} "
              f"{(s.get('d7') or {}).get('nsi', -1):4.1f} "
              f"{(s.get('d1') or {}).get('n_stages', -1):3d} "
              f"{str(fl.get('box_limit'))[:3]:>3s}")

if __name__ == "__main__":
    table(sys.argv[1] if len(sys.argv) > 1 else None)
