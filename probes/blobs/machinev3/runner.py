"""machinev3/runner.py — job runner (save-as-you-go into results.json).

Usage: MPLBACKEND=Agg python runner.py --jobs jobs_x.json [--tag T]
Job kinds:
  engine_solo {coupling, eta, engine, L, T}          -> c measurement (kicked)
  cargo_solo  {coupling, eta, engine, L, T, n, spacing, noise, seed} -> park
  tow         {coupling, eta, engine, L, T, x_e, x_c, n, spacing, noise, seed,
               stop_dial_t?, stop_dial?}             -> grip/tow measurement
Each job appends one record. Snapshots saved to strips/ as npz (last field).
"""
import argparse, copy, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("mv3_metrics", os.path.join(HERE, "metrics.py"))
MT = _ilu.module_from_spec(_spec); _spec.loader.exec_module(MT)
import lib as LB
G = LB.G

Y0 = 48.0


def measure_c(r, act, win=150.0):
    t = np.asarray(r["t"], float)
    pos = r[f"pos{act}"]
    n = min(len(t), len(pos))
    xs = np.array([p[0][1] if len(p) else np.nan for p in pos[:n]])
    m = (t[:n] >= t[n - 1] - win) & np.isfinite(xs)
    if m.sum() < 3:
        return None
    return float(np.polyfit(t[:n][m], xs[m], 1)[0])


def do_engine_solo(job):
    g = LB.build_world(job.get("coupling", "none"), job.get("eta", 0.0),
                       job.get("engine", "base"), job.get("cargo_mod"))
    L = job.get("L", 96.0); T = job.get("T", 600.0)
    N = int(round(L / 0.5))
    F = G.state_vacuum(g, N)
    F = LB.place_engine(F, g, L / 2, Y0, 0.5)
    r = G.run_genome(g, F=F, L=L, T=T, track_acts=[0, 1, 2],
                     stop_explode_n=6)
    c = measure_c(r, 0)
    nc1 = r["ncomp1"]; nc2 = r["ncomp2"]
    return dict(cls="engine_solo", status=r["status"], c=c,
                ncomp_end=[int(r["ncomp0"][-1]), int(nc1[-1]), int(nc2[-1])],
                cargo_nucleated=bool(nc1.max() > 0 or nc2.max() > 0),
                wall_s=round(r["wall_s"], 1))


def do_cargo_solo(job):
    g = LB.build_world(job.get("coupling", "none"), job.get("eta", 0.0),
                       job.get("engine", "base"), job.get("cargo_mod"))
    L = job.get("L", 96.0); T = job.get("T", 800.0)
    n = job.get("n", 1); spacing = job.get("spacing", 14.0)
    N = int(round(L / 0.5))
    F = G.state_vacuum(g, N)
    x0 = L / 2 - spacing * (n - 1) / 2.0
    for j in range(n):
        F = LB.place_cargo(F, g, x0 + j * spacing, Y0, 0.5)
    r = G.run_genome(g, F=F, L=L, T=T, track_acts=[0, 1, 2],
                     noise=job.get("noise", 0.0), seed=job.get("seed", 0),
                     stop_explode_n=n + 3)
    t = np.asarray(r["t"], float)
    ncc = r["ncomp1"]
    coms = []
    for k, p in enumerate(r["pos1"]):
        if len(p) == n:
            coms.append((t[k], np.mean([q[1] for q in p]), np.mean([q[0] for q in p])))
    out = dict(cls="cargo_solo", status=r["status"], n=n,
               ncomp_end=[int(r["ncomp0"][-1]), int(ncc[-1]), int(r["ncomp2"][-1])],
               engine_nucleated=bool(r["ncomp0"].max() > 0),
               wall_s=round(r["wall_s"], 1))
    if len(coms) >= 3:
        arr = np.array(coms)
        out["com_net_px"] = float(np.hypot(arr[-1, 1] - arr[0, 1],
                                           arr[-1, 2] - arr[0, 2]))
        out["parked"] = bool(out["com_net_px"] < MT.PARK_DRIFT_MAX
                             and int(ncc[-1]) == n)
    return out


