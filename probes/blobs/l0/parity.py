"""parity.py — PARITY GATES: the four reference genomes must reproduce certified
behavior in the L0 generic simulator BEFORE any sampling. Appends to results.json.

Gates (certified numbers from probes/blobs/PROGRAM.md):
  P-M0    : poke -> 1 blob, area 26-28 at dx=0.5, persists 2000 tu.
  P-XV    : rotor ref (tau1=5.7,tau2=2.5,eta=0.1,d0=8, tangential kick):
            |omega| in [0.0100, 0.0122] (cert 0.01106-0.01111 +-10%%), sep~8.44.
  P-VVW   : species B blob (act1) persists 1000 tu at dx=0.5 (continuum-clean per
            M5-prep); species A NOT gated (documented labyrinth caveat at dx=0.5).
  P-BF0   : bfield genome, gamma=0: M4-family blob at tau=5.7 parked (|c|<0.005,
            below single-blob drift threshold 5.748), alive 400 tu.
  P-BF5   : gamma=0.05: SELF-LAUNCH, c within 20%% of law 0.209*0.05^0.341=0.0752.
"""
import sys, os, json, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "lib"))
import genome as G


def com_speed(r, i, win_tu, rec_tu):
    """Speed from unwrapped positions of act i over the last win_tu."""
    pos = [p[0] for p, n in zip(r[f"pos{i}"], r[f"ncomp{i}"]) if n >= 1 and len(p)]
    t = [tt for tt, n in zip(r["t"], r[f"ncomp{i}"]) if n >= 1]
    if len(pos) < 3:
        return None
    pos = np.array(pos); t = np.array(t)
    m = t >= t[-1] - win_tu
    if m.sum() < 3:
        return None
    cy = np.polyfit(t[m], pos[m, 0], 1)[0]
    cx = np.polyfit(t[m], pos[m, 1], 1)[0]
    return float(np.hypot(cy, cx))


def p_m0():
    g = G.ref_M0()
    N = int(round(96 / 0.5))
    F = G.state_vacuum(g, N)
    F = G.poke(F, g, 0, 48.0, 48.0, 2.0, 3.0, 0.5)
    r = G.run_genome(g, F=F, T=2000.0, rec_tu=20.0)
    a = [x[0] if x else 0.0 for x in r["area0"]]
    ok = (r["status"] == "ok" and r["ncomp0"][-1] == 1
          and 24.0 <= a[-1] <= 30.0 and max(r["ncomp0"][4:]) == 1)
    return dict(gate="P-M0", passed=bool(ok), status=r["status"],
                area_end=a[-1], ncomp_max=int(max(r["ncomp0"][4:])),
                wall_s=round(r["wall_s"], 1), tu_per_s=round(r["tu_per_s"], 2))


def p_xv():
    g = G.ref_XV(tau1=5.7, tau2=2.5, eta12=0.1, eta21=0.1)
    N = int(round(96 / 0.5))
    F = G.state_vacuum(g, N)
    st = G.load_stamp_A4()
    # S (act1) at center, M (act0) at d0=8 to the right; M kicked tangentially
    # (90 deg, kd=0.5): v,w stamp displaced 0.5 OPPOSITE +y.
    G.paste_stamp(F, dict(du=st["du"]), {"du": 1}, 48.0, 48.0, 0.5)
    G.paste_stamp(F, dict(dv=st["dv"], dw=st["dw"]), {"dv": 3, "dw": 5}, 48.0, 48.0, 0.5)
    G.paste_stamp(F, dict(du=st["du"]), {"du": 0}, 56.0, 48.0, 0.5)
    G.paste_stamp(F, dict(dv=st["dv"], dw=st["dw"]), {"dv": 2, "dw": 4}, 56.0, 47.5, 0.5)
    r = G.run_genome(g, F=F, T=1500.0, rec_tu=5.0,
                     ref_pos={0: [(56.0, 48.0)], 1: [(48.0, 48.0)]})
    if r["status"] != "ok":
        return dict(gate="P-XV", passed=False, status=r["status"])
    t = np.array(r["t"]); n1 = r["ncomp0"]; n2 = r["ncomp1"]
    phis, seps, tt2 = [], [], []
    for i in range(len(t)):
        if n1[i] == 1 and n2[i] == 1:
            d = r["pos0"][i][0] - r["pos1"][i][0]
            phis.append(np.arctan2(d[0], d[1])); seps.append(np.hypot(*d))
            tt2.append(t[i])
    phis = np.unwrap(np.array(phis)); tt2 = np.array(tt2); seps = np.array(seps)
    m = tt2 >= tt2[-1] - 300.0
    om = float(np.polyfit(tt2[m], phis[m], 1)[0])
    sep_m = float(seps[m].mean())
    ok = 0.0100 <= abs(om) <= 0.0122 and abs(sep_m - 8.44) < 0.3
    return dict(gate="P-XV", passed=bool(ok), omega=om, sep_mean=sep_m,
                status=r["status"], wall_s=round(r["wall_s"], 1),
                tu_per_s=round(r["tu_per_s"], 2))


