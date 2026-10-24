"""Heredity assay of kick-arisen markers (committee r2 design).
python assay.py ARM SEED [--kick polar|fill] [--T 600] [--dx 0.5] [--kill 0.5] [--founders 4]
ARM: gated | L0.05 | L0.1 | L0.02 (ungated h with that Dh). Genome = xcell-evo2-N (evo.genome).
At t=100: kick half of the cells: 'polar' = sigma 1.5 amp 2.5 at a random interior point
(<= 0.6 body radius from the centroid); 'fill' = sigma 3.0 amp 2.5 at the centroid.
Dilution: Poisson disk erasure (radius 5, rate --kill), event RNG identical across arms.
Writes assay/<tag>.npz (u, h deviations every 2 t; float16) and assay/<tag>.json (division table)."""
import argparse, json, os, time
import numpy as np
from scipy import ndimage
import xgenome as X
import evo
from screen import soup

ap = argparse.ArgumentParser()
ap.add_argument("arm"); ap.add_argument("seed", type=int)
ap.add_argument("--kick", default="polar"); ap.add_argument("--T", type=float, default=600)
ap.add_argument("--dx", type=float, default=0.5); ap.add_argument("--kill", type=float, default=0.5)
ap.add_argument("--founders", type=int, default=4); ap.add_argument("--kick_t", type=float, default=100.0); ap.add_argument("--L", type=float, default=64.0)
a = ap.parse_args()
g = evo.genome("N") if a.arm == "gated" else evo.genome("L", DhL=float(a.arm[1:]))
dx = a.dx; N = int(round(a.L / dx)); dt = 0.02 if dx >= 0.5 else 0.01
F = soup(g, N, a.seed, n=a.founders, acts=[0], dress_chans=[0, 1], dx=dx, dmin=20.0)
S = X.make_state(g, N, F=F, dx=dx, dt=dt, seed=a.seed)
u0, u0h = g["acts"][0]["u0"], g["acts"][1]["u0"]
erng = np.random.default_rng(10_000 + a.seed)        # event RNG (kills, kick choices): same in every arm
yy, xx = np.mgrid[:N, :N]
def disk(cy, cx, r_px):
    dy = (yy - cy + N / 2) % N - N / 2; dxx = (xx - cx + N / 2) % N - N / 2
    return dy ** 2 + dxx ** 2 < r_px ** 2
def cells(F):
    lab, n = ndimage.label(F[0] - u0 > 0.45 * (np.sqrt(2) - u0))
    return lab, n
rec_every = int(round(2.0 / dt)); steps = int(round(a.T / dt)); kick_step = int(round(a.kick_t / dt))
frames_u, frames_h, times, kicks, kills = [], [], [], [], []
t0 = time.time()
for k in range(steps + 1):
    if k == kick_step:
        lab, n = cells(S["F"])
        chosen = erng.permutation(n)[: max(1, n // 2)]
        for j in chosen:
            m = lab == j + 1
            cy, cx = ndimage.center_of_mass(m)
            r = np.sqrt(m.sum() / np.pi)
            if a.kick == "polar":
                ang, rr = erng.uniform(0, 2 * np.pi), 0.6 * r * np.sqrt(erng.uniform())
                ky, kx = cy + rr * np.sin(ang), cx + rr * np.cos(ang); sig = 1.5
            else:
                ky, kx = cy, cx; sig = 3.0
            X.poke(S["F"], 1, (ky + 0.5) * dx, (kx + 0.5) * dx, 2.5, sig, dx)
            kicks.append(dict(t=k * dt, cell_cy=float(cy), cell_cx=float(cx), ky=float(ky), kx=float(kx),
                              offset_px=float(np.hypot(ky - cy, kx - cx)), radius_px=float(r)))
    if k % rec_every == 0:
        frames_u.append((S["F"][0] - u0).astype(np.float16)); frames_h.append((S["F"][1] - u0h).astype(np.float16))
        times.append(k * dt)
    if k == steps:
        break
    X.step(S)
    if erng.random() < a.kill * dt:
        cy, cx = erng.uniform(0, N, 2)
        msk = disk(cy, cx, 5.0 / dx)
        S["F"][:, msk] = 0.0; S["F"][:2, msk] = np.array([u0, u0h])[:, None]
        kills.append((k * dt, float(cy), float(cx)))
os.makedirs("assay", exist_ok=True)
tag = f"{a.arm}_{a.kick}_s{a.seed}_k{int(a.kick_t)}_kill{a.kill}" + (f"_dx{dx}" if dx != 0.5 else "")
np.savez_compressed(f"assay/{tag}.npz", u=np.array(frames_u), h=np.array(frames_h), t=np.array(times), dx=dx)
json.dump(dict(args=vars(a), kicks=kicks, kills=kills, wall=time.time() - t0), open(f"assay/{tag}.json", "w"))
print(tag, "wall", round(time.time() - t0), "kicks", len(kicks), "kills", len(kills))
