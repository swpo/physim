"""assay_v3.py — v3 Track B assay glue (2026-08-31). NEW module per relock
protocol: composes the LOCKED soup_sim_v2 + metrics_v2 + assay_v2 machinery
(imported verbatim, never edited) with metrics_v3 (C9/d7b).

Differences vs assay_v2.run_assay (all additive):
 1. Advances in SUB-CHUNKS (default 500tu) and keeps a rolling buffer of
    FULL-field snapshots (activators + channels, f32) from the trailing
    window — metrics_v3.s9 needs coupling-term flux maps, and the locked
    recorder only stores act-only snaps at t=0/250. Chunked continuation is
    parity-gated bitwise-identical to one long run, so scores are unchanged.
 2. ic_override: optional (na+nc, N, N) array replacing the soup IC after
    init_soup (data-level hook on the returned state dict S; S["F"] is a
    documented mutable field — no locked-file edit). Used by
    operators_v3.merge_spatial_ic offspring and hand-built bank worlds.
 3. n_soup / noise passthrough to init_soup (bank-c anti-gaming probes).
 4. Decision rule: assay_v2's horizon_criteria VERBATIM (imported), same
    extend ladder, same c_acf one-doubling cap.
Return dict = metrics_v3.full_battery_v3 output + horizon (same layout as
assay_v2) + summary (lean_summary_v3).

Error contract (ASSAY_V2_API lesson, guard now lives at THIS layer): a
subcritical genome that dies before BURN gives an empty post-burn window and
locked metrics_v1.d2 crashes; run_assay catches that and returns a scored-0
stub (status="no_blobs", interest 0, C9 0) instead of propagating.
"""
import argparse, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stage2", "lib"))
import soup_sim_v2 as SS2
import metrics_v2 as MV2
import metrics_v3 as MV3
import assay_v2 as AV2
import genome as G

T0_DEFAULT, T_CAP = 2500.0, 20000.0
SNAP_DT = 500.0        # full-field capture cadence (tu)
NSNAP_KEEP = 6         # rolling buffer length (trailing window)


def _capture(S, buf_t, buf_F):
    """Append a full-field f32 snapshot of the current state."""
    buf_t.append(S["t_step"] * S["dt"])
    buf_F.append(np.asarray(S["F"], np.float32).copy())
    while len(buf_t) > NSNAP_KEEP:
        buf_t.pop(0)
        buf_F.pop(0)


def _void_masks(fsnaps, rec):
    """Effective-void masks (True = void) from full snapshots: union act
    support at thr_a, dilated by the VOID_DILATE_PX skirt."""
    na = rec["na"]
    thr_a = np.asarray(rec["thr"], float)
    dil = int(round(MV3.VOID_DILATE_PX / 0.5))
    masks, raw = [], []
    for F in fsnaps["F"]:
        m = MV3.support_mask(np.asarray(F[:na]), thr_a)
        raw.append(1.0 - m.mean())
        masks.append(~MV3._wrap_binary(m, "dil", dil))
    return masks, (float(np.mean(raw)) if raw else None)


def _dead_stub(rec, why, t_wall0):
    """Scored-0 stub for worlds whose record cannot support the battery."""
    d9 = dict(C9=0.0, factors=dict(t9=0.0, s9=None, e9=0.0, r9=0.0),
              partial=True, spatial_class="mixed", alive=False)
    return dict(D=dict(d9=d9), C=dict(C9_spatial=0.0), interest=0.0,
                interest_v2=0.0, spatial_class="mixed", status=why,
                horizon=dict(T_used=rec["T"], why_stopped=why,
                             n_extensions=0, decisions=[],
                             interest_trajectory=[],
                             wall_total=round(time.time() - t_wall0, 1)),
                flags=dict(box_limit=None, box_span_frac=None,
                           box_persist=None),
                summary=dict(interest=0.0, status=why,
                             d9=dict(C9=0.0, cls="mixed")))


