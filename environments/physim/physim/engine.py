"""physim.engine — hidden micro-world + anonymous port layer.

Design (DESIGN.md v0.1-v0.5): the agent sees only
    run(U) -> Y      U: [T, n_in] in [-1,1], Y: [T, n_out]
State persists across calls. Everything else (micro state, wiring, params)
is evaluator-only.

World family for M0: modular tanh lattice.
  x' = tanh( J * ((1-a)*x + a*mix(x)) + block_bias + field(U) + sigma*xi )
  mix = (1-beta_g)*[(1-bm)*local_neighbors + bm*module_mean] + beta_g*global_mean
Motifs: locality, modularity (n_modules), heterogeneity (block biases),
global tie (beta_g). J>Jc gives collective bistability + hysteresis.

Port layer: inputs couple as smooth bump fields; outputs are noisy affine
reads of small patches with random gain/sign/offset, shuffled order, plus
dead channels. Difficulty knobs are all here + in the core params.
"""

from __future__ import annotations

import os

from dataclasses import dataclass, field
from typing import Any

import numpy as np

__all__ = ["WorldParams", "World", "make_world", "DIFFICULTY_PRESETS"]


@dataclass(frozen=True)
class WorldParams:
    # --- micro core ---
    L: int = 24                  # lattice side (N = L*L)
    J: float = 1.35              # coupling gain (>~1.15 => bistable collective)
    alpha: float = 0.5           # neighbor mixing
    n_modules: int = 1           # modular blocks (k* driver)
    module_mix: float = 0.0      # 0=pure local, 1=pure module-mean coupling
    beta_global: float = 0.0     # weak global tie
    bias_spread: float = 0.0     # per-module bias std (heterogeneity)
    sigma: float = 0.05          # micro noise
    lam_min: float = 1.0         # slowest module response rate (1.0 = instant)
    lam_max: float = 1.0         # fastest module response rate
    eps_adapt: float = 0.0       # slow adaptation rate (0 = off); timescale ~ 1/eps
    g_adapt: float = 0.0         # adaptation feedback strength
    # --- ports ---
    n_in: int = 6
    n_out: int = 24
    n_dead: int = 0
    meas_noise: float = 0.03
    gain_min: float = 0.8
    gain_max: float = 1.25
    p_flip: float = 0.0          # probability an output has negative sign
    in_width: float = 8.0        # input bump width (bigger = smoother/global)
    in_gain: float = 0.6         # field strength at U=1 on all ports
    patch_r: float = 2.5         # output patch radius
    # --- budget ---
    max_ticks: int = 60_000      # experiment budget (world ticks)

    def to_dict(self) -> dict[str, Any]:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}


