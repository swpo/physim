
import numpy as np
from scipy import ndimage
import slime
from slime import smooth9

def run_diag(params=None, T=20000, seed=0, rec=20):
    """Copy of slime.run with fed/hungry flux diagnostics."""
    p = dict(slime.DEFAULTS)
    if params: p.update(params)
    L = int(p["L"]); rng = np.random.default_rng(seed)
    R = np.ones((L, L)); V = p["V0"]*(1+0.1*rng.standard_normal((L,L))); V=np.maximum(V,0.01)
    S = np.zeros((L,L)); A = np.zeros((L,L))
    E = np.zeros((L,L),np.int32); Q = np.zeros((L,L),np.int32); H = np.zeros((L,L),bool)
    Wd = np.zeros((L,L),np.int32); Ww = np.zeros((L,L),np.int32)
    rows = []
    for t in range(T):
        Rs = smooth9(R, int(p["n_sense"]))
        starving = (Rs < p["R_star"]) | ((S > p["S_dev"]) & (Rs < p["R_join"]))
        want_h = np.where(starving, True, np.where(Rs > p["R_wake"], False, H))
        newly_h = want_h & ~H & (Ww == 0)
        newly_f = ~want_h & H & (Wd == 0)
        to_h = V[newly_h].sum(); to_f = V[newly_f].sum()
        H = H.copy(); H[newly_h]=True; H[newly_f]=False
        Wd[newly_h]=int(p["T_dev"]); Ww[newly_f]=int(p["T_wake"])
        Wd=np.maximum(Wd-1,0); Ww=np.maximum(Ww-1,0)
        Hf = H.astype(float)
        Vs = smooth9(V,1); C = Vs*Vs/(Vs*Vs+p["V_c"]**2)
        can = H & (Q==0) & (V>p["V_min"]) & (C<p["C_spore"])
        fire = can & ((S>p["S_thr"]) | (rng.random((L,L))<p["p_spont"]*V))
        E[fire]=int(p["T_e"]); Q[fire]=int(p["T_e"])+int(p["T_r"])
        sat = V/(V+p["V_h"]); firing=(E>0)
        for _ in range(int(p["S_sub"])): S = S + (p["Ds"]/p["S_sub"])*slime.lap(S)
        S = S - p["ks"]*S + p["a_s"]*sat*firing; np.maximum(S,0,out=S)
        E=np.maximum(E-1,0); Q=np.maximum(Q-1,0)
        A = A + p["Da"]*slime.lap(A) - p["ka"]*A + p["a_a"]*sat*firing
        gax,gay = slime.gradc(A)
        pack = np.clip(1-Vs/p["V_pack"],0,1)
        ux = np.clip(p["chi_a"]*gax,-p["u_max"],p["u_max"])*Hf*pack
        uy = np.clip(p["chi_a"]*gay,-p["u_max"],p["u_max"])*Hf*pack
        Dv = p["Dv0"] + p["Dv_fed"]*(1-Hf)*(1+Vs/p["V_disp"]); np.minimum(Dv,0.24,out=Dv)
        V = V + slime.advect(V,ux,uy); V = V + slime.diffuse_var(V,Dv); np.maximum(V,0,out=V)
        Vs = smooth9(V,1); C = Vs*Vs/(Vs*Vs+p["V_c"]**2)
        eatf = p["g"]*(1-Hf)
        Rold=R.copy(); R = R*np.exp(-eatf*V); eaten=Rold-R
        grow = (p["Y"]*eaten).sum()
        V = V + p["Y"]*eaten
        death = p["d_base"] + p["d0"]*Hf*(1-p["pd"]*C)
        died = (V*(1-np.exp(-death))).sum()
        V = V*np.exp(-death)
        R = R + p["rho"]*(1-R) + p["Dr"]*slime.lap(R)
        if t % rec == 0:
            fedV = V[~H].sum(); hunV = V[H].sum()
            rows.append(dict(t=t, Rm=R.mean(), fedV=fedV, hunV=hunV, hf=H.mean(),
                             to_h=to_h, to_f=to_f, grow=grow, died=died,
                             fedA=(~H).mean(), fire=int(fire.sum()),
                             cv=V.std()/max(V.mean(),1e-9)))
    return rows, dict(V=V,R=R,S=S,A=A,H=H), p
