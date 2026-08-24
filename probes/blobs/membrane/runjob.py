"""runjob.py — membrane job driver. Usage: python runjob.py '<json-spec>'

Job kinds:
  smoke_bind   A5 pair anchor (binding d*=15.70 +- 0.02)
  smoke_travel M4 traveling-bond anchor (tau=6: c=0.1408, sep=14.78)
  smoke_rotor  xv rotor anchor (tau1=5.7 eta=0.1: |omega|~0.0111)
  ring         single-species N-ring (family A5 | A4s), G_RING evaluation
  xvring       alternating A-B ring (cross-bond braced)
  barrier      cargo kick probe at membrane wall (init_from ring state)
  cargo        cargo-in-cell longrun (G_CARGO)
  push         motile cargo inside membrane (R4)

Every job: appends one record to results.json (fcntl-locked), saves track npz
(data/<name>_track.npz) and final state (data/<name>_final.npz). SAVE-AS-YOU-GO.
"""
import json, os, sys
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import sim
import metrics as mx

FAM = dict(
    A5=dict(tau=2.5, Dv=2.0, stamp="stamp_P7s_dx05.npz", dstar=15.70),
    A4s=dict(tau=2.5, Dv=1.6, stamp="stamp_A4_dx05.npz", dstar=15.40),
)


def save_track(name, r, extra=None):
    n1 = max((len(p) for p in r["pos1"]), default=0)
    P1 = np.full((len(r["pos1"]), n1, 2), np.nan)
    for i, p in enumerate(r["pos1"]):
        P1[i, :len(p)] = p
    kw = dict(t=r["t"], P1=P1, ncomp1=r["ncomp1"],
              area1=np.array([a + [np.nan] * (n1 - len(a)) for a in r["area1"]])
              if n1 else np.zeros((0, 0)))
    if r.get("two"):
        n2 = max((len(p) for p in r["pos2"]), default=0)
        P2 = np.full((len(r["pos2"]), n2, 2), np.nan)
        for i, p in enumerate(r["pos2"]):
            P2[i, :len(p)] = p
        kw.update(P2=P2, ncomp2=r["ncomp2"],
                  area2=np.array([a + [np.nan] * (n2 - len(a)) for a in r["area2"]])
                  if n2 else np.zeros((0, 0)))
    np.savez_compressed(os.path.join(BASE, "data", name + "_track.npz"), **kw)
    if r["fields"] is not None:
        np.savez_compressed(os.path.join(BASE, "data", name + "_final.npz"),
                            F=r["fields"].astype(np.float32), **(extra or {}))
    for tt, S in r.get("snaps", {}).items():
        np.savez_compressed(os.path.join(BASE, "data",
                            f"{name}_snap{int(tt):05d}.npz"),
                            F=S.astype(np.float32))
    if r.get("film"):
        fl = r["film"]
        np.savez_compressed(os.path.join(BASE, "data", name + "_film.npz"),
                            t=fl["t"], u1=fl["u1"],
                            **({"u2": fl["u2"]} if fl["u2"] is not None else {}))


def tail_speed(t, P, frac=0.35):
    """Speed from unwrapped positions over the last frac of the run."""
    t = np.asarray(t); n = len(t)
    i0 = int(n * (1 - frac))
    dp = P[-1] - P[i0]
    return float(np.hypot(*dp) / (t[-1] - t[i0]))


