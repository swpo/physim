"""physim.session — the agent-facing surface + contract scoring.

Chat-tier interface (M0): the agent sends JSON commands; we execute against the
persistent World and return compact JSON observations (context-bandwidth
discipline: server-side reduction, capped numbers).

Commands
  {"op":"run", "segments":[SEG,...], "observe":{...}?}   advance the world
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
        return {
            "id": self.id,
            "protocol": {"from": "fresh_state", "segments": self.segments},
            "predict": {"channel": self.channel, "stat": self.stat,
                        "window": f"last_{TAIL}_ticks"},
            "answer_format": {"mean": "float", "low": "float", "high": "float"},
        }


def sample_contracts(world: World, rng: np.random.Generator,
                     n_per_stratum: int = 4) -> list[Contract]:
    """Ontology-neutral protocol grammar, stratified (DESIGN.md v0.4)."""
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


def truth_statistic(world: World, contract: Contract, ensemble: int = ENSEMBLE
                    ) -> tuple[float, float, list[float]]:
    """Run the contract protocol on `ensemble` fresh clones; return
    (mu, tau, samples) of the statistic."""
    U = render_protocol(contract.segments, world.p.n_in)
    vals = []
    for e in range(ensemble):
        clone = world.clone_fresh(noise_seed=1000 + 97 * contract.id + e)
        Y = clone.run(U)
        vals.append(float(Y[-TAIL:, contract.channel].mean()))
    v = np.asarray(vals)
    tau_floor = world.p.meas_noise / np.sqrt(TAIL)   # sd of a TAIL-tick mean read
    return float(v.mean()), float(max(v.std(), tau_floor, 1e-6)), vals


def answer_scale(tau: float, channel_range: float) -> float:
    """Error tolerance: ensemble spread when the world is genuinely stochastic,
    floored at 10% of the channel's dynamic range when it is quasi-deterministic
    (predicting within a few % of range is 'understanding'; branch confusion
    ~ full range still scores ~0)."""
    return float(max(3.0 * tau, 0.1 * channel_range, 1e-3))


def score_answer(mu: float, scale: float, ans: dict) -> dict:
    """Accuracy in (0,1]: exp(-|err|/scale). Coverage: does mu land in [low,high]."""
    try:
        mean = float(ans["mean"]); low = float(ans["low"]); high = float(ans["high"])
    except (KeyError, TypeError, ValueError):
        return {"accuracy": 0.0, "covered": 0.0, "z": None, "answered": 0.0}
    z = abs(mean - mu) / scale
    return {"accuracy": float(np.exp(-z)), "covered": float(low <= mu <= high),
            "z": float(z), "answered": 1.0}


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


# ---------------------------------------------------------------- session
class PhysimSession:
    """Holds the persistent world + phase machine (explore -> answer -> done)."""

    def __init__(self, world: World, contract_seed: int, n_per_stratum: int = 4):
        self.world = world
        self.phase = "explore"
        self.rng = np.random.default_rng(np.random.SeedSequence([0xC047, contract_seed]))
        self.n_per_stratum = n_per_stratum
        self.contracts: list[Contract] = []
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
        if self.phase == "answer" and op != "answer":
            return {"error": "exploration is over; reply with the answers object",
                    "contracts": [c.spec() for c in self.contracts]}
        if op == "run":
            return self._op_run(cmd)
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

    def issue_contracts(self) -> dict:
        self.phase = "answer"
        if not self.contracts:
            self.contracts = sample_contracts(self.world, self.rng, self.n_per_stratum)
        return {
            "phase": "answer",
            "note": ("Exploration over. Answer ALL contracts in one JSON object: "
                     '{"op":"answer","answers":[{"id":0,"mean":..,"low":..,"high":..},...]}. '
                     "Each contract runs from a FRESH world state (same laws, new draw); "
                     "predict the statistic and give a [low,high] interval you believe "
                     "covers the true ensemble mean."),
            "contracts": [c.spec() for c in self.contracts],
        }

    def score(self, answer_text: str | None) -> dict:
        """Score the answer message. Returns rewards/metrics + per-contract detail."""
        if not self.contracts:
            self.contracts = sample_contracts(self.world, self.rng, self.n_per_stratum)
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
        acc_all, cov_all, ceil_all = [], [], []
        ranges = self.world.true_channel_range()
        for c in self.contracts:
            mu, tau, samples = truth_statistic(self.world, c)
            scale = answer_scale(tau, float(ranges[c.channel]))
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
        result = {
            "reward_accuracy": float(np.mean(acc_all)),
            "coverage": float(np.mean(cov_all)),
            "replication_ref": float(np.mean(ceil_all)),
            "per_stratum": {k: float(np.mean(v)) for k, v in per_stratum.items()},
            "n_answered": float(np.mean([d["answered"] for d in detail])),
            "budget_used_frac": self.world.ticks_used / self.world.p.max_ticks,
            "detail": detail,
        }
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
