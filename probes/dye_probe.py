
import numpy as np
rng = np.random.default_rng(0)
L = 96
gx, gy = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")

def make_membrane(closed=True):
    r = np.hypot(gx-48, gy-48)
    ring = (r > 18) & (r < 21)
    if not closed:
        gap = (np.abs(gx-48) < 4) & (gy > 48)   # 8-cell gap in the ring
        ring = ring & ~gap
    return ring

def dye_assay(closed, T_steps=4000, D=0.2):
    memb = make_membrane(closed)
    cond = (~memb).astype(float)          # dye cannot enter membrane cells
    T = np.zeros((L, L))
    inside = np.hypot(gx-48, gy-48) < 4   # injection site (a "port bump" at center)
    outside_sensors = [(10,10), (85,20), (20,85), (80,80), (48,5), (5,48)]
    for t in range(T_steps):
        if t < 400:
            T[inside] += 0.01             # inject dye for 400 steps
        flux = np.zeros_like(T)
        for ax, sh in ((0,1),(0,-1),(1,1),(1,-1)):
            c = cond * np.roll(cond, sh, ax)
            flux += c * (np.roll(T, sh, ax) - T)
        T = np.clip(T + D * flux, 0, None)
    reads = [float(T[max(0,x-2):x+3, max(0,y-2):y+3].mean()) for (x,y) in outside_sensors]
    return reads

closed_reads = dye_assay(True)
open_reads = dye_assay(False)
print("outside-sensor dye levels, CLOSED membrane:", [round(v,4) for v in closed_reads])
print("outside-sensor dye levels, OPEN membrane:  ", [round(v,4) for v in open_reads])
print("separation (min open / max closed): %.1fx" % (min(open_reads) / max(max(closed_reads), 1e-9)))
