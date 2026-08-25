"""ds2_lib.py — deepsearch v2 shared layer (phase 6).

Differences vs v1 ds_lib.py (which stays untouched):
  - results_v2.json / archive_v2.json / runs2/ / jobs2/ (no v1 collisions).
  - config ds2_config.json: metrics backend "v1"(fallback)|"v2"(locked assay),
    adaptive-T ladder, caps (MAX_FIELDS=14).
  - battery adapter: uses assay_v2 when locked; else metrics_v1 fixed screen
    with a LOCAL adaptive-T extend rule (late-succession detector, T3 lesson:
    ds3_014 needed 12000tu; the 2500tu screen misses late booms).
  - cell key v2: assay_v2's key when present; fallback = v1 key + |a<n_act>.
  - vertex bookkeeping: every row logs bilin count + minted-vertex uids
    (vtags not starting "fdr_"), for the T1 research question.
  - archive entries carry seed2 confirmation fields; block library REQUIRES
    seed2_ok (v1 single-seed-fluke lesson: g0_jit_11 66.5 -> 51.6).
"""
import copy, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
L0 = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(L0, "complexity"))
sys.path.insert(0, os.path.join(L0, "evolve"))
sys.path.insert(0, os.path.join(L0, "lib"))
sys.path.insert(0, HERE)

import ds_lib as DL            # v1 helpers reused: js, locked_json, truncate
import genome as G
import funnel as FU
import soup_sim
import ds2_ops as OPS2

RESULTS2 = os.path.join(HERE, "results_v2.json")
ARCHIVE2 = os.path.join(HERE, "archive_v2.json")
STATE2 = os.path.join(HERE, "data", "state_v2.json")
RUNS2 = os.path.join(HERE, "runs2")
JOBS2 = os.path.join(HERE, "jobs2")
CONFIG = os.path.join(HERE, "ds2_config.json")
SEEDS2 = os.path.join(HERE, "seeds_v2")

MAX_ACT, MAX_FIELDS = 4, 14
NPZ_MIN_INTEREST = 15.0

_DEFAULT_CFG = dict(
    metrics="v1",              # flips to "v2" when the lock is detected
    T_screen=2500.0, T_extend=5000.0, T_confirm=5000.0,
    adaptive=True,             # local extend rule under the v1 fallback
    seed=1, seed2=2,
    pop=24,
    mix=dict(mutate=5, mint_bilin=3, delete_bilin=1, add_chan=2, dup_act=2,
             merge=6, immigrate=5),
    merge_mix=dict(cross_edge=3, slow_tanh=2, share_chan=1),
    n_workers=4)


def config():
    try:
        cfg = json.load(open(CONFIG))
    except Exception:
        cfg = {}
    out = dict(_DEFAULT_CFG)
    out.update(cfg)
    return out


def save_config(cfg):
    json.dump(DL.js(cfg), open(CONFIG, "w"), indent=1)


def v2_locked():
    """Lock detection per ASSAY_V2_API.md: its header flips to LOCKED (they
    also message). Requires metrics_v2.py + assay_v2.py present."""
    mp = os.path.join(L0, "complexity", "metrics_v2.py")
    ap = os.path.join(L0, "complexity", "assay_v2.py")
    doc = os.path.join(L0, "complexity", "ASSAY_V2_API.md")
    if not (os.path.exists(mp) and os.path.exists(ap)):
        return False
    try:
        head = open(doc).read(600)
    except FileNotFoundError:
        return False
    first = head.split("\n")[0]
    return ("LOCKED" in first) or ("Status: LOCKED" in head)


def battery_mod(cfg=None):
    cfg = cfg or config()
    if cfg["metrics"] == "v2":
        sys.path.insert(0, os.path.join(L0, "complexity"))
        import assay_v2
        return assay_v2
    import metrics_v1 as MV
    return MV


def lean_horizon(h):
    if not isinstance(h, dict):
        return None
    return dict(T_used=h.get("T_used"), why=h.get("why_stopped"),
                n_ext=h.get("n_extensions"),
                traj=h.get("interest_trajectory"))


# ------------------------------------------------------------- vertex stats
def minted_uids(g):
    return [t for t in (g.get("vtags") or []) if not str(t).startswith("fdr_")]


def vertex_row_fields(g):
    vt = g.get("vtags") or []
    return dict(n_bilin=len(g.get("bilin", []) or []),
                vtags=list(vt), minted=minted_uids(g))


