"""blobgpu/packing.py — genomes -> padded parameter tensors for the batched stepper.

A batch of B genomes is padded to a common (na_max, nc_max) field layout.
Padded slots are inert BY PARAMETER CONSTRUCTION (verified in tests/test_padding.py):
  activator pad: lam=k1=u0=0, K row=0, noise masked  -> du/dt = -u^3, u==0 stays 0
  channel  pad: inv_tau=0, W rows=0, K cols=0        -> dx/dt = 0
  diffusion pad: D=0 -> E=1 (identity in k-space)
so a padded field that starts at 0 stays exactly 0 and couples to nothing.
There is no cross-world term anywhere; each world's trajectory equals its
unpadded single-world trajectory bit-for-bit (same dtype, same backend).

Layout of the packed state: F (B, nf_max, N, N) with fields [acts | chans].
"""
import numpy as np


def pack_genomes(genomes, dtype=np.float32):
    """-> (params: dict of np arrays, struct: dict of static ints/tuples).
    params keys: lam,k1,u0,act_mask (B,na) | K (B,na,nc) | Wid,Wtanh (B,nc,na)
    | thr,sc,inv_tau,chan_mask (B,nc) | D (B,nf) | bi_i,bi_c,bi_c2,bi_coef (B,nb)
    | thr_a, thr_lo (B,na) f64 tracking thresholds (not used on device).
    """
    B = len(genomes)
    na_max = max(len(g["acts"]) for g in genomes)
    nc_max = max(len(g["chans"]) for g in genomes)
    nb_max = max((len(g.get("bilin", [])) for g in genomes), default=0)
    nf_max = na_max + nc_max

    lam = np.zeros((B, na_max)); k1 = np.zeros((B, na_max))
    u0 = np.zeros((B, na_max)); act_mask = np.zeros((B, na_max))
    K = np.zeros((B, na_max, nc_max))
    Wid = np.zeros((B, nc_max, na_max)); Wtanh = np.zeros((B, nc_max, na_max))
    thr = np.zeros((B, nc_max)); sc = np.ones((B, nc_max))
    inv_tau = np.zeros((B, nc_max)); chan_mask = np.zeros((B, nc_max))
    D = np.zeros((B, nf_max))
    nbm = max(nb_max, 1)
    bi_i = np.zeros((B, nbm), np.int32); bi_c = np.zeros((B, nbm), np.int32)
    bi_c2 = np.zeros((B, nbm), np.int32); bi_coef = np.zeros((B, nbm))
    thr_a = np.zeros((B, na_max)); thr_lo = np.zeros((B, na_max))
    tanh_slots = set()

    for b, g in enumerate(genomes):
        na, nc = len(g["acts"]), len(g["chans"])
        Wg = np.asarray(g["W"], float); Kg = np.asarray(g["K"], float)
        for i, a in enumerate(g["acts"]):
            lam[b, i] = a["lam"]; k1[b, i] = a["k1"]; u0[b, i] = a["u0"]
            act_mask[b, i] = 1.0
            D[b, i] = a["Du"]
            s = np.sqrt(max(a["lam"], 1e-9))
            thr_a[b, i] = a["u0"] + 0.45 * (s - a["u0"])
            thr_lo[b, i] = a["u0"] + 0.30 * (s - a["u0"])
        K[b, :na, :nc] = Kg
        for c, ch in enumerate(g["chans"]):
            inv_tau[b, c] = 1.0 / ch["tau"]
            chan_mask[b, c] = 1.0
            D[b, na_max + c] = ch["D"]
            thr[b, c] = ch.get("thr", 0.0); sc[b, c] = ch.get("sc", 1.0)
            if ch["g"] == "id":
                Wid[b, c, :na] = Wg[c]
            else:
                Wtanh[b, c, :na] = Wg[c]
                tanh_slots.add(c)
        for k, (i, c, c2, coef) in enumerate(g.get("bilin", [])):
            bi_i[b, k] = i; bi_c[b, k] = c; bi_c2[b, k] = c2; bi_coef[b, k] = coef

    f = lambda a: a.astype(dtype)
    params = dict(lam=f(lam), k1=f(k1), u0=f(u0), act_mask=f(act_mask),
                  K=f(K), Wid=f(Wid), Wtanh=f(Wtanh), thr=f(thr), sc=f(sc),
                  inv_tau=f(inv_tau), chan_mask=f(chan_mask), D=D,
                  bi_i=bi_i, bi_c=bi_c, bi_c2=bi_c2, bi_coef=f(bi_coef))
    struct = dict(B=B, na_max=na_max, nc_max=nc_max, nb_max=nb_max,
                  nf_max=nf_max, tanh_slots=tuple(sorted(tanh_slots)),
                  has_bilin=bool(nb_max > 0))
    aux = dict(thr_a=thr_a, thr_lo=thr_lo)
    return params, struct, aux


def pack_states(genomes, states, na_max=None, nc_max=None):
    """Stack per-world (na_i+nc_i, N, N) states into (B, nf_max, N, N), padding
    activator block and channel block separately (channels start at na_max)."""
    B = len(genomes)
    na_max = na_max or max(len(g["acts"]) for g in genomes)
    nc_max = nc_max or max(len(g["chans"]) for g in genomes)
    N = states[0].shape[-1]
    F = np.zeros((B, na_max + nc_max, N, N), states[0].dtype)
    for b, (g, s) in enumerate(zip(genomes, states)):
        na, nc = len(g["acts"]), len(g["chans"])
        F[b, :na] = s[:na]
        F[b, na_max:na_max + nc] = s[na:na + nc]
    return F


def unpack_state(g, Fb, na_max):
    """(nf_max, N, N) padded world state -> (na+nc, N, N) natural layout."""
    na, nc = len(g["acts"]), len(g["chans"])
    return np.concatenate([Fb[:na], Fb[na_max:na_max + nc]], axis=0)
