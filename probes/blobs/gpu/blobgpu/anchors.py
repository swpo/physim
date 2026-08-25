"""blobgpu/anchors.py — bond-anchor gate drivers (the A5-dt cautionary tale).

Anchor physics (membrane/binding programs, CPU-certified):
  A4s pair (tau=2.5, Dv=1.6, stamp_A4)  @ dt=0.02 : d0=16 -> d* = 15.40
  A5  pair (tau=2.5, Dv=2.0, stamp_P7s) @ dt=0.005: d0=16 -> d* = 15.70 (+-0.5%)
  A5  pair @ dt=0.02 is the TRAP: slides THROUGH 15.7, hits the 14.4 saddle and
  replicates (~2600tu) — an integrator artifact, reproduced in two CPU engines.
  A correct GPU port must reproduce the artifact too (same equations + same dt
  = same wrong answer); silently "fixing" it would mean the numerics differ.

World: single M0-chemistry species (lam=2, k1=-0.7, k3=1, k4=1.5, theta=0.7,
Du=1, Dw=20) with free (tau, Dv) — expressed as an L0 genome; ICs are the
certified stamps pasted at (c +- d0/2, c), no kick, noise=0 (deterministic).
Separation measured with the verbatim CPU tracker (genome.blob_list).
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, "..", "..", "l0", "stage2", "lib"))
MEMB = os.path.normpath(os.path.join(HERE, "..", "..", "membrane"))
COMP = os.path.normpath(os.path.join(HERE, "..", "..", "composite", "data"))
GDATA = os.path.normpath(os.path.join(HERE, "..", "data"))
for p in (LIB,):
    if p not in sys.path:
        sys.path.insert(0, p)
import genome as G                                             # noqa: E402
import jax.numpy as jnp                                        # noqa: E402
from .packing import pack_genomes, pack_states, unpack_state   # noqa: E402
from .core import make_stepper, diffusion_E, batch_keys        # noqa: E402

M0P = dict(lam=2.0, k1=-0.7, k3=1.0, k4=1.5, theta=0.7, Du=1.0, Dw=20.0)


def pair_genome(tau, Dv):
    """Single M0-chemistry species with free (tau, Dv) as an L0 genome."""
    p = M0P
    r = np.roots([-1.0, 0.0, p["lam"] - p["k3"] - p["k4"], p["k1"]])
    u0 = sorted(x.real for x in r if abs(x.imag) < 1e-9)[0]
    k1g = p["k1"] - (p["k3"] + p["k4"]) * u0
    act = dict(lam=p["lam"], k1=k1g, Du=p["Du"],
               u0=G.polish_root(p["lam"], k1g, u0))
    return dict(id=f"pair_tau{tau}_Dv{Dv}",
                acts=[act],
                chans=[dict(tau=tau, D=Dv, g="id", thr=0.0, sc=1.0),
                       dict(tau=p["theta"], D=p["Dw"], g="id", thr=0.0, sc=1.0)],
                W=[[1.0], [1.0]], K=[[p["k3"], p["k4"]]], bilin=[],
                provenance=dict(kind="anchor", source="membrane pair world"))


def load_stamp(name):
    for root in (GDATA, os.path.join(MEMB, "data"), COMP):
        pth = os.path.join(root, name)
        if os.path.exists(pth):
            st = np.load(pth)
            return dict(du=st["du"], dv=st["dv"], dw=st["dw"], u0=float(st["u0"]))
    raise FileNotFoundError(name)


def pair_state(g, stamp, N, dx, d0):
    """Vacuum + two stamps at (c +- d0/2, c). genome.paste_stamp (subpixel FFT
    shift), matching membrane.paste_blobs with kick=None."""
    F = G.state_vacuum(g, N)
    L = N * dx
    c = L / 2
    for px in (c - d0 / 2, c + d0 / 2):
        F = G.paste_stamp(F, dict(u=stamp["du"], v=stamp["dv"], w=stamp["dw"]),
                          dict(u=0, v=1, w=2), px, c, dx)
    return F


def run_pair(tau, Dv, stamp_name, dt, T, d0=16.0, L=64.0, dx=0.5,
             rec_tu=25.0, dtype="f64", stop_ncomp_change=True):
    """Integrate the pair on the JAX backend; track separation on CPU.
    Returns dict(t, sep, ncomp, d_final, status)."""
    if dtype == "f64":
        from .core import enable_x64
        enable_x64()
    npdt = np.float32 if dtype == "f32" else np.float64
    g = pair_genome(tau, Dv)
    N = int(round(L / dx))
    stamp = load_stamp(stamp_name)
    F0 = pair_state(g, stamp, N, dx, d0)
    params, struct, aux = pack_genomes([g], dtype=npdt)
    Fb = pack_states([g], [F0.astype(npdt)], struct["na_max"], struct["nc_max"])
    p = {k: jnp.asarray(v) for k, v in params.items()}
    p["E"] = diffusion_E(params["D"], N, dx, dt, npdt)
    step = make_stepper(struct, N, dx, dt, noise=0.0)
    keys = batch_keys([0])
    a = g["acts"][0]
    thr = a["u0"] + 0.45 * (np.sqrt(a["lam"]) - a["u0"])

    steps = int(round(T / dt))
    rec = max(int(round(rec_tu / dt)), 1)
    Fj = jnp.asarray(Fb)
    ts, seps, ncs = [], [], []
    status = "ok"
    t = 0
    while t <= steps:
        Fh = np.asarray(Fj[0], np.float64)
        u = unpack_state(g, Fh, struct["na_max"])[0]
        if not np.isfinite(u).all():
            status = "blowup"
            break
        bl = G.blob_list(u, thr, dx, L)
        pos = np.array([[b["y"], b["x"]] for b in bl])
        sep = None
        if len(bl) == 2:
            d = G.min_image(pos[1] - pos[0], L)
            sep = float(np.hypot(*d))
        ts.append(t * dt)
        seps.append(sep)
        ncs.append(len(bl))
        if stop_ncomp_change and t * dt > 10.0 and len(bl) != 2:
            status = "replicated" if len(bl) > 2 else "died"
            break
        if t == steps:
            break
        n = min(rec, steps - t)
        Fj = step(Fj, p, keys, t, n)
        t += n
    good = [s for s in seps if s is not None]
    return dict(t=ts, sep=seps, ncomp=ncs, status=status,
                d_final=(good[-1] if good else None),
                tau=tau, Dv=Dv, dt=dt, T=T, d0=d0, stamp=stamp_name,
                dtype=dtype)