class World:
    """Persistent world process. Deterministic given (params, seed, action history,
    noise stream); noise stream is seeded per-instance and advances with use."""

    def __init__(self, params: WorldParams, seed: int):
        self.p = params
        self.seed = int(seed)
        # Optional evaluator-side salt: mixes into wiring + noise so public code
        # + a guessed seed cannot reproduce a live world (set PHYSIM_WORLD_SALT
        # for held-out evals; unset = reproducible published defaults).
        salt = int(os.environ.get("PHYSIM_WORLD_SALT", "0") or "0")
        self._salt = salt
        rng = np.random.default_rng(np.random.SeedSequence([0xF15, self.seed, salt]))
        p = self.p
        self.N = p.L * p.L
        gx, gy = np.meshgrid(np.arange(p.L), np.arange(p.L), indexing="ij")
        self.coords = np.stack([gx.ravel(), gy.ravel()], 1).astype(float)

        # module assignment: contiguous vertical stripes
        stripe = (self.coords[:, 1] * p.n_modules // p.L).astype(int)
        self.module = np.clip(stripe, 0, p.n_modules - 1)
        self.block_bias = rng.normal(0.0, p.bias_spread, p.n_modules)[self.module]

        # local links (torus), masked so locality respects module boundaries:
        # left/right neighbors in a different module contribute 0 and the
        # average renormalizes -- modules are separate sublattices, coupled
        # only through module_mix / beta_global.
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

        # input wiring
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
        self.chan_map = rng.permutation(p.n_out)  # position -> internal id

        # per-module response rates (timescale separation motif); drawn LAST so
        # presets with lam_min=lam_max=1 keep byte-identical wiring to older runs
        lams = np.linspace(p.lam_min, p.lam_max, p.n_modules)
        self.lam = rng.permutation(lams)[self.module]

        # persistent state
        self._noise = np.random.default_rng(
            np.random.SeedSequence([0xA11, self.seed, self._salt]))
        self.x = 0.01 * self._noise.standard_normal(self.N)
        self.a = np.zeros(self.N)            # slow adaptation state
        self.ticks_used = 0
        self.n_resets = 0

    # ---------------- micro dynamics ----------------
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

    def _step(self, u: np.ndarray) -> None:
        p = self.p
        field = self.B @ np.clip(u, -1.0, 1.0)
        pre = p.J * ((1 - p.alpha) * self.x + p.alpha * self._mix(self.x))
        pre = pre + self.block_bias + field - p.g_adapt * self.a
        target = np.tanh(pre + p.sigma * self._noise.standard_normal(self.N))
        self.x = (1.0 - self.lam) * self.x + self.lam * target
        if p.eps_adapt > 0:
            self.a += p.eps_adapt * (self.x - self.a)

    def _read(self) -> np.ndarray:
        p = self.p
        n_live = p.n_out - p.n_dead
        raw = np.array([self.x[idx].mean() for idx in self.patches])
        live = self.gain * raw + self.offset \
            + p.meas_noise * self._noise.standard_normal(n_live)
        dead = self.dead_offset + p.meas_noise * self._noise.standard_normal(p.n_dead)
        return np.concatenate([live, dead])[self.chan_map]

    # ---------------- public surface ----------------
    def run(self, U: np.ndarray) -> np.ndarray:
        """Advance T ticks under open-loop input program U [T, n_in]; return Y [T, n_out].
        Raises RuntimeError when the tick budget would be exceeded."""
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
        """Closed-loop advance: per tick, read ports, ask the jailed policy for
        an action, step. Returns Y [T, n_out]. Budget checked like run()."""
        if self.ticks_used + T > self.p.max_ticks:
            raise RuntimeError(
                f"budget exceeded: {self.ticks_used} used + {T} requested "
                f"> {self.p.max_ticks}")
        Y = np.empty((T, self.p.n_out))
        y = self._read()                      # observation before first action
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
        """Reset to a new draw of initial conditions (costed: 200 ticks)."""
        cost = 200
        if self.ticks_used + cost > self.p.max_ticks:
            raise RuntimeError("budget exceeded on fresh_sample")
        self.ticks_used += cost
        self.n_resets += 1
        self.x = 0.01 * self._noise.standard_normal(self.N)
        self.a = np.zeros(self.N)

    @property
    def budget_left(self) -> int:
        return self.p.max_ticks - self.ticks_used

    # ---------------- evaluator-only ----------------
    def clone_fresh(self, noise_seed: int) -> "World":
        """Same wiring/params, fresh state, independent noise stream (truth ensembles)."""
        w = World(self.p, self.seed)
        w._noise = np.random.default_rng(
            np.random.SeedSequence([0xE7A1, self.seed, self._salt, noise_seed]))
        w.x = 0.01 * w._noise.standard_normal(w.N)
        w.a = np.zeros(w.N)
        w.ticks_used = 0
        return w

    def true_channel_range(self) -> np.ndarray:
        """Approx dynamic range (2*|gain|) per agent-visible channel; dead -> 0."""
        n_live = self.p.n_out - self.p.n_dead
        internal = np.concatenate([2.0 * np.abs(self.gain), np.zeros(self.p.n_dead)])
        return internal[self.chan_map]

    def true_is_dead(self) -> np.ndarray:
        """Boolean mask over agent-visible channel positions (evaluator-only)."""
        n_live = self.p.n_out - self.p.n_dead
        return self.chan_map >= n_live

    def true_macro(self) -> np.ndarray:
        """Per-module mean of micro state (ground-truth macro variables)."""
        mmean = np.zeros(self.p.n_modules)
        np.add.at(mmean, self.module, self.x)
        counts = np.bincount(self.module, minlength=self.p.n_modules)
        return mmean / np.maximum(counts, 1)


# ---------------- difficulty ladder ----------------
# Axes (DESIGN.md v0.5): port opacity (dead, flips, noise, gain spread),
# macro complexity k* (n_modules, module_mix, bias_spread),
# law cleanness (sigma, J margin), economy (max_ticks).
DIFFICULTY_PRESETS: dict[str, WorldParams] = {
    "D0": WorldParams(  # clean ports, single collective mode, generous budget
        L=24, J=1.35, n_modules=1, sigma=0.04,
        n_in=6, n_out=24, n_dead=0, meas_noise=0.02,
        gain_min=0.9, gain_max=1.1, p_flip=0.0, max_ticks=80_000),
    "D1": WorldParams(  # murky ports: dead channels, sign flips, more noise
        L=24, J=1.35, n_modules=1, sigma=0.05,
        n_in=6, n_out=32, n_dead=4, meas_noise=0.05,
        gain_min=0.6, gain_max=1.6, p_flip=0.35, max_ticks=80_000),
    "D2": WorldParams(  # richer law: 3 modules, heterogeneity, murky ports
        L=24, J=1.35, n_modules=3, module_mix=0.55, bias_spread=0.10, sigma=0.05,
        n_in=6, n_out=36, n_dead=4, meas_noise=0.05,
        gain_min=0.6, gain_max=1.6, p_flip=0.35, in_width=3.0, in_gain=0.9,
        max_ticks=100_000),
    "D3": WorldParams(  # hard: 6 modules + weak global tie, tighter budget
        L=30, J=1.45, n_modules=6, module_mix=0.6, beta_global=0.08,
        bias_spread=0.04, sigma=0.06,
        n_in=8, n_out=48, n_dead=8, meas_noise=0.07,
        gain_min=0.5, gain_max=1.8, p_flip=0.4, in_width=2.5, in_gain=1.0,
        max_ticks=60_000),
    "D4": WorldParams(  # frontier: 8 modules, slow/fast timescales, opaque ports
        L=32, J=1.40, n_modules=8, module_mix=0.55, beta_global=0.05,
        bias_spread=0.05, sigma=0.06, lam_min=0.04, lam_max=1.0,
        eps_adapt=0.005, g_adapt=0.55,
        n_in=10, n_out=60, n_dead=10, meas_noise=0.08,
        gain_min=0.4, gain_max=2.0, p_flip=0.4, in_width=2.5, in_gain=1.1,
        max_ticks=150_000),
}


def make_world(difficulty: str, seed: int) -> World:
    return World(DIFFICULTY_PRESETS[difficulty], seed)