# ---------------------------------------------------------------- cell key
def _stages_bin(ns):
    if ns is None:
        return "s?"
    return "s1" if ns <= 1 else ("s2" if ns == 2 else "s3")


def cell_key_v2(out, genome, metrics="v1"):
    """v2 key (ASSAY_V2_API.md pinned fields):
      sppInt | growth-class | motion | phase | stages | memgrade
    - sppInt: round(D.d7.n_species_int) clipped [0,4]
    - growth: "grow" if D.d1.org_growth else D.d1.org_model
    - motion/phase: v1 semantics (DL.motion_class works on D)
    - stages: s1 (0-1) | s2 | s3 (>=3)
    - mem: g0|g1|g2 (write-only vs READ memory — ds3_014 lesson)
    Fallback under metrics_v1: v1 4-key + |a<n_act>.
    """
    D = out["D"]
    if metrics == "v2":
        spp = D.get("d7", {}).get("n_species_int")
        spp = int(np.clip(round(spp), 0, 4)) if spp is not None else 0
        d1 = D.get("d1", {})
        growth = "grow" if d1.get("org_growth") else str(d1.get("org_model"))
        mot = DL.motion_class(D)
        ph = D["d5"]["phase"]
        st = _stages_bin(d1.get("n_stages"))
        mg = D.get("d6", {}).get("mem_grade", 0)
        return f"{spp}|{growth}|{mot}|{ph}|{st}|g{mg}"
    key = DL.cell_key(out)
    return f'{key}|a{len(genome["acts"])}'