def run_assay(genome, seed=1, L=128.0, workers=2, t0=T0_DEFAULT, cap=T_CAP,
              tag=None, save_npz=None, kicks=None, verbose=True,
              ic_override=None, n_soup=None, noise=None, snap_dt=SNAP_DT):
    """Adaptive-horizon v3 assay. Returns battery_v3 dict + horizon."""
    t_wall0 = time.time()
    tag = tag or genome.get("id", "anon")
    kw = dict(L=L, seed=seed, workers=workers)
    if kicks is not None:
        kw["kicks"] = kicks
    if n_soup is not None:
        kw["n_soup"] = int(n_soup)
    if noise is not None:
        kw["noise"] = float(noise)
    S = SS2.init_soup(genome, **kw)
    if ic_override is not None:
        ic = np.asarray(ic_override)
        assert ic.shape == S["F"].shape, (ic.shape, S["F"].shape)
        S["F"] = ic.astype(S["fdt"])
    T = float(t0)
    buf_t, buf_F = [], []
    traj, decisions = [], []
    n_ext, c_used = 0, 0
    why = None
    out2 = None
    while True:
        # ---- advance to T in sub-chunks, capturing full snapshots
        status = S["status"]
        t_now = S["t_step"] * S["dt"]
        subs = np.arange(np.floor(t_now / snap_dt) * snap_dt + snap_dt,
                         T + 1e-9, snap_dt)
        subs = [float(x) for x in subs if x > t_now + 1e-9]
        if not subs or subs[-1] < T - 1e-9:
            subs = subs + [T]
        for Ts in subs:
            status = SS2.advance(S, Ts)
            if status != "ok":
                break
            _capture(S, buf_t, buf_F)
        rec = SS2.snapshot_rec(S)
        if status != "ok":
            why = status
            break
        rec_used = dict(rec)
        try:
            out2 = MV2.full_battery(rec_used, genome=genome)
        except Exception as e:
            msg = repr(e)
            if "non-empty vector" in msg or "empty slice" in msg:
                return _dead_stub(rec, why="no_blobs", t_wall0=t_wall0)
            raise
        traj.append((rec["T"], round(out2["interest"], 2)))
        crit = AV2.horizon_criteria(rec, genome, D=out2["D"])
        fired = [k for k in ("a_mem", "b_org", "c_acf") if crit[k]]
        decisions.append(dict(T=T, fired=fired, detail=crit["detail"]))
        if verbose:
            print(f"[assay_v3 {tag} s{seed}] T={T:.0f} "
                  f"interest_v2={out2['interest']:.1f} fired={fired}",
                  flush=True)
        if not fired:
            why = "converged" if n_ext else "static"
            break
        if T >= cap:
            why = "cap"
            break
        if fired == ["c_acf"]:
            if c_used >= 1:
                why = "converged"
                break
            c_used += 1
        T = min(T * 2, cap)
        n_ext += 1
    rec = SS2.snapshot_rec(S)
    if out2 is None or (traj and rec["T"] != traj[-1][0]) or not traj:
        rec_used = dict(rec)
        try:
            out2 = MV2.full_battery(rec_used, genome=genome)
        except Exception as e:
            msg = repr(e)
            if "non-empty vector" in msg or "empty slice" in msg:
                return _dead_stub(rec, why=(why or "no_blobs"),
                                  t_wall0=t_wall0)
            raise
        traj.append((rec["T"], round(out2["interest"], 2)))
    # ---- v3 extension on the final record (reuse the battery's record copy:
    # _tracks and attached series already built at the final T)
    fsnaps = dict(t=list(buf_t), F=list(buf_F))
    rec3 = rec_used
    vm = None
    if buf_F:
        vm, _ = _void_masks(fsnaps, rec)
    out = MV3.full_battery_v3(rec3, genome=genome, fsnaps=fsnaps,
                              v2_out=out2, void_masks=vm,
                              void_mask_ts=(list(buf_t) if vm else None))
    out["horizon"] = dict(T_used=rec["T"], why_stopped=why,
                          n_extensions=n_ext, decisions=decisions,
                          interest_trajectory=traj,
                          wall_total=round(time.time() - t_wall0, 1))
    out["flags"] = MV2.box_flag(rec3)
    out["summary"] = MV3.lean_summary_v3(out)
    out["summary"]["horizon"] = dict(T_used=rec["T"], why=why, next=n_ext)
    if save_npz:
        SS2.save_run(rec, save_npz)
    return out


def main():
    sys.path.insert(0, HERE)
    import worlds
    ap = argparse.ArgumentParser()
    ap.add_argument("world")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--L", type=float, default=128.0)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--t0", type=float, default=T0_DEFAULT)
    ap.add_argument("--cap", type=float, default=T_CAP)
    ap.add_argument("--tag", default=None)
    a = ap.parse_args()
    if a.world in worlds.WORLDS:
        g = worlds.WORLDS[a.world]()
        kicks = worlds.KICKS.get(g["id"])
    else:
        g = json.load(open(a.world))
        g = g.get("genome", g)
        kicks = None
    out = run_assay(g, seed=a.seed, L=a.L, workers=a.workers, t0=a.t0,
                    cap=a.cap, tag=a.tag or g.get("id"), kicks=kicks)
    d9 = out["D"]["d9"]
    print(json.dumps(AV2.js(dict(
        tag=a.tag or g.get("id"), seed=a.seed,
        interest_v2=out["interest_v2"], interest_v3=out["interest"],
        C9=d9["C9"], cls=d9["spatial_class"], factors=d9["factors"],
        partial=d9["partial"], T=out["horizon"]["T_used"],
        why=out["horizon"]["why_stopped"]))))


if __name__ == "__main__":
    main()
