
import sys, numpy as np
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
_GPU = os.path.normpath(os.path.join(_HERE, ".."))
_BLOBS = os.path.normpath(os.path.join(_GPU, ".."))
sys.path.insert(0, _GPU)
sys.path.insert(0, os.path.join(_BLOBS, "l0", "stage2", "lib"))
sys.path.insert(0, os.path.join(_BLOBS, "l0", "complexity"))
import genome as G
import worlds as W
from blobgpu import pack_genomes, pack_states, unpack_state, make_stepper, diffusion_E
from blobgpu.core import batch_keys
import jax, jax.numpy as jnp

gens = [W.WORLDS[k]() for k in ("m0", "m4", "xv", "bf")]
N, dx, dt = 64, 0.5, 0.02
params, struct, aux = pack_genomes(gens, dtype=np.float32)
print("struct", struct)

# states: vacuum + a poke on act 0
states = []
rng = np.random.default_rng(0)
for g in gens:
    F = G.state_vacuum(g, N)
    F = G.poke(F, g, 0, 16.0, 16.0, 2.0, 3.0, dx)
    states.append(F.astype(np.float32))
Fb = pack_states(gens, states, struct["na_max"], struct["nc_max"])
params = {k: jnp.asarray(v) for k, v in params.items()}
params["E"] = diffusion_E(np.zeros((len(gens), struct["nf_max"])) + 0, N, dx, dt)  # placeholder
# real D packing
import blobgpu.packing as P
params2, _, _ = pack_genomes(gens, dtype=np.float32)
params["E"] = diffusion_E(params2["D"], N, dx, dt, np.float32)

step = make_stepper(struct, N, dx, dt, noise=0.0)
keys = batch_keys([1, 2, 3, 4])
Fj = jnp.asarray(Fb)
Fj = step(Fj, params, keys, 0, 50)
Fj = np.asarray(Fj)
print("gpu-kernel 50 steps ok, finite:", np.isfinite(Fj).all())

# CPU reference: 50 steps of the same, per world, with genome.py conventions (f32 soup_sim op order)
import scipy.fft as sfft
def cpu_steps(g, F0, nsteps, dtype=np.float32):
    na, nc = len(g["acts"]), len(g["chans"])
    W_ = np.asarray(g["W"], float); K_ = np.asarray(g["K"], float)
    bilin = [tuple(b) for b in g.get("bilin", [])]
    lam = np.array([a["lam"] for a in g["acts"]])[:, None, None]
    k1 = np.array([a["k1"] for a in g["acts"]])[:, None, None]
    u0s = np.array([a["u0"] for a in g["acts"]])
    tau_c = np.array([c["tau"] for c in g["chans"]])
    kf = 2*np.pi*np.fft.fftfreq(N, d=dx); kr = 2*np.pi*np.fft.rfftfreq(N, d=dx)
    k2 = kf[:, None]**2 + kr[None, :]**2
    Ds = np.array([a["Du"] for a in g["acts"]] + [c["D"] for c in g["chans"]])
    E = np.exp(-Ds[:, None, None]*k2[None]*dt)
    id_mask = np.array([c["g"] == "id" for c in g["chans"]])
    thr_ch = np.array([c.get("thr", 0.0) for c in g["chans"]])
    sc_ch = np.array([c.get("sc", 1.0) for c in g["chans"]])
    fdt = dtype
    F = F0.astype(fdt); E = E.astype(fdt)
    lam = lam.astype(fdt); k1 = k1.astype(fdt)
    Wf = W_.astype(fdt); Kf = K_.astype(fdt)
    u0f = u0s[:, None, None].astype(fdt)
    Wid = Wf.copy(); Wid[~id_mask] = 0.0
    tanh_rows = [c for c in range(nc) if not id_mask[c]]
    inv_tau = (1.0/tau_c)[:, None, None].astype(fdt)
    thr_f = thr_ch.astype(fdt); sc_f = sc_ch.astype(fdt)
    for t in range(nsteps):
        U = F[:na]; X = F[na:]
        Z = U - u0f
        R = np.empty_like(F)
        np.multiply(U, U, out=R[:na]); R[:na] *= -U
        R[:na] += lam*U; R[:na] += k1
        R[:na] -= np.tensordot(Kf, X, axes=(1, 0))
        for (i, c, c2, coef) in bilin:
            R[i] -= fdt(coef)*X[c]*X[c2]
        Rch = np.tensordot(Wid, Z, axes=(1, 0))
        for c in tanh_rows:
            acc = None
            for a in range(na):
                if Wf[c, a] != 0.0:
                    v = np.tanh(np.clip(Z[a]-thr_f[c], 0, None)/sc_f[c]); v *= Wf[c, a]
                    acc = v if acc is None else acc+v
            if acc is not None:
                Rch[c] = acc
        Rch -= X; Rch *= inv_tau
        R[na:] = Rch
        F = F + fdt(dt)*R
        F = sfft.irfft2(sfft.rfft2(F)*E, s=(N, N))
    return F

for b, g in enumerate(gens):
    ref = cpu_steps(g, states[b], 50)
    got = unpack_state(g, Fj[b], struct["na_max"])
    err = np.linalg.norm(got-ref)/np.linalg.norm(ref)
    print(g["id"], "relL2 f32 50 steps:", f"{err:.2e}")
