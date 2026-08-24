import os, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BASE = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, BASE)
import metrics as mx

fig = plt.figure(figsize=(15, 9))

# (a) R(t) for PULL runs N6: two-sided convergence
ax = fig.add_subplot(2, 3, 1)
for d0, c in [("13p5", "tab:blue"), ("14p5", "tab:cyan"), ("17p0", "tab:orange"), ("18p0", "tab:red")]:
    tr = np.load(f"{BASE}/data/PULL_A4s_N6_d{d0}_track.npz")
    t, P = tr["t"], tr["P1"]
    Rm = []
    for k in range(len(t)):
        p = P[k][~np.isnan(P[k, :, 0])]
        Rm.append(mx.ring_stats(p % 96.0, 96.0)["R_mean"] if len(p) == 6 else np.nan)
    ax.plot(t, Rm, color=c, label=f"chord0={d0.replace('p','.')}")
ax.axhline(15.4015, color="k", lw=0.6, ls="--")
ax.set_xlabel("t (tu)"); ax.set_ylabel("ring radius R (px)")
ax.set_title("(a) N=6 ring: two-sided convergence\n(ring = attractor)")
ax.legend(fontsize=7)

# (b) R_final vs N with bond law
ax = fig.add_subplot(2, 3, 2)
Ns = np.array([4, 5, 6, 8, 10, 12])
Rf = np.array([10.9221, 13.1412, 15.4015, 20.1191, 24.9114, 29.7315])
law = 15.40 / (2 * np.sin(np.pi / Ns))
ax.plot(Ns, Rf, "o", ms=8, label="measured (5000tu, noise)")
ax.plot(Ns, law, "-", lw=1, label="R = d*/(2 sin(pi/N)), d*=15.40")
ax.set_xlabel("N blobs"); ax.set_ylabel("R (px)")
ax.set_title("(b) ring radius law")
ax.legend(fontsize=8)

# (c) chord (= realized bond length) vs N
ax = fig.add_subplot(2, 3, 3)
chords = 2 * Rf * np.sin(np.pi / Ns)
ax.plot(Ns, chords, "s-", ms=7)
ax.axhline(15.40, color="k", ls="--", lw=0.6, label="pair d* = 15.40")
ax.set_ylim(15.2, 15.6)
ax.set_xlabel("N"); ax.set_ylabel("chord (px)")
ax.set_title("(c) bond length on the ring")
ax.legend(fontsize=8)

# (d) enclosure asymmetry vs N
ax = fig.add_subplot(2, 3, 4)
Ns2 = [5, 6, 8, 10, 12]
du = [0.034602, 0.011960, 0.002649, 0.001341, 0.000644]
dv = [-0.010941, -0.003952, -0.002148, -0.001192, -0.000536]
dw = [0.008657, 0.006065, 0.002394, 0.001259, 0.000603]
ax.semilogy(Ns2, np.abs(du), "o-", label="|u_in - u_out|")
ax.semilogy(Ns2, np.abs(dv), "s-", label="|v_in - v_out|")
ax.semilogy(Ns2, np.abs(dw), "^-", label="|w_in - w_out|")
ax.axhline(1e-4, color="k", ls=":", lw=0.8, label="detection floor")
ax.set_xlabel("N"); ax.set_ylabel("in/out asymmetry")
ax.set_title("(d) R2a: enclosed vacuum differs from outside")
ax.legend(fontsize=7)

# (e) radial profiles for N6/N10
ax = fig.add_subplot(2, 3, 5)
d = np.load(f"{BASE}/data/enc_profiles.npz")
for N, c in [(6, "tab:blue"), (10, "tab:green")]:
    ax.plot(d[f"r{N}"], d[f"u{N}"], color=c, label=f"u dev, N={N}")
ax.axhline(0, color="k", lw=0.5)
ax.set_xlabel("r from ring center (px)"); ax.set_ylabel("u - u0 (azimuthal mean)")
ax.set_title("(e) interior pool / wall / outside")
ax.set_ylim(-0.25, 0.1); ax.legend(fontsize=8)

# (f) A5 dt artifact
ax = fig.add_subplot(2, 3, 6)
import json as J
for lg, lab, c in [("probe_dt02b", "dt=0.02 (replicates 2600tu)", "tab:red"),
                    ("probe_dt005", "dt=0.005 (freezes 15.711)", "tab:green"),
                    ("probe_dt0025", "dt=0.0025 (freezes 15.724)", "tab:blue")]:
    rec = J.loads(open(f"{BASE}/logs/{lg}.log").read().strip().splitlines()[-1])
    s = np.array([[a, b] for a, b in rec["sep"] if b is not None])
    ax.plot(s[:, 0], s[:, 1], color=c, label=lab)
ax.axhline(15.70, color="k", ls="--", lw=0.6)
ax.set_xlabel("t (tu)"); ax.set_ylabel("A5 pair separation (px)")
ax.set_title("(f) TRAP: A5 statics need dt<=0.005 (IMEX)")
ax.legend(fontsize=7)

fig.suptitle("R1/R2a certification: closed rings (A4s), ring law, enclosure asymmetry, A5-dt trap", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(f"{BASE}/strips/fig2_R1_certification.png", dpi=110)
print("fig2 saved")
