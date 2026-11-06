"""lenia_world.py -- the first two-level VW-0 example: Flow-Lenia at level 0, two coarse-grainings.

    level 0   h0 = A (C, H, W) flattened, Flow-Lenia (../level0/flowlenia.py) with per-cell flow
              noise of std `noise_std` drawn from the VW-0 noise stream (mass conserved exactly).
              One VW-0 tick = `stride` Flow-Lenia steps (default 20).
    Phi_coarse  block means of every channel on a G x G grid plus the block mean of A_sum^2
              (a second moment: how concentrated the block's matter is). No memory.
    Phi_objects K tracked object slots with persistent identities (tracking memory m).
              Per slot: presence, mass, channel-1 fraction, periodic centroid embedded on the
              torus (4 numbers), radius of gyration, nematic elongation/orientation (2), velocity (2).

Inputs (both worlds): the actuators are the H*W cells of the grid (matter at a cell, all channels
together: one physical type, as DESIGN.md section 3 rule 4 asks), anonymised by a hidden permutation.
Default constraint: k = 8 non-zero coordinates per tick, values in [-1, 1], sum|a| <= 4, zero sum.
The kick kappa is physics, not a rejection: a source (negative) coordinate removes at most the
matter that is there; for a zero-sum command the sinks receive exactly what was removed, in the
commanded proportions, so total mass per channel is conserved exactly and A stays >= 0.

Tracking rules (declared; m is a deterministic function of the level-0 history):
  bodies    periodic 8-connected components of gaussian_blur(A_sum, blur) > thr with mass >= m_min
  matching  overlap of each slot's previous pixel mask with the current components, greedy by
            overlap size (a slot keeps the component it overlaps most, a component keeps the slot
            that overlaps it most); unmatched slots fall back to the nearest unmatched component
            within rg + 4 px of their predicted position (x + v).
  fusion    a slot whose pixels overlap a component already taken by another slot dies (event
            'fused'); the survivor gets event 'fusion' and the mass-weighted mean of the parents'
            velocities.
  fission   a component that overlaps only slots already matched is born into a free slot with
            event 'fission' and inherits the parent's velocity; the parent keeps its identity and
            its previous velocity for that tick.
  birth     a component with no parent takes the lowest free slot (velocity 0); in decreasing mass
            order; slots freed this tick are not reused before the next tick; with no free slot the
            component is left untracked until one frees up.
  death     a slot with no component and no fallback match is emptied (all features 0).
  velocity  min-image centroid displacement over the last tick (px per tick) for a slot that
            continued without an event.
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
import scipy.ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC_DIR = os.path.join(os.path.dirname(HERE), "spec")
L0_DIR = os.path.join(os.path.dirname(HERE), "level0")
for _p in (SPEC_DIR, L0_DIR):        # appended, so that modules here (analyze.py) shadow level0's
    if _p not in sys.path:
        sys.path.append(_p)

import vecworld as vw          # noqa: E402
import flowlenia as fl         # noqa: E402
from metrics import periodic_label   # noqa: E402

# per-world integration settings (tracker settings follow the level-0 screens)
WORLD_CFG = {
    "A_gliders": dict(stride=20, K=12, G=8, m_min=20.0, burn_in=50),
    "B_swarm": dict(stride=20, K=24, G=8, m_min=20.0, burn_in=50),
    "C_cells": dict(stride=20, K=12, G=8, m_min=40.0, burn_in=50),
}

OBJ_FEATURES = ["present", "mass", "frac_c1", "x_cos", "x_sin", "y_cos", "y_sin", "rg", "q1", "q2", "vx", "vy"]
NF = len(OBJ_FEATURES)
# memory slot table: the NF features, then raw centroid (cy, cx), age, event code, track uid
SLOT_EXTRA = ["cy", "cx", "age", "event", "uid"]
NS = NF + len(SLOT_EXTRA)
EV = {"none": 0, "birth": 1, "fission": 2, "fusion": 3, "fused": -1, "death": -2}
N_GLOBAL = 5   # next_uid, births, deaths, fusions, fissions (cumulative)

DEFAULT_INPUTS = vw.InputConstraints(k=8, lo=-1.0, hi=1.0, total=4.0, zero_sum=True)
DEFAULT_OBS = vw.ObservationSpec(noise=0.0, quantum=1e-3)


# ----------------------------------------------------------------------------------- level 0
class Level0:
    """Flow-Lenia law, initial distribution and the mass-moving kick for one level-0 world."""

    def __init__(self, name: str, stride: int = 20, noise_std: float = 0.5):
        P = json.load(open(os.path.join(L0_DIR, "worlds", name, "params.json")))
        self.name = name
        self.meta = P
        self.params = dict(P["params"])
        self.params["noise"] = {"mode": "none", "std": 0.0, "seed": 0}   # noise comes from VW-0
        self.C = int(self.params["C"])
        self.H = self.W = int(P["init"]["size"])
        self.HW = self.H * self.W
        self.n0 = self.C * self.HW
        self.shape = (self.C, self.H, self.W)
        self.init_cfg = P["init"]
        self.screen = P["screen"]
        self.stride = int(stride)
        self.noise_std = float(noise_std)
        self.noise_dim = self.stride * 2 * self.n0 if self.noise_std > 0 else 0

    def substep(self, A, z=None):
        Fy, Fx = fl.flow(A, self.params)
        if z is not None:
            Fy = Fy + self.noise_std * z[0]
            Fx = Fx + self.noise_std * z[1]
        return fl.reintegrate(A, Fy, Fx, self.params)

    def law(self, h, xi):
        out = np.empty_like(h)
        m = 2 * self.n0
        for b in range(h.shape[0]):
            A = h[b].reshape(self.shape)
            for s in range(self.stride):
                z = xi[b, s * m:(s + 1) * m].reshape((2,) + self.shape) if self.noise_dim else None
                A = self.substep(A, z)
            out[b] = A.ravel()
        return out

    def init(self, rng):
        c = self.init_cfg
        seed = int(rng.integers(0, 2 ** 31 - 1))
        return fl.init_patches(seed, self.C, self.H, self.W, c["n_patches"], c["L"]).ravel()

    def kick(self, h, u):
        """Actuators are the H*W cells (one physical type: matter at a cell, all channels together).
        u (B, H*W): commanded matter moves. A source (u < 0) removes min(-u, A_sum) from its cell
        with the cell's own channel composition; for a zero-sum command the removed matter is
        pooled and the sinks (u > 0) receive all of it, in the commanded proportions, with the pooled
        composition. Every channel's mass is conserved exactly and A stays >= 0. A non-zero-sum
        command (designer probes only) adds its positive part as given, split equally over channels."""
        C, HW = self.C, self.HW
        out = h.copy()
        for b in range(h.shape[0]):
            nz = np.flatnonzero(u[b])
            if nz.size == 0:
                continue
            v = u[b, nz]
            A = out[b].reshape(C, HW)
            src, snk = nz[v < 0], nz[v > 0]
            S = A[:, src].sum(0)
            take = np.minimum(-v[v < 0], np.maximum(S, 0.0))
            frac = np.where(S > 0, take / np.maximum(S, 1e-300), 0.0)
            removed = A[:, src] * frac[None, :]                      # (C, n_src)
            A[:, src] -= removed
            pooled = removed.sum(1)                                  # (C,)
            w = v[v > 0]
            # same tolerance as InputConstraints' zero-sum check, so every accepted zero-sum input
            # takes the mass-conserving branch (review: a sum of 9e-10 passed the check but added matter)
            if abs(v.sum()) <= 1e-9 * max(1.0, np.abs(v).sum()):
                if w.sum() > 0 and pooled.sum() > 0:
                    A[:, snk] += pooled[:, None] * (w / w.sum())[None, :]
            else:
                A[:, snk] += w[None, :] / C
            A[:, src] = np.maximum(A[:, src], 0.0)
        return out

    def invariants(self):
        HW = self.HW
        return {f"mass_c{c}": (lambda c: (lambda h: h[:, c * HW:(c + 1) * HW].sum(1)))(c)
                for c in range(self.C)}


# ----------------------------------------------------------------------------- Phi_coarse
def make_phi_coarse(l0: Level0, G: int = 8):
    C, H, W = l0.shape
    b = H // G
    assert b * G == H and W == H

    def coarse(h, m=None):
        B = h.shape[0]
        A = h.reshape(B, C, G, b, G, b)
        mean = A.mean((3, 5)).reshape(B, -1)
        S = A.sum(1)
        m2 = (S ** 2).mean((2, 4)).reshape(B, -1)
        return np.concatenate([mean, m2], 1)

    n1 = C * G * G + G * G
    names = [f"mean_c{c}[{i},{j}]" for c in range(C) for i in range(G) for j in range(G)] + \
            [f"m2[{i},{j}]" for i in range(G) for j in range(G)]
    return coarse, n1, names


# ----------------------------------------------------------------------------- Phi_objects
class Tracker:
    """Object tracker: memory m = [slot-label map (H*W) | slot table (K*NS) | globals]."""

    def __init__(self, l0: Level0, K: int, m_min: float, blur=None, thr=None):
        self.l0 = l0
        self.K = int(K)
        self.m_min = float(m_min)
        self.blur = float(l0.screen["blur_px"] if blur is None else blur)
        self.thr = float(l0.screen["threshold_on_blurred_Asum"] if thr is None else thr)
        H, W = l0.H, l0.W
        self.n_m = H * W + self.K * NS + N_GLOBAL
        yy, xx = np.mgrid[0:H, 0:W]
        self.yy, self.xx = yy.ravel().astype(float), xx.ravel().astype(float)
        self.ty, self.tx = 2 * np.pi * self.yy / H, 2 * np.pi * self.xx / W
        self.E = H / (2 * np.pi)

    # ---- components of one state ----
    def components(self, hb):
        l0 = self.l0
        A = hb.reshape(l0.shape)
        S = A.sum(0)
        Bl = ndi.gaussian_filter(S, self.blur, mode="wrap")
        lab, n = periodic_label(Bl > self.thr)
        lab = lab.ravel()
        if n == 0:
            return lab, []
        s = S.ravel()
        bc = lambda w: np.bincount(lab, w, minlength=n + 1)[1:]
        mass = bc(s)
        keep = np.flatnonzero(mass >= self.m_min)
        if keep.size == 0:
            return np.zeros_like(lab), []
        relab = np.zeros(n + 1, int)
        relab[keep + 1] = np.arange(1, keep.size + 1)
        lab = relab[lab]
        n2 = keep.size
        bc2 = lambda w: np.bincount(lab, w, minlength=n2 + 1)[1:]
        m = bc2(s)
        m1 = bc2(A[1].ravel()) if l0.C > 1 else np.zeros(n2)
        cy = np.arctan2(bc2(s * np.sin(self.ty)), bc2(s * np.cos(self.ty))) * l0.H / (2 * np.pi) % l0.H
        cx = np.arctan2(bc2(s * np.sin(self.tx)), bc2(s * np.cos(self.tx))) * l0.W / (2 * np.pi) % l0.W
        idx = lab - 1
        on = idx >= 0
        dy = (self.yy[on] - cy[idx[on]] + l0.H / 2) % l0.H - l0.H / 2
        dx = (self.xx[on] - cx[idx[on]] + l0.W / 2) % l0.W - l0.W / 2
        w = s[on]
        L = lab[on]
        syy = np.bincount(L, w * dy * dy, minlength=n2 + 1)[1:] / m
        sxx = np.bincount(L, w * dx * dx, minlength=n2 + 1)[1:] / m
        sxy = np.bincount(L, w * dx * dy, minlength=n2 + 1)[1:] / m
        tr = np.maximum(sxx + syy, 1e-12)
        comps = []
        for i in range(n2):
            comps.append({"mass": float(m[i]), "f1": float(m1[i] / m[i]), "cy": float(cy[i]), "cx": float(cx[i]),
                          "rg": float(np.sqrt(tr[i])), "q1": float((sxx[i] - syy[i]) / tr[i]),
                          "q2": float(2 * sxy[i] / tr[i])})
        return lab, comps

    def _feat(self, c, vy, vx):
        th_x, th_y = 2 * np.pi * c["cx"] / self.l0.W, 2 * np.pi * c["cy"] / self.l0.H
        return [1.0, c["mass"], c["f1"], self.E * math.cos(th_x), self.E * math.sin(th_x),
                self.E * math.cos(th_y), self.E * math.sin(th_y), c["rg"], c["q1"], c["q2"], vx, vy]

    def _mi(self, d, L):
        return (d + L / 2) % L - L / 2

    # ---- one memory update for one member ----
    def update_one(self, mb, hb):
        l0, K, HW = self.l0, self.K, self.l0.HW
        prev = mb[:HW].astype(int) if mb is not None else np.zeros(HW, int)
        T = mb[HW:HW + K * NS].reshape(K, NS).copy() if mb is not None else np.zeros((K, NS))
        g = mb[HW + K * NS:].copy() if mb is not None else np.zeros(N_GLOBAL)
        if mb is None:
            g[0] = 1.0
        active = T[:, 0] > 0.5
        lab, comps = self.components(hb)
        n = len(comps)
        newT = np.zeros((K, NS))
        assign = -np.ones(n, int)          # component -> slot
        slot_of = -np.ones(K, int)         # slot -> component
        if n and active.any():
            O = np.bincount(prev * (n + 1) + lab, minlength=(K + 1) * (n + 1)).reshape(K + 1, n + 1)[1:, 1:]
            O[~active] = 0
            pairs = np.argwhere(O > 0)
            order = np.argsort(-O[pairs[:, 0], pairs[:, 1]], kind="stable")
            for s, j in pairs[order]:
                if slot_of[s] < 0 and assign[j] < 0:
                    slot_of[s], assign[j] = j, s
            # fallback: nearest unmatched component to the predicted position
            for s in np.flatnonzero(active & (slot_of < 0) & (O.sum(1) == 0)):
                py = T[s, NF + 0] + T[s, 11]
                px = T[s, NF + 1] + T[s, 10]
                best, bd = -1, T[s, 7] + 4.0
                for j in np.flatnonzero(assign < 0):
                    if O[:, j].sum() > 0:
                        continue
                    d = math.hypot(self._mi(comps[j]["cy"] - py, l0.H), self._mi(comps[j]["cx"] - px, l0.W))
                    if d < bd:
                        best, bd = j, d
                if best >= 0:
                    slot_of[s], assign[best] = best, s
        else:
            O = np.zeros((K, max(n, 1)), int)
        events = {"fusion": 0, "fission": 0, "birth": 0, "death": 0}
        # unmatched slots that overlap a (necessarily matched) component are absorbed into the
        # component they overlap most
        absorbed = {}
        if n and active.any():
            for s in np.flatnonzero(active & (slot_of < 0)):
                if O[s].sum() > 0:
                    absorbed.setdefault(int(np.argmax(O[s])), []).append(int(s))
        # continuing slots (and fusion survivors)
        for s in np.flatnonzero(slot_of >= 0):
            j = slot_of[s]
            c = comps[j]
            parents = absorbed.get(int(j), [])
            if parents:
                ps = [s] + parents
                mm = np.array([T[p, 1] for p in ps])
                vy = float((mm * T[ps, 11]).sum() / mm.sum())
                vx = float((mm * T[ps, 10]).sum() / mm.sum())
                ev = EV["fusion"]
                events["fusion"] += len(parents)
            else:
                dy = self._mi(c["cy"] - T[s, NF + 0], l0.H)
                dx = self._mi(c["cx"] - T[s, NF + 1], l0.W)
                lost = n and any(assign[jj] < 0 and O[s, jj] > 0 for jj in range(n))
                if lost:      # this slot is the parent of a fission: keep the previous velocity
                    vy, vx, ev = float(T[s, 11]), float(T[s, 10]), EV["fission"]
                else:
                    vy, vx, ev = float(dy), float(dx), EV["none"]
            newT[s, :NF] = self._feat(c, vy, vx)
            newT[s, NF:] = [c["cy"], c["cx"], T[s, NF + 2] + 1, ev, T[s, NF + 4]]
        # slots that disappeared
        freed = np.zeros(K, bool)
        for s in np.flatnonzero(active & (slot_of < 0)):
            freed[s] = True
            fused = n and (O[s] > 0).any()
            newT[s, NF + 3] = EV["fused"] if fused else EV["death"]
            if not fused:
                events["death"] += 1
        # new components: fission products and births, by decreasing mass
        free = [s for s in range(K) if not active[s] and not freed[s]]
        for j in sorted(np.flatnonzero(assign < 0), key=lambda j: -comps[j]["mass"]):
            if not free:
                break
            s = free.pop(0)
            c = comps[j]
            par = np.flatnonzero(O[:, j] > 0) if (n and active.any()) else np.array([], int)
            if par.size:
                p = par[np.argmax(O[par, j])]
                vy, vx, ev = float(T[p, 11]), float(T[p, 10]), EV["fission"]
                events["fission"] += 1
            else:
                vy, vx, ev = 0.0, 0.0, EV["birth"]
                events["birth"] += 1
            assign[j] = s
            newT[s, :NF] = self._feat(c, vy, vx)
            newT[s, NF:] = [c["cy"], c["cx"], 0, ev, g[0]]
            g[0] += 1
        g[1] += events["birth"]
        g[2] += events["death"]
        g[3] += events["fusion"]
        g[4] += events["fission"]
        smap = np.zeros(HW)
        on = lab > 0
        sl = assign[lab[on] - 1]
        smap[np.flatnonzero(on)] = np.where(sl >= 0, sl + 1, 0)
        return np.concatenate([smap, newT.ravel(), g])

    def memory_init(self, h):
        return np.stack([self.update_one(None, h[b]) for b in range(h.shape[0])])

    def memory_update(self, m, h):
        return np.stack([self.update_one(m[b], h[b]) for b in range(h.shape[0])])

    def phi(self, h, m):
        HW, K = self.l0.HW, self.K
        T = m[:, HW:HW + K * NS].reshape(m.shape[0], K, NS)
        return T[:, :, :NF].reshape(m.shape[0], K * NF).copy()

    def table(self, m):
        HW, K = self.l0.HW, self.K
        return m[:, HW:HW + K * NS].reshape(m.shape[0], K, NS)

    def names(self):
        return [f"slot{s}.{f}" for s in range(self.K) for f in OBJ_FEATURES]


# ----------------------------------------------------------------------------------- specs
def make_specs(name: str, inputs: vw.InputConstraints = DEFAULT_INPUTS,
               observation: vw.ObservationSpec = DEFAULT_OBS, noise_std: float = 0.5, **over):
    """Two WorldSpecs (Phi_coarse, Phi_objects) on the same level 0. Returns (specs, parts)."""
    cfg = dict(WORLD_CFG[name])
    cfg.update(over)
    l0 = Level0(name, cfg["stride"], noise_std)
    tr = Tracker(l0, cfg["K"], cfg["m_min"])
    coarse, n1c, names_c = make_phi_coarse(l0, cfg["G"])
    note = (f"Level 0 is hidden. One tick = {cfg['stride']} hidden sub-steps. Inputs move matter: "
            "a negative coordinate removes at most the matter present at its site; under zero sum "
            "the positive coordinates receive exactly what was removed, in proportion.")
    common = dict(n0=l0.n0, law=l0.law, init=l0.init, noise_dim=l0.noise_dim, n_u=l0.HW, kick=l0.kick,
                  inputs=inputs, observation=observation, burn_in=cfg["burn_in"], replay="initial",
                  invariants=l0.invariants(), notes=note)
    s_coarse = vw.WorldSpec(n1=n1c, coarse=coarse, name=f"{name}/coarse{cfg['G']}", **common)
    s_obj = vw.WorldSpec(n1=tr.K * NF, coarse=tr.phi, n_m=tr.n_m, memory_init=tr.memory_init,
                         memory_update=tr.memory_update, name=f"{name}/objects{tr.K}", **common)
    parts = {"l0": l0, "tracker": tr, "phi_coarse": coarse, "names_coarse": names_c,
             "names_objects": tr.names(), "cfg": cfg}
    return {"coarse": s_coarse, "objects": s_obj}, parts


def inverse_in_map(world: vw.VectorWorld):
    inv = -np.ones(world.spec.n_u, int)
    inv[world.in_map] = np.arange(world.n_in)
    return inv
