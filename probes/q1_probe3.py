
import numpy as np, time

def lap(z):
    return np.roll(z,1,0)+np.roll(z,-1,0)+np.roll(z,1,1)+np.roll(z,-1,1)-4*z

def run(storms=True, cap=0.15, T=60000, seed=0, tag=""):
    rng = np.random.default_rng(seed)
    L = 64
    gx, gy = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    V = np.zeros((L,L)); E = np.zeros((L,L)); R = 0.6*np.ones((L,L))
    Ge = np.full((L,L), 0.5)
    for gval in (0.15,0.3,0.45,0.6,0.75,0.9):
        for _ in range(2):
            cx, cy = rng.integers(6, L-6, 2)
            m = (gx-cx)**2+(gy-cy)**2 <= 9
            V[m] = 0.3; Ge[m] = gval; E[m] = 0.04
    c_max, m0, m1 = 0.02, 0.0006, 0.0030
    rows = []; deaths_storm = 0; deaths_calm = 0
    g_dead_storm = []; g_colon_calm = []
    for t in range(T):
        storm = storms and ((t // 3000) % 2 == 1)
        regen = 0.004 * (0.05 if storm else 1.0)
        R += 0.06*lap(R) + regen*(1-R)
        income = c_max*Ge*V*R
        R = np.clip(R - income, 0, 1)
        E += income - (m0 + m1*Ge)*V
        deficit = np.minimum(E, 0)
        V = np.clip(V + deficit/0.05, 0, 1)     # burn tissue to cover deficit
        E = np.maximum(E, 0)
        surplus = np.maximum(E - 0.04*V, 0)
        used = 0.3*surplus
        V2 = np.clip(V + np.minimum(2.0*used, 0.05)*(1-V), 0, 1)
        E -= used
        V_old = V2.copy()
        alive = V2 > 0.05
        nA = np.stack([np.roll(alive&(E>0.02*V2),1,0), np.roll(alive&(E>0.02*V2),-1,0),
                       np.roll(alive&(E>0.02*V2),1,1), np.roll(alive&(E>0.02*V2),-1,1)])
        can_col = (~alive) & (nA.any(0)) & (R > 0.15)   # colonization needs local resource
        if can_col.any():
            nV = np.stack([np.roll(V2,1,0), np.roll(V2,-1,0),
                           np.roll(V2,1,1), np.roll(V2,-1,1)])
            nG = np.stack([np.roll(Ge,1,0), np.roll(Ge,-1,0),
                           np.roll(Ge,1,1), np.roll(Ge,-1,1)])
            pick = can_col & (rng.random((L,L)) < 0.10)
            if pick.any():
                G_par = np.take_along_axis(nG, nV.argmax(0)[None], 0)[0]
                newg = np.clip(G_par + rng.normal(0, 0.04, (L,L)), 0.02, 0.98)
                V2 = np.where(pick, 0.12, V2)
                E = np.where(pick, 0.02, E)
                Ge = np.where(pick, newg, Ge)
                if not storm: g_colon_calm += list(newg[pick][:50])
        V = V2
        E = np.minimum(E, cap*V)                 # finite larder
        dying = (V < 0.05) & (V_old >= 0.005)
        dead = V < 0.05
        if dying.any():
            if storm: deaths_storm += int(dying.sum()); g_dead_storm += list(Ge[dying][:50])
            else: deaths_calm += int(dying.sum())
        V[dead] = 0; E[dead] = 0
        if (t+1) % 6000 == 0:
            a = V > 0.05
            if a.sum() == 0:
                rows.append((t+1, "EXT ", 0, 0, 0, 0)); break
            mg = float((Ge*V)[a].sum()/V[a].sum())
            sg = float(np.sqrt(((Ge-mg)**2*V)[a].sum()/V[a].sum()))
            rows.append((t+1, "storm" if storm else "calm ", int(a.sum()),
                         round(float(V.sum()),1), round(mg,3), round(sg,3)))
    print("== %s (cap=%s) ==" % (tag, cap))
    print("   t   phase  cells  mass  mean_g  sd_g")
    for r in rows: print("%6d  %s %5s %6s  %6s  %s" % r)
    print("deaths: storm=%d calm=%d | mean g of storm-dead: %s | mean g of calm-colonizers: %s" % (
        deaths_storm, deaths_calm,
        round(float(np.mean(g_dead_storm)),3) if g_dead_storm else "-",
        round(float(np.mean(g_colon_calm)),3) if g_colon_calm else "-"))

t0=time.time()
run(storms=True,  cap=0.15, tag="storms + finite larder")
run(storms=True,  cap=1e9,  tag="storms + INFINITE larder (control)")
run(storms=False, cap=0.15, tag="no storms (control)")
print("(%ds)" % (time.time()-t0))