def p_vvw():
    g = G.ref_VVW()
    N = int(round(96 / 0.5))
    F = G.state_vacuum(g, N)
    F = G.poke(F, g, 1, 48.0, 48.0, 2.0, 3.0, 0.5)   # species B = act1
    r = G.run_genome(g, F=F, T=1000.0, rec_tu=20.0, track_acts=[1])
    a = [x[0] if x else 0.0 for x in r["area1"]]
    ok = (r["status"] == "ok" and r["ncomp1"][-1] == 1
          and 10.0 <= a[-1] <= 60.0 and max(r["ncomp1"][4:]) == 1)
    return dict(gate="P-VVW-B", passed=bool(ok), status=r["status"],
                area_end=a[-1] if a else None,
                ncomp_max=int(max(r["ncomp1"][4:])) if len(r["ncomp1"]) > 4 else None,
                wall_s=round(r["wall_s"], 1), tu_per_s=round(r["tu_per_s"], 2))


def p_bf(gamma, T, gate, c_lo, c_hi, kick=0.0):
    g = G.ref_BFIELD(gamma=gamma)
    N = int(round(96 / 0.5))
    F = G.state_vacuum(g, N)
    st = G.load_stamp_A4()
    G.paste_stamp(F, dict(du=st["du"]), {"du": 0}, 48.0, 48.0, 0.5)
    # kick: v,w displaced kick px in -x (blob drifts +x); kick=0 = symmetric
    G.paste_stamp(F, dict(dv=st["dv"], dw=st["dw"]), {"dv": 1, "dw": 2},
                  48.0 - kick, 48.0, 0.5)
    r = G.run_genome(g, F=F, T=T, rec_tu=5.0)
    if r["status"] != "ok":
        return dict(gate=gate, passed=False, status=r["status"])
    c = com_speed(r, 0, 300.0, 5.0)   # last 300tu = t in [700,1000] for T=1000
    ok = c is not None and c_lo <= c <= c_hi and r["ncomp0"][-1] == 1
    return dict(gate=gate, passed=bool(ok), c=c, status=r["status"],
                ncomp_end=int(r["ncomp0"][-1]),
                wall_s=round(r["wall_s"], 1), tu_per_s=round(r["tu_per_s"], 2))


def p_bf0():
    return p_bf(0.0, 400.0, "P-BF0", 0.0, 0.005)


def p_bf5():
    """Self-launch is round-off symmetry breaking (M6: noiseless spontaneous);
    a symmetric paste can sit on the unstable branch long. Gate = the BF1
    dx-refine protocol: kicked kd=0.5, T=1000, c over t in [700,1000], vs law
    c(0.05)=0.0752 +-20%% (their own dx tolerance was 15%%). D_b=0 certified."""
    return p_bf(0.05, 1000.0, "P-BF5", 0.0752 * 0.8, 0.0752 * 1.2, kick=0.5)


JOBS = dict(m0=p_m0, xv=p_xv, vvw=p_vvw, bf0=p_bf0, bf5=p_bf5)


def main():
    names = sys.argv[1:] or list(JOBS)
    with ProcessPoolExecutor(max_workers=min(5, len(names))) as ex:
        futs = {n: ex.submit(JOBS[n]) for n in names}
        for n, fu in futs.items():
            rec = fu.result()
            rec["kind"] = "parity"
            G.append_result(rec)
            print(json.dumps(rec))


if __name__ == "__main__":
    main()