def rail_setup(job, g, F, L):
    """Apply in-genome rail (frozen channel) if job['rail'] is set.
    rail = {k_rail, amp, sig, y0, x_dock, dock_w, dock_amp}."""
    rc = job.get("rail")
    if not rc:
        return g, F
    g = LB.add_rail(g, rc.get("k_rail", 1.0))
    N = F.shape[1]
    F2 = np.zeros((F.shape[0] + 1, N, N))
    F2[:-1] = F
    F2 = LB.rail_ic(F2, g, 0.5, y0=rc.get("y0", 48.0), amp=rc.get("amp", 0.35),
                    sig=rc.get("sig", 5.0), x_dock=rc.get("x_dock"),
                    dock_w=rc.get("dock_w", 2.0), dock_amp=rc.get("dock_amp"))
    return g, F2


def do_tow(job):
    g = LB.build_world(job.get("coupling", "none"), job.get("eta", 0.0),
                       job.get("engine", "base"), job.get("cargo_mod"))
    L = job.get("T_L_unused", None) or job.get("L", 96.0); T = job.get("T", 800.0)
    n = job.get("n", 1); spacing = job.get("spacing", 14.0)
    x_e = job.get("x_e", 16.0); x_c = job.get("x_c", 52.0)
    N = int(round(L / 0.5))
    F = G.state_vacuum(g, N)
    F = LB.place_engine(F, g, x_e, Y0, 0.5)
    axis = job.get("stack_axis", "x")
    for j in range(n):
        off = (j - (n - 1) / 2.0) * spacing
        if axis == "y":
            F = LB.place_cargo(F, g, x_c, Y0 + off, 0.5)
        else:
            F = LB.place_cargo(F, g, x_c + j * spacing, Y0, 0.5)
    g, F = rail_setup(job, g, F, L)
    snap = job.get("snaps", ())
    r = G.run_genome(g, F=F, L=L, T=T, track_acts=[0, 1, 2],
                     noise=job.get("noise", 0.0), seed=job.get("seed", 0),
                     stop_explode_n=n + 4, snap_times=snap, save_fields=True)
    S = LB.sep_series(r, n_cargo=n)
    lock = MT.lock_analysis(S["t"], S["xe"], S["xc_com"], S["sep"],
                            S["nce"], S["ncc"], n)
    out = dict(cls="tow", status=r["status"], n=n,
               ncomp_end=[int(r["ncomp0"][-1]), int(r["ncomp1"][-1]),
                          int(r["ncomp2"][-1])],
               ncomp_max=[int(r["ncomp0"].max()), int(r["ncomp1"].max()),
                          int(r["ncomp2"].max())],
               lock=lock, wall_s=round(r["wall_s"], 1))
    # engine speed pre-contact (first 100 tu window where sep>25)
    m_pre = (S["sep"] > 25) & np.isfinite(S["xe"])
    if m_pre.sum() > 4:
        i1 = np.nonzero(m_pre)[0]
        seg = i1[i1 < len(S["t"])]
        tt, xx = S["t"][seg], S["xe"][seg]
        if tt[-1] - tt[0] > 30:
            out["c_engine_pre"] = float(np.polyfit(tt, xx, 1)[0])
    out["cargo_net_x"] = (float(S["xc_com"][np.isfinite(S["xc_com"])][-1]
                                - S["xc_com"][np.isfinite(S["xc_com"])][0])
                          if np.isfinite(S["xc_com"]).sum() >= 2 else None)
    out["sep_end"] = float(S["sep"][-1]) if np.isfinite(S["sep"][-1]) else None
    # save compact series for later analysis
    tag = job.get("name", "tow")
    npz = os.path.join(HERE, "strips", f"{tag}.npz")
    # per-blob cargo tracks (nan-padded to n)
    nrec = len(S["t"])
    pb = np.full((nrec, n, 2), np.nan)
    for k in range(nrec):
        p = r["pos1"][k]
        for j in range(min(len(p), n)):
            pb[k, j, 0] = p[j][0]; pb[k, j, 1] = p[j][1]
    np.savez_compressed(npz, t=S["t"], xe=S["xe"], ye=S["ye"],
                        xc=S["xc_com"], sep=S["sep"], nce=S["nce"],
                        ncc=S["ncc"], pos_c=pb,
                        fin_u_e=r["fields"][0], fin_u_c=r["fields"][1])
    out["series"] = os.path.basename(npz)
    return out


