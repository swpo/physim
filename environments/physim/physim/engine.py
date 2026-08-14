"""physim.engine — unified multi-channel lattice-field worlds + configurable apparatus.

Template (DESIGN v0.6-v0.7): hidden state = fields x ∈ R^{C×L×L} plus apparatus
state (per-sensor position/gain/enable). One tick:

    fields:    x += dt·[ S(x) + R(x) + B(u_field) ] + noise      (or exact map form)
    apparatus: a_s += A(a_s, u_apparatus)                         (rate-limited stages)
    readout:   Y = sense(x, a_s) + measurement noise

Two reaction families ship:
  * "tanh"      — C=1 bistable lattice (+ optional slow adaptation channel):
                  the D0-D4 bulk-matter track, bit-identical to the legacy engine.
  * "grayscott" — C=2 activator-substrate kinetics: the C-track ("chemistry"),
                  localized spot objects with interactions.

Apparatus: a fraction of input ports may be wired to sensor properties
(y-position stage, gain, enable) instead of field bumps. Nothing at the
interface distinguishes them; stages integrate (persist after release),
fields relax — discovering which is which is part of the task.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

import numpy as np

__all__ = ["WorldParams", "World", "make_world", "DIFFICULTY_PRESETS"]


@dataclass(frozen=True)
class WorldParams:
    # --- core selection ---
    reaction: str = "tanh"       # "tanh" | "grayscott"
    # --- shared lattice ---
    L: int = 24                  # lattice side
    sigma: float = 0.05          # micro noise (per-tick, on the primary field)
    # --- tanh family ---
    J: float = 1.35
    alpha: float = 0.5
    n_modules: int = 1
    module_mix: float = 0.0
    beta_global: float = 0.0
    bias_spread: float = 0.0
    lam_min: float = 1.0
    lam_max: float = 1.0
    eps_adapt: float = 0.0
    g_adapt: float = 0.0
    # --- grayscott family ---
    gs_F: float = 0.030          # feed
    gs_k: float = 0.066          # kill
    gs_Du: float = 0.16
    gs_Dv: float = 0.08
    gs_warp: float = 0.0         # per-instance kinetic warp amplitude (alienization)
    gs_n_seeds: int = 3          # initial spots
    gs_steps_per_tick: int = 4   # PDE substeps per world tick (spot dynamics are slow)
    gs_drift: float = 0.0        # V-advection speed (cells/substep): objects self-drift
    # --- excitable (FitzHugh-Nagumo waves; C4) ---
    ex_Du: float = 0.9
    ex_eps: float = 0.08
    ex_beta: float = 0.7
    ex_gamma: float = 0.5
    ex_dt: float = 0.2
    ex_substeps: int = 5
    ex_pace_period: int = 70     # intrinsic pacemaker period (world ticks)
    ex_n_pace: int = 1           # intrinsic pacemakers
    # --- ecology (B0: two variants + shared consumable resource) ---
    eco_k1: float = 0.060        # variant-1 kill ("fast": grows quickly)
    eco_k2: float = 0.0615       # variant-2 kill ("efficient": dies faster alone)
    eco_c1: float = 0.010        # variant-1 resource consumption
    eco_c2: float = 0.003        # variant-2 resource consumption
    eco_R_max: float = 0.036     # resource ceiling (richness knob; selection!)
    eco_regen: float = 0.00012   # resource regeneration rate
    eco_DR: float = 0.05         # resource diffusion
    eco_n_seeds: int = 2         # seeds per variant
    eco_R_warp: float = 0.0      # alienization half-width of eco_R_max (B1 boundary worlds)
    # --- grayscott2 (two coupled species; M4) ---
    gs2_k2_delta: float = 0.0037 # species-2 kill excess (dies alone)
    gs2_alpha21: float = 0.010   # V1 presence lowers species-2 kill (dependency)
    gs2_n_seeds2: int = 3        # species-2 seeds (placed near species-1 seeds + decoys)
    # --- ports ---
    n_in: int = 6
    n_out: int = 24
    n_dead: int = 0
    meas_noise: float = 0.03
    gain_min: float = 0.8
    gain_max: float = 1.25
    p_flip: float = 0.0
    in_width: float = 8.0
    in_gain: float = 0.6
    patch_r: float = 2.5
    # --- apparatus (v0.7): input ports wired to sensor properties ---
    n_apparatus: int = 0         # how many input ports drive apparatus instead of fields
    app_rate: float = 0.35       # stage speed (cells/tick at u=1) or property rate
    # --- budget ---
    max_ticks: int = 60_000

    def to_dict(self) -> dict[str, Any]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}


class World:
    """Persistent world process; deterministic given (params, seed, salt, action
    history, noise stream)."""

    def __init__(self, params: WorldParams, seed: int):
        self.p = params
        self.seed = int(seed)
        salt = int(os.environ.get("PHYSIM_WORLD_SALT", "0") or "0")
        self._salt = salt
        rng = np.random.default_rng(np.random.SeedSequence([0xF15, self.seed, salt]))
        p = self.p
        self.N = p.L * p.L
        gx, gy = np.meshgrid(np.arange(p.L), np.arange(p.L), indexing="ij")
        self.coords = np.stack([gx.ravel(), gy.ravel()], 1).astype(float)
        self._gx, self._gy = gx, gy

        # ---------------- family-specific construction (LEGACY RNG ORDER for tanh) ---
        if p.reaction == "tanh":
            stripe = (self.coords[:, 1] * p.n_modules // p.L).astype(int)
            self.module = np.clip(stripe, 0, p.n_modules - 1)
            self.block_bias = rng.normal(0.0, p.bias_spread, p.n_modules)[self.module]
            idx = np.arange(self.N).reshape(p.L, p.L)
            self._nb = np.stack([
                np.roll(idx, 1, 0).ravel(), np.roll(idx, -1, 0).ravel(),
                np.roll(idx, 1, 1).ravel(), np.roll(idx, -1, 1).ravel()])
            self._nb_w = (self.module[self._nb] == self.module[None, :]).astype(float)
            self._nb_wsum = np.maximum(self._nb_w.sum(0), 1.0)

        def torus_d2(c):
            d = np.abs(self.coords - c)
            d = np.minimum(d, p.L - d)
            return (d ** 2).sum(1)

        # input wiring (same order/shape as legacy)
        self.centers_in = rng.uniform(0, p.L, size=(p.n_in, 2))
        B = np.stack([np.exp(-torus_d2(c) / (2 * p.in_width ** 2))
                      for c in self.centers_in], 1)
        B *= p.in_gain / max(B.sum(1).mean(), 1e-12)
        self.B = B

        # output wiring
        n_live = p.n_out - p.n_dead
        self.centers_out = rng.uniform(0, p.L, size=(n_live, 2))
        self.patches = [np.where(torus_d2(c) <= p.patch_r ** 2)[0]
                        for c in self.centers_out]
        gain = rng.uniform(p.gain_min, p.gain_max, n_live)
        flip = rng.random(n_live) < p.p_flip
        self.gain = gain * np.where(flip, -1.0, 1.0)
        self.offset = rng.normal(0, 0.15, n_live)
        self.dead_offset = rng.normal(0, 0.15, p.n_dead)
        self.chan_map = rng.permutation(p.n_out)

        if p.reaction == "tanh":
            lams = np.linspace(p.lam_min, p.lam_max, p.n_modules)
            self.lam = rng.permutation(lams)[self.module]
        elif p.reaction == "excitable":
            # alienize: jitter wave speed (Du) and refractory scale (eps, gamma)
            self.ex_Du = p.ex_Du * (1.0 + 0.15 * rng.uniform(-1, 1))
            self.ex_eps = p.ex_eps * (1.0 + 0.15 * rng.uniform(-1, 1))
            self.ex_gamma = p.ex_gamma * (1.0 + 0.1 * rng.uniform(-1, 1))
            self.ex_pace_period = int(p.ex_pace_period * (1.0 + 0.2 * rng.uniform(-1, 1)))
            self.ex_pace_centers = rng.uniform(0.15 * p.L, 0.85 * p.L,
                                               size=(p.ex_n_pace, 2))
        elif p.reaction == "ecology":
            # alienize: jitter the trade-off and richness modestly (stay in the
            # coexist-able neighborhood; certification gates the rest)
            self.eco_k1 = p.eco_k1 * (1.0 + 0.02 * rng.uniform(-1, 1))
            self.eco_k2 = p.eco_k2 * (1.0 + 0.02 * rng.uniform(-1, 1))
            self.eco_c1 = p.eco_c1 * (1.0 + 0.15 * rng.uniform(-1, 1))
            self.eco_c2 = p.eco_c2 * (1.0 + 0.15 * rng.uniform(-1, 1))
            if p.eco_R_warp > 0:
                self.eco_R_max = p.eco_R_max + p.eco_R_warp * rng.uniform(-1, 1)
            else:
                self.eco_R_max = p.eco_R_max * (1.0 + 0.06 * rng.uniform(-1, 1))
            self.eco_seed_centers1 = rng.uniform(0.12 * p.L, 0.88 * p.L,
                                                 size=(p.eco_n_seeds, 2))
            self.eco_seed_centers2 = rng.uniform(0.12 * p.L, 0.88 * p.L,
                                                 size=(p.eco_n_seeds, 2))
            self._gs_field_scale = 0.0   # set after port wiring (needs B)
        elif p.reaction in ("grayscott", "grayscott2"):
            # alienized kinetics per instance: walk ALONG the stable-spot valley
            # (empirically k_stable(F) ~ 0.066 + 0.55*(F-0.030) near F=0.030),
            # plus a small transverse jitter that stays inside the window.
            t_along = p.gs_warp * rng.uniform(-1, 1)          # valley coordinate
            t_perp = 0.01 * p.gs_warp * rng.uniform(-1, 1)    # tiny transverse
            self.gsF = float(np.clip(p.gs_F * (1.0 + t_along), 0.0295, 0.0325))
            # drift thins spots (division pressure); compensate kill rate.
            drift_dk = 0.05 * p.gs_drift
            self.gsk = (p.gs_k + drift_dk
                        + 0.55 * (self.gsF - p.gs_F)) * (1.0 + t_perp)
            n_seeds = min(p.gs_n_seeds, 5 if p.gs_drift > 0 else p.gs_n_seeds)
            self.gs_seed_centers = rng.uniform(0.15 * p.L, 0.85 * p.L,
                                               size=(n_seeds, 2))
            self._gs_field_scale = 0.0   # set after port wiring (needs B)
            # drift direction: per-world random axis-aligned-ish unit vector
            ang = rng.uniform(0, 2 * np.pi)
            self.gs_drift_vec = np.array([np.cos(ang), np.sin(ang)])
            # co-locate half the input bumps and half the sensors with objects
            # (detectors go where the sample is); the rest stay random decoys.
            n_target_in = max(1, p.n_in // 2)
            for i in range(n_target_in):
                c = self.gs_seed_centers[i % p.gs_n_seeds]
                jitter = rng.normal(0, 1.5, 2)
                self.centers_in[i] = (c + jitter) % p.L
            B = np.stack([np.exp(-torus_d2(c) / (2 * p.in_width ** 2))
                          for c in self.centers_in], 1)
            B *= p.in_gain / max(B.sum(1).mean(), 1e-12)
            self.B = B
            n_live_gs = p.n_out - p.n_dead
            n_target_out = max(1, n_live_gs // 2)
            for s_i in range(n_target_out):
                c = self.gs_seed_centers[s_i % p.gs_n_seeds]
                jitter = rng.normal(0, 2.0, 2)
                self.centers_out[s_i] = (c + jitter) % p.L
            self.patches = [np.where(torus_d2(c) <= p.patch_r ** 2)[0]
                            for c in self.centers_out]

        # ---------------- apparatus wiring (v0.7; drawn AFTER legacy stream) --------
        # Which input ports are apparatus, and what each drives. Frozen presets
        # (n_apparatus=0) draw nothing -> legacy RNG streams untouched.
        self.app_port_map: dict[int, tuple[str, int]] = {}
        if p.n_apparatus > 0:
            arng = np.random.default_rng(np.random.SeedSequence(
                [0xA99, self.seed, salt]))
            ports = arng.permutation(p.n_in)[:p.n_apparatus]
            n_live_s = p.n_out - p.n_dead
            props = ["move", "move", "gain", "enable"]   # movement twice as likely
            self.app_move_dir: dict[int, np.ndarray] = {}
            for i, port in enumerate(ports):
                prop = props[int(arng.integers(0, len(props)))]
                target = int(arng.integers(0, n_live_s))
                self.app_port_map[int(port)] = (prop, target)
                if prop == "move":
                    ang = arng.uniform(0, 2 * np.pi)
                    self.app_move_dir[int(port)] = np.array(
                        [np.cos(ang), np.sin(ang)])
            # mutable apparatus state (per live sensor)
            self.app_pos = self.centers_out.copy()          # movable positions
            self.app_gain_mult = np.ones(n_live_s)
            self.app_enabled = np.ones(n_live_s, dtype=bool)
        else:
            self.app_pos = None
            self.app_gain_mult = None
            self.app_enabled = None

        if p.reaction in ("grayscott", "grayscott2"):
            # normalize: |u|=1 on ONE port -> peak local |ΔF| = 0.012 (~40% of F)
            peak = float(self.B.max())
            self._gs_field_scale = 0.012 / max(peak, 1e-12)
        elif p.reaction == "ecology":
            # |u|=1 on one port -> peak local regen-rate multiplier ±0.8
            # (fertilize/poison a region)
            peak = float(self.B.max())
            self._gs_field_scale = 0.8 / max(peak, 1e-12)
        if p.reaction in ("grayscott2", "ecology"):
            # species tags (gs2: ports feed one species) / sensor mixes (both)
            srng = np.random.default_rng(np.random.SeedSequence(
                [0x5A2, self.seed, self._salt]))
            self.port_species = srng.integers(0, 2, p.n_in)
            n_live_s2 = p.n_out - p.n_dead
            wmix = srng.uniform(0, 1, n_live_s2)
            hard = srng.random(n_live_s2) < 0.6   # 60% of sensors are species-pure
            self.sensor_mix = np.where(hard, (wmix > 0.5).astype(float), wmix)

        # ---------------- persistent state ------------------------------------------
        self._noise = np.random.default_rng(
            np.random.SeedSequence([0xA11, self.seed, self._salt]))
        self._init_fields()
        self.ticks_used = 0
        self.n_resets = 0
        self.port_energy = np.zeros(p.n_in)   # cumulative |commanded drive| per port

    # ---------------- field initialization ----------------
    def _init_fields(self):
        p = self.p
        if p.reaction == "tanh":
            self.x = 0.01 * self._noise.standard_normal(self.N)
            self.a = np.zeros(self.N)
        elif p.reaction == "ecology":
            L = p.L
            self.U1e = np.ones((L, L)); self.V1e = np.zeros((L, L))
            self.U2e = np.ones((L, L)); self.V2e = np.zeros((L, L))
            self.Re = self.eco_R_max * np.ones((L, L))
            for cs, (Uf, Vf) in ((self.eco_seed_centers1, (self.U1e, self.V1e)),
                                 (self.eco_seed_centers2, (self.U2e, self.V2e))):
                for c in cs:
                    dx = np.minimum(np.abs(self._gx - c[0]), L - np.abs(self._gx - c[0]))
                    dy = np.minimum(np.abs(self._gy - c[1]), L - np.abs(self._gy - c[1]))
                    m = dx ** 2 + dy ** 2 <= 9
                    Uf[m] = 0.5
                    Vf[m] = 0.25
            # settle to an established ecosystem (population near capacity);
            # cache like the GS families
            if not hasattr(self, "_eco_settled"):
                zero = np.zeros(self.N)
                for _ in range(6000):
                    self._eco_substep(zero, noisy=False)
                self._eco_settled = (self.U1e.copy(), self.V1e.copy(),
                                     self.U2e.copy(), self.V2e.copy(),
                                     self.Re.copy())
            else:
                (u1, v1, u2, v2, r_) = self._eco_settled
                self.U1e = u1.copy(); self.V1e = v1.copy()
                self.U2e = u2.copy(); self.V2e = v2.copy()
                self.Re = r_.copy()
        elif p.reaction == "excitable":
            self.eu = -1.2 * np.ones((p.L, p.L))
            self.ev = -0.62 * np.ones((p.L, p.L))
            self._ex_t = 0
            self._ex_pace_masks = []
            for c in self.ex_pace_centers:
                dx = np.minimum(np.abs(self._gx - c[0]), p.L - np.abs(self._gx - c[0]))
                dy = np.minimum(np.abs(self._gy - c[1]), p.L - np.abs(self._gy - c[1]))
                self._ex_pace_masks.append(dx ** 2 + dy ** 2 <= 9)
        else:
            self.U = np.ones((p.L, p.L))
            self.V = np.zeros((p.L, p.L))
            for (cx, cy) in self.gs_seed_centers:
                m = (self._gx - cx) ** 2 + (self._gy - cy) ** 2 <= 3.0 ** 2
                self.U[m] = 0.5
                self.V[m] = 0.25
            # settle so tasks start with formed objects (no agent budget spent);
            # cache the settled fields so clone_fresh / fresh_sample skip the
            # expensive re-settle (they restart from the same formed state).
            if self.p.reaction == "grayscott2" and not hasattr(self, "U2"):
                pass  # initialized below with U/V
            if not hasattr(self, "_gs_settled"):
                if self.p.reaction == "grayscott2":
                    self.U2 = np.ones((self.p.L, self.p.L))
                    self.V2 = np.zeros((self.p.L, self.p.L))
                    rng2 = np.random.default_rng(np.random.SeedSequence(
                        [0x5A3, self.seed, self._salt]))
                    for i in range(self.p.gs2_n_seeds2):
                        if i < len(self.gs_seed_centers) and rng2.random() < 0.7:
                            c = self.gs_seed_centers[i] + rng2.normal(0, 2.5, 2)
                        else:
                            c = rng2.uniform(0.15 * self.p.L, 0.85 * self.p.L, 2)
                        m = ((self._gx - c[0]) % self.p.L) ** 2 +                             ((self._gy - c[1]) % self.p.L) ** 2 <= 9
                        m = (np.minimum(np.abs(self._gx - c[0]), self.p.L - np.abs(self._gx - c[0])) ** 2
                             + np.minimum(np.abs(self._gy - c[1]), self.p.L - np.abs(self._gy - c[1])) ** 2) <= 9
                        self.U2[m] = 0.5
                        self.V2[m] = 0.25
                zero_field = np.zeros(self.N)
                for _ in range(1500):
                    self._gs_substep(zero_field, noisy=False)
                # cull to <=6 objects (crowded starts cascade into replication
                # on drifting worlds); remove smallest by V-mass, then re-settle
                from scipy import ndimage
                lab, n = ndimage.label(self.V > 0.15)
                if n > 6:
                    masses = ndimage.sum(self.V, lab, range(1, n + 1))
                    keep = set((np.argsort(masses)[-6:] + 1).tolist())
                    for obj_id in range(1, n + 1):
                        if obj_id not in keep:
                            self.V[lab == obj_id] = 0.0
                    for _ in range(400):
                        self._gs_substep(zero_field, noisy=False)
                if self.p.reaction == "grayscott2":
                    self._gs_settled = (self.U.copy(), self.V.copy(),
                                        self.U2.copy(), self.V2.copy())
                else:
                    self._gs_settled = (self.U.copy(), self.V.copy())
            else:
                self.U = self._gs_settled[0].copy()
                self.V = self._gs_settled[1].copy()
                if self.p.reaction == "grayscott2":
                    self.U2 = self._gs_settled[2].copy()
                    self.V2 = self._gs_settled[3].copy()

    # ---------------- tanh micro dynamics (bit-identical to legacy) ----------------
    def _mix(self, x: np.ndarray) -> np.ndarray:
        p = self.p
        out = (x[self._nb] * self._nb_w).sum(0) / self._nb_wsum
        if p.n_modules > 1 and p.module_mix > 0:
            mmean = np.zeros(p.n_modules)
            np.add.at(mmean, self.module, x)
            counts = np.bincount(self.module, minlength=p.n_modules)
            mmean = mmean / np.maximum(counts, 1)
            out = (1 - p.module_mix) * out + p.module_mix * mmean[self.module]
        if p.beta_global > 0:
            out = (1 - p.beta_global) * out + p.beta_global * x.mean()
        return out

    def _tanh_step(self, field_u: np.ndarray) -> None:
        p = self.p
        pre = p.J * ((1 - p.alpha) * self.x + p.alpha * self._mix(self.x))
        pre = pre + self.block_bias + field_u - p.g_adapt * self.a
        target = np.tanh(pre + p.sigma * self._noise.standard_normal(self.N))
        self.x = (1.0 - self.lam) * self.x + self.lam * target
        if p.eps_adapt > 0:
            self.a += p.eps_adapt * (self.x - self.a)

    # ---------------- gray-scott micro dynamics ----------------
    def _gs_substep(self, field_u: np.ndarray, noisy: bool = True,
                    field_u2: np.ndarray | None = None) -> None:
        p = self.p
        lap = lambda z: (np.roll(z, 1, 0) + np.roll(z, -1, 0)
                         + np.roll(z, 1, 1) + np.roll(z, -1, 1) - 4 * z)
        uvv = self.U * self.V * self.V
        Feff = self.gsF + field_u.reshape(p.L, p.L)
        newU = self.U + p.gs_Du * lap(self.U) - uvv + Feff * (1 - self.U)
        newV = self.V + p.gs_Dv * lap(self.V) + uvv - (Feff + self.gsk) * self.V
        if p.gs_drift > 0:
            wx = p.gs_drift * self.gs_drift_vec[0]
            wy = p.gs_drift * self.gs_drift_vec[1]
            dVx = (np.roll(self.V, -1, 0) - np.roll(self.V, 1, 0)) / 2.0
            dVy = (np.roll(self.V, -1, 1) - np.roll(self.V, 1, 1)) / 2.0
            newV = newV - wx * dVx - wy * dVy
        self.U = newU
        self.V = newV
        if noisy and p.sigma > 0:
            self.V = np.clip(
                self.V + p.sigma * 0.01 * self._noise.standard_normal((p.L, p.L)),
                0.0, None)
        if p.reaction == "grayscott2":
            V1s = (self.V + np.roll(self.V, 1, 0) + np.roll(self.V, -1, 0)
                   + np.roll(self.V, 1, 1) + np.roll(self.V, -1, 1)) / 5.0
            uvv2 = self.U2 * self.V2 * self.V2
            F2eff = self.gsF + (field_u2.reshape(p.L, p.L)
                                if field_u2 is not None else 0.0)
            k2eff = (self.gsk + p.gs2_k2_delta
                     - p.gs2_alpha21 * (V1s / 0.25))
            newU2 = self.U2 + p.gs_Du * lap(self.U2) - uvv2 + F2eff * (1 - self.U2)
            newV2 = self.V2 + p.gs_Dv * lap(self.V2) + uvv2 - (F2eff + k2eff) * self.V2
            self.U2 = newU2
            self.V2 = newV2
            if noisy and p.sigma > 0:
                self.V2 = np.clip(
                    self.V2 + p.sigma * 0.01 * self._noise.standard_normal((p.L, p.L)),
                    0.0, None)

    # ---------------- ecology dynamics ----------------
    def _eco_substep(self, field_u: np.ndarray, noisy: bool = True) -> None:
        p = self.p
        lapf = lambda z: (np.roll(z, 1, 0) + np.roll(z, -1, 0)
                          + np.roll(z, 1, 1) + np.roll(z, -1, 1) - 4 * z)
        uvv1 = self.U1e * self.V1e * self.V1e
        uvv2 = self.U2e * self.V2e * self.V2e
        R = self.Re
        self.U1e = self.U1e + p.gs_Du * lapf(self.U1e) - uvv1 + R * (1 - self.U1e)
        self.V1e = self.V1e + p.gs_Dv * lapf(self.V1e) + uvv1 - (R + self.eco_k1) * self.V1e
        self.U2e = self.U2e + p.gs_Du * lapf(self.U2e) - uvv2 + R * (1 - self.U2e)
        self.V2e = self.V2e + p.gs_Dv * lapf(self.V2e) + uvv2 - (R + self.eco_k2) * self.V2e
        # resource: diffusion + regeneration (port-modulated) - consumption
        regen_mult = 1.0 + field_u.reshape(p.L, p.L)      # ports fertilize/poison
        regen_mult = np.clip(regen_mult, 0.0, 2.0)
        self.Re = R + p.eco_DR * lapf(R)             + p.eco_regen * regen_mult * (self.eco_R_max - R) * self.eco_R_max * 300             - (self.eco_c1 * self.V1e + self.eco_c2 * self.V2e) * R
        self.Re = np.clip(self.Re, 0.0, self.eco_R_max)
        if noisy and p.sigma > 0:
            self.V1e = np.clip(self.V1e + p.sigma * 0.01
                               * self._noise.standard_normal((p.L, p.L)), 0.0, None)
            self.V2e = np.clip(self.V2e + p.sigma * 0.01
                               * self._noise.standard_normal((p.L, p.L)), 0.0, None)

    # ---------------- apparatus dynamics ----------------
    def _apparatus_step(self, u: np.ndarray) -> np.ndarray:
        """Apply apparatus port drives; return u with apparatus ports zeroed
        (they do not couple into the fields)."""
        if not self.app_port_map:
            return u
        u = u.copy()
        p = self.p
        for port, (prop, s) in self.app_port_map.items():
            v = float(np.clip(u[port], -1, 1))
            u[port] = 0.0
            if v == 0.0:
                continue
            if prop == "move":
                step = p.app_rate * v * self.app_move_dir[port]
                self.app_pos[s] = (self.app_pos[s] + step) % p.L
            elif prop == "gain":
                self.app_gain_mult[s] = float(
                    np.clip(self.app_gain_mult[s] + 0.02 * v, 0.0, 2.5))
            elif prop == "enable":
                # accumulate drive; crossing +-1 toggles state (needs sustained push)
                acc = getattr(self, "_app_enable_acc", None)
                if acc is None:
                    acc = np.zeros(len(self.app_enabled))
                    self._app_enable_acc = acc
                acc[s] += 0.05 * v
                if acc[s] >= 1.0:
                    self.app_enabled[s] = True
                    acc[s] = 0.0
                elif acc[s] <= -1.0:
                    self.app_enabled[s] = False
                    acc[s] = 0.0
        return u

    # ---------------- readout ----------------
    def _read(self) -> np.ndarray:
        p = self.p
        n_live = p.n_out - p.n_dead
        if p.reaction == "tanh":
            primary = self.x
        elif p.reaction == "excitable":
            primary = (self.eu.ravel() + 1.2) * 0.8 - 0.5   # rest ~ -0.5, pulse ~ +1.2
        elif p.reaction in ("grayscott2", "ecology"):
            primary = None   # per-sensor mix computed below
        else:
            primary = self.V.ravel() * 4.0 - 0.5
        if p.reaction in ("grayscott2", "ecology"):
            if p.reaction == "ecology":
                s1 = self.V1e.ravel() * 4.0 - 0.5
                s2 = self.V2e.ravel() * 4.0 - 0.5
            else:
                s1 = self.V.ravel() * 4.0 - 0.5
                s2 = self.V2.ravel() * 4.0 - 0.5
            def read_patch(idx, s_i):
                w_ = float(self.sensor_mix[s_i])
                return (1 - w_) * s1[idx].mean() + w_ * s2[idx].mean()
        else:
            def read_patch(idx, s_i):
                return primary[idx].mean()
        if self.app_pos is None:
            raw = np.array([read_patch(idx, s_i)
                            for s_i, idx in enumerate(self.patches)])
            gains = self.gain
            enabled = None
        else:
            raw = np.empty(n_live)
            for s in range(n_live):
                d = np.abs(self.coords - self.app_pos[s])
                d = np.minimum(d, p.L - d)
                m = (d ** 2).sum(1) <= p.patch_r ** 2
                raw[s] = read_patch(np.where(m)[0], s) if m.any() else 0.0
            gains = self.gain * self.app_gain_mult
            enabled = self.app_enabled
        live = gains * raw + self.offset \
            + p.meas_noise * self._noise.standard_normal(n_live)
        if enabled is not None:
            off = self.offset + p.meas_noise * self._noise.standard_normal(n_live)
            live = np.where(enabled, live, off)
        dead = self.dead_offset + p.meas_noise * self._noise.standard_normal(p.n_dead)
        return np.concatenate([live, dead])[self.chan_map]

    # ---------------- public stepping ----------------
    def _step(self, u: np.ndarray) -> None:
        u = np.clip(np.asarray(u, dtype=float), -1.0, 1.0)
        self.port_energy += np.abs(u)
        u = self._apparatus_step(u)
        field = self.B @ u
        if self.p.reaction == "tanh":
            self._tanh_step(field)
        elif self.p.reaction == "ecology":
            eco_field = field * self._gs_field_scale
            for _ in range(self.p.gs_steps_per_tick):
                self._eco_substep(eco_field)
        elif self.p.reaction == "excitable":
            p = self.p
            lapf = lambda z: (np.roll(z, 1, 0) + np.roll(z, -1, 0)
                              + np.roll(z, 1, 1) + np.roll(z, -1, 1) - 4 * z)
            # ports inject current: scale so |u|=1 -> peak I ~ 0.8 (pulse-capable)
            inj = (field / max(float(self.B.max()), 1e-12) * 0.8).reshape(p.L, p.L)
            for _ in range(p.ex_substeps):
                I = inj.copy()
                for m in self._ex_pace_masks:
                    if (self._ex_t % (self.ex_pace_period * p.ex_substeps)) < 8 * p.ex_substeps:
                        I = I + np.where(m, 0.8, 0.0)
                du = (self.eu - self.eu ** 3 / 3 - self.ev
                      + self.ex_Du * lapf(self.eu) + I)
                dv = self.ex_eps * (self.eu + p.ex_beta - self.ex_gamma * self.ev)
                self.eu = self.eu + p.ex_dt * du
                self.ev = self.ev + p.ex_dt * dv
                self._ex_t += 1
            if p.sigma > 0:
                self.eu = self.eu + p.sigma * 0.02 * self._noise.standard_normal((p.L, p.L))
        elif self.p.reaction == "grayscott2":
            u1 = u * (self.port_species == 0)
            u2 = u * (self.port_species == 1)
            f1 = (self.B @ u1) * self._gs_field_scale
            f2 = (self.B @ u2) * self._gs_field_scale
            for _ in range(self.p.gs_steps_per_tick):
                self._gs_substep(f1, field_u2=f2)
        else:
            gs_field = field * self._gs_field_scale
            for _ in range(self.p.gs_steps_per_tick):
                self._gs_substep(gs_field)

    def run(self, U: np.ndarray) -> np.ndarray:
        U = np.atleast_2d(np.asarray(U, dtype=float))
        if U.ndim != 2 or U.shape[1] != self.p.n_in:
            raise ValueError(f"U must be [T, {self.p.n_in}], got {U.shape}")
        T = U.shape[0]
        if self.ticks_used + T > self.p.max_ticks:
            raise RuntimeError(
                f"budget exceeded: {self.ticks_used} used + {T} requested "
                f"> {self.p.max_ticks}")
        Y = np.empty((T, self.p.n_out))
        for t in range(T):
            self._step(U[t])
            Y[t] = self._read()
        self.ticks_used += T
        return Y

    def run_policy(self, jail, T: int) -> np.ndarray:
        if self.ticks_used + T > self.p.max_ticks:
            raise RuntimeError(
                f"budget exceeded: {self.ticks_used} used + {T} requested "
                f"> {self.p.max_ticks}")
        Y = np.empty((T, self.p.n_out))
        y = self._read()
        for t in range(T):
            a = jail.act(t, [float(v) for v in y])
            if len(a) != self.p.n_in:
                raise ValueError(f"policy returned {len(a)} values; need {self.p.n_in}")
            self._step(np.asarray(a, dtype=float))
            y = self._read()
            Y[t] = y
        self.ticks_used += T
        return Y

    def fresh_sample(self) -> None:
        cost = 200
        if self.ticks_used + cost > self.p.max_ticks:
            raise RuntimeError("budget exceeded on fresh_sample")
        self.ticks_used += cost
        self.n_resets += 1
        self._init_fields()
        if self.app_pos is not None:
            n_live = self.p.n_out - self.p.n_dead
            self.app_pos = self.centers_out.copy()
            self.app_gain_mult = np.ones(n_live)
            self.app_enabled = np.ones(n_live, dtype=bool)

    @property
    def budget_left(self) -> int:
        return self.p.max_ticks - self.ticks_used

    # ---------------- evaluator-only ----------------
    def conduct_metrics(self) -> dict:
        """Report-only exploration-conduct summary (evaluator-side).
        port_coverage: fraction of input ports the agent drove for >=10
        cumulative full-drive-tick equivalents; apparatus_displacement: how far
        any movable sensor was actually moved from its home position."""
        out = {
            "port_coverage": float(np.mean(self.port_energy >= 10.0)),
            "port_energy_min": float(self.port_energy.min()),
        }
        if self.app_pos is not None:
            d = np.abs(self.app_pos - self.centers_out)
            d = np.minimum(d, self.p.L - d)
            out["apparatus_displacement"] = float(np.hypot(d[:, 0], d[:, 1]).max())
        return out

    def certify(self) -> bool:
        """Cheap generation-time health check (evaluator-side, no budget).
        Gray-Scott: object count stays in [1, 12] over a long free run."""
        if self.p.reaction == "ecology":
            probe = self.clone_fresh(noise_seed=555)
            from scipy import ndimage
            boundary = self.p.eco_R_warp > 0
            for _ in range(3):
                probe.run(np.zeros((1200, self.p.n_in)))
                n1 = ndimage.label(probe.V1e > 0.15)[1]
                n2 = ndimage.label(probe.V2e > 0.15)[1]
                if boundary:
                    # exclusion of variant 1 is legitimate physics here; require
                    # a living ecosystem overall and variant 2 healthy
                    if not (3 <= n2 <= 90 and n1 <= 90 and (n1 + n2) >= 5):
                        return False
                else:
                    if not (3 <= n1 <= 90 and 3 <= n2 <= 90):
                        return False
            return True
        if self.p.reaction not in ("grayscott", "grayscott2"):
            return True
        probe = self.clone_fresh(noise_seed=555)
        from scipy import ndimage
        for _ in range(3):
            probe.run(np.zeros((800, self.p.n_in)))
            n = ndimage.label(probe.V > 0.15)[1]
            if not (1 <= n <= 12):
                return False
            if self.p.reaction == "grayscott2":
                n2 = ndimage.label(probe.V2 > 0.15)[1]
                if not (1 <= n2 <= 12):
                    return False
        return True

    def clone_fresh(self, noise_seed: int) -> "World":
        w = World.__new__(World)
        w.__dict__.update({k: v for k, v in self.__dict__.items()
                           if k not in ("U", "V", "U2", "V2", "x", "a", "eu", "ev",
                                        "U1e", "V1e", "U2e", "V2e", "Re",
                                        "_ex_t", "_noise",
                                        "ticks_used", "n_resets", "port_energy",
                                        "app_pos", "app_gain_mult", "app_enabled",
                                        "_app_enable_acc")})
        w.port_energy = np.zeros(self.p.n_in)
        w._noise = np.random.default_rng(
            np.random.SeedSequence([0xE7A1, self.seed, self._salt, noise_seed]))
        if self.p.n_apparatus > 0:
            n_live = self.p.n_out - self.p.n_dead
            w.app_pos = self.centers_out.copy()
            w.app_gain_mult = np.ones(n_live)
            w.app_enabled = np.ones(n_live, dtype=bool)
        else:
            w.app_pos = None
            w.app_gain_mult = None
            w.app_enabled = None
        w._init_fields()
        w.ticks_used = 0
        w.n_resets = 0
        return w

    def true_channel_range(self) -> np.ndarray:
        n_live = self.p.n_out - self.p.n_dead
        internal = np.concatenate([2.0 * np.abs(self.gain), np.zeros(self.p.n_dead)])
        return internal[self.chan_map]

    def true_is_dead(self) -> np.ndarray:
        n_live = self.p.n_out - self.p.n_dead
        return self.chan_map >= n_live

    def true_macro(self) -> np.ndarray:
        if self.p.reaction == "ecology":
            from scipy import ndimage
            n1 = ndimage.label(self.V1e > 0.15)[1]
            n2 = ndimage.label(self.V2e > 0.15)[1]
            return np.array([float(n1), float(n2),
                             float(self.Re.mean() / self.eco_R_max)])
        if self.p.reaction == "excitable":
            return np.array([float((self.eu > 0).mean()), float(self.ev.mean())])
        if self.p.reaction == "tanh":
            mmean = np.zeros(self.p.n_modules)
            np.add.at(mmean, self.module, self.x)
            counts = np.bincount(self.module, minlength=self.p.n_modules)
            return mmean / np.maximum(counts, 1)
        # grayscott: object count + total mass as the macro summary
        from scipy import ndimage
        mask = self.V > 0.15
        _, n = ndimage.label(mask)
        if self.p.reaction == "grayscott2":
            mask2 = self.V2 > 0.15
            _, n2 = ndimage.label(mask2)
            return np.array([float(n), float(self.V.sum()),
                             float(n2), float(self.V2.sum())])
        return np.array([float(n), float(self.V.sum())])

    def true_objects(self) -> list[tuple[float, float]]:
        """Gray-Scott only: centroids of live spots (evaluator/certifier use)."""
        if self.p.reaction == "ecology":
            from scipy import ndimage
            mask = self.V1e > 0.15
            lab, n = ndimage.label(mask)
            return [tuple(map(float, c)) for c in
                    ndimage.center_of_mass(mask, lab, range(1, n + 1))]
        if self.p.reaction not in ("grayscott", "grayscott2"):
            return []
        from scipy import ndimage
        mask = self.V > 0.15
        lab, n = ndimage.label(mask)
        return [tuple(map(float, c)) for c in
                ndimage.center_of_mass(mask, lab, range(1, n + 1))]

    def true_objects2(self) -> list[tuple[float, float]]:
        """Species-2 object centroids (grayscott2/ecology; evaluator use)."""
        if self.p.reaction == "ecology":
            from scipy import ndimage
            mask = self.V2e > 0.15
            lab, n = ndimage.label(mask)
            return [tuple(map(float, c)) for c in
                    ndimage.center_of_mass(mask, lab, range(1, n + 1))]
        if self.p.reaction != "grayscott2":
            return []
        from scipy import ndimage
        mask = self.V2 > 0.15
        lab, n = ndimage.label(mask)
        return [tuple(map(float, c)) for c in
                ndimage.center_of_mass(mask, lab, range(1, n + 1))]


# ---------------- difficulty ladder ----------------
DIFFICULTY_PRESETS: dict[str, WorldParams] = {
    # -------- bulk-matter track (bit-identical to legacy engine) --------
    "D0": WorldParams(
        L=24, J=1.35, n_modules=1, sigma=0.04,
        n_in=6, n_out=24, n_dead=0, meas_noise=0.02,
        gain_min=0.9, gain_max=1.1, p_flip=0.0, max_ticks=80_000),
    "D1": WorldParams(
        L=24, J=1.35, n_modules=1, sigma=0.05,
        n_in=6, n_out=32, n_dead=4, meas_noise=0.05,
        gain_min=0.6, gain_max=1.6, p_flip=0.35, max_ticks=80_000),
    "D2": WorldParams(
        L=24, J=1.35, n_modules=3, module_mix=0.55, bias_spread=0.10, sigma=0.05,
        n_in=6, n_out=36, n_dead=4, meas_noise=0.05,
        gain_min=0.6, gain_max=1.6, p_flip=0.35, in_width=3.0, in_gain=0.9,
        max_ticks=100_000),
    "D3": WorldParams(
        L=30, J=1.45, n_modules=6, module_mix=0.6, beta_global=0.08,
        bias_spread=0.04, sigma=0.06,
        n_in=8, n_out=48, n_dead=8, meas_noise=0.07,
        gain_min=0.5, gain_max=1.8, p_flip=0.4, in_width=2.5, in_gain=1.0,
        max_ticks=60_000),
    "D4": WorldParams(
        L=32, J=1.40, n_modules=8, module_mix=0.55, beta_global=0.05,
        bias_spread=0.05, sigma=0.06, lam_min=0.04, lam_max=1.0,
        eps_adapt=0.005, g_adapt=0.55,
        n_in=10, n_out=60, n_dead=10, meas_noise=0.08,
        gain_min=0.4, gain_max=2.0, p_flip=0.4, in_width=2.5, in_gain=1.1,
        max_ticks=150_000),
    # -------- chemistry track (Gray-Scott objects; v0.7 apparatus) --------
    "C0": WorldParams(  # visible chemistry: fixed sensors, few objects, clean
        reaction="grayscott", L=64, sigma=0.02,
        gs_F=0.030, gs_k=0.066, gs_warp=0.05, gs_n_seeds=3, gs_steps_per_tick=4,
        n_in=6, n_out=30, n_dead=2, meas_noise=0.03,
        gain_min=0.8, gain_max=1.3, p_flip=0.2, in_width=5.0, in_gain=1.0,
        patch_r=4.0, n_apparatus=0, max_ticks=120_000),
    "C1": WorldParams(  # microscopy: 2 apparatus ports (movable sensing), murkier
        reaction="grayscott", L=96, sigma=0.02,
        gs_F=0.030, gs_k=0.066, gs_warp=0.08, gs_n_seeds=4, gs_steps_per_tick=4,
        n_in=8, n_out=36, n_dead=4, meas_noise=0.05,
        gain_min=0.6, gain_max=1.6, p_flip=0.35, in_width=5.0, in_gain=1.0,
        patch_r=4.0, n_apparatus=2, app_rate=0.5, max_ticks=150_000),
    "C2": WorldParams(  # moving chemistry: drifting objects + apparatus + count dynamics
        reaction="grayscott", L=96, sigma=0.02,
        gs_F=0.030, gs_k=0.066, gs_warp=0.06, gs_n_seeds=5, gs_steps_per_tick=4,
        gs_drift=0.005,
        n_in=8, n_out=40, n_dead=4, meas_noise=0.05,
        gain_min=0.6, gain_max=1.6, p_flip=0.35, in_width=5.0, in_gain=1.0,
        patch_r=4.0, n_apparatus=2, app_rate=0.5, max_ticks=200_000),
    "C3": WorldParams(  # multi-species chemistry (M4): two coupled species,
        # species-tagged ports/sensors, dependency + cascade laws
        reaction="grayscott2", L=96, sigma=0.02,
        gs_F=0.030, gs_k=0.066, gs_warp=0.05, gs_n_seeds=4, gs_steps_per_tick=4,
        gs2_k2_delta=0.0037, gs2_alpha21=0.010, gs2_n_seeds2=4,
        n_in=8, n_out=40, n_dead=4, meas_noise=0.05,
        gain_min=0.6, gain_max=1.6, p_flip=0.35, in_width=5.0, in_gain=1.0,
        patch_r=4.0, n_apparatus=0, max_ticks=200_000),
    "C4": WorldParams(  # excitable chemistry: traveling waves, refractory block,
        # pacemaker competition; ports can CREATE rhythm sources
        reaction="excitable", L=96, sigma=0.03,
        ex_pace_period=70, ex_n_pace=1,
        n_in=8, n_out=40, n_dead=4, meas_noise=0.05,
        gain_min=0.6, gain_max=1.6, p_flip=0.35, in_width=3.0, in_gain=1.0,
        patch_r=3.0, n_apparatus=0, max_ticks=200_000),
    "B0": WorldParams(  # biology track: two organism variants + shared resource
        # laws: carrying capacity; competition; scarcity selects the efficient
        reaction="ecology", L=96, sigma=0.02, gs_steps_per_tick=4,
        eco_k1=0.060, eco_k2=0.0615, eco_c1=0.010, eco_c2=0.003,
        eco_R_max=0.036, eco_regen=0.00012, eco_DR=0.05, eco_n_seeds=2,
        n_in=8, n_out=40, n_dead=4, meas_noise=0.05,
        gain_min=0.6, gain_max=1.6, p_flip=0.35, in_width=16.0, in_gain=1.0,
        patch_r=4.0, n_apparatus=0, max_ticks=250_000),
    "B1": WorldParams(  # selection-boundary worlds: richness straddles exclusion
        reaction="ecology", L=96, sigma=0.02, gs_steps_per_tick=4,
        eco_k1=0.060, eco_k2=0.0615, eco_c1=0.010, eco_c2=0.003,
        eco_R_max=0.034, eco_R_warp=0.003,   # instances span [0.031, 0.037]
        eco_regen=0.00012, eco_DR=0.05, eco_n_seeds=2,
        n_in=8, n_out=40, n_dead=4, meas_noise=0.05,
        gain_min=0.6, gain_max=1.6, p_flip=0.35, in_width=16.0, in_gain=1.0,
        patch_r=4.0, n_apparatus=0, max_ticks=250_000),
}


def make_world(difficulty: str, seed: int) -> World:
    return World(DIFFICULTY_PRESETS[difficulty], seed)
