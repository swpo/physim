
"""sync_figs.py -- final figures for the sync tower."""
import sys, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/morpho-counter/sync")
import numpy as np
from sync_sim import simulate2
from sync_metrics import l4_analysis
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = dict(ny=8, nx=64, dx=1.0, dt=0.1, a=0.1, b=0.9, Du=1.0, Dv=11.0,
            Dc=10.0, sigma=1.0, kstar2=0.2682)

# --- panel A: Delta(t) traces locked vs slip ---
tr = {}
for tag, R in [("locked R=1.30", 1.30), ("slip R=1.85", 1.85)]:
    eps_g = 2.4e-3
    p = dict(BASE, eps1=eps_g*np.sqrt(R), eps2=eps_g/np.sqrt(R), kappa_c=2e-3,
             steps=300000, meas_every=25, seed=1, noise_amp=2e-3)
    r = simulate2(p)
    a = l4_analysis(r["t"], r["nz"][:, 0], r["nz"][:, 1])
    tr[tag] = (a["delta_t"], a["delta"], r)

fig, axes = plt.subplots(3, 1, figsize=(11, 8), gridspec_kw=dict(height_ratios=[1.4, 1, 1]))
for tag, (dt_, d_, _) in tr.items():
    axes[0].plot(dt_, d_, lw=1.2, label=tag)
axes[0].set_ylabel("Delta = phi1-phi2 (cycles)"); axes[0].legend()
axes[0].set_title("L4: relative phase — locked plateau vs phase slips (kc=2e-3)")
_, _, rl = tr["locked R=1.30"]
axes[1].plot(rl["t"], rl["nz"][:, 0], lw=0.8, label="ring1 n")
axes[1].plot(rl["t"], rl["nz"][:, 1], lw=0.8, label="ring2 n")
axes[1].set_xlim(20000, 40000); axes[1].set_ylabel("count n (locked)"); axes[1].legend(fontsize=7)
_, _, rs = tr["slip R=1.85"]
axes[2].plot(rs["t"], rs["nz"][:, 0], lw=0.8, label="ring1 n")
axes[2].plot(rs["t"], rs["nz"][:, 1], lw=0.8, label="ring2 n")
axes[2].set_xlim(20000, 40000); axes[2].set_ylabel("count n (slip)"); axes[2].set_xlabel("t")
axes[2].legend(fontsize=7)
fig.tight_layout(); fig.savefig("strips/L4_traces.png", dpi=110)

# --- panel B: staircase rho(R) + tongue edges ---
campA = json.load(open("results_campA.json"))
campC = json.load(open("results_campC.json"))
fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.8))
Rs = [r["cand"]["R"] for r in campA]; rhos = [r.get("rho") for r in campA]
axes[0].plot(Rs, rhos, "o-", label="measured rho")
axes[0].plot([1, 2.3], [1, 2.3], "k--", lw=0.7, label="uncoupled rho=R")
axes[0].axhline(1.0, color="gray", lw=0.5)
Rc2 = campC["0.002"]["R_c_upper"]
axes[0].axvline(Rc2, color="r", ls=":", lw=1, label="edge R_c=%.3f" % Rc2)
axes[0].set_xlabel("detuning R = eps1/eps2"); axes[0].set_ylabel("rotation number rho")
axes[0].set_title("1:1 plateau (kc=2e-3)"); axes[0].legend(fontsize=7); axes[0].grid(alpha=0.3)

kcs = sorted(float(k) for k in campC if "R_c_upper" in campC[k])
w = [np.log(campC[str(k)]["R_c_upper"]) for k in kcs]
axes[1].plot(kcs, w, "s-")
kk = np.linspace(0, 0.0045, 10)
axes[1].plot(kk, 228.7 * kk + 0.067, "k--", lw=0.8, label="linear fit (4 smallest kc)")
axes[1].set_xlabel("coupling kc"); axes[1].set_ylabel("tongue half-width ln R_c")
axes[1].set_title("G3b: tongue width vs coupling"); axes[1].legend(fontsize=7); axes[1].grid(alpha=0.3)

Rc = 1.7271
Rp = np.array([1.76, 1.80, 1.85, 1.92, 2.00, 2.15, 2.30])
Tp = np.array([22627, 8203, 5881, 6002, 3702, 3362, 2295])
axes[2].loglog(Rp - Rc, Tp, "o", label="pooled T_slip (3 seeds)")
xx = np.linspace(0.03, 0.6, 40)
axes[2].loglog(xx, np.exp(7.75) * xx ** -0.72, "-", lw=1, label="fit slope -0.72 (r2=.95)")
axes[2].loglog(xx, 2321 * xx ** -0.5, "--", lw=1, label="slope -1/2 (r2=.86)")
axes[2].set_xlabel("R - R_c"); axes[2].set_ylabel("T_slip")
axes[2].set_title("G3a: slip-period divergence at edge"); axes[2].legend(fontsize=7)
axes[2].grid(alpha=0.3, which="both")
fig.tight_layout(); fig.savefig("strips/sync_laws.png", dpi=110)
print("figs saved")
