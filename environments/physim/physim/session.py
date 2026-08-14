"""physim.session — the agent-facing surface + contract scoring.

Chat-tier interface (M0): the agent sends JSON commands; we execute against the
persistent World and return compact JSON observations (context-bandwidth
discipline: server-side reduction, capped numbers).

Commands
  {"op":"run", "segments":[SEG,...], "observe":{...}?}   advance the world (open loop)
  {"op":"run_policy", "code":"...", "t":T, "observe":{...}?}  closed loop: code defines
        policy(t, y, mem) -> [n_in floats]; executed tick-synchronously in a jail
  {"op":"reset"}                                          fresh initial draw (costed)
  {"op":"status"}                                         budget / interface info
  {"op":"ready"}                                          end exploration -> contracts

SEG (open-loop program pieces; concatenated):
  {"t":T, "u":[n_in floats]}                              hold u for T ticks
  {"t":T, "u_start":[...], "u_end":[...]}                 linear ramp

observe (optional):
  {"channels":[ids] | "all", "series":true?, "stride":k?}
  default: per-channel mean/sd over the LAST 20 ticks of the run.
  series: downsampled per-tick values for <=6 channels, total <=360 numbers.

Contracts (issued after "ready" or when budget/turns run out): each is a fully
specified protocol FROM A FRESH STATE plus one statistic of one channel; the
agent answers mean + [low, high] interval. Scored against a fresh truth
ensemble; accuracy = exp(-|err|/(3*tau)), tau = ensemble sd of the statistic.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import numpy as np

from physim.engine import World

TAIL = 20          # ticks in the default observation window
MAX_SERIES_NUMBERS = 360
MAX_SEG_TICKS = 5_000
ENSEMBLE = 12      # truth ensemble size per contract
S4_SETTLE_MAX = 700  # longest slow-settle segment S4 may use


# ---------------------------------------------------------------- protocols
def render_protocol(segments: list[dict], n_in: int) -> np.ndarray:
    """Segment list -> U [T, n_in]. Raises ValueError on malformed input."""
    if not isinstance(segments, list) or not segments:
        raise ValueError("segments must be a non-empty list")
    parts = []
    for i, seg in enumerate(segments):
        if not isinstance(seg, dict):
            raise ValueError(f"segment {i} must be an object")
        T = seg.get("t")
        if not isinstance(T, int) or not (1 <= T <= MAX_SEG_TICKS):
            raise ValueError(f"segment {i}: t must be an int in [1, {MAX_SEG_TICKS}]")
        def vec(key):
            v = seg.get(key)
            if (not isinstance(v, list) or len(v) != n_in
                    or not all(isinstance(x, (int, float)) for x in v)):
                raise ValueError(f"segment {i}: {key} must be a list of {n_in} numbers")
            return np.clip(np.asarray(v, dtype=float), -1.0, 1.0)
        if "u" in seg:
            parts.append(np.tile(vec("u"), (T, 1)))
        elif "u_start" in seg and "u_end" in seg:
            a, b = vec("u_start"), vec("u_end")
            w = np.linspace(0.0, 1.0, T)[:, None]
            parts.append(a[None, :] * (1 - w) + b[None, :] * w)
        else:
            raise ValueError(f"segment {i}: need 'u' or 'u_start'+'u_end'")
    return np.concatenate(parts, axis=0)


def protocol_ticks(segments: list[dict]) -> int:
    return sum(int(s.get("t", 0)) for s in segments if isinstance(s, dict))


# ---------------------------------------------------------------- contracts
@dataclass
class Contract:
    id: int
    stratum: str                  # S1 autonomous / S2 interpolation / S3 extrapolation
    segments: list[dict]          # protocol from fresh state
    channel: int                  # live channel index (agent-visible ordering)
    stat: str = "mean"            # statistic over last TAIL ticks

    def spec(self) -> dict:
        window = (f"last_{STAT_WINDOW_LONG}_ticks" if self.stat == "sd"
                  else f"last_{TAIL}_ticks")
        return {
            "id": self.id,
            "protocol": {"from": "fresh_state", "segments": self.segments},
            "predict": {"channel": self.channel, "stat": self.stat,
                        "window": window},
            "answer_format": {"mean": "float", "low": "float", "high": "float"},
        }


def sample_contracts(world: World, rng: np.random.Generator,
                     n_per_stratum: int = 4) -> list[Contract]:
    """Ontology-neutral protocol grammar, stratified (DESIGN.md v0.4).
    Gray-Scott worlds get object-scale protocols (longer, localized, asymmetric)
    via the same spec shape."""
    if getattr(world.p, "reaction", "tanh") in ("grayscott", "grayscott2"):
        return _sample_contracts_gs(world, rng, n_per_stratum)
    if getattr(world.p, "reaction", "tanh") == "excitable":
        return _sample_contracts_excitable(world, rng, n_per_stratum)
    if getattr(world.p, "reaction", "tanh") == "ecology":
        return _sample_contracts_ecology(world, rng, n_per_stratum)
    n_in = world.p.n_in
    dead = world.true_is_dead()
    live = [c for c in range(world.p.n_out) if not bool(dead[c])]
    contracts: list[Contract] = []
    cid = 0

    def pick_channel() -> int:
        return int(rng.choice(live))

    def hold(u_vec, T):
        return {"t": int(T), "u": [round(float(x), 3) for x in u_vec]}

    for _ in range(n_per_stratum):          # S1: weak push then autonomous relaxation
        sgn = 1.0 if rng.random() < 0.5 else -1.0
        u = np.full(n_in, sgn * rng.uniform(0.25, 0.45))
        contracts.append(Contract(cid, "S1",
            [hold(u, int(rng.integers(30, 60))),
             hold(np.zeros(n_in), int(rng.integers(60, 120)))], pick_channel()))
        cid += 1
    for _ in range(n_per_stratum):          # S2: moderate uniform/local/subset drives
        u = np.zeros(n_in)
        roll = rng.random()
        if roll < 0.4:
            u[:] = rng.uniform(-0.5, 0.5)
        elif roll < 0.7:
            u[rng.integers(0, n_in)] = rng.uniform(-0.6, 0.6)
        else:
            mask = rng.random(n_in) < 0.5
            u[mask] = rng.uniform(-0.6, 0.6)
        contracts.append(Contract(cid, "S2",
            [hold(u, int(rng.integers(60, 120)))], pick_channel()))
        cid += 1
    for _ in range(n_per_stratum):          # S3: strong drive + release (memory)
        sgn = 1.0 if rng.random() < 0.5 else -1.0
        u = np.full(n_in, sgn * rng.uniform(0.8, 1.0))
        if rng.random() < 0.5:              # subset push: only some ports driven
            mask = rng.random(n_in) < 0.6
            if not mask.any():
                mask[rng.integers(0, n_in)] = True
            u = np.where(mask, u, 0.0)
        segs = [hold(u, int(rng.integers(60, 100))),
                hold(np.zeros(n_in), int(rng.integers(60, 120)))]
        if rng.random() < 0.5:              # opposite-branch push-past
            u2 = -u * rng.uniform(0.15, 0.45)
            segs.insert(1, hold(u2, int(rng.integers(30, 60))))
        contracts.append(Contract(cid, "S3", segs, pick_channel()))
        cid += 1
    for _ in range(n_per_stratum):          # S4: long-horizon composition
        # multi-stage sequence: strong set -> partial counter-push on a port
        # subset -> long settle. Tests slow modes + per-port memory jointly.
        sgn = 1.0 if rng.random() < 0.5 else -1.0
        u1 = np.full(n_in, sgn * rng.uniform(0.7, 1.0))
        mask = rng.random(n_in) < 0.5
        if not mask.any():
            mask[rng.integers(0, n_in)] = True
        u2 = np.where(mask, -sgn * rng.uniform(0.5, 0.9), 0.0)
        segs = [hold(u1, int(rng.integers(80, 140))),
                hold(u2, int(rng.integers(60, 120))),
                hold(np.zeros(n_in), int(rng.integers(300, S4_SETTLE_MAX)))]
        contracts.append(Contract(cid, "S4", segs, pick_channel()))
        cid += 1
    return contracts


def _sample_contracts_gs(world: World, rng: np.random.Generator,
                         n_per_stratum: int = 4) -> list[Contract]:
    """Chemistry-track strata: S1 autonomous drift; S2 sustained local feed
    perturbation (single port, both signs — stall/grow/shrink objects);
    S3 strong perturbation then long release (does the change persist?);
    S4 two-stage push-pull with long settle (object rearrangement)."""
    n_in = world.p.n_in
    dead = world.true_is_dead()
    live = [c for c in range(world.p.n_out) if not bool(dead[c])]
    # object-adjacent sensors = internal ids 0..n_live//2-1 -> agent-visible positions
    n_live_s = world.p.n_out - world.p.n_dead
    hot_internal = set(range(max(1, n_live_s // 2)))
    hot_channels = [pos for pos in live
                    if int(world.chan_map[pos]) in hot_internal]
    contracts: list[Contract] = []
    cid = 0

    # traffic-visited channels (for sd contracts): resting fluctuation above noise
    traffic_channels: list[int] = []
    if getattr(world.p, "gs_drift", 0.0) > 0:
        probe = world.clone_fresh(noise_seed=655)
        Yp = probe.run(np.zeros((600, world.p.n_in)))
        sds = Yp[-STAT_WINDOW_LONG:].std(0)
        noise_floor = float(np.median(sds[live]))
        traffic_channels = [c for c in live if sds[c] > 3 * noise_floor]

    def pick_channel(stat: str = "mean") -> int:
        if stat == "sd" and traffic_channels:
            return int(rng.choice(traffic_channels))
        pool = hot_channels if (hot_channels and rng.random() < 0.75) else live
        return int(rng.choice(pool))

    def hold(u_vec, T):
        return {"t": int(T), "u": [round(float(x), 3) for x in u_vec]}

    for _ in range(n_per_stratum):          # S1: autonomous evolution
        contracts.append(Contract(cid, "S1",
            [hold(np.zeros(n_in), int(rng.integers(150, 300)))], pick_channel()))
        cid += 1
    # ports 0..n_in//2-1 are object-adjacent by construction (evaluator knowledge;
    # opaque to the agent) — protocols draw mostly from those so they genuinely
    # perturb the chemistry (kill/grow/move objects), with decoy ports mixed in.
    hot = list(range(max(1, n_in // 2)))
    drifting_c = getattr(world.p, "gs_drift", 0.0) > 0
    def stat_pick(i):
        # on drifting worlds, alternate mean/sd so half the contracts probe
        # traffic structure (sd) — tail means converge to traffic averages
        return "sd" if (drifting_c and i % 2 == 1) else "mean"
    for i in range(n_per_stratum):          # S2: sustained single-port feed shift
        u = np.zeros(n_in)
        port = int(rng.choice(hot)) if rng.random() < 0.8 else int(rng.integers(0, n_in))
        u[port] = rng.choice([-1.0, 1.0]) * rng.uniform(0.7, 1.0)
        st_ = stat_pick(i)
        contracts.append(Contract(cid, "S2",
            [hold(u, int(rng.integers(250, 400)))], pick_channel(st_),
            stat=st_))
        cid += 1
    for i in range(n_per_stratum):          # S3: kill/grow hard, release long
        u = np.zeros(n_in)
        port = int(rng.choice(hot))
        u[port] = rng.choice([-1.0, 1.0])
        st_ = stat_pick(i)
        contracts.append(Contract(cid, "S3",
            [hold(u, int(rng.integers(250, 400))),
             hold(np.zeros(n_in), int(rng.integers(300, 500)))], pick_channel(st_),
            stat=st_))
        cid += 1
    for _ in range(n_per_stratum):          # S4: two-port push-pull, long settle
        u1 = np.zeros(n_in); u2 = np.zeros(n_in)
        p1 = int(rng.choice(hot))
        p2 = int(rng.choice(hot)) if len(hot) > 1 else p1
        u1[p1] = rng.uniform(0.8, 1.0)
        u2[p2] = -rng.uniform(0.8, 1.0)
        contracts.append(Contract(cid, "S4",
            [hold(u1, int(rng.integers(200, 300))),
             hold(u2, int(rng.integers(150, 250))),
             hold(np.zeros(n_in), int(rng.integers(400, 650)))], pick_channel()))
        cid += 1
    if getattr(world.p, "gs_drift", 0.0) > 0:   # S5: transit variability (moving worlds)
        for _ in range(n_per_stratum):
            segs = [hold(np.zeros(n_in), int(rng.integers(500, 900)))]
            if rng.random() < 0.5:               # optionally perturb first (kill/grow changes traffic)
                u = np.zeros(n_in)
                u[int(rng.choice(hot))] = rng.choice([-1.0, 1.0])
                segs = [hold(u, int(rng.integers(200, 300)))] + segs
            contracts.append(Contract(cid, "S5", segs, pick_channel("sd"), stat="sd"))
            cid += 1
    return contracts


STAT_WINDOW_LONG = 200   # window for dynamic statistics (sd) on moving worlds


def compute_stat(Y: np.ndarray, contract: "Contract") -> float:
    """Ontology-neutral statistic of a channel's trajectory tail."""
    c = contract.channel
    if contract.stat == "sd":
        w = Y[-min(STAT_WINDOW_LONG, len(Y)):, c]
        return float(w.std())
    if contract.stat == "rate":
        w = Y[-min(STAT_WINDOW_LONG, len(Y)):, c]
        thr = float(np.median(w) + w.std())
        ups = int(((w[1:] > thr) & (w[:-1] <= thr)).sum())
        return float(ups)
    return float(Y[-TAIL:, c].mean())