DO = dict(engine_solo=do_engine_solo, cargo_solo=do_cargo_solo, tow=do_tow)


def do_deliver(job):
    """Two-phase delivery: phase1 tow (coupling eta), phase2 release
    (coupling eta2, default 0 = grip off; or engine stall dial dv115).
    Phase 2 continues from the exact phase-1 end fields."""
    L = job.get("L", 96.0); n = job.get("n", 3); spacing = job.get("spacing", 14.0)
    T1 = job.get("T1", 700.0); T2 = job.get("T2", 900.0)
    g1 = LB.build_world(job.get("coupling", "mimic"), job.get("eta", 0.6),
                        job.get("engine", "base"), job.get("cargo_mod"))
    rel = job.get("release", "eta0")
    if rel == "eta0":
        g2 = LB.build_world("none", 0.0, job.get("engine", "base"), job.get("cargo_mod"))
    elif rel == "dv115":
        g2 = LB.build_world(job.get("coupling", "mimic"), job.get("eta", 0.6),
                            job.get("engine", "base"), job.get("cargo_mod"))
        g2["chans"][LB.CH_VE]["D"] *= 1.15
    else:
        raise ValueError(rel)
    x_e = job.get("x_e", 10.0); x_c = job.get("x_c", 40.0)
    N = int(round(L / 0.5))
    F = G.state_vacuum(g1, N)
    F = LB.place_engine(F, g1, x_e, Y0, 0.5)
    axis = job.get("stack_axis", "x")
    for j in range(n):
        off = (j - (n - 1) / 2.0) * spacing
        if axis == "y":
            F = LB.place_cargo(F, g1, x_c, Y0 + off, 0.5)
        else:
            F = LB.place_cargo(F, g1, x_c + j * spacing, Y0, 0.5)
    r1 = G.run_genome(g1, F=F, L=L, T=T1, track_acts=[0, 1, 2],
                      noise=job.get("noise", 0.0), seed=job.get("seed", 0),
                      stop_explode_n=n + 4, save_fields=True)
    S1 = LB.sep_series(r1, n_cargo=n)
    out = dict(cls="deliver", status1=r1["status"],
               ncomp1_end=[int(r1["ncomp0"][-1]), int(r1["ncomp1"][-1]),
                           int(r1["ncomp2"][-1])])
    lock1 = MT.lock_analysis(S1["t"], S1["xe"], S1["xc_com"], S1["sep"],
                             S1["nce"], S1["ncc"], n)
    fin = np.isfinite(S1["xc_com"])
    out["phase1"] = dict(lock=lock1,
                         cargo_net_x=(float(S1["xc_com"][fin][-1] - S1["xc_com"][fin][0])
                                      if fin.sum() >= 2 else None))
    if r1["status"] != "ok" or r1["fields"] is None:
        out["status"] = r1["status"]; return out
    # phase 2 from exact end fields
    r2 = G.run_genome(g2, F=r1["fields"], L=L, T=T2, track_acts=[0, 1, 2],
                      noise=job.get("noise", 0.0), seed=job.get("seed", 0) + 100,
                      stop_explode_n=n + 4, save_fields=True)
    S2 = LB.sep_series(r2, n_cargo=n)
    out["status2"] = r2["status"]
    out["ncomp2_end"] = [int(r2["ncomp0"][-1]), int(r2["ncomp1"][-1]),
                         int(r2["ncomp2"][-1])]
    t2 = S2["t"]
    m_fin = (t2 >= t2[-1] - MT.POST_RELEASE_WIN) & np.isfinite(S2["xc_com"])
    if m_fin.sum() >= 3:
        seg_x = S2["xc_com"][m_fin]
        # per-record full-census COM positions (y too)
        coms = []
        for k, p in enumerate(r2["pos1"]):
            if len(p) == n and t2[k] >= t2[-1] - MT.POST_RELEASE_WIN:
                coms.append((np.mean([q[1] for q in p]), np.mean([q[0] for q in p])))
        drift = (float(np.hypot(coms[-1][0] - coms[0][0], coms[-1][1] - coms[0][1]))
                 if len(coms) >= 2 else None)
        # spacings at end: sort along stack axis, euclidean neighbor dists
        spac = []
        pend = r2["pos1"][-1]
        if len(pend) == n:
            ax = 0 if job.get("stack_axis", "x") == "y" else 1
            ps = sorted(pend, key=lambda p: p[ax])
            spac = [float(np.hypot(ps[j + 1][0] - ps[j][0],
                                   ps[j + 1][1] - ps[j][1]))
                    for j in range(n - 1)]
        out["release"] = dict(final_drift_px=drift, spacings_end=spac,
                              sep_engine_end=(float(S2["sep"][-1])
                                              if np.isfinite(S2["sep"][-1]) else None),
                              engine_alive=bool(r2["ncomp0"][-1] > 0))
    tag = job.get("name", "deliver")
    npz = os.path.join(HERE, "strips", f"{tag}.npz")
    np.savez_compressed(npz, t1=S1["t"], xe1=S1["xe"], xc1=S1["xc_com"],
                        sep1=S1["sep"], ncc1=S1["ncc"],
                        t2=S2["t"], xe2=S2["xe"], xc2=S2["xc_com"],
                        sep2=S2["sep"], ncc2=S2["ncc"],
                        fin_u_e=r2["fields"][0], fin_u_c=r2["fields"][1])
    out["series"] = os.path.basename(npz)
    out["wall_s"] = round(r1["wall_s"] + r2["wall_s"], 1)
    return out


