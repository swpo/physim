"""merge_islands.py — controller-side island merge (runs on the laptop or any
pod). UNION archives by cell-max, concat+dedup results, redistribute the union
back to islands.

Usage:
  python3 merge_islands.py union out_i0/archive.json out_i1/archive.json ... \
      --out union_archive.json [--results out_i0/results.json ...]
  python3 merge_islands.py push union_archive.json out_i0 out_i1 ...

Union rules:
  - key = cell string; winner = max interest. LOSERS with DIFFERENT ghash are
    retained in cell history (capped 8) so lineage survives.
  - vtags/provenance ride the winning genome verbatim (never rewritten;
    minted-uid namespace is island-scoped: v<island>_<gen>_<k> — collisions
    impossible by construction).
  - seed2/seed3 flags ride the winner. count = sum of counts.
  - results concat: dedup on (island, cand, phase); ghash kept per row.
Push rule: pod archives are REPLACED by the union (breeding pool refresh);
per-island results/state stay local.
"""
import argparse, json, os, sys


def load(p):
    with open(p) as f:
        return json.load(f)


def union(archives):
    out = {}
    for src, arch in archives:
        for key, cell in arch.items():
            cell = dict(cell)
            cell.setdefault("src_island_file", src)
            cur = out.get(key)
            if cur is None:
                out[key] = cell
                continue
            a, b = (cell, cur) if cell["interest"] > cur["interest"] else (cur, cell)
            hist = list(a.get("history", []))
            if b.get("ghash") and b.get("ghash") != a.get("ghash"):
                hist.append(dict(cand=b["cand"], interest=b["interest"],
                                 gen=b.get("gen"), island=b.get("island"),
                                 ghash=b.get("ghash")))
            a = dict(a)
            a["history"] = hist[-8:]
            a["count"] = (cur.get("count", 1) or 1) + (cell.get("count", 1) or 1)
            fg = [x.get("first_gen") for x in (cur, cell)
                  if x.get("first_gen") is not None]
            if fg:
                a["first_gen"] = min(fg)
            out[key] = a
    return out


def concat_results(paths):
    seen, rows = set(), []
    for p in paths:
        for r in load(p):
            k = (r.get("island"), r.get("cand"), r.get("phase"))
            if k in seen:
                continue
            seen.add(k)
            rows.append(r)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["union", "push"])
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", default="union_archive.json")
    ap.add_argument("--results", nargs="*", default=[])
    a = ap.parse_args()
    if a.cmd == "union":
        archives = [(p, load(p)) for p in a.paths]
        u = union(archives)
        json.dump(u, open(a.out, "w"))
        n_mint = sum(1 for v in u.values() if v.get("minted"))
        n_blk = sum(1 for v in u.values()
                    if v.get("seed2_ok") and v.get("seed3_ok"))
        print(f"union: {len(u)} cells from {len(archives)} islands "
              f"({n_mint} minted, {n_blk} block-eligible) -> {a.out}")
        if a.results:
            rows = concat_results(a.results)
            rp = os.path.splitext(a.out)[0] + "_results.json"
            json.dump(rows, open(rp, "w"))
            print(f"results concat: {len(rows)} rows -> {rp}")
    else:
        u = load(a.paths[0])
        for d in a.paths[1:]:
            tgt = os.path.join(d, "archive.json")
            json.dump(u, open(tgt, "w"))
            print(f"pushed union -> {tgt}")


if __name__ == "__main__":
    main()