def _sample_contracts_excitable(world: World, rng: np.random.Generator,
                                n_per_stratum: int = 4) -> list[Contract]:
    """Wave-engaging grammar: S1 autonomous rhythm (mean+rate); S2 second
    pacemaker via strong sustained port drive (entrainment); S3 pulse-train
    drives at varied periods (conduction ratio / refractory block); S4
    two-port interleaved pulse trains (collision physics)."""
    n_in = world.p.n_in
    dead = world.true_is_dead()
    live = [c for c in range(world.p.n_out) if not bool(dead[c])]
    contracts: list[Contract] = []
    cid = 0

    def pick_channel() -> int:
        return int(rng.choice(live))

    def hold(u_vec, T):
        return {"t": int(T), "u": [round(float(x), 3) for x in u_vec]}

    def pulse_train(port, period_on, period_off, reps, amp=1.0):
        segs = []
        for _ in range(reps):
            u = np.zeros(n_in); u[port] = amp
            segs.append(hold(u, period_on))
            segs.append(hold(np.zeros(n_in), period_off))
        return segs

    for i in range(n_per_stratum):          # S1: autonomous rhythm
        contracts.append(Contract(cid, "S1",
            [hold(np.zeros(n_in), int(rng.integers(250, 400)))], pick_channel(),
            stat="rate" if i % 2 else "mean"))
        cid += 1
    for i in range(n_per_stratum):          # S2: create a competing pacemaker
        port = int(rng.integers(0, n_in))
        u = np.zeros(n_in); u[port] = rng.uniform(0.8, 1.0)
        contracts.append(Contract(cid, "S2",
            [hold(u, int(rng.integers(300, 450)))], pick_channel(),
            stat="rate" if i % 2 else "mean"))
        cid += 1
    for i in range(n_per_stratum):          # S3: pulse train at varied period
        port = int(rng.integers(0, n_in))
        p_on = 8
        p_off = int(rng.integers(20, 120))
        reps = max(3, int(360 // (p_on + p_off)))
        segs = pulse_train(port, p_on, p_off, reps) +             [hold(np.zeros(n_in), int(rng.integers(100, 200)))]
        contracts.append(Contract(cid, "S3", segs, pick_channel(),
                                  stat="rate" if i % 2 else "mean"))
        cid += 1
    for i in range(n_per_stratum):          # S4: two-port interleaved trains
        p1 = int(rng.integers(0, n_in)); p2 = int(rng.integers(0, n_in))
        per1 = int(rng.integers(60, 110)); per2 = int(rng.integers(60, 110))
        T = 420
        segs = []
        t = 0
        while t < T:                        # interleave by 10-tick blocks
            u = np.zeros(n_in)
            if (t % per1) < 8: u[p1] = 1.0
            if (t % per2) < 8: u[p2] = max(u[p2], 1.0) if p2 == p1 else 1.0
            segs.append(hold(u, 10))
            t += 10
        contracts.append(Contract(cid, "S4", segs, pick_channel(),
                                  stat="rate" if i % 2 else "mean"))
        cid += 1
    return contracts


def _sample_contracts_ecology(world: World, rng: np.random.Generator,
                              n_per_stratum: int = 4) -> list[Contract]:
    """Population-scale grammar: S1 equilibrium ecosystem; S2 sustained
    fertilize/poison (carrying-capacity shift); S3 poison pulse + recovery
    (resilience); S4 extinction-boundary (strong sustained poison — the
    selection law: the fast variant dies first)."""
    n_in = world.p.n_in
    dead = world.true_is_dead()
    live = [c for c in range(world.p.n_out) if not bool(dead[c])]
    contracts: list[Contract] = []
    cid = 0

    def pick_channel() -> int:
        return int(rng.choice(live))

    def hold(u_vec, T):
        return {"t": int(T), "u": [round(float(x), 3) for x in u_vec]}

    def stat_pick(i):
        return ("mean", "sd")[i % 2]

    for i in range(n_per_stratum):          # S1: equilibrium
        contracts.append(Contract(cid, "S1",
            [hold(np.zeros(n_in), int(rng.integers(500, 900)))], pick_channel(),
            stat=stat_pick(i)))
        cid += 1
    for i in range(n_per_stratum):          # S2: sustained global tilt
        amp = float(rng.choice([-0.6, -0.3, 0.4, 0.8]))
        u = np.full(n_in, amp)
        contracts.append(Contract(cid, "S2",
            [hold(u, int(rng.integers(900, 1400)))], pick_channel(),
            stat=stat_pick(i)))
        cid += 1
    for i in range(n_per_stratum):          # S3: poison pulse + recovery
        u = np.full(n_in, -float(rng.uniform(0.7, 1.0)))
        contracts.append(Contract(cid, "S3",
            [hold(u, int(rng.integers(500, 800))),
             hold(np.zeros(n_in), int(rng.integers(700, 1100)))], pick_channel(),
            stat=stat_pick(i)))
        cid += 1
    for i in range(n_per_stratum):          # S4: extinction boundary
        u = np.full(n_in, -1.0)
        # partial-port poison: some ports only (spatially partial suppression)
        if rng.random() < 0.5:
            mask = rng.random(n_in) < 0.6
            u = np.where(mask, u, 0.0)
        contracts.append(Contract(cid, "S4",
            [hold(u, int(rng.integers(1200, 1800)))], pick_channel(),
            stat=stat_pick(i)))
        cid += 1
    return contracts


def truth_statistic(world: World, contract: Contract, ensemble: int = ENSEMBLE
                    ) -> tuple[float, float, list[float]]:
    """Run the contract protocol on `ensemble` fresh clones; return
    (mu, tau, samples) of the statistic."""
    U = render_protocol(contract.segments, world.p.n_in)
    if getattr(world.p, "reaction", "tanh") in ("grayscott", "grayscott2"):
        ensemble = min(ensemble, 8)
    if getattr(world.p, "reaction", "tanh") == "ecology":
        ensemble = min(ensemble, 6)
    vals = []
    for e in range(ensemble):
        clone = world.clone_fresh(noise_seed=1000 + 97 * contract.id + e)
        Y = clone.run(U)
        vals.append(compute_stat(Y, contract))
    v = np.asarray(vals)
    tau_floor = world.p.meas_noise / np.sqrt(TAIL)   # sd of a TAIL-tick mean read
    return float(v.mean()), float(max(v.std(), tau_floor, 1e-6)), vals


def answer_scale(tau: float, channel_range: float, stat: str = "mean",
                 reaction: str = "tanh") -> float:
    """Error tolerance: ensemble spread when the world is genuinely stochastic,
    floored at a fraction of the channel's dynamic range when quasi-deterministic
    (predicting within a few % of range is 'understanding'; branch confusion
    ~ full range still scores ~0). sd-statistics live on a smaller scale."""
    if stat == "rate":
        return float(max(3.0 * tau, 1.0))
    frac = 0.05 if stat == "sd" else 0.1
    if reaction in ("grayscott", "grayscott2", "ecology"):
        # GS ensembles are quasi-deterministic (shared settled start): the
        # range floor dominates and must be tight or replication saturates.
        frac = 0.015 if stat == "sd" else 0.03
    return float(max(3.0 * tau, frac * channel_range, 1e-3))


def score_answer(mu: float, scale: float, ans: dict) -> dict:
    """Accuracy in (0,1]: exp(-|err|/scale). Coverage: does mu land in [low,high].
    Calibration: Winkler interval score (alpha=0.2) mapped through exp(-W/6*scale):
    narrow-and-right ~1, wide-honest moderate, narrow-and-wrong ~0."""
    try:
        mean = float(ans["mean"]); low = float(ans["low"]); high = float(ans["high"])
    except (KeyError, TypeError, ValueError):
        return {"accuracy": 0.0, "covered": 0.0, "z": None, "answered": 0.0,
                "calibration": 0.0}
    z = abs(mean - mu) / scale
    lo, hi = (low, high) if low <= high else (high, low)
    winkler = (hi - lo) + 10.0 * max(0.0, lo - mu) + 10.0 * max(0.0, mu - hi)
    calib = float(np.exp(-winkler / (10.0 * scale)))
    return {"accuracy": float(np.exp(-z)), "covered": float(lo <= mu <= hi),
            "z": float(z), "answered": 1.0, "calibration": calib}


def replication_accuracy(samples: list[float], scale: float) -> float:
    """Leave-one-out self-score of the truth ensemble: the expected score of an
    agent that runs the contract protocol once on the real world and reports
    what it saw. A strong empirical reference (true ceiling for predicting the
    ensemble mean is 1.0)."""
    v = np.asarray(samples)
    accs = []
    for i in range(len(v)):
        rest = np.delete(v, i)
        z = abs(v[i] - rest.mean()) / scale
        accs.append(np.exp(-z))
    return float(np.mean(accs))


# ---------------------------------------------------------------- prep contracts
@dataclass
class PrepContract:
    id: int
    channel: int
    lo: float
    hi: float
    t_prep: int          # max ticks the policy may run
    hold: int            # release window: predicate on tail of `hold` FREE ticks
    clones: int = 5
    stat: str = "mean"   # "mean" (last TAIL ticks) or "sd" (last STAT_WINDOW_LONG)

    def spec(self) -> dict:
        if self.stat == "sd":
            measured = (f"standard deviation over the final "
                        f"{min(STAT_WINDOW_LONG, self.hold)} ticks of a "
                        f"{self.hold}-tick free run (all inputs 0) after your "
                        "policy finishes")
        else:
            measured = (f"mean over final {TAIL} ticks of a {self.hold}-tick "
                        "free run (all inputs 0) after your policy finishes")
        return {
            "id": self.id, "type": "preparation",
            "goal": {"channel": self.channel, "band": [round(self.lo, 3), round(self.hi, 3)],
                     "measured": measured},
            "policy_budget_ticks": self.t_prep,
            "evaluation": f"policy runs from {self.clones} fresh draws; score = fraction "
                          "of draws where the released tail lands in the band",
            "submit": {"op": "answer_prep", "id": self.id, "code": "policy(t, y, mem)"},
        }


def sample_prep_contracts(world: World, rng: np.random.Generator,
                          n: int = 4) -> list["PrepContract"]:
    """Reachable-by-construction: drive a probe clone to each branch, read the
    tail values of live channels, and ask for bands around those values."""
    if getattr(world.p, "reaction", "tanh") in ("grayscott", "grayscott2"):
        return _sample_prep_gs(world, rng, n)
    if getattr(world.p, "reaction", "tanh") == "excitable":
        return []   # v1: wave states are transient; preps deferred
    if getattr(world.p, "reaction", "tanh") == "ecology":
        return []   # v1: population targets need long holds; preps deferred
    p = world.p
    dead = world.true_is_dead()
    live = [c for c in range(p.n_out) if not dead[c]]
    ranges = world.true_channel_range()

    # do-nothing baseline ENSEMBLE (fresh draws can relax to different branches)
    rest_draws = []
    for e in range(6):
        cl = world.clone_fresh(noise_seed=771 + e)
        Yr = cl.run(np.zeros((420, p.n_in)))
        rest_draws.append(Yr[-TAIL:].mean(0))
    rest_draws = np.stack(rest_draws)
    rest = rest_draws.mean(0)

    targets: list[tuple[int, float, float]] = []   # (channel, value, |shift from rest|)
    for sgn in (+1.0, -1.0):
        clone = world.clone_fresh(noise_seed=777 + int(sgn > 0))
        clone.run(np.full((120, p.n_in), sgn * 0.9))
        Yf = clone.run(np.zeros((260, p.n_in)))
        tail = Yf[-TAIL:].mean(0)
        for c in live:
            targets.append((c, float(tail[c]), abs(float(tail[c]) - float(rest[c]))))
    # non-trivial first: bands whose resting value is far away
    rng.shuffle(targets)
    targets.sort(key=lambda t: -t[2])
    contracts, used = [], set()
    for c, v, _shift in targets:
        if len(contracts) >= n:
            break
        if c in used:
            continue
        half = max(0.15 * float(ranges[c]), 0.12)
        lo, hi = v - half, v + half
        # do-nothing must fail on MOST draws (allow rare lucky landings)
        p_nothing = float(np.mean((rest_draws[:, c] >= lo) & (rest_draws[:, c] <= hi)))
        if p_nothing > 0.25:
            continue
        used.add(c)
        contracts.append(PrepContract(
            id=100 + len(contracts), channel=c, lo=lo, hi=hi,
            t_prep=int(rng.integers(250, 450)), hold=int(rng.integers(180, 300))))
    return _verified_nontrivial(world, contracts)


def _sample_prep_gs(world: World, rng: np.random.Generator,
                    n: int = 4) -> list["PrepContract"]:
    """GS preparation targets: post-release states reachable by strong drives on
    object-adjacent ports (kill/grow outcomes). A candidate band is kept only if
    the RESTING trajectory does NOT satisfy it (preparation must require action)
    and the probe outcome is reproducible across two noise draws."""
    p = world.p
    dead = world.true_is_dead()
    live = [c for c in range(p.n_out) if not dead[c]]
    ranges = world.true_channel_range()

    # resting tails (do-nothing baseline) ENSEMBLE
    rest_draws = []
    for e in range(3):
        cl = world.clone_fresh(noise_seed=770 + e)
        Yr = cl.run(np.zeros((520, p.n_in)))
        rest_draws.append(Yr[-TAIL:].mean(0))
    rest_draws = np.stack(rest_draws)
    rest = rest_draws.mean(0)

    hot = list(range(max(1, p.n_in // 2)))     # object-adjacent by construction

    # apparatus-forced preparation (apparatus worlds): target a MOVABLE sensor's
    # channel with a band around what it reads ON an object — reachable only by
    # driving the stage (parked/resting readings stay far away).
    app_contracts: list[PrepContract] = []
    move_ports = [(port, tgt) for port, (prop, tgt)
                  in (world.app_port_map or {}).items() if prop == "move"]
    if move_ports and getattr(p, "gs_drift", 0.0) == 0:
        port, tgt = move_ports[0]
        chan = int(np.where(world.chan_map == tgt)[0][0])
        clone = world.clone_fresh(noise_seed=4321)
        objs = clone.true_objects()
        if objs:
            clone.app_pos[tgt] = np.array(objs[0])
            Yon = clone.run(np.zeros((30, p.n_in)))
            v_on = float(Yon[-TAIL:, chan].mean())
            rest_v = float(rest[chan])
            if abs(v_on - rest_v) > 0.5:
                half = max(0.15 * float(ranges[chan]), 0.15)
                app_contracts.append(PrepContract(
                    id=190, channel=chan, lo=v_on - half, hi=v_on + half,
                    t_prep=700, hold=30, clones=3))

    drifting = getattr(p, "gs_drift", 0.0) > 0
    if drifting:
        # On drifting worlds single-channel outcomes fade (objects wander);
        # v1 ships NO preparation contracts here — C2's challenge is
        # prediction-under-motion (S5). Tracking preps are C3 material.
        return []
    candidates: list[tuple[int, float, float]] = []   # (channel, value, |shift|)
    probe_i = 0
    for port in hot:
        for sgn in (-1.0, 1.0):
            vals = []
            for e in range(2):             # reproducibility across draws
                clone = world.clone_fresh(noise_seed=888 + 13 * probe_i + e)
                u = np.zeros(p.n_in)
                u[port] = sgn
                clone.run(np.tile(u, (300, 1)))
                Yf = clone.run(np.zeros((300, p.n_in)))
                vals.append(Yf[-TAIL:].mean(0))
            probe_i += 1
            v_mean = np.mean(vals, axis=0)
            v_spread = np.abs(vals[0] - vals[1])
            for c in live:
                shift = abs(float(v_mean[c]) - float(rest[c]))
                if shift > 0.35 and v_spread[c] < 0.15:
                    candidates.append((c, float(v_mean[c]), shift))

    # prefer the largest shifts (real kill/grow outcomes), dedupe channels
    candidates.sort(key=lambda t: -t[2])
    contracts, used = [], set()
    for c, v, _shift in candidates:
        if len(contracts) >= n:
            break
        if c in used:
            continue
        half = max(0.12 * float(ranges[c]), 0.10)
        lo, hi = v - half, v + half
        p_nothing = float(np.mean((rest_draws[:, c] >= lo) & (rest_draws[:, c] <= hi)))
        if p_nothing > 0.25:
            continue                        # do-nothing must mostly fail
        used.add(c)
        contracts.append(PrepContract(
            id=100 + len(contracts), channel=c, lo=lo, hi=hi,
            t_prep=int(rng.integers(350, 550)),
            hold=int(rng.integers(250, 400)),
            clones=4, stat="mean"))
    return _verified_nontrivial(world, contracts + app_contracts)


def _verified_nontrivial(world: World, contracts: list["PrepContract"]
                         ) -> list["PrepContract"]:
    """Final gate: run the ACTUAL scorer with a do-nothing policy; drop any
    contract where doing nothing succeeds on >20% of clones. This uses the
    same code path as scoring, so phase/oscillation effects are captured."""
    null_code = f"def policy(t, y, mem):\n    return [0.0]*{world.p.n_in}"
    kept = []
    for c in contracts:
        r = score_prep(world, c, null_code)
        if r["success_rate"] <= 0.2:
            c.id = 100 + len(kept)
            kept.append(c)
    return kept


def score_prep(world: World, contract: PrepContract, code: str) -> dict:
    """Run the submitted policy on fresh clones; measure the released tail."""
    from physim.jail import Jail, JailError
    hits, errors, finals = 0, [], []
    for e in range(contract.clones):
        clone = world.clone_fresh(noise_seed=4242 + 31 * contract.id + e)
        try:
            with Jail(code, mode="policy") as jail:
                clone.run_policy(jail, contract.t_prep)
        except (JailError, RuntimeError, ValueError) as ex:
            errors.append(f"clone {e}: {str(ex)[:120]}")
            finals.append(None)
            continue
        Yf = clone.run(np.zeros((contract.hold, world.p.n_in)))
        if contract.stat == "sd":
            w_ = Yf[-min(STAT_WINDOW_LONG, len(Yf)):, contract.channel]
            val = float(w_.std())
        else:
            val = float(Yf[-TAIL:, contract.channel].mean())
        finals.append(round(val, 4))
        if contract.lo <= val <= contract.hi:
            hits += 1
    return {"success_rate": hits / contract.clones, "finals": finals,
            "errors": errors[:3]}


# ---------------------------------------------------------------- theory (M3)
def score_theory(world: World, contracts: list[Contract], code: str,
                 warmup: int = 40) -> dict:
    """Score an executable observable-process simulator G (init/step) by
    replaying each prediction contract's protocol through it and comparing the
    tail statistic against the truth ensemble (same scale as answers).
    G sees a short real warmup history (autonomous run from fresh state), then
    must simulate the protocol on its own."""
    from physim.jail import Jail, JailError
    ranges = world.true_channel_range()
    accs, detail = [], []
    for c in contracts:
        U = render_protocol(c.segments, world.p.n_in)
        mu, tau, _ = truth_statistic(world, c)
        scale = answer_scale(tau, float(ranges[c.channel]), c.stat,
                             getattr(world.p, "reaction", "tanh"))
        try:
            with Jail(code, mode="simulator") as jail:
                hist_clone = world.clone_fresh(noise_seed=9000 + c.id)
                Yh = hist_clone.run(np.zeros((warmup, world.p.n_in)))
                jail.sim_init([[float(v) for v in row] for row in Yh])
                preds = []
                for t_ in range(U.shape[0]):
                    y = jail.sim_step([float(v) for v in U[t_]])
                    if len(y) != world.p.n_out:
                        raise JailError(f"step returned {len(y)} values; need {world.p.n_out}")
                    preds.append(y)
            pred_stat = compute_stat(np.asarray(preds), c)
            z = abs(pred_stat - mu) / scale
            acc = float(np.exp(-z))
            detail.append({"id": c.id, "stratum": c.stratum, "mu": round(mu, 4),
                           "pred": round(pred_stat, 4), "accuracy": round(acc, 4)})
        except JailError as e:
            acc = 0.0
            detail.append({"id": c.id, "stratum": c.stratum, "mu": round(mu, 4),
                           "error": str(e)[:160], "accuracy": 0.0})
        accs.append(acc)
    per_stratum: dict[str, list[float]] = {}
    for d, a in zip(detail, accs):
        per_stratum.setdefault(d["stratum"], []).append(a)
    return {"theory_accuracy": float(np.mean(accs)) if accs else 0.0,
            "per_stratum": {k: float(np.mean(v)) for k, v in per_stratum.items()},
            "detail": detail, "code_chars": len(code)}


# ---------------------------------------------------------------- session
class PhysimSession:
    """Holds the persistent world + phase machine (explore -> answer -> done)."""

    def __init__(self, world: World, contract_seed: int, n_per_stratum: int = 4,
                 n_prep: int = 0):
        self.world = world
        self.phase = "explore"
        self._contract_seed = contract_seed
        self.rng = np.random.default_rng(np.random.SeedSequence([0xC047, contract_seed]))
        self.n_per_stratum = n_per_stratum
        self.n_prep = n_prep
        self.contracts: list[Contract] = []
        self.prep_contracts: list[PrepContract] = []
        self.prep_answers: dict[int, str] = {}
        self.theory_code: str = ""
        self.turns = 0

    # ---- interface description shown in the system prompt ----
    def interface_card(self) -> dict:
        p = self.world.p
        return {
            "input_ports": p.n_in, "output_ports": p.n_out,
            "input_range": [-1.0, 1.0],
            "tick_budget": p.max_ticks, "reset_cost": 200,
            "observation_window": TAIL,
        }

    def handle(self, text: str) -> dict:
        """One agent message -> one JSON-serializable response."""
        self.turns += 1
        try:
            cmd = _extract_json(text)
        except ValueError as e:
            return {"error": f"could not parse a JSON command: {e}"}
        op = cmd.get("op")
        if self.phase == "answer":
            self._ensure_contracts()
        if self.phase == "answer" and op not in ("answer", "answer_prep", "submit_theory"):
            return {"error": "exploration is over; reply with the answers object",
                    "contracts": [c.spec() for c in self.contracts],
                    "preparation_contracts": [c.spec() for c in self.prep_contracts]}
        if op == "submit_theory":
            code = cmd.get("code")
            if not isinstance(code, str) or not code.strip():
                return {"error": "code must define init(y_history) and step(state, a)"}
            self.theory_code = code
            return {"ok": True, "note": ("theory recorded; it will be scored after the "
                                          "rollout by simulating every prediction-contract "
                                          "protocol and comparing tail statistics")}
        if op == "answer_prep":
            cid = cmd.get("id")
            code = cmd.get("code")
            ids = {c.id for c in self.prep_contracts}
            if cid not in ids:
                return {"error": f"unknown preparation contract id {cid!r}; ids: {sorted(ids)}"}
            if not isinstance(code, str) or not code.strip():
                return {"error": "code must be a non-empty string defining policy(t, y, mem)"}
            self.prep_answers[cid] = code
            return {"ok": True, "recorded_policy_for": cid,
                    "pending": sorted(ids - set(self.prep_answers))}
        if op == "run":
            return self._op_run(cmd)
        if op == "run_policy":
            return self._op_run_policy(cmd)
        if op == "reset":
            try:
                self.world.fresh_sample()
            except RuntimeError as e:
                return {"error": str(e), "budget_left": self.world.budget_left}
            return {"ok": True, "note": "fresh initial state drawn",
                    "budget_left": self.world.budget_left}
        if op == "status":
            return {"phase": self.phase, "budget_left": self.world.budget_left,
                    "interface": self.interface_card()}
        if op == "ready":
            used = self.world.ticks_used / max(self.world.p.max_ticks, 1)
            if used < 0.05 and not cmd.get("confirm"):
                return {"error": (
                    f"you have used only {used:.1%} of the tick budget; ending "
                    "exploration now is almost certainly premature. Send "
                    '{"op":"ready","confirm":true} to end anyway.'),
                    "budget_left": self.world.budget_left}
            return self.issue_contracts()
        return {"error": f"unknown op {op!r}; ops: run, reset, status, ready"}

    def _op_run(self, cmd: dict) -> dict:
        try:
            U = render_protocol(cmd.get("segments"), self.world.p.n_in)
        except ValueError as e:
            return {"error": str(e)}
        try:
            Y = self.world.run(U)
        except RuntimeError as e:
            return {"error": str(e), "budget_left": self.world.budget_left}
        return self._observe(Y, cmd.get("observe") or {})

    def _op_run_policy(self, cmd: dict) -> dict:
        from physim.jail import Jail, JailError
        code = cmd.get("code")
        T = cmd.get("t")
        if not isinstance(T, int) or not (1 <= T <= MAX_SEG_TICKS):
            return {"error": f"t must be an int in [1, {MAX_SEG_TICKS}]"}
        try:
            with Jail(code, mode="policy") as jail:
                Y = self.world.run_policy(jail, T)
        except JailError as e:
            return {"error": f"policy failed: {e}", "budget_left": self.world.budget_left}
        except RuntimeError as e:
            return {"error": str(e), "budget_left": self.world.budget_left}
        except ValueError as e:
            return {"error": str(e), "budget_left": self.world.budget_left}
        return self._observe(Y, cmd.get("observe") or {})

    def _observe(self, Y: np.ndarray, spec: dict) -> dict:
        n_out = Y.shape[1]
        chans = spec.get("channels", "all")
        if chans == "all":
            idx = list(range(n_out))
        elif (isinstance(chans, list) and chans
              and all(isinstance(c, int) and 0 <= c < n_out for c in chans)):
            idx = sorted(set(chans))
        else:
            return {"error": "observe.channels must be 'all' or a list of valid ids"}
        tail = Y[-TAIL:]
        out: dict[str, Any] = {
            "ticks_run": int(Y.shape[0]),
            "budget_left": self.world.budget_left,
            "tail_mean": {str(c): round(float(tail[:, c].mean()), 4) for c in idx},
            "tail_sd": {str(c): round(float(tail[:, c].std()), 4) for c in idx},
        }
        if spec.get("series"):
            if len(idx) > 6:
                return {"error": "series observation limited to <=6 channels"}
            maxn = spec.get("max_numbers")
            if not isinstance(maxn, int):
                maxn = MAX_SERIES_NUMBERS
            maxn = int(min(max(maxn, 40), 4000))
            stride = spec.get("stride")
            if not isinstance(stride, int) or stride < 1:
                stride = max(1, (Y.shape[0] * len(idx)) // maxn)
            ds = Y[::stride]
            while ds.shape[0] * len(idx) > maxn:
                stride *= 2
                ds = Y[::stride]
            out["series"] = {str(c): [round(float(v), 3) for v in ds[:, c]]
                             for c in idx}
            out["series_stride"] = stride
        return out

    def _ensure_contracts(self) -> None:
        """Idempotent, deterministic (fresh RNG from the seed each time): both
        contract families exist whenever we are in/entering the answer phase."""
        if not self.contracts:
            rng = np.random.default_rng(
                np.random.SeedSequence([0xC047, self._contract_seed]))
            self.contracts = sample_contracts(self.world, rng, self.n_per_stratum)
            if self.n_prep > 0:
                self.prep_contracts = sample_prep_contracts(self.world, rng, self.n_prep)

    def issue_contracts(self) -> dict:
        self.phase = "answer"
        self._ensure_contracts()
        out = {
            "phase": "answer",
            "note": ("Exploration over. Answer ALL contracts in one JSON object: "
                     '{"op":"answer","answers":[{"id":0,"mean":..,"low":..,"high":..},...]}. '
                     "Each contract runs from a FRESH world state (same laws, new draw); "
                     "predict the statistic and give a [low,high] interval you believe "
                     "covers the true ensemble mean."),
            "contracts": [c.spec() for c in self.contracts],
        }
        if self.prep_contracts:
            out["preparation_contracts"] = [c.spec() for c in self.prep_contracts]
            out["note"] += (" ALSO: preparation contracts ask you to SUBMIT A POLICY "
                            "(code defining policy(t, y, mem) -> action list) that "
                            "steers a fresh draw into the stated band; submit each with "
                            '{"op":"answer_prep","id":<id>,"code":"..."}.')
        return out

    def score(self, answer_text: str | None) -> dict:
        """Score the answer message. Returns rewards/metrics + per-contract detail."""
        self._ensure_contracts()
        answers: dict[int, dict] = {}
        parse_error = None
        if answer_text:
            try:
                obj = _extract_json(answer_text)
                for a in obj.get("answers", []):
                    if isinstance(a, dict) and isinstance(a.get("id"), int):
                        answers[a["id"]] = a
            except ValueError as e:
                parse_error = str(e)
        detail, per_stratum = [], {}
        acc_all, cov_all, ceil_all, cal_all = [], [], [], []
        ranges = self.world.true_channel_range()
        for c in self.contracts:
            mu, tau, samples = truth_statistic(self.world, c)
            scale = answer_scale(tau, float(ranges[c.channel]), c.stat,
                             getattr(self.world.p, "reaction", "tanh"))
            s = score_answer(mu, scale, answers.get(c.id, {}))
            ceil = replication_accuracy(samples, scale)
            detail.append({"id": c.id, "stratum": c.stratum, "channel": c.channel,
                           "mu": round(mu, 4), "tau": round(tau, 4),
                           "scale": round(scale, 4),
                           **{k: (round(v, 4) if isinstance(v, float) else v)
                              for k, v in s.items()},
                           "replication": round(ceil, 4)})
            per_stratum.setdefault(c.stratum, []).append(s["accuracy"])
            acc_all.append(s["accuracy"]); cov_all.append(s["covered"]); ceil_all.append(ceil)
            cal_all.append(s.get("calibration", 0.0))
        prep_detail, prep_rates = [], []
        for c in self.prep_contracts:
            code = self.prep_answers.get(c.id)
            if code:
                pr = score_prep(self.world, c, code)
            else:
                pr = {"success_rate": 0.0, "finals": [], "errors": ["no policy submitted"]}
            prep_detail.append({"id": c.id, "channel": c.channel,
                                "band": [c.lo, c.hi], **pr})
            prep_rates.append(pr["success_rate"])
        result = {
            "reward_accuracy": float(np.mean(acc_all)),
            "reward_calibration": float(np.mean(cal_all)),
            "coverage": float(np.mean(cov_all)),
            "replication_ref": float(np.mean(ceil_all)),
            "per_stratum": {k: float(np.mean(v)) for k, v in per_stratum.items()},
            "n_answered": float(np.mean([d["answered"] for d in detail])),
            "budget_used_frac": self.world.ticks_used / self.world.p.max_ticks,
            "detail": detail,
        }
        if self.prep_contracts:
            result["reward_preparation"] = float(np.mean(prep_rates))
            result["prep_detail"] = prep_detail
        if self.theory_code:
            result["theory"] = score_theory(self.world, self.contracts, self.theory_code)
        if parse_error:
            result["parse_error"] = parse_error
        return result


def _extract_json(text: str) -> dict:
    """Parse the last JSON object in a message (tolerates code fences/prose)."""
    if text is None:
        raise ValueError("empty message")
    s = text.strip()
    if s.startswith("```"):
        s = s.strip("`")
        if s.startswith("json"):
            s = s[4:]
    # fast path
    try:
        obj = json.loads(s)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass
    # scan for balanced {...} blocks, prefer the LAST parsable one
    candidates = []
    depth, start = 0, None
    for i, ch in enumerate(s):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    candidates.append(s[start:i + 1])
    for cand in reversed(candidates):
        try:
            obj = json.loads(cand)
            if isinstance(obj, dict) and "op" in obj or "answers" in (obj if isinstance(obj, dict) else {}):
                return obj
        except json.JSONDecodeError:
            continue
    for cand in reversed(candidates):
        try:
            obj = json.loads(cand)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    raise ValueError("no JSON object found")
