"""make_strips.py — species portraits + encounter figure for SUMMARY."""
import sys, os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors")
from flavors_core import default_params, run, make_state, stepper, thresholds
import metrics

OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors/strips"
os.makedirs(OUT, exist_ok=True)
UB = -0.86756

def pair_params():
    p = default_params()
    p["k1_1"], p["k4_1"], p["Du_1"] = -1.0, 1.4, 0.65
    p["k1_2"], p["k4_2"], p["Du_2"] = -1.0 + 0.75*UB, 2.15, 0.65
    return p

# ---------- portrait: lone A, lone B, and one A+B world ----------
p = pair_params()
rA = run(p, arch="vvw", T=500.0, spots=((1, 48, 48, 2.0, 3.0),))
rB = run(p, arch="vvw", T=500.0, spots=((2, 48, 48, 2.0, 3.0),))
rAB = run(p, arch="vvw", T=800.0, spots=((1, 48, 30, 2.0, 3.0), (2, 48, 66, 2.0, 3.0)))

def crop(X, c=48, h=24):
    return X[c-h:c+h, c-h:c+h]

fig, axes = plt.subplots(3, 4, figsize=(13.6, 10))
rows = [("lone A (t=500)", rA), ("lone B (t=500)", rB), ("A+B world (t=800)", rAB)]
for i, (name, r) in enumerate(rows):
    F, bg = r["F"], r["bg"]
    ims = [(F[0]-bg["u1"], "u1 - bg (species A field)", "magma"),
           (F[1]-bg["u2"], "u2 - bg (species B field)", "magma"),
           (F[4]-bg["w"], "w - bg (shared inhibitor)", "viridis"),
           (F[2]-bg["v1"], "v1 - bg", "cividis")]
    for j, (X, t, cm) in enumerate(ims):
        ax = axes[i, j]
        im = ax.imshow(X, cmap=cm)
        plt.colorbar(im, ax=ax, fraction=0.045)
        ax.set_title(f"{name}\n{t}" if j == 0 else t, fontsize=9)
        ax.axis("off")
plt.tight_layout()
plt.savefig(f"{OUT}/species_portraits.png", dpi=110)
plt.close()
print("portraits saved", flush=True)

# ---------- cross-sections ----------
fig, axes = plt.subplots(1, 3, figsize=(14, 3.6))
for r, lab, col in ((rA, "A", "tab:red"), (rB, "B", "tab:blue")):
    F, bg = r["F"], r["bg"]
    axes[0].plot(F[0][48]-bg["u1"], color=col, ls="-" if lab=="A" else "--", label=f"{lab}: u1")
    axes[0].plot(F[1][48]-bg["u2"], color=col, alpha=0.45, label=f"{lab}: u2")
    axes[1].plot(F[4][48]-bg["w"], color=col, label=f"{lab}: w bump")
    axes[2].plot((F[0]+F[1])[48]-bg["u1"]-bg["u2"], color=col, label=f"{lab}: total act")
axes[0].set_title("activator channels (row y=48)"); axes[0].legend(fontsize=7)
axes[1].set_title("shared w port signature"); axes[1].legend(fontsize=8)
axes[2].set_title("field-agnostic total activity"); axes[2].legend(fontsize=8)
for ax in axes: ax.axhline(0, color="k", lw=0.4)
plt.tight_layout()
plt.savefig(f"{OUT}/port_signatures.png", dpi=110)
plt.close()
print("signatures saved", flush=True)

# ---------- encounter strips (one seed each) ----------
def encounter_snaps(kind, d0=10, seed=0, T=2000.0, snaps=(0, 100, 400, 1000, 2000)):
    p = pair_params()
    sp = dict(AA=(1,1), AB=(1,2), BB=(2,2))[kind]
    spots = ((sp[0], 48.0, 48.0-d0/2, 2.0, 3.0), (sp[1], 48.0, 48.0+d0/2, 2.0, 3.0))
    F, bg = make_state(p, L=96, arch="vvw", spots=spots)
    step = stepper(p, arch="vvw")
    rng = np.random.default_rng(seed)
    dt = 0.01
    out = {}
    for t in range(int(T/dt)+1):
        tu = t*dt
        if any(abs(tu - s) < dt/2 for s in snaps):
            out[int(round(tu))] = F.copy()
        if t < int(T/dt):
            F = step(F, dt, rng, 2.5e-3)
    return out, bg

fig, axes = plt.subplots(3, 5, figsize=(16, 10))
for i, kind in enumerate(("AA", "AB", "BB")):
    snaps, bg = encounter_snaps(kind)
    for j, t in enumerate(sorted(snaps)):
        F = snaps[t]
        # RGB: A field -> red, B field -> blue
        a = np.clip((F[0]-bg["u1"])/2.0, 0, 1)
        b = np.clip((F[1]-bg["u2"])/2.0, 0, 1)
        img = np.stack([a, 0.25*a+0.25*b, b], -1)
        ax = axes[i, j]
        ax.imshow(img)
        ax.set_title(f"{kind} t={t}", fontsize=10)
        ax.axis("off")
plt.suptitle("Encounters at d0=10, noise 2.5e-3, seed 0 (A=red, B=blue)", fontsize=12)
plt.tight_layout()
plt.savefig(f"{OUT}/encounter_strips.png", dpi=110)
plt.close()
print("encounter strips saved", flush=True)
