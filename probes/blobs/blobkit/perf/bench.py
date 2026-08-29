#!/usr/bin/env python
"""bench.py — blobkit benchmark harness (perf governance tool).

Any blobkit perf claim requires a row from this harness. Three tiers
(configs in benchconfigs.py; workloads are FROZEN and hashed):

  T1 kernel     pure batched stepping + pull/launch/record microbenches.
  T2 assay-mix  prod-distribution lane mix through run_assay_batch incl.
                full battery — THE prod-like worlds/hour number.
  T3 gen-sim    one synthetic generation (screens -> confirms) end-to-end.

Same script runs CPU-JAX and GPU: --device cpu|gpu (sets JAX_PLATFORMS
before jax loads; profile/config pick the scale). Rows are versioned JSON
appended to perf/results/rows.jsonl plus a full-detail per-run JSON.

  python perf/bench.py t1 --device cpu
  python perf/bench.py t2 --config t2mini --device cpu
  python perf/bench.py t2 --config t2 --device gpu            # pod
  python perf/bench.py t3 --config t3mini --device cpu
  python perf/bench.py t2 --config t2mini --device cpu --instrument
  python perf/bench.py compare --tier t2 --config t2mini --device cpu

compare: one command; prints all comparable rows (same tier/config/device
class/workload hash) across blobkit versions with ratios vs the oldest.

Instrumented runs (--instrument) time the driver seams (dispatch / pull /
record / snapshot / battery, battery inline) — they explain WHERE the wall
goes but are NOT headline rows (row carries instrumented=true; compare
skips them by default).

No locked blobkit file is modified; instrumentation wraps module attributes
at runtime (driver.run_chunks kwargs + snapshot/battery seams).
"""
import argparse
import datetime
import json
import os
import platform
import socket
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RESULTS_DIR = os.path.join(HERE, "results")
ROWS = os.path.join(RESULTS_DIR, "rows.jsonl")

SUITE_V = 1


# ------------------------------------------------------------------ utils
def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def device_info():
    import jax
    d = jax.devices()[0]
    plat = d.platform
    kind = getattr(d, "device_kind", plat)
    cls = "cpu" if plat == "cpu" else str(kind).replace(" ", "_")
    return dict(platform=plat, device_kind=str(kind), device_class=cls,
                n_devices=len(jax.devices()), jax=jax.__version__)


def base_row(tier, config, args, workload, profile=None):
    import blobkit
    from blobkit.assay_batch import _locks12
    row = dict(v=SUITE_V, suite="blobkit-perf", ts=now_iso(),
               host=socket.gethostname(), machine=platform.machine(),
               cpu_count=os.cpu_count(),
               blobkit=blobkit.__version__, locks=_locks12(),
               tier=tier, config=config, profile=profile,
               dtype="f32", workload=workload,
               instrumented=bool(getattr(args, "instrument", False)),
               tag=args.tag, device=args.device)
    row.update(device_info())
    return row


def emit(row, detail=None):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(ROWS, "a") as f:
        f.write(json.dumps(row, default=str) + "\n")
    name = (f"{row['ts'].replace(':', '')}_{row['tier']}_{row['config']}"
            f"_{row['device_class']}.json")
    p = os.path.join(RESULTS_DIR, name)
    with open(p, "w") as f:
        json.dump(dict(row=row, detail=detail or {}), f, indent=1,
                  default=str)
    print(f"\n[row] {ROWS}")
    print(json.dumps({k: row[k] for k in
                      ("tier", "config", "blobkit", "device_class",
                       "workload", "w_h", "wall_s", "instrumented")
                      if k in row}, default=str))
    return p