DO["deliver"] = do_deliver


def do_assemble(job):
    """V3-1 sequential stack assembly: n_phase single-cargo pushes on one
    lane build a parked bonded chain (gap aim 14.0 -> d*=14.06 snap).
    Per phase: engine fields reset to vacuum (decoupled blocks are exactly
    transparent - zero cross W/K), fresh kicked engine at x_e, fresh cargo
    at x_pick; coupling ON; chunked integration until the NEWEST cargo
    (min-x blob) crosses its release x; then coupling OFF + settle.
    Gates measured: per-cargo displacement, chain census, final spacings,
    final-drift over last settle, engine transparency.
    """
    L = job.get("L", 96.0); N = int(round(L / 0.5))
    noise = job.get("noise", 0.0); seed = job.get("seed", 0)
    n_phase = job.get("n_phase", 3)
    x_pick = job.get("x_pick", 12.0); x_e0 = job.get("x_e", 2.0)
    x_front = job.get("x_front", 88.0); gap = job.get("gap", 14.0)
    T_settle = job.get("T_settle", 150.0); T_max = job.get("T_max", 900.0)
    g_on = LB.build_world(job.get("coupling", "mimic"), job.get("eta", 0.6),
                          job.get("engine", "base"), job.get("cargo_mod"))
    g_off = LB.build_world("none", 0.0, job.get("engine", "base"),
                           job.get("cargo_mod"))
    na = len(g_on["acts"])
    aC = g_on["acts"][LB.ACT_C]
    thr_c = aC["u0"] + 0.45 * (np.sqrt(aC["lam"]) - aC["u0"])
    aE = g_on["acts"][LB.ACT_E]
    thr_e = aE["u0"] + 0.45 * (np.sqrt(aE["lam"]) - aE["u0"])

    def cargo_xs(F):
        bl = G.blob_list(F[LB.ACT_C], thr_c, 0.5, L)
        return sorted(b["x"] for b in bl), len(bl)

    F = G.state_vacuum(g_on, N)
    phases = []
    t_glob = 0.0
    sim_wall = 0.0
    status = "ok"
    for ph in range(n_phase):
        # release target
        if ph == 0:
            x_rel = x_front
        else:
            x_rel = phases[-1]["parked_xs"][0] - gap  # leftmost parked - gap
        # engine reset + fresh pokes
        F[LB.ACT_E] = aE["u0"]
        F[na + LB.CH_VE] = 0.0
        F[na + LB.CH_WE] = 0.0
        F = LB.place_engine(F, g_on, x_e0, Y0, 0.5)
        F = LB.place_cargo(F, g_on, x_pick, Y0, 0.5)
        t_ph = 0.0
        crossed = False
        while t_ph < T_max:
            xs, ncc = cargo_xs(F)
            newest = xs[0] if xs else None
            chunk = (25.0 if (newest is None or newest < x_rel - 15.0)
                     else (10.0 if newest < x_rel - 8.0 else 2.5))
            r = G.run_genome(g_on, F=F, L=L, T=chunk, dx=0.5, rec_tu=chunk,
                             noise=noise, seed=seed + int(t_glob * 7) % 9973,
                             track_acts=[1], stop_all_dead=False,
                             save_fields=True)
            sim_wall += r["wall_s"]
            F = r["fields"]; t_ph += chunk; t_glob += chunk
            if r["status"] != "ok":
                status = f"ph{ph}_{r['status']}"; break
            xs, ncc = cargo_xs(F)
            if ncc != ph + 1:
                status = f"ph{ph}_census_{ncc}"; break
            if xs and xs[0] >= x_rel:
                crossed = True; break
        if status != "ok":
            break
        if not crossed:
            status = f"ph{ph}_timeout"; break
        # release: coupling off, settle
        xs_before = cargo_xs(F)[0]
        r = G.run_genome(g_off, F=F, L=L, T=T_settle, dx=0.5, rec_tu=T_settle,
                         noise=noise, seed=seed + 31 * ph,
                         track_acts=[1], stop_all_dead=False, save_fields=True)
        sim_wall += r["wall_s"]
        F = r["fields"]; t_glob += T_settle
        xs_park, ncc = cargo_xs(F)
        phases.append(dict(ph=ph, t_tow=round(t_ph, 1), x_rel=round(x_rel, 2),
                           xs_at_release=[round(x, 2) for x in xs_before],
                           parked_xs=[round(x, 2) for x in xs_park],
                           ncc=ncc))
        if ncc != ph + 1:
            status = f"ph{ph}_settle_census_{ncc}"; break
    out = dict(cls="assemble", status=status, phases=phases,
               t_total=round(t_glob, 1), sim_wall=round(sim_wall, 1))
    if status == "ok" and len(phases) == n_phase:
        # final verification hold: 800 tu decoupled + hold noise (park gate)
        xs0 = phases[-1]["parked_xs"]
        r = G.run_genome(g_off, F=F, L=L, T=job.get("T_hold", 800.0), dx=0.5,
                         rec_tu=job.get("T_hold", 800.0),
                         noise=job.get("noise_hold", noise), seed=seed + 777,
                         track_acts=[1], stop_all_dead=False, save_fields=True)
        sim_wall += r["wall_s"]; F = r["fields"]
        xs1, ncc1 = cargo_xs(F)
        drift = (max(abs(a - b) for a, b in zip(xs0, xs1))
                 if (len(xs0) == len(xs1)) else None)
        spac = [round(xs1[j + 1] - xs1[j], 2) for j in range(len(xs1) - 1)]
        disp = [round(x - x_pick, 1) for x in xs1]
        out["final"] = dict(ncc=ncc1, xs=[round(x, 2) for x in xs1],
                            spacings=spac, hold_drift_px=drift,
                            displacements=disp,
                            com_displacement=round(float(np.mean(disp)), 1))
        eng_bl = G.blob_list(F[LB.ACT_E], thr_e, 0.5, L)
        out["final"]["engine_alive"] = len(eng_bl) > 0
        out["final"]["engine_x"] = ([round(b["x"], 1) for b in eng_bl][:2])
        tag = job.get("name", "asm")
        np.savez_compressed(os.path.join(HERE, "strips", f"{tag}_final.npz"),
                            u_e=F[LB.ACT_E], u_c=F[LB.ACT_C])
    return out


DO["assemble"] = do_assemble




def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", required=True)
    ap.add_argument("--tag", default="")
    args = ap.parse_args()
    jobs = json.load(open(args.jobs))
    for k, job in enumerate(jobs):
        t0 = time.time()
        rec = dict(kind=job["kind"], name=job.get("name"),
                   job={k2: v for k2, v in job.items() if k2 not in ("kind", "name")},
                   batch=args.tag)
        try:
            rec.update(DO[job["kind"]](job))
        except Exception as e:
            import traceback
            rec["status"] = "error"; rec["err"] = repr(e)
            rec["tb"] = traceback.format_exc()[-1500:]
        rec["wall_s_total"] = round(time.time() - t0, 1)
        nrec = LB.append(rec)
        print(f"[{k + 1}/{len(jobs)}] {job.get('name')} -> "
              f"{rec.get('cls', rec['status'])} status={rec.get('status')} "
              f"({rec['wall_s_total']}s, results n={nrec})", flush=True)


if __name__ == "__main__":
    main()
