
import numpy as np
from scipy import ndimage
def lap(z):
    return np.roll(z,1,0)+np.roll(z,-1,0)+np.roll(z,1,1)+np.roll(z,-1,1)-4*z
L = 64
gx, gy = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")

print(" g   | realized uptake/capita | local R (organism cells) | pop mass")
results = []
for g in (0.1, 0.3, 0.5, 0.7, 0.9):
    U = np.ones((L,L)); V = np.zeros((L,L))
    for (cx,cy) in [(20,20),(44,44)]:
        m = (gx-cx)**2+(gy-cy)**2 <= 9; U[m]=0.5; V[m]=0.25
    R_max, DR, regen = 0.036, 0.05, 0.00010
    R = R_max*np.ones((L,L))
    c_g = 0.012*g            # PURE LINEAR micro coupling: enzyme amount ∝ gene
    k_g = 0.0615             # constant death (no authored trade-off curve at all)
    for t in range(16000):
        uvv = U*V*V
        U += 0.16*lap(U) - uvv + R*(1-U)
        V = V + 0.08*lap(V) + uvv - (R + k_g)*V
        R += DR*lap(R) + regen*(R_max-R)*R_max*300 - c_g*V*R
        R = np.clip(R, 0, R_max)
    organ = V > 0.10
    if organ.sum() == 0:
        print(f"{g:4.1f} | EXTINCT"); results.append((g, 0, 0, 0)); continue
    per_capita = float((c_g*R*V)[organ].sum() / max(V[organ].sum(), 1e-9))
    r_local = float(R[organ].mean())
    results.append((g, per_capita, r_local, float(V.sum())))
    print(f"{g:4.1f} | {per_capita:.6f}            | {r_local:.4f}                  | {V.sum():.1f}")

# shape check: is realized uptake linear in g (slope constant) or saturating (slope falling)?
gs = [r[0] for r in results if r[1] > 0]
up = [r[1] for r in results if r[1] > 0]
if len(gs) >= 3:
    slopes = [(up[i+1]-up[i])/(gs[i+1]-gs[i]) for i in range(len(gs)-1)]
    print("\nincremental slopes d(uptake)/dg:", [round(s,5) for s in slopes])
    print("saturating (slopes falling):", all(slopes[i+1] < slopes[i] for i in range(len(slopes)-1)))
