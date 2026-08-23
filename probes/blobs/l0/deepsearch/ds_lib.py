"""ds_lib.py — deepsearch shared: eval pipeline, cell key, archive, truncation.
Phase 5b: complexity-driven MAP-Elites search. Fitness = metrics_v1 interest
(T=2500 screen / T=5000 confirm). Cell key = spp|motion|phase|mem.
"""
import copy, fcntl, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
L0 = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(L0, "complexity"))
sys.path.insert(0, os.path.join(L0, "evolve"))
sys.path.insert(0, os.path.join(L0, "lib"))
sys.path.insert(0, os.path.join(L0, "stage2", "lib"))

import genome as G
import funnel as FU
import soup_sim
import metrics_v1 as MV

RESULTS = os.path.join(HERE, "results.json")
ARCHIVE = os.path.join(HERE, "archive.json")
STATE = os.path.join(HERE, "data", "state.json")
RUNS = os.path.join(HERE, "runs")

T_SCREEN, T_CONFIRM, SEED = 2500.0, 5000.0, 1
MAX_ACT, MAX_FIELDS = 4, 12


def js(o):
    if isinstance(o, dict):
        return {k: js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [js(v) for v in o]
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def locked_json(path, default):
    class _ctx:
        def __enter__(self):
            self.lk = open(path + ".lock", "w")
            fcntl.flock(self.lk, fcntl.LOCK_EX)
            try:
                with open(path) as f:
                    self.data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                self.data = copy.deepcopy(default)
            return self

        def write(self):
            tmp = path + ".tmp"
            with open(tmp, "w") as f:
                json.dump(js(self.data), f)
            os.replace(tmp, path)

        def __exit__(self, *a):
            self.lk.close()
    return _ctx()


def append_result(row, path=RESULTS):
    with locked_json(path, []) as c:
        row = dict(row)
        row.setdefault("ts", time.strftime("%Y-%m-%d %H:%M:%S"))
        c.data.append(js(row))
        c.write()
        return len(c.data)


# ---------------------------------------------------------------- cell key
def motion_class(D):
    wind = D["d5"].get("winding_max", 0.0) or 0.0
    com = D["d5"].get("wind_com_speed")
    mv = D["d4"].get("moving_frac", 0.0)
    if wind >= 1.5 and com is not None and com < 0.03:
        return "rotor"
    if mv >= 0.25:
        return "mobile"
    if mv >= 0.05:
        return "drift"
    return "still"


def cell_key(out):
    D = out["D"]
    spp = min(int(D["d1"].get("n_species_alive", 0)), MAX_ACT)
    mem = 1 if (D["d6"].get("cover") or 0.0) > 0.01 else 0
    return f'{spp}|{motion_class(D)}|{D["d5"]["phase"]}|m{mem}'


def lean_summary(out):
    D, C = out["D"], out["C"]
    return dict(
        interest=out["interest"], C={k: round(v, 4) for k, v in C.items()},
        d1=dict(model=D["d1"].get("model"), n_end=D["d1"].get("n_end"),
                turn=round(D["d1"].get("turnover", 0.0), 4),
                spp=D["d1"].get("n_species_alive")),
        d2=dict(slow=D["d2"].get("tau_slow"), obs=D["d2"].get("tau_slow_obs"),
                r_emerg=D["d2"].get("r_emerg")),
        d4=dict(mv=D["d4"].get("moving_frac"), vc=D["d4"].get("v_corr"),
                role=D["d4"].get("role_div")),
        d5=dict(phase=D["d5"].get("phase"), churn=D["d5"].get("churn100"),
                wind=D["d5"].get("winding_max"),
                com=D["d5"].get("wind_com_speed")),
        d6=dict(cover=D["d6"].get("cover"), elong=D["d6"].get("elong"),
                rmem=D["d6"].get("r_mem")))


# ---------------------------------------------------------------- truncation
def truncate_rec(rec, T):
    """Exact T-truncation of a saved run record (deterministic sim => the
    truncated record IS the shorter run; snaps unused by the battery)."""
    r = {k: v for k, v in rec.items() if not k.startswith("_")}
    t = np.asarray(rec["t"])
    nk = int((t <= T + 1e-9).sum())
    r["t"] = t[:nk]
    r["blobs"] = {i: rec["blobs"][i][:nk] for i in rec["blobs"]}
    r["mass"] = {i: list(rec["mass"][i])[:nk] for i in rec["mass"]}
    ct = np.asarray(rec["ct"])
    ck = int((ct <= T + 1e-9).sum())
    r["ct"] = ct[:ck]
    r["patches"] = {i: rec["patches"][i][:ck] for i in rec["patches"]}
    r["memf"] = {c: np.asarray(rec["memf"][c])[:ck] for c in rec.get("memf", {})}
    r["T"] = float(T)
    return r


# ---------------------------------------------------------------- evaluate
def evaluate(job):
    """One candidate: funnel -> soup -> battery. Returns full row (appended).
    job: cand, gen, op, parents, params, genome, T, seed, kind(screen|confirm)."""
    g = job["genome"]
    T = float(job.get("T", T_SCREEN))
    seed = int(job.get("seed", SEED))
    row = dict(kind="ds_eval", phase=job.get("kind", "screen"),
               cand=job["cand"], gen=job.get("gen"), op=job.get("op"),
               parents=job.get("parents"), params=job.get("params"),
               T=T, seed=seed)
    na, nc = len(g["acts"]), len(g["chans"])
    row["na"], row["nc"] = na, nc
    if na > MAX_ACT or na + nc > MAX_FIELDS:
        row["status"] = "size_cap"
        append_result(row)
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
        append_result(row)
        return row
    rec = soup_sim.run_soup(g, T=T, seed=seed, dtype="f32", workers=1)
    row["status"] = rec["status"]
    row["wall_sim"] = rec["wall_s"]
    # blowup or death before/near burn-in: alive-gate zero, battery skipped
    # (metrics_v1 is LOCKED; empty post-burn windows crash d2 on dead worlds)
    tmax = float(np.asarray(rec["t"]).max()) if len(rec["t"]) else 0.0
    if rec["status"] == "blowup" or (rec["status"] == "all_dead"
                                     and tmax < MV.BURN + 100.0):
        row["interest"] = 0.0
        row["genome"] = G.genome_json(g)
        append_result(row)
        return row
    t1 = time.time()
    try:
        out = MV.full_battery(rec)
    except Exception as e:          # battery edge case: log, score 0, go on
        row["status"] = "battery_error"
        row["error"] = repr(e)[:300]
        row["interest"] = 0.0
        row["genome"] = G.genome_json(g)
        append_result(row)
        return row
    row["wall_battery"] = round(time.time() - t1, 1)
    row["interest"] = out["interest"]
    row["cell"] = cell_key(out)
    row["summary"] = lean_summary(out)
    row["genome"] = G.genome_json(g)
    tagT = "c" if T >= T_CONFIRM else "s"
    npz = os.path.join(RUNS, f'{job["cand"]}_{tagT}.npz')
    soup_sim.save_run(rec, npz)
    row["npz"] = os.path.basename(npz)
    append_result(row)
    return row


# ---------------------------------------------------------------- archive
def archive_insert(row):
    """MAP-Elites insert by SCREEN interest. Returns (event, cell) where event
    in {new, improved, held, dead, na}."""
    if row.get("interest", 0.0) <= 0.0 or "cell" not in row:
        return ("dead", None)
    key = row["cell"]
    with locked_json(ARCHIVE, {}) as c:
        cell = c.data.get(key)
        entry = dict(cand=row["cand"], gen=row.get("gen"), op=row.get("op"),
                     parents=row.get("parents"),
                     interest=row["interest"], summary=row.get("summary"),
                     genome=row.get("genome"), origin=row.get("origin", "ds"),
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


def archive_confirm(row):
    """Attach a T=5000 confirm to the archive cell held by row's cand."""
    with locked_json(ARCHIVE, {}) as c:
        for key, cell in c.data.items():
            if cell["cand"] == row["cand"]:
                cell["confirm_interest"] = row.get("interest")
                cell["confirm_cell"] = row.get("cell")
                cell["confirm_summary"] = row.get("summary")
                c.write()
                return key
    return None