# ------------------------------------------------------- instrumentation
class Probe:
    """Times the injected driver seams + assay seams. Runtime attribute
    wrapping only; restore() puts everything back."""

    def __init__(self):
        self.t = dict(dispatch=0.0, pull=0.0, record=0.0, snapshot=0.0,
                      battery=0.0)
        self.n = dict(chunks=0, pulls=0, full_pulls=0, records=0,
                      snapshots=0, batteries=0)
        self.chunk_walls = []
        self._lock = threading.Lock()
        import blobkit.soup.driver as DRV
        import blobkit.soup.sim_gpu as SG
        import blobkit.assay_batch as AB
        self._mods = (DRV, SG, AB)
        self._orig = (DRV.run_chunks, SG.snapshot_rec_gpu,
                      AB._battery_worker)
        probe = self

        def run_chunks(worlds, steps_target, *, step_fn, pull_fn, record_fn,
                       **kw):
            def sf(t, n):
                t0 = time.perf_counter()
                step_fn(t, n)
                dt_ = time.perf_counter() - t0
                probe.t["dispatch"] += dt_
                probe.chunk_walls.append(dt_)
                probe.n["chunks"] += 1

            def pf(full):
                t0 = time.perf_counter()
                r = pull_fn(full)
                probe.t["pull"] += time.perf_counter() - t0
                probe.n["pulls"] += 1
                probe.n["full_pulls"] += int(bool(full))
                return r

            def rf(S, Fh, t):
                t0 = time.perf_counter()
                record_fn(S, Fh, t)
                with probe._lock:
                    probe.t["record"] += time.perf_counter() - t0
                    probe.n["records"] += 1

            return probe._orig[0](worlds, steps_target, step_fn=sf,
                                  pull_fn=pf, record_fn=rf, **kw)

        def snapshot(S):
            t0 = time.perf_counter()
            r = self._orig[1](S)
            probe.t["snapshot"] += time.perf_counter() - t0
            probe.n["snapshots"] += 1
            return r

        def battery(payload):
            t0 = time.perf_counter()
            r = self._orig[2](payload)
            probe.t["battery"] += time.perf_counter() - t0
            probe.n["batteries"] += 1
            return r

        DRV.run_chunks = run_chunks
        SG.snapshot_rec_gpu = snapshot
        AB._battery_worker = battery

    def restore(self):
        DRV, SG, AB = self._mods
        DRV.run_chunks, SG.snapshot_rec_gpu, AB._battery_worker = self._orig

    def summary(self, wall):
        s = dict(seconds={k: round(v, 2) for k, v in self.t.items()},
                 counts=dict(self.n))
        acc = sum(self.t.values())
        s["accounted_s"] = round(acc, 2)
        s["other_s"] = round(wall - acc, 2)
        if self.chunk_walls:
            cw = sorted(self.chunk_walls)
            s["chunk_dispatch_median_ms"] = round(
                1e3 * cw[len(cw) // 2], 2)
            s["chunk_dispatch_max_ms"] = round(1e3 * cw[-1], 2)
        return s


# ------------------------------------------------------------------- T1
def run_t1(args):
    import numpy as np
    import benchconfigs as bc
    import jax.numpy as jnp
    from blobkit import genome as G
    from blobkit.soup import sim_cpu as SC
    from blobkit.soup import sim_gpu as SG
    from blobkit.soup.sim_v1 import NOISE
    from blobkit import worlds

    prof = bc.T1_PROFILES[args.profile]
    pm = bc.load_prodmix()
    detail = dict(cells=[], pullcadence=None, launch=None, record=None)
    t_tier0 = time.time()

    def packed(gens, B, N=prof.get("N", 256)):
        states = [G.state_vacuum(g, N).astype(np.float32) for g in gens]
        params, struct, aux = SG.pack_genomes(gens, np.float32)
        p = {k: jnp.asarray(v) for k, v in params.items()}
        p["E"] = SG.diffusion_E(params["D"], N, 0.5, 0.02, np.float32)
        F = jnp.asarray(SG.pack_states(gens, states, struct["na_max"],
                                       struct["nc_max"]))
        keys = SG.batch_keys(list(range(B)))
        step = SG.make_stepper(struct, N, 0.5, 0.02, noise=NOISE)
        return F, p, keys, step, struct

    # --- kernel cells
    for (name, B, bucket, nsteps) in prof["cells"]:
        gens = bc.t1_lanes(bucket, B, pm)
        F, p, keys, step, struct = packed(gens, B)
        t0 = time.time()
        F = step(F, p, keys, 0, nsteps)
        F.block_until_ready()
        compile_s = time.time() - t0
        reps = []
        for r in range(3):
            t0 = time.time()
            F = step(F, p, keys, (r + 1) * nsteps, nsteps)
            F.block_until_ready()
            reps.append(time.time() - t0)
        run_s = sorted(reps)[1]                      # median of 3
        us_ws = run_s * 1e6 / (nsteps * B)
        w_h_sim2500 = 3600.0 / (us_ws * 125000 / 1e6)
        cell = dict(name=name, B=B, bucket=bucket,
                    nf_max=struct["na_max"] + struct["nc_max"],
                    nsteps=nsteps, compile_s=round(compile_s, 2),
                    us_per_world_step=round(us_ws, 2),
                    w_h_sim_ceiling_T2500=round(w_h_sim2500, 1),
                    reps_s=[round(x, 3) for x in reps])
        detail["cells"].append(cell)
        print(f"[t1 {name}] B={B} nf_max={cell['nf_max']} "
              f"compile={compile_s:.1f}s us/world-step={us_ws:.1f} "
              f"simT2500-ceiling={w_h_sim2500:.0f} w/h", flush=True)

    # --- pull cadence: chunk loop with none / acts-only / full pulls
    # (stepper donates F: re-upload a host copy per mode, chain inside)
    pc = prof["pullcadence"]
    gens = bc.t1_lanes(pc["bucket"], pc["B"], pm)
    F, p, keys, step, struct = packed(gens, pc["B"])
    na_max = struct["na_max"]
    F = step(F, p, keys, 0, pc["chunk"])
    F.block_until_ready()                            # compile out of band
    F_host = np.asarray(F)
    res = {}
    for mode in ("none", "acts", "full"):
        Fm = jnp.asarray(F_host)
        t0 = time.time()
        for k in range(pc["n_chunks"]):
            Fm = step(Fm, p, keys, (k + 1) * pc["chunk"], pc["chunk"])
            if mode == "acts":
                np.asarray(Fm[:, :na_max])
            elif mode == "full":
                np.asarray(Fm)
        Fm.block_until_ready()
        res[mode] = round(time.time() - t0, 3)
    per_pull_acts = (res["acts"] - res["none"]) / pc["n_chunks"]
    per_pull_full = (res["full"] - res["none"]) / pc["n_chunks"]
    detail["pullcadence"] = dict(pc, walls_s=res,
                                 per_pull_acts_ms=round(1e3 * per_pull_acts, 1),
                                 per_pull_full_ms=round(1e3 * per_pull_full, 1))
    print(f"[t1 pull] B={pc['B']} b{pc['bucket']}: {res}  "
          f"acts_pull={per_pull_acts*1e3:.0f}ms full_pull="
          f"{per_pull_full*1e3:.0f}ms per chunk", flush=True)

    # --- launch overhead: n single-step calls vs one n-step chunk
    # (donation-safe: re-upload the post-compile state per variant)
    lc = prof["launch"]
    gens = bc.t1_lanes(lc["bucket"], lc["B"], pm)
    F, p, keys, step, struct = packed(gens, lc["B"])
    F1 = step(F, p, keys, 0, 1)
    F1.block_until_ready()                           # compile 1-step
    F1_host = np.asarray(F1)
    t0 = time.time()
    Fs = jnp.asarray(F1_host)
    for i in range(lc["n"]):
        Fs = step(Fs, p, keys, 1 + i, 1)
    Fs.block_until_ready()
    singles_s = time.time() - t0
    Fc = step(jnp.asarray(F1_host), p, keys, 1, lc["n"])
    Fc.block_until_ready()                           # compile n-step
    t0 = time.time()
    Fc = step(jnp.asarray(F1_host), p, keys, 1 + lc["n"], lc["n"])
    Fc.block_until_ready()
    chunk_s = time.time() - t0
    detail["launch"] = dict(lc, singles_s=round(singles_s, 3),
                            chunk_s=round(chunk_s, 3),
                            per_step_overhead_us=round(
                                (singles_s - chunk_s) * 1e6 / lc["n"], 1))
    print(f"[t1 launch] {lc['n']}x1step={singles_s:.3f}s vs chunk="
          f"{chunk_s:.3f}s -> {detail['launch']['per_step_overhead_us']}us/step",
          flush=True)

    # --- host record cost (locked CPU tracking on real seeded states)
    recs = []
    for wname in prof["record_worlds"]:
        g = worlds.load(wname)
        S = SC.init_soup(g, L=128.0, seed=1, workers=0)
        rec_i, crec_i = S["rec"], S["crec"]
        n = prof["record_reps"]
        ratio = crec_i // rec_i                      # every ratio-th REC
        ks_rec = [k for k in range(1, 10 * n) if k % ratio][:n]
        t0 = time.time()
        for k in ks_rec:
            SC._record(S, k * rec_i)                 # pure REC points
        rec_ms = (time.time() - t0) / n * 1e3
        m = max(n // 5, 1)
        t0 = time.time()
        for k in range(1, m + 1):
            SC._record(S, k * crec_i)                # REC+CREC points
        crec_ms = (time.time() - t0) / m * 1e3
        recs.append(dict(world=wname, na=S["na"],
                         rec_ms=round(rec_ms, 2), crec_ms=round(crec_ms, 2)))
        print(f"[t1 record] {wname}: REC={rec_ms:.1f}ms "
              f"CREC={crec_ms:.1f}ms per world-record", flush=True)
    detail["record"] = recs

    wall = time.time() - t_tier0
    row = base_row("t1", args.profile, args,
                   workload=f"t1profile-{args.profile}-v{SUITE_V}",
                   profile=args.profile)
    row["wall_s"] = round(wall, 1)
    row["cells"] = {c["name"]: c["us_per_world_step"]
                    for c in detail["cells"]}
    row["pull_full_ms"] = detail["pullcadence"]["per_pull_full_ms"]
    row["pull_acts_ms"] = detail["pullcadence"]["per_pull_acts_ms"]
    row["launch_us"] = detail["launch"]["per_step_overhead_us"]
    row["record_ms"] = {r["world"]: r["rec_ms"] for r in recs}
    emit(row, detail)


# ------------------------------------------------------------------- T2
def _run_lane_calls(lanes, cfg, args, tier, config):
    """Shared T2/T3 executor: group lanes 0.3.2-style, run one
    run_assay_batch per call, collect walls + outcomes."""
    import benchconfigs as bc
    from blobkit.assay_batch import run_assay_batch

    calls = bc.group_lanes(lanes, cfg["bmax"])
    probe = Probe() if args.instrument else None
    kw = {}
    if cfg.get("B_pad"):
        kw["B_pad"] = tuple(cfg["B_pad"])
    call_rows, outs_by_lane = [], {}
    t_tier0 = time.time()
    for ci, idx in enumerate(calls):
        jobs = [dict(genome=lanes[i]["genome"], seed=lanes[i]["seed"],
                     t0=lanes[i]["t0"], cap=lanes[i]["cap"])
                for i in idx]
        t0 = time.time()
        outs = run_assay_batch(
            jobs, L=cfg["L"], t0=cfg["t0"], cap=cfg["cap"],
            results_path=None, verbose=args.verbose,
            battery_procs=(0 if args.instrument else args.battery_procs),
            **kw)
        w = time.time() - t0
        for i, out in zip(idx, outs):
            outs_by_lane[i] = out
        hor = [(out or {}).get("horizon", {}) for out in outs]
        call_rows.append(dict(
            call=ci, n_lanes=len(idx), bucket=lanes[idx[0]]["bucket"],
            wall_s=round(w, 1),
            T_used=[h.get("T_used") for h in hor],
            why=[h.get("why_stopped") for h in hor]))
        print(f"[{tier} {config} call{ci}] b{call_rows[-1]['bucket']} "
              f"n={len(idx)} wall={w:.1f}s T={call_rows[-1]['T_used']}",
              flush=True)
    wall = time.time() - t_tier0
    if probe:
        probe.restore()
    return calls, call_rows, outs_by_lane, wall, probe


def _lane_stats(lanes, outs_by_lane):
    import numpy as np
    tu, errs, statuses = 0.0, 0, {}
    for i in range(len(lanes)):
        out = outs_by_lane.get(i) or {}
        hor = out.get("horizon", {})
        tu += float(hor.get("T_used") or 0.0)
        why = hor.get("why_stopped")
        statuses[why] = statuses.get(why, 0) + 1
        if out.get("assay_error"):
            errs += 1
    return tu, errs, statuses


def run_t2(args):
    import benchconfigs as bc
    cfg = dict(bc.T2_CONFIGS[args.config])
    lanes = bc.build_t2_lanes(args.config)
    wl = bc.workload_hash(lanes, extra=dict(cfg=cfg, tier="t2"))
    print(f"[t2 {args.config}] {len(lanes)} lanes, L={cfg['L']} "
          f"t0={cfg['t0']} cap={cfg['cap']} workload={wl}", flush=True)
    for rep in range(args.repeat):
        calls, call_rows, outs, wall, probe = _run_lane_calls(
            lanes, cfg, args, "t2", args.config)
        tu, errs, statuses = _lane_stats(lanes, outs)
        w_h = len(lanes) / (wall / 3600.0)
        row = base_row("t2", args.config, args, workload=wl)
        row.update(wall_s=round(wall, 1), n_lanes=len(lanes),
                   n_calls=len(calls), w_h=round(w_h, 2),
                   tu_total=tu, tu_per_s=round(tu / wall, 1),
                   assay_errors=errs, statuses=statuses, rep=rep)
        detail = dict(cfg=cfg, calls=call_rows,
                      lanes=[{k: ln[k] for k in
                              ("cand", "phase", "bucket", "seed", "t0",
                               "cap", "T_stamp")} for ln in lanes])
        if probe:
            detail["probe"] = probe.summary(wall)
            row["probe"] = detail["probe"]["seconds"]
        emit(row, detail)
        print(f"[t2 {args.config} rep{rep}] wall={wall:.0f}s "
              f"w/h={w_h:.2f} tu/s={tu/wall:.1f} errors={errs}", flush=True)


# ------------------------------------------------------------------- T3
def run_t3(args):
    import benchconfigs as bc
    cfg = dict(bc.T3_CONFIGS[args.config])
    screens = bc.build_t3_screens(args.config)
    wl = bc.workload_hash(screens, extra=dict(cfg=cfg, tier="t3"))
    print(f"[t3 {args.config}] {len(screens)} screens, L={cfg['L']} "
          f"workload={wl}", flush=True)

    t_gen0 = time.time()
    calls_s, rows_s, outs_s, wall_s, probe = _run_lane_calls(
        screens, cfg, args, "t3", args.config + "/screen")

    # confirms: top-K screens by interest, seeds 2..3, t0 = screen T_used
    ranked = sorted(range(len(screens)),
                    key=lambda i: -float((outs_s.get(i) or {})
                                         .get("interest", 0.0)))
    top = ranked[:cfg["n_confirm"]]
    confirms = []
    for i in top:
        out = outs_s.get(i) or {}
        T_used = float(out.get("horizon", {}).get("T_used") or cfg["t0"])
        for seed in (2, 3):
            confirms.append(dict(genome=screens[i]["genome"], seed=seed,
                                 t0=min(T_used, cfg["cap"]), cap=cfg["cap"],
                                 bucket=screens[i]["bucket"],
                                 cand=f"{screens[i]['cand']}_s{seed}",
                                 phase=f"seed{seed}", T_stamp=T_used))
    calls_c, rows_c, outs_c, wall_c, probe_c = _run_lane_calls(
        confirms, cfg, args, "t3", args.config + "/confirm")

    wall = time.time() - t_gen0
    n_worlds = len(screens) + len(confirms)
    tu_s, err_s, st_s = _lane_stats(screens, outs_s)
    tu_c, err_c, st_c = _lane_stats(confirms, outs_c)
    w_h = n_worlds / (wall / 3600.0)
    row = base_row("t3", args.config, args, workload=wl)
    row.update(wall_s=round(wall, 1), n_worlds=n_worlds,
               n_screens=len(screens), n_confirms=len(confirms),
               w_h=round(w_h, 2), wall_screen_s=round(wall_s, 1),
               wall_confirm_s=round(wall_c, 1),
               tu_total=tu_s + tu_c, assay_errors=err_s + err_c)
    emit(row, dict(cfg=cfg, screen_calls=rows_s, confirm_calls=rows_c,
                   statuses=dict(screen=st_s, confirm=st_c)))
    print(f"[t3 {args.config}] wall={wall:.0f}s w/h={w_h:.2f} "
          f"(screen {wall_s:.0f}s + confirm {wall_c:.0f}s)", flush=True)


# --------------------------------------------------------------- compare
def run_compare(args):
    if not os.path.exists(ROWS):
        print("no rows yet:", ROWS)
        return
    rows = [json.loads(l) for l in open(ROWS) if l.strip()]
    rows = [r for r in rows
            if (not args.tier or r.get("tier") == args.tier)
            and (not args.config or r.get("config") == args.config)
            and (args.device == "any" or r.get("device") == args.device)
            and (args.instrumented or not r.get("instrumented"))]
    if not rows:
        print("no matching rows")
        return
    key = lambda r: (r.get("tier"), r.get("config"), r.get("device_class"),
                     r.get("workload"))
    groups = {}
    for r in rows:
        groups.setdefault(key(r), []).append(r)
    for k, rs in sorted(groups.items()):
        rs.sort(key=lambda r: r.get("ts", ""))
        print(f"\n== tier={k[0]} config={k[1]} device={k[2]} workload={k[3]}")
        base = None
        hdr = f"  {'ts':22s} {'blobkit':9s} {'w_h':>9s} {'wall_s':>8s} {'ratio':>7s} tag"
        print(hdr)
        for r in rs:
            wh = r.get("w_h")
            if wh is not None and base is None:
                base = wh
            ratio = (f"{wh / base:6.2f}x" if (wh is not None and base)
                     else "      -")
            print(f"  {r.get('ts', ''):22s} {r.get('blobkit', ''):9s} "
                  f"{(f'{wh:9.2f}' if wh is not None else '        -')} "
                  f"{r.get('wall_s', 0):8.1f} {ratio} {r.get('tag') or ''}")


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--device", choices=("cpu", "gpu"), default="cpu")
        p.add_argument("--tag", default=None)
        p.add_argument("--verbose", action="store_true")
        p.add_argument("--instrument", action="store_true",
                       help="time driver seams; battery inline; "
                            "row marked instrumented (not for headlines)")
        p.add_argument("--battery-procs", type=int, default=None,
                       dest="battery_procs")
        p.add_argument("--repeat", type=int, default=1)

    p1 = sub.add_parser("t1", help="kernel tier")
    common(p1)
    p1.add_argument("--profile", choices=("cpu", "gpu"), default=None)

    p2 = sub.add_parser("t2", help="assay-mix tier (prod-like w/h)")
    common(p2)
    p2.add_argument("--config", default=None,
                    help="t2|t2mini|t2smoke (default by device)")

    p3 = sub.add_parser("t3", help="gen-sim tier")
    common(p3)
    p3.add_argument("--config", default=None, help="t3|t3mini")

    pc = sub.add_parser("compare", help="compare rows across versions")
    pc.add_argument("--tier", default=None)
    pc.add_argument("--config", default=None)
    pc.add_argument("--device", default="any")
    pc.add_argument("--instrumented", action="store_true")

    args = ap.parse_args()
    if args.cmd == "compare":
        run_compare(args)
        return

    # device pinning BEFORE any jax import (blobkit imports jax lazily)
    if args.device == "cpu":
        os.environ["JAX_PLATFORMS"] = "cpu"
    os.environ.setdefault("BLOBKIT_SKIP_LOCK", "0")
    import jax  # noqa: F401  (fail fast on missing gpu)
    di = device_info()
    if args.device == "gpu" and di["platform"] == "cpu":
        ap.error("--device gpu but jax sees only CPU")
    print(f"[bench] device={di['device_kind']} jax={di['jax']}", flush=True)

    if args.cmd == "t1":
        args.profile = args.profile or ("gpu" if args.device == "gpu"
                                        else "cpu")
        run_t1(args)
    elif args.cmd == "t2":
        args.config = args.config or ("t2" if args.device == "gpu"
                                      else "t2mini")
        run_t2(args)
    elif args.cmd == "t3":
        args.config = args.config or ("t3" if args.device == "gpu"
                                      else "t3mini")
        run_t3(args)


if __name__ == "__main__":
    main()