def main(spec):
    kind = spec["kind"]
    name = spec["name"]
    rec = dict(kind=kind, name=name, spec=spec)

    if kind == "smoke_bind":
        f = FAM["A5"]
        d0 = spec.get("d0", 16.5)
        L = spec.get("L", 96.0)
        c = L / 2
        r = sim.run(tau1=f["tau"], Dv1=f["Dv"], stamp1_name=f["stamp"],
                    L=L, T=spec.get("T", 2500.0),
                    blobs1=[(c - d0 / 2, c, None), (c + d0 / 2, c, None)],
                    rec_tu=10.0, save_fields=False)
        P = np.array([p for p in r["pos1"]])
        sep = np.hypot(*(P[:, 1] - P[:, 0]).T)
        rec.update(status=r["status"], d_final=float(sep[-1]),
                   d_last100=float(sep[np.asarray(r["t"]) >= r["t"][-1] - 100].mean()),
                   ncomp_final=int(r["ncomp1"][-1]), tu_per_s=r["tu_per_s"])

    elif kind == "smoke_travel":
        tau = spec.get("tau", 6.0)
        L = 96.0; c = L / 2; d0 = 15.0
        r = sim.run(tau1=tau, Dv1=4.0 / tau, stamp1_name="stamp_A4_dx05.npz",
                    L=L, T=spec.get("T", 1500.0),
                    blobs1=[(c - d0 / 2, c, (0.0, 0.5)), (c + d0 / 2, c, (0.0, 0.5))],
                    rec_tu=10.0, save_fields=False)
        P = np.array([p for p in r["pos1"]])
        sep = np.hypot(*(P[:, 1] - P[:, 0]).T)
        com = P.mean(axis=1)
        rec.update(status=r["status"], c=tail_speed(r["t"], com),
                   sep_final=float(sep[-1]), ncomp_final=int(r["ncomp1"][-1]),
                   tu_per_s=r["tu_per_s"])

    elif kind == "smoke_rotor":
        L = 96.0; c = L / 2; d0 = 8.0
        r = sim.run(tau1=5.7, tau2=2.5, eta12=0.1, eta21=0.1,
                    stamp1_name="stamp_A4_dx05.npz", stamp2_name="stamp_A4_dx05.npz",
                    L=L, T=spec.get("T", 3000.0),
                    blobs1=[(c + d0, c, (90.0, 0.5))], blobs2=[(c, c, None)],
                    rec_tu=5.0, save_fields=False)
        P1 = np.array([p[0] for p in r["pos1"]])
        P2 = np.array([p[0] for p in r["pos2"]])
        d = P1 - P2
        th = np.unwrap(np.arctan2(d[:, 0], d[:, 1]))
        t = np.asarray(r["t"]); m = t >= t[-1] - 1000.0
        om = np.polyfit(t[m], th[m], 1)[0]
        rec.update(status=r["status"], omega=float(om),
                   sep_final=float(np.hypot(*d[-1])),
                   ncomp=[int(r["ncomp1"][-1]), int(r["ncomp2"][-1])],
                   tu_per_s=r["tu_per_s"])

    elif kind == "ring":
        f = FAM[spec["fam"]]
        N = spec["N"]
        dstar = spec.get("dstar", f["dstar"])
        R0 = spec.get("R0", dstar / (2 * np.sin(np.pi / N)))
        L = spec.get("L", 96.0); dx = spec.get("dx", 0.5)
        c = L / 2
        pos = sim.ring_positions(N, R0, c, c, spec.get("phase", 0.0))
        r = sim.run(tau1=f["tau"], Dv1=f["Dv"], stamp1_name=f["stamp"],
                    L=L, dx=dx, T=spec.get("T", 5000.0), dt=spec.get("dt", 0.02),
                    blobs1=[(x, y, None) for (x, y) in pos],
                    noise=spec.get("noise", 0.0), seed=spec.get("seed", 0),
                    rec_tu=spec.get("rec_tu", 10.0),
                    stop_split=spec.get("stop_split", False),
                    save_fields=True,
                    snap_times=spec.get("snap_times", ()))
        v = mx.ring_timeseries_verdict(r["t"], r["pos1"], L, N,
                                       T_min=spec.get("T", 5000.0))
        last = mx.ring_record_check(r["pos1"][-1], L, N)
        rec.update(status=r["status"], R0=float(R0), verdict=v,
                   final=last, ncomp_final=int(r["ncomp1"][-1]),
                   ncomp_max=int(r["ncomp1"].max()),
                   ncomp_min=int(r["ncomp1"].min()),
                   area_final=(float(np.mean(r["area1"][-1]))
                               if r["area1"][-1] else None),
                   tu_per_s=r["tu_per_s"])
        save_track(name, r)

    elif kind == "xvring":
        Nh = spec["Nhalf"]
        dcross = spec.get("dcross", 7.976)
        Ntot = 2 * Nh
        R0 = spec.get("R0", dcross / (2 * np.sin(np.pi / Ntot)))
        L = spec.get("L", 96.0); c = L / 2
        pos = sim.ring_positions(Ntot, R0, c, c, spec.get("phase", 0.0))
        b1 = [(x, y, None) for (x, y) in pos[0::2]]
        b2 = [(x, y, None) for (x, y) in pos[1::2]]
        eta = spec.get("eta", 0.05)
        r = sim.run(tau1=2.5, tau2=2.5, Dv1=1.6, Dv2=1.6,
                    eta12=eta, eta21=eta,
                    stamp1_name="stamp_A4_dx05.npz", stamp2_name="stamp_A4_dx05.npz",
                    L=L, T=spec.get("T", 5000.0),
                    blobs1=b1, blobs2=b2,
                    noise=spec.get("noise", 0.0), seed=spec.get("seed", 0),
                    rec_tu=10.0, stop_split=False, save_fields=True)
        v = mx.xvring_timeseries_verdict(r["t"], r["pos1"], r["pos2"], L, Nh,
                                         T_min=spec.get("T", 5000.0))
        rec.update(status=r["status"], R0=float(R0), verdict=v,
                   ncomp_final=[int(r["ncomp1"][-1]), int(r["ncomp2"][-1])],
                   tu_per_s=r["tu_per_s"])
        save_track(name, r)

    elif kind in ("barrier", "cargo", "push"):
        L = spec.get("L", 96.0); c = L / 2
        cargo = spec["cargo"]              # dict(x,y,kick,tau)
        tau1 = cargo.get("tau", 2.5)
        Dv1 = cargo.get("Dv", 4.0 / tau1)
        kick = cargo.get("kick")
        r = sim.run(tau1=tau1, tau2=spec.get("tau2", 2.5),
                    Dv1=Dv1, Dv2=spec.get("Dv2", 1.6),
                    eta12=spec.get("eta12", 0.05), eta21=spec.get("eta21", 0.0),
                    etaw12=spec.get("etaw12", 0.0), etaw21=spec.get("etaw21", 0.0),
                    adia_w1=spec.get("adia_w1", False),
                    prerelax_tu=spec.get("prerelax_tu", 0.0),
                    ramp_tu=spec.get("ramp_tu", 0.0),
                    film_tu=spec.get("film_tu", 0.0),
                    stamp1_name=cargo.get("stamp", "stamp_A4_dx05.npz"),
                    stamp2_name=spec.get("stamp2", "stamp_A4_dx05.npz"),
                    L=L, T=spec.get("T", 2000.0),
                    init_from=spec["ring_state"], init_slot=2,
                    add_blobs1=[(cargo["x"], cargo["y"],
                                 tuple(kick) if kick else None)],
                    noise=spec.get("noise", 0.0), seed=spec.get("seed", 0),
                    rec_tu=5.0, stop_split=False, save_fields=True,
                    n1_expect=1, n2_expect=spec["N"],
                    snap_times=spec.get("snap_times", ()))
        # analysis: cargo radius vs membrane ring
        t = np.asarray(r["t"])
        rc, Rw, closed = [], [], []
        for p1, p2 in zip(r["pos1"], r["pos2"]):
            if len(p2) == spec["N"]:
                st = mx.ring_stats(p2, L)
                C = np.array(st["C"]); Rw.append(st["R_mean"])
                chk = mx.ring_record_check(p2, L, spec["N"])
                closed.append(bool(chk["cycle"]))
            else:
                C = np.array([c, c]); Rw.append(np.nan); closed.append(False)
            if len(p1) >= 1:
                d = mx.minimg(np.asarray(p1[0]) - C, L)
                rc.append(float(np.hypot(*d)))
            else:
                rc.append(np.nan)
        rc = np.array(rc); Rw = np.array(Rw)
        Rwall = float(np.nanmedian(Rw))
        cls = mx.classify_barrier(t, rc, Rwall) if kind == "barrier" else None
        confined = bool(np.all(rc[~np.isnan(rc)] < Rw[~np.isnan(rc)]))
        rec.update(status=r["status"], Rwall=Rwall, outcome=cls,
                   rc_first=float(rc[0]), rc_final=float(rc[-1]),
                   rc_max=float(np.nanmax(rc)), rc_min=float(np.nanmin(rc)),
                   closed_frac=float(np.mean(closed)),
                   ring_closed_all=bool(all(closed[i] for i in range(len(closed))
                                            if t[i] >= mx.T_TRANS)),
                   cargo_alive=bool(np.all(r["ncomp1"] == 1)),
                   ring_ncomp_ok=bool(np.all(r["ncomp2"] == spec["N"])),
                   confined=confined, tu_per_s=r["tu_per_s"])
        save_track(name, r)
        np.savez_compressed(os.path.join(BASE, "data", name + "_probe.npz"),
                            t=t, rc=rc, Rw=Rw,
                            closed=np.array(closed, bool))

    else:
        raise ValueError(kind)

    n = sim.append_result(rec)
    print(json.dumps(dict(name=name, kind=kind, nrec=n,
                          **{k: rec.get(k) for k in
                             ("status", "verdict", "outcome", "c", "omega",
                              "d_final", "confined") if k in rec})))


if __name__ == "__main__":
    arg = sys.argv[1]
    if arg.startswith("@"):
        with open(arg[1:]) as f:
            main(json.load(f))
    else:
        main(json.loads(arg))
