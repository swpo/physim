"""assay_v2b.py — backend-injected entry to the LOCKED adaptive-horizon assay.

blobkit 0.2 (L3 science layer). run_assay_b is a VERBATIM port of
assay_v2.run_assay (LOCKED, 2026-02-25 — see its docstring for the horizon
rules) with exactly one change: the simulator namespace is injected instead of
hard-bound to blobkit.soup.sim_cpu. Every decision rule, constant, and call
order is identical; G1 (verify_v02/) gates bit-identical battery + horizon
vs the locked run_assay on the CPU backend.

    backend = blobkit.soup.backend.get_backend("cpu"|"gpu")
    ns contract: init_soup(g, L=, seed=, workers=, kicks=) -> S
                 advance(S, T_target) -> status
                 snapshot_rec(S) -> record dict
                 save_run(rec, path)

run_assay_b(genome)                    == locked CPU assay (backend=None)
run_assay_b(genome, backend=gpu_ns)    == same science, GPU kernel
run_assay_gpu(genome, **kw)            == convenience for the line above

assay_v2.py itself stays LOCKED and untouched; this module is the 0.2
injection seam (interface = the 4-function namespace, kernels prove equality
via parity gates, science stays single-copy here).
"""
import time

from . import metrics_v2 as MV2
from . import genome as G
from .assay_v2 import (RESULTS, T0_DEFAULT, T_CAP, js, horizon_criteria)
from .soup.backend import get_backend


def run_assay_b(genome, seed=1, L=128.0, workers=2, t0=T0_DEFAULT, cap=T_CAP,
                tag=None, results_path=RESULTS, save_npz=None, kicks=None,
                verbose=True, backend=None):
    """Adaptive-horizon assay with injected sim backend (None -> locked CPU).
    Returns metrics_v2 battery dict + horizon — same contract as
    assay_v2.run_assay."""
    SS2 = backend or get_backend("cpu")
    t_wall0 = time.time()
    tag = tag or genome.get("id", "anon")
    S = SS2.init_soup(genome, L=L, seed=seed, workers=workers, kicks=kicks)
    T = float(t0)
    traj, decisions = [], []
    n_ext, c_used = 0, 0
    why = None
    out = None
    while True:
        status = SS2.advance(S, T)
        rec = SS2.snapshot_rec(S)
        if status != "ok":
            why = status
            break
        # battery at every decision point (checkpoint score + d2 for crit c)
        out = MV2.full_battery(dict(rec), genome=genome)
        traj.append((rec["T"], round(out["interest"], 2)))
        crit = horizon_criteria(rec, genome, D=out["D"])
        fired = [k for k in ("a_mem", "b_org", "c_acf") if crit[k]]
        decisions.append(dict(T=T, fired=fired,
                              detail=crit["detail"]))
        if verbose:
            print(f"[assay_v2b {tag} s{seed}] T={T:.0f} "
                  f"interest={out['interest']:.1f} fired={fired}", flush=True)
        if not fired:
            why = "converged" if n_ext else "static"
            break
        if T >= cap:
            why = "cap"
            break
        # criterion (c) alone grants at most ONE doubling
        if fired == ["c_acf"]:
            if c_used >= 1:
                why = "converged"
                break
            c_used += 1
        T = min(T * 2, cap)
        n_ext += 1
    rec = SS2.snapshot_rec(S)
    if out is None or rec["T"] != traj[-1][0]:
        out = MV2.full_battery(dict(rec), genome=genome)
        traj.append((rec["T"], round(out["interest"], 2)))
    out["horizon"] = dict(T_used=rec["T"], why_stopped=why,
                          n_extensions=n_ext, decisions=decisions,
                          interest_trajectory=traj,
                          wall_total=round(time.time() - t_wall0, 1))
    out["summary"] = MV2.lean_summary(out)
    out["summary"]["horizon"] = dict(T_used=rec["T"], why=why, next=n_ext)
    if save_npz:
        SS2.save_run(rec, save_npz)
    if results_path:
        row = dict(kind="assay_v2", world=genome.get("id"), tag=f"v2_{tag}",
                   seed=seed, T=rec["T"], L=L, dtype=rec["dtype"],
                   status=rec["status"], wall_sim=rec["wall_s"],
                   wall_total=round(time.time() - t_wall0, 1),
                   metrics="metrics_v2", horizon=js(out["horizon"]),
                   battery=js(dict(C=out["C"], interest=out["interest"],
                                   flags=out["flags"])),
                   summary=js(out["summary"]))
        row["backend"] = SS2.name
        G.append_result(row, path=results_path)
    return out


def run_assay_gpu(genome, **kw):
    """run_assay_b on the GPU backend (requires jax; pip install 'blobkit[gpu]').

    Same science, GPU kernel. GPU noise is a different RNG stream than CPU
    (same law) -> scores are seed-level equivalent, not bitwise (GATES.md)."""
    kw.pop("backend", None)
    return run_assay_b(genome, backend=get_backend("gpu"), **kw)