# ------------------------------------------------- adaptive-T (v1 fallback)
def needs_extend(rec):
    """Late-succession detector on the blob-count series: extend when the
    last quarter of the window still shows secular change or a species
    turns on/off late (ds3_014's red/yellow booms were post-2500tu class).
    Cheap: uses only rec["blobs"] counts. Returns (bool, why)."""
    t = np.asarray(rec["t"])
    if len(t) < 40:
        return False, "short"
    q = len(t) - len(t) // 4
    n_i = {i: np.array([len(rec["blobs"][i][k]) for k in range(len(t))])
           for i in range(rec["na"])}
    n_tot = sum(n_i.values())
    a, b = n_tot[q:], n_tot[len(t) // 2:q]
    if len(b) == 0 or len(a) == 0:
        return False, "short"
    d = abs(float(a.mean()) - float(b.mean()))
    if d >= max(2.0, 0.15 * max(float(n_tot[len(t) // 4:].mean()), 1.0)):
        return True, f"n_trend d={d:.1f}"
    for i, ni in n_i.items():
        was = float(ni[len(t) // 2:q].mean())
        now = float(ni[q:].mean())
        if (was < 0.5 and now >= 1.0) or (was >= 1.0 and now < 0.5):
            return True, f"species_{i}_switch {was:.1f}->{now:.1f}"
    return False, "steady"


# ---------------------------------------------------------------- evaluate
def evaluate_v2(job):
    """funnel -> soup -> battery (+ optional extend rerun). Appends row to
    results_v2.json. Row extras vs v1: n_bilin/vtags/minted, extended, key
    with n_act axis, npz only when interesting (lean disk)."""
    cfg = config()
    g = job["genome"]
    OPS2.ensure_vtags(g)
    T = float(job.get("T", cfg["T_screen"]))
    seed = int(job.get("seed", cfg["seed"]))
    row = dict(kind="ds2_eval", phase=job.get("kind", "screen"),
               cand=job["cand"], gen=job.get("gen"), op=job.get("op"),
               parents=job.get("parents"), params=job.get("params"),
               T=T, seed=seed, metrics=cfg["metrics"])
    na, nc = len(g["acts"]), len(g["chans"])
    row["na"], row["nc"] = na, nc
    row.update(vertex_row_fields(g))
    if na > MAX_ACT or na + nc > MAX_FIELDS:
        row["status"] = "size_cap"
        DL.append_result(row, RESULTS2)
        return row
    t0 = time.time()
    fu = FU.funnel(g)
    row["funnel"] = dict(stage=fu["stage"], margin=fu.get("g0a_margin"),
                         chem=fu.get("g0c_any_chem"),
                         osc=fu.get("g0c_any_osc"))
    row["wall_funnel"] = round(time.time() - t0, 3)
    if fu["stage"] != "pass":
        row["status"] = fu["stage"]
        row["genome"] = G.genome_json(g)
        DL.append_result(row, RESULTS2)
        return row

    MOD = battery_mod(cfg)
    if cfg["metrics"] == "v2":
        # ---- assay_v2 GENOME-IN contract (ASSAY_V2_API.md pinned):
        # run_assay(genome, seed, L, workers, results_path, tag, save_npz).
        # Assay owns sim + adaptive-T ladder 2500->20000 (continuations).
        t1 = time.time()
        try:
            npz = (os.path.join(RUNS2, f'{job["cand"]}_a.npz')
                   if job.get("save_npz", True) else None)
            out = MOD.run_assay(G.genome_json(g), seed=seed, L=128.0,
                                workers=1, results_path=None,
                                tag=job["cand"], save_npz=npz)
        except Exception as e:
            row["status"] = "assay_error"
            row["error"] = repr(e)[:300]
            row["interest"] = 0.0
            row["genome"] = G.genome_json(g)
            DL.append_result(row, RESULTS2)
            return row
        hor = out.get("horizon") or {}
        row["wall_assay"] = round(time.time() - t1, 1)
        why = hor.get("why_stopped")
        row.update(status=("blowup" if why == "blowup" else
                           "all_dead" if why == "all_dead" else "ok"),
                   interest=out.get("interest", 0.0),
                   T_used=hor.get("T_used"), horizon=lean_horizon(hor),
                   flags=out.get("flags"),
                   summary=out.get("summary") or None)
        row["extended"] = bool(hor.get("n_extensions"))
        try:
            row["cell"] = cell_key_v2(out, g, metrics="v2")
        except Exception as e:
            row["cell"] = None
            row["cell_error"] = repr(e)[:200]
        if npz and os.path.exists(npz):
            if (row["interest"] or 0.0) >= NPZ_MIN_INTEREST:
                row["npz"] = os.path.basename(npz)
            else:
                os.remove(npz)
        row["genome"] = G.genome_json(g)
        DL.append_result(row, RESULTS2)
        return row

    # ---- v1 fallback: run soup ourselves, metrics_v1 battery
    import metrics_v1 as MV
    rec = soup_sim.run_soup(g, T=T, seed=seed, dtype="f32", workers=1)
    row["status"] = rec["status"]
    row["wall_sim"] = rec["wall_s"]
    tmax = float(np.asarray(rec["t"]).max()) if len(rec["t"]) else 0.0
    if rec["status"] == "blowup" or (rec["status"] == "all_dead"
                                     and tmax < MV.BURN + 100.0):
        row["interest"] = 0.0
        row["genome"] = G.genome_json(g)
        DL.append_result(row, RESULTS2)
        return row
    row["extended"] = False
    if (cfg.get("adaptive") and job.get("kind", "screen") == "screen"
            and rec["status"] == "ok" and T < cfg["T_extend"]):
        ext, why = needs_extend(rec)
        row["extend_why"] = why
        if ext:
            rec2 = soup_sim.run_soup(g, T=cfg["T_extend"], seed=seed,
                                     dtype="f32", workers=1)
            row["wall_sim_ext"] = rec2["wall_s"]
            if rec2["status"] in ("ok", "all_dead"):
                rec = rec2
                row["extended"] = True
                row["status"] = rec2["status"]
                T = cfg["T_extend"]
    row["T_used"] = T
    t1 = time.time()
    try:
        out = MV.full_battery(rec)
    except Exception as e:
        row["status"] = "battery_error"
        row["error"] = repr(e)[:300]
        row["interest"] = 0.0
        row["genome"] = G.genome_json(g)
        DL.append_result(row, RESULTS2)
        return row
    row["wall_battery"] = round(time.time() - t1, 1)
    row["interest"] = out["interest"]
    row["cell"] = cell_key_v2(out, g, metrics="v1")
    row["summary"] = DL.lean_summary(out)
    row["genome"] = G.genome_json(g)
    if out["interest"] >= NPZ_MIN_INTEREST:
        tag = "c" if job.get("kind") == "confirm" else (
            "e" if row["extended"] else "s")
        npz = os.path.join(RUNS2, f'{job["cand"]}_{tag}.npz')
        soup_sim.save_run(rec, npz)
        row["npz"] = os.path.basename(npz)
    DL.append_result(row, RESULTS2)
    return row


# ---------------------------------------------------------------- archive
def archive2_insert(row):
    if row.get("interest", 0.0) <= 0.0 or not row.get("cell"):
        return ("dead", None)
    key = row["cell"]
    with DL.locked_json(ARCHIVE2, {}) as c:
        # metric-mixing guard: v1-scored and v2-scored entries never share
        # an archive (scores/keys not comparable; pod run starts fresh)
        rm = row.get("metrics", "v1")
        for v in c.data.values():
            if v.get("metrics", "v1") != rm:
                raise RuntimeError(
                    f"archive metric mix: row={rm} archive has "
                    f'{v.get("metrics", "v1")} — reset archive for v2 runs')
            break
        cell = c.data.get(key)
        entry = dict(cand=row["cand"], gen=row.get("gen"), op=row.get("op"),
                     metrics=rm,
                     parents=row.get("parents"),
                     interest=row["interest"], summary=row.get("summary"),
                     genome=row.get("genome"), origin=row.get("origin", "ds2"),
                     n_bilin=row.get("n_bilin"), minted=row.get("minted"),
                     vtags=row.get("vtags"),
                     seed2_interest=None, seed2_ok=False,
                     count=(cell["count"] + 1 if cell else 1),
                     history=(cell.get("history", []) if cell else []))
        if cell is None:
            c.data[key] = entry
            c.write()
            return ("new", key)
        if row["interest"] > cell["interest"]:
            entry["history"] = (cell.get("history", [])
                                + [dict(cand=cell["cand"],
                                        interest=cell["interest"],
                                        gen=cell.get("gen"))])[-8:]
            if "first_gen" in cell:
                entry["first_gen"] = cell["first_gen"]
            c.data[key] = entry
            c.write()
            return ("improved", key)
        cell["count"] = entry["count"]
        c.write()
        return ("held", key)


def archive2_seed2(row):
    """Attach a 2nd-seed screen to the holder (cand minus _s2 suffix).
    seed2_ok iff alive and interest >= 0.6 * screen interest."""
    base = row["cand"][:-3] if row["cand"].endswith("_s2") else row["cand"]
    with DL.locked_json(ARCHIVE2, {}) as c:
        for key, cell in c.data.items():
            if cell["cand"] == base:
                i2 = row.get("interest", 0.0) or 0.0
                cell["seed2_interest"] = i2
                cell["seed2_cell"] = row.get("cell")
                cell["seed2_ok"] = bool(i2 >= 0.6 * cell["interest"]
                                        and i2 > 0.0)
                c.write()
                return key, cell["seed2_ok"]
    return None, None


def archive2_confirm(row):
    base = row["cand"][:-3] if row["cand"].endswith("_cf") else row["cand"]
    with DL.locked_json(ARCHIVE2, {}) as c:
        for key, cell in c.data.items():
            if cell["cand"] == base:
                cell["confirm_interest"] = row.get("interest")
                cell["confirm_cell"] = row.get("cell")
                c.write()
                return key
    return None


# ------------------------------------------------------------ vertex census
def vertex_census(gen=None):
    """Archive-wide minted-vertex stats + per-gen uptake from results rows."""
    try:
        arch = json.load(open(ARCHIVE2))
    except Exception:
        arch = {}
    rows = []
    try:
        rows = [r for r in json.load(open(RESULTS2))
                if r.get("kind") == "ds2_eval" and r.get("phase") == "screen"]
    except Exception:
        pass
    if gen is not None:
        rows = [r for r in rows if r.get("gen") == gen]
    mint_rows = [r for r in rows if r.get("op") == "mint_bilin"]
    carriers = [r for r in rows if r.get("minted")]
    holders_minted = {k: v for k, v in arch.items() if v.get("minted")}
    alive_uids = sorted({u for v in arch.values() for u in (v.get("minted") or [])})
    return dict(
        gen=gen,
        mint_attempt_rows=len(mint_rows),
        mint_ok=sum(1 for r in mint_rows if r.get("status") == "ok"),
        mint_funnel_fail=sum(1 for r in mint_rows
                             if str(r.get("status", "")).startswith("fail")),
        mint_best=max([r.get("interest", 0) or 0 for r in mint_rows],
                      default=0.0),
        carrier_rows=len(carriers),
        carrier_ok=sum(1 for r in carriers if r.get("status") == "ok"),
        carrier_best=max([r.get("interest", 0) or 0 for r in carriers],
                         default=0.0),
        archive_cells=len(arch),
        cells_with_minted=len(holders_minted),
        minted_uids_alive=alive_uids)
