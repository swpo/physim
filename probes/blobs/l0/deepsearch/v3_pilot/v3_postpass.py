"""v3_postpass.py — pilot overlay: v3 rescoring of batch rows (C9 partial mode).
s9 needs dense full-field snaps (absent in batch npz) -> fsnaps=None, metrics_v3
computes available factors (t9/e9/r9) and flags partial. interest_v3 = 0.75*iv2+25*C9.
Called by pod_worker_batch after finalize with (row, rec).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metrics_v3 as MV3

def rescore_row(row, rec, v2_out=None):
    try:
        import genome as GG
        g = row.get("genome")
        if isinstance(g, (str, dict)):
            g = GG.genome_load(g) if isinstance(g, str) else g
        out = MV3.c9_spatial_economy(rec, genome=g, fsnaps=None, v2_out=None)
        row["C9"] = float(out.get("C9", 0.0))
        row["C9_factors"] = out.get("factors")
        row["spatial_class"] = out.get("spatial_class", "mixed")
        row["c9_partial"] = bool(out.get("partial", True))
        iv2 = float(row.get("interest", 0.0))
        row["interest_v2"] = iv2
        # blend via metrics_v3.W9 (single source of truth; 0.25 pilot v1,
        # 0.40 for the gens-8-12 continuation)
        row["interest"] = (1.0 - MV3.W9) * iv2 + MV3.W9 * 100.0 * row["C9"]
    except Exception as e:
        row["c9_error"] = str(e)[:120]
    return row
