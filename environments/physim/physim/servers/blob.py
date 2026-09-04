"""physim.servers.blob — probe-device world server (BLOB family, MCP tier).

Agent-facing surface for Track A round 1: two anonymous probe devices in an
evolved field world. The agent sees ONLY anonymized scalar streams, per-port
global mean/var, budget counters, and episode time. No coordinates, no
device geometry, no field names, no world topology (barrier b1-b3; see
physim.blobcore for the evaluator-side design notes).

Tools (prefix `probe_`):
  probe_status()                     time, budgets, interface counts, phase,
                                     announced contracts, pricing, locks
  probe_read_streams(window, ...)    advance + read sensors (costed)
  probe_wait(steps)                  advance without reading (free)
  probe_adjust(device, u1, u2, u3)   3-channel actuator (costed; R3-final:
                                     fixed global convention u1->dx, u2->dy,
                                     u3->dlog spacing — UNDOCUMENTED to
                                     agents; mastery transfers across worlds)
  probe_inject(port, amp, dur, ...)  ONLY at the end of the span: fork a
                                     live replica with the agent's emission
                                     on the fixed emission channel (location
                                     undisclosed, R2); returns replica
                                     streams (sensor-costed, amp-priced)
  probe_submit(contract, payload)    submit/revise a contract payload

Episode clock: the main line replays a cached (world, seed) trajectory from
t=0 to T0 in 5tu control steps (passive sensors: replay == live, A0-gated).
The main line HARD-STOPS at T0. Replicas fork from the T0 state and run the
world engine live. The first probe_inject LOCKS P1/P2 (they are forecasts
issued at T0). State that crosses the state channel is evaluator-side only
(poses are secret-frame coordinates; never surfaced by any tool).
"""

from __future__ import annotations

import hashlib
import json

import numpy as np

import verifiers.v1 as vf

from physim import blobcore as B
from physim.blobstate import BlobToolState


def _r(x, nd=5):
    """Round nested arrays for compact JSON."""
    return np.round(np.asarray(x, float), nd).tolist()


class BlobToolsetConfig(vf.ToolsetConfig):
    pass


# ═══════════════════════════════════════════════════════════ round 5 (v2.1)
# BLOB2v2 surface (TRACKA_R5_ANCHORS.md 2.5): two-phase closed-book episode.
# Registered INSTEAD of the v1 tools when the rollout task's difficulty tag
# starts with "BLOB2v2" (BlobToolset.register filters; the v1 surface is
# frozen byte-identical for v1 tags). Tool set:
#   probe_status [A+B]  probe_read [A]   probe_wait [A]   probe_adjust [A]
#   probe_fork [A]      probe_reset [A]  probe_inject [A, fork ctx only]
#   probe_ready [A->B]  probe_submit [B]
# Phase B: every world tool returns one generic phase error; status/submit
# stay. No budget/pricing/meter language anywhere agent-visible; silent
# meters + safety caps live in physim.blobround5 (CAPS5), cap refusals are
# the generic "instrument saturated".
#
# Live fork sims are held in server-process memory (_LIVE5) keyed by
# (rollout nonce, fork id); the serializable state carries each fork's
# anchor + op log, so a cold registry rebuilds any fork deterministically
# (fork noise streams are salted per (nonce, fork counter): same prefix of
# ops => same stream => same state).

_LIVE5: dict = {}          # (nonce, fork_id) -> dict(S=sim state, steps=int)
_TPL5: dict = {}           # (world, seed) -> shared init_soup template

_PHASE_ERR = "not available in the current phase"
V1_TOOL_NAMES = ("status", "read_streams", "wait", "adjust", "inject",
                 "submit")
V2_TOOL_NAMES = ("status", "read", "wait", "adjust", "fork", "reset",
                 "inject", "ready", "submit")


def _r5tool(fn):
    """Marker: this @vf.tool belongs to the round-5 surface."""
    fn._r5_tool = True
    return fn


def _template5(world: str, seed: int) -> dict:
    key = (world, seed)
    if key not in _TPL5:
        from blobkit.soup import sim_cpu
        c = B.get_cached(world, seed)
        _TPL5[key] = sim_cpu.init_soup(
            B.load_genome(world), L=c.meta["L"], seed=seed, dtype="f32",
            workers=3)
    return _TPL5[key]


class Blob5Mixin:
    """Round-5 tool implementations, mixed into BlobToolset. Shares v1
    helpers (_ready, _parse_devices, _k_of); all round-5 state lives on the
    same BlobToolState under r5_* fields."""

    # ------------------------------------------------------------ plumbing
    def _R5(self):
        from physim import blobround5 as R5
        return R5

    def _ensure5(self):
        st = self.state
        if not st.r5_nonce:
            import uuid
            st.r5_nonce = uuid.uuid4().hex
        if not st.r5_poses_base:
            sec = B.get_secrets(st.world, st.seed)
            st.r5_poses_base = [[*sec["devices"][i]["center"], 1.0]
                                for i in range(len(B.ROSTER))]
        if not st.r5_meters:
            st.r5_meters = dict(sensor=0.0, adjust=0.0, injection=0.0,
                                sim_tu=0.0)
        if not st.r5_cap_hits:
            st.r5_cap_hits = {k: 0 for k in ("sensor", "adjust", "injection",
                                             "sim_tu", "fork_spawns",
                                             "open_forks")}

    def _err5(self, msg: str, **extra) -> str:
        out = {"error": msg}
        out.update(extra)
        return json.dumps(out)

    def _phase_gate(self, need: str) -> str | None:
        """need = "A" (world tools) or "B" (submit)."""
        revealed = self.state.r5_phase == "revealed"
        if need == "A" and revealed:
            return self._err5(_PHASE_ERR)
        if need == "B" and not revealed:
            return self._err5(_PHASE_ERR)
        return None

    def _cap_check(self, meter: str, add: float = 1.0) -> str | None:
        """Silent safety caps (blobround5.CAPS5). A refusal is generic and
        counted; caps are runaway protection, target hit rate 0."""
        R5 = self._R5()
        st = self.state
        if meter in ("fork_spawns", "open_forks"):
            cur = (st.r5_fork_seq if meter == "fork_spawns" else
                   sum(1 for f in st.r5_forks.values() if f["open"]))
            if cur + add > R5.CAPS5[meter]:
                st.r5_cap_hits[meter] += 1
                return self._err5(R5.CAP_MSG)
            return None
        if st.r5_meters.get(meter, 0.0) + add > R5.CAPS5[meter] + 1e-9:
            st.r5_cap_hits[meter] += 1
            return self._err5(R5.CAP_MSG)
        return None

    def _meter(self, key: str, add: float):
        st = self.state
        st.r5_meters[key] = st.r5_meters.get(key, 0.0) + float(add)

    # ------------------------------------------------------- fork registry
    def _fork_record(self, src: list, poses: list, anchor_abs: float) -> str:
        st = self.state
        st.r5_fork_seq += 1
        idx = st.r5_fork_seq
        fid = "f" + hashlib.sha256(
            f"{st.r5_nonce}|{idx}".encode()).hexdigest()[:8]
        st.r5_forks[fid] = dict(
            src=src, salt_idx=idx, poses=[list(p) for p in poses],
            poses0=[list(p) for p in poses], steps=0, emissions=[],
            log=[], open=True, anchor_abs=float(anchor_abs))
        return fid

    def _anchor_state5(self, fk: dict):
        """f32 anchor fields for a fork record: a base grid frame (the f16
        record promoted to f32 — the A0-tolerance base state) or a rebuild
        of the parent fork at the spawn step."""
        st = self.state
        src = fk["src"]
        if src[0] == "base":
            return B.get_cached(st.world, st.seed).fields_at(int(src[1]))
        parent_S = self._fork_sim(src[1], upto_steps=int(src[2]))
        return np.array(parent_S["F"], np.float32)

    def _fresh_sim(self, fk: dict) -> dict:
        R5 = self._R5()
        st = self.state
        tpl = _template5(st.world, st.seed)
        S = dict(tpl)
        S["F"] = np.array(self._anchor_state5(fk), np.float32)
        S["rng"] = np.random.default_rng(
            R5.fork_stream_seed(st.r5_nonce, fk["salt_idx"]))
        S["t_step"] = 0
        return S

    def _advance_sim(self, S: dict, fk_like: dict, from_step: int,
                     n_steps: int):
        """Advance a fork sim n_steps control steps, applying the fork's
        emissions at substep resolution (continuous dur)."""
        R5 = self._R5()
        st = self.state
        perm = np.asarray(B.get_secrets(st.world, st.seed)["port_perm"],
                          int)
        inj_yx = B.get_secrets(st.world, st.seed)["devices"][
            B.DEV_A]["center"]
        spc = R5.SPC
        for j in range(from_step, from_step + n_steps):
            a, b = j * spc, (j + 1) * spc
            cuts = {a, b}
            for e in fk_like["emissions"]:
                for k in (int(e[2]), int(e[3])):
                    if a < k < b:
                        cuts.add(k)
            seq = sorted(cuts)
            for s0, s1 in zip(seq[:-1], seq[1:]):
                injs = [dict(field=int(perm[int(e[0])]), y=inj_yx[0],
                             x=inj_yx[1], amp=float(e[1]))
                        for e in fk_like["emissions"]
                        if int(e[2]) <= s0 < int(e[3])]
                B.agdev.step_chunk(S, s1 - s0, injections=injs)

    def _fork_sim(self, fid: str, upto_steps: int | None = None) -> dict:
        """The live sim state of a fork, rebuilt from the op log when the
        in-memory registry is cold (deterministic: salted stream + logged
        ops). upto_steps: historical state for fork-of-fork anchors."""
        st = self.state
        fk = st.r5_forks[fid]
        target = fk["steps"] if upto_steps is None else upto_steps
        key = (st.r5_nonce, fid)
        ent = _LIVE5.get(key)
        if ent is not None and ent["steps"] == target and \
                upto_steps is None:
            return ent["S"]
        # deterministic rebuild: replay the op log up to `target` steps
        S = self._fresh_sim(fk)
        steps = 0
        rec = dict(emissions=[], poses=[list(p) for p in fk["poses0"]])
        for op in fk["log"]:
            if steps >= target:
                break
            kind = op[0]
            if kind == "adv":
                n = min(int(op[1]), target - steps)
                self._advance_sim(S, rec, steps, n)
                steps += n
            elif kind == "adj":
                _dev, u1, u2, u3, nreq = op[1], op[2], op[3], op[4], op[5]
                applied = self._walk_poses(rec["poses"], int(op[1]),
                                           [u1, u2, u3], int(nreq))
                n = min(applied, target - steps)
                self._advance_sim(S, rec, steps, n)
                steps += n
            elif kind == "inj":
                k0 = steps * self._R5().SPC
                rec["emissions"].append(
                    [int(op[1]), float(op[2]), k0,
                     k0 + int(round(float(op[3]) / self._R5().SIM_DT))])
        if upto_steps is None:
            _LIVE5[key] = dict(S=S, steps=steps)
        return S

    def _walk_poses(self, poses: list, device: int, u: list,
                    steps: int) -> int:
        """Apply the R3-final actuator to a pose list in place; returns the
        number of applied steps (a refused step stops the walk; v1
        semantics — only the dilation channel can strike its bounds)."""
        st = self.state
        L = B.get_cached(st.world, st.seed).meta["L"]
        lo, hi = B.agdev.DIL_BOUNDS
        M = B.adjust_mix(B.world_key(st.world, st.seed))
        d = M @ np.clip(np.asarray(u, float), -1.0, 1.0)
        applied = 0
        for _ in range(int(steps)):
            new_dil = poses[device][2] * float(np.exp(d[2]))
            if not (lo - 1e-12 <= new_dil <= hi + 1e-12):
                break
            poses[device][0] = (poses[device][0] + d[0]) % L
            poses[device][1] = (poses[device][1] + d[1]) % L
            poses[device][2] = float(new_dil)
            applied += 1
        return applied

    # ------------------------------------------------------ context helpers
    def _ctx_of(self, ctx):
        """Resolve a context argument -> ("base", None) | ("fork", fid) |
        (None, error_json)."""
        st = self.state
        c = str(ctx).strip() if ctx is not None else "base"
        if c in ("", "base"):
            return "base", None
        if c in st.r5_forks:
            if not st.r5_forks[c]["open"]:
                return None, self._err5(f"unknown context {c!r}")
            return "fork", c
        return None, self._err5(f"unknown context {c!r}")

    def _devices5(self, poses):
        st = self.state
        return [B.make_device(st.world, st.seed, i, center=poses[i][:2],
                              dilation=poses[i][2])
                for i in range(len(B.ROSTER))]

    def _parse_ports5(self, ports, nf):
        if ports in ("all", None, ""):
            return list(range(nf)), None
        if isinstance(ports, str):
            try:
                ports = json.loads(ports)
            except json.JSONDecodeError:
                return None, self._err5("ports must be 'all' or a list")
        try:
            port_ids = [int(x) for x in ports]
        except (TypeError, ValueError):
            return None, self._err5("ports must be 'all' or a list of ints")
        if any(x < 0 or x >= nf for x in port_ids):
            return None, self._err5(f"port ids must be in [0, {nf - 1}]")
        return port_ids, None

    def _fork_fields(self, fid):
        S = self._fork_sim(fid)
        return np.asarray(S["F"], np.float32)

    def _sample_ctx(self, kind, fid, dev_ids, devs):
        """Streams at the context's CURRENT state, devices in the context's
        poses. Base: cached frame at the read head; fork: live fields."""
        st = self.state
        if kind == "base":
            return {i: B.sample_at(st.world, st.seed, st.r5_ibase, devs[i])
                    for i in dev_ids}
        perm = np.asarray(B.get_secrets(st.world, st.seed)["port_perm"],
                          int)
        dx = B.get_cached(st.world, st.seed).meta["dx"]
        f = self._fork_fields(fid)[perm]
        return {i: devs[i].sample(f, dx) for i in dev_ids}

    def _glob_ctx(self, kind, fid):
        st = self.state
        if kind == "base":
            return B.global_stats(st.world, st.seed, st.r5_ibase)
        perm = np.asarray(B.get_secrets(st.world, st.seed)["port_perm"],
                          int)
        f = self._fork_fields(fid)[perm]
        return np.stack([f.mean(axis=(1, 2)), f.var(axis=(1, 2))], axis=1)

    def _t_of(self, kind, fid):
        st = self.state
        if kind == "base":
            return st.r5_ibase * B.CTRL_TU
        fk = st.r5_forks[fid]
        return fk["anchor_abs"] + fk["steps"] * B.CTRL_TU

    def _advance_fork_live(self, fid, n_steps):
        """Advance a live fork n_steps control steps (sim_tu metered by the
        caller after cap check)."""
        st = self.state
        fk = st.r5_forks[fid]
        S = self._fork_sim(fid)
        self._advance_sim(S, fk, fk["steps"], n_steps)
        fk["steps"] += n_steps
        _LIVE5[(st.r5_nonce, fid)] = dict(S=S, steps=fk["steps"])

    def _open_forks(self):
        st = self.state
        return [fid for fid, f in st.r5_forks.items() if f["open"]]

    # -------------------------------------------------------------- tools
    @_r5tool
    @vf.tool(name="status")
    async def status5(self) -> str:
        """Report the episode phase, the base-record read head, open fork
        contexts, interface counts, apparatus ranges, the syllabus, and —
        after probe_ready — the revealed instance menu with submission
        flags."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure5()
        R5 = self._R5()
        st = self.state
        st.turns += 1
        nf = B.n_ports(st.world, st.seed)
        devs = self._devices5(st.r5_poses_base)
        revealed = st.r5_phase == "revealed"
        out = dict(
            phase=("revealed" if revealed else "exploration"),
            t_base_head=st.r5_ibase * B.CTRL_TU,
            T_BASE=R5.T_BASE,
            step_tu=B.CTRL_TU,
            n_devices=len(devs),
            ports=nf,
            slots_per_device=[d.k for d in devs],
            n_actuator_channels=3,
            apparatus=dict(u_range=[-1.0, 1.0],
                           amp_range=[B.AMP_MIN, B.AMP_CAP],
                           amp_zero_ok=True,
                           dur_range_tu=[0.0, B.DUR_CAP],
                           emission=("all emissions enter through the same "
                                     "fixed emission channel; where and "
                                     "what it couples to is undisclosed")),
            contexts=[dict(id=fid,
                           anchor_t=st.r5_forks[fid]["anchor_abs"],
                           t_now=self._t_of("fork", fid))
                      for fid in self._open_forks()],
            syllabus=R5.syllabus5(st.world, st.seed, st.round5),
        )
        if revealed:
            out["instances"] = R5.reveal_menu5(st.world, st.seed, st.round5,
                                               _active_salt())
            out["submitted"] = {i["id"]: bool(st.r5_subs.get(
                i["id"].split("@")[0])) for i in out["instances"]}
        return json.dumps(out)

    @_r5tool
    @vf.tool(name="read")
    async def read5(self, ctx="base", window: int = 1, devices="all",
                    ports="all", stride: int = 1,
                    include_global: bool = True) -> str:
        """Read sensor streams in a context ("base" = the base record, or a
        fork id). Advances the context up to `window` 5tu steps, reading
        the selected devices every `stride`-th step; window=0 reads the
        current state without advancing. The base head only moves forward
        (use probe_fork for random access to any base time). Returns
        values[device][port][slot] per read step plus per-port global
        mean/variance."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure5()
        st = self.state
        st.turns += 1
        gate = self._phase_gate("A")
        if gate:
            return gate
        kind, fid = self._ctx_of(ctx)
        if kind is None:
            return fid
        try:
            window = int(window)
            stride = max(int(stride), 1)
        except (TypeError, ValueError):
            return self._err5("window and stride must be integers")
        if window < 0:
            return self._err5("window must be >= 0")
        nf = B.n_ports(st.world, st.seed)
        dev_ids = self._parse_devices(devices)
        if not dev_ids:
            return self._err5("devices must be 'all' or a list of device "
                              "ids")
        port_ids, perr = self._parse_ports5(ports, nf)
        if perr:
            return perr
        if kind == "base" and window > 0:
            head_max = int(round(self._R5().T_BASE / B.CTRL_TU))
            room = head_max - st.r5_ibase
            if room <= 0:
                return self._err5(
                    "the base record ends at t = 2500 (window=0 reads the "
                    "current state; probe_fork reaches any base time)")
            window = min(window, room)
        read_steps = ([0] if window == 0 else
                      list(range(stride - 1, window, stride)))
        k_read = self._k_of(dev_ids)
        n_numbers = len(read_steps) * len(port_ids) * k_read
        if n_numbers > 60000:
            return self._err5(f"response too large ({n_numbers} numbers > "
                              "60000); narrow the read")
        sensor_cost = len(read_steps) * k_read * B.CTRL_TU
        cap = self._cap_check("sensor", sensor_cost)
        if cap:
            return cap
        if kind == "fork":
            cap = self._cap_check("sim_tu", window * B.CTRL_TU)
            if cap:
                return cap
        poses = (st.r5_poses_base if kind == "base"
                 else st.r5_forks[fid]["poses"])
        devs = self._devices5(poses)
        out_steps = []
        if window == 0:
            sm = self._sample_ctx(kind, fid, dev_ids, devs)
            out_steps.append(dict(
                t=self._t_of(kind, fid),
                values={str(i): _r(sm[i][port_ids]) for i in dev_ids}))
        else:
            for j in range(window):
                if kind == "base":
                    st.r5_ibase += 1
                else:
                    self._advance_fork_live(fid, 1)
                if j in read_steps:
                    sm = self._sample_ctx(kind, fid, dev_ids, devs)
                    out_steps.append(dict(
                        t=self._t_of(kind, fid),
                        values={str(i): _r(sm[i][port_ids])
                                for i in dev_ids}))
        self._meter("sensor", sensor_cost)
        if kind == "fork" and window > 0:
            fk = st.r5_forks[fid]
            fk["log"] = list(fk["log"]) + [["adv", window]]
            self._meter("sim_tu", window * B.CTRL_TU)
        if kind == "base":
            st.r5_reads_base += len(read_steps)
        else:
            st.r5_reads_fork += len(read_steps)
        resp = dict(ctx=("base" if kind == "base" else fid),
                    t=self._t_of(kind, fid), steps=out_steps,
                    ports=port_ids)
        if include_global:
            resp["global_stats"] = _r(self._glob_ctx(kind, fid))
        return json.dumps(resp)

    @_r5tool
    @vf.tool(name="wait")
    async def wait5(self, ctx="base", steps: int = 1) -> str:
        """Advance a context ("base" or a fork id) up to `steps` 5tu steps
        without reading. Returns the context's new time and the free
        per-port global mean/variance."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure5()
        st = self.state
        st.turns += 1
        gate = self._phase_gate("A")
        if gate:
            return gate
        kind, fid = self._ctx_of(ctx)
        if kind is None:
            return fid
        try:
            steps = int(steps)
        except (TypeError, ValueError):
            return self._err5("steps must be an integer")
        if steps < 1:
            return self._err5("steps must be >= 1")
        if kind == "base":
            head_max = int(round(self._R5().T_BASE / B.CTRL_TU))
            room = head_max - st.r5_ibase
            if room <= 0:
                return self._err5("the base record ends at t = 2500")
            steps = min(steps, room)
            st.r5_ibase += steps
        else:
            cap = self._cap_check("sim_tu", steps * B.CTRL_TU)
            if cap:
                return cap
            self._advance_fork_live(fid, steps)
            fk = st.r5_forks[fid]
            fk["log"] = list(fk["log"]) + [["adv", steps]]
            self._meter("sim_tu", steps * B.CTRL_TU)
        return json.dumps(dict(
            ctx=("base" if kind == "base" else fid),
            t=self._t_of(kind, fid),
            global_stats=_r(self._glob_ctx(kind, fid))))

    @_r5tool
    @vf.tool(name="adjust")
    async def adjust5(self, device: int, u1: float, u2: float, u3: float,
                      ctx="base", steps: int = 1, read: bool = True) -> str:
        """Apply the 3-channel actuator (u1, u2, u3) to one device in a
        context ("base" or a fork id) for `steps` 5tu steps. Each u is
        clipped to [-1, 1]. What the channels do to the device is fixed for
        the whole episode but undisclosed — discovering it is part of the
        task. The actuator may refuse a step (the response marks it
        "adjust_rejected"; steps after it do not run). read=True samples
        the device after each completed step. Device configurations are
        per-context; a fork inherits them from its spawning context."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure5()
        st = self.state
        st.turns += 1
        gate = self._phase_gate("A")
        if gate:
            return gate
        kind, fid = self._ctx_of(ctx)
        if kind is None:
            return fid
        try:
            device = int(device)
            u = np.clip([float(u1), float(u2), float(u3)], -1.0, 1.0)
            steps = int(steps)
        except (TypeError, ValueError):
            return self._err5("device, u1, u2, u3, steps must be numeric")
        if device not in (0, 1):
            return self._err5("device must be 0 or 1")
        if steps < 1:
            return self._err5("steps must be >= 1")
        if kind == "base":
            head_max = int(round(self._R5().T_BASE / B.CTRL_TU))
            room = head_max - st.r5_ibase
            if room <= 0:
                return self._err5("the base record ends at t = 2500")
            steps = min(steps, room)
        adj_per_step = float(np.abs(u).sum())
        cap = self._cap_check("adjust", adj_per_step * steps)
        if cap:
            return cap
        if kind == "fork":
            cap = self._cap_check("sim_tu", steps * B.CTRL_TU)
            if cap:
                return cap
        k_dev = self._k_of([device])
        if read:
            cap = self._cap_check("sensor", steps * k_dev * B.CTRL_TU)
            if cap:
                return cap
        poses = (st.r5_poses_base if kind == "base"
                 else st.r5_forks[fid]["poses"])
        out_steps = []
        applied = 0
        rejected = False
        sensor_charge = 0.0
        for _ in range(steps):
            n_ok = self._walk_poses(poses, device, list(u), 1)
            if n_ok == 0:
                rejected = True
                break
            applied += 1
            if kind == "base":
                st.r5_ibase += 1
            else:
                self._advance_fork_live(fid, 1)
            if read:
                sensor_charge += k_dev * B.CTRL_TU
                devs = self._devices5(poses)
                sm = self._sample_ctx(kind, fid, [device], devs)
                out_steps.append(dict(t=self._t_of(kind, fid),
                                      values=_r(sm[device])))
        charge = adj_per_step * (applied + (1 if rejected else 0))
        self._meter("adjust", charge)
        self._meter("sensor", sensor_charge)
        if kind == "fork":
            if applied:
                fk = st.r5_forks[fid]
                fk["log"] = list(fk["log"]) + [["adj", device, float(u[0]),
                                                float(u[1]), float(u[2]),
                                                applied]]
            self._meter("sim_tu", applied * B.CTRL_TU)
            st.r5_reads_fork += len(out_steps)
        else:
            st.r5_reads_base += len(out_steps)
        return json.dumps(dict(
            ctx=("base" if kind == "base" else fid),
            t=self._t_of(kind, fid), applied=[float(x) for x in u],
            steps_requested=steps, steps_applied=applied,
            result=("adjust_rejected" if rejected else "ok"),
            device=device, steps_read=out_steps))

    @_r5tool
    @vf.tool(name="fork")
    async def fork5(self, t=None, fork="") -> str:
        """Spawn an exploration fork: from any base-record grid time `t`
        (a multiple of 5 in [0, 2500]) or from another fork's current state
        (pass its id as `fork`). The new fork runs live and independently
        under your control (probe_read / probe_wait / probe_adjust /
        probe_inject with ctx = its id); it inherits the spawning context's
        device configurations. Returns the fork id."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure5()
        R5 = self._R5()
        st = self.state
        st.turns += 1
        gate = self._phase_gate("A")
        if gate:
            return gate
        cap = self._cap_check("fork_spawns")
        if cap:
            return cap
        cap = self._cap_check("open_forks")
        if cap:
            return cap
        if fork:
            kind, pfid = self._ctx_of(fork)
            if kind != "fork":
                return pfid if kind is None else self._err5(
                    "fork must name an open fork id")
            pf = st.r5_forks[pfid]
            fid = self._fork_record(["fork", pfid, pf["steps"]],
                                    pf["poses"],
                                    self._t_of("fork", pfid))
        else:
            if t is None:
                return self._err5("give a base grid t or a fork id")
            try:
                t = float(t)
            except (TypeError, ValueError):
                return self._err5("t must be numeric")
            i_grid = int(round(t / B.CTRL_TU))
            if abs(i_grid * B.CTRL_TU - t) > 1e-6 or i_grid < 0 or \
                    i_grid > int(round(R5.T_BASE / B.CTRL_TU)):
                return self._err5(
                    "t must be a multiple of 5 in [0, 2500]")
            fid = self._fork_record(["base", i_grid], st.r5_poses_base, t)
        st.r5_open_peak = max(st.r5_open_peak, len(self._open_forks()))
        # realize the sim state now (registry warm; also validates anchor)
        self._fork_sim(fid)
        fk = st.r5_forks[fid]
        return json.dumps(dict(fork=fid, anchor_t=fk["anchor_abs"],
                               t=self._t_of("fork", fid)))

    @_r5tool
    @vf.tool(name="reset")
    async def reset5(self, fork="") -> str:
        """Discard a fork. Its id stops being a valid context."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure5()
        st = self.state
        st.turns += 1
        gate = self._phase_gate("A")
        if gate:
            return gate
        kind, fid = self._ctx_of(fork)
        if kind != "fork":
            return fid if kind is None else self._err5(
                "reset needs a fork id")
        st.r5_forks[fid]["open"] = False
        st.r5_n_resets += 1
        _LIVE5.pop((st.r5_nonce, fid), None)
        return json.dumps(dict(ok=True, fork=fid))

    @_r5tool
    @vf.tool(name="inject")
    async def inject5(self, ctx, port: int, amp: float, dur: float) -> str:
        """Drive the fixed emission channel inside fork ctx, starting at the
        fork's current time, with (port, amp) for dur tu. Fork contexts
        only — the base record is immutable history. amp = 0 or in
        [0.05, 1.0] (the apparatus cannot emit stronger); dur in (0, 50]
        tu. The emission acts while the fork advances (probe_read /
        probe_wait); reading is separate."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure5()
        R5 = self._R5()
        st = self.state
        st.turns += 1
        gate = self._phase_gate("A")
        if gate:
            return gate
        kind, fid = self._ctx_of(ctx)
        if kind is None:
            return fid
        if kind != "fork":
            return self._err5(
                "emissions run inside forks only; the base record is "
                "immutable history (spawn a fork first)")
        nf = B.n_ports(st.world, st.seed)
        try:
            port = int(port)
            amp = float(amp)
            dur = float(dur)
        except (TypeError, ValueError):
            return self._err5("port, amp, dur must be numeric")
        if port < 0 or port >= nf:
            return self._err5(f"port must be in [0, {nf - 1}]")
        if amp != 0.0 and not (B.AMP_MIN <= amp <= B.AMP_CAP):
            return self._err5(
                f"amp must be 0 or in [{B.AMP_MIN}, {B.AMP_CAP}] — the "
                "apparatus cannot emit stronger")
        if not (0.0 < dur <= B.DUR_CAP):
            return self._err5(f"dur must be in (0, {B.DUR_CAP:g}] tu")
        inj_cost = B.inj_price(amp) * dur
        cap = self._cap_check("injection", inj_cost)
        if cap:
            return cap
        fk = st.r5_forks[fid]
        k0 = fk["steps"] * R5.SPC
        k1 = k0 + int(round(dur / R5.SIM_DT))
        fk["emissions"] = list(fk["emissions"]) + [[port, amp, k0, k1]]
        fk["log"] = list(fk["log"]) + [["inj", port, amp, dur]]
        self._meter("injection", inj_cost)
        return json.dumps(dict(ok=True, ctx=fid, port=port, amp=amp,
                               dur=dur, t=self._t_of("fork", fid),
                               note="the emission acts over the next "
                                    f"{dur:g} tu as this fork advances"))

    @_r5tool
    @vf.tool(name="ready")
    async def ready5(self) -> str:
        """Irreversible: end exploration and open the envelope. Returns the
        six concrete instances (ids, anchors, protocols, observables,
        payload shapes). Every world tool closes for the rest of the
        episode; probe_submit opens; probe_status keeps reporting the
        instance menu and your submission flags."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure5()
        R5 = self._R5()
        st = self.state
        st.turns += 1
        if st.r5_phase == "revealed":
            return self._err5(_PHASE_ERR)
        st.r5_phase = "revealed"
        st.r5_t_ready_sim = float(st.r5_meters.get("sim_tu", 0.0))
        st.r5_t_ready_turns = int(st.turns)
        for fid in self._open_forks():
            st.r5_forks[fid]["open"] = False
            _LIVE5.pop((st.r5_nonce, fid), None)
        menu = R5.reveal_menu5(st.world, st.seed, st.round5, _active_salt())
        return json.dumps(dict(
            phase="revealed",
            instances=menu,
            note=("world access is closed; submit {\"mean\",\"sigma\"} "
                  "arrays of the stated shapes with probe_submit; "
                  "resubmission replaces; the episode is scored at its "
                  "end")))

    @_r5tool
    @vf.tool(name="submit")
    async def submit5(self, instance: str, payload) -> str:
        """Submit or revise one instance's payload after probe_ready.
        payload = {"mean": nested list in the instance's payload shape,
        "sigma": scalar or same-shape list} (sigma = your predictive sd;
        scoring is CRPS-based, so honest spread beats overconfidence). The
        last accepted submission per instance is the one scored."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure5()
        R5 = self._R5()
        st = self.state
        st.turns += 1
        gate = self._phase_gate("B")
        if gate:
            return gate
        fam = str(instance).strip().upper().split("@")[0]
        if fam not in R5.MENUS5[st.round5]:
            ids = [f"{c}@i1" for c in R5.MENUS5[st.round5]]
            return self._err5("instance must be one of " + ", ".join(ids))
        if isinstance(payload, str):
            js = payload
        else:
            try:
                js = json.dumps(payload)
            except (TypeError, ValueError):
                return self._err5("payload not JSON-serializable")
        shape = R5.payload_shapes5(st.world, st.seed, st.round5,
                                   _active_salt())[fam]
        parsed, why = B._parse_payload(js, shape)
        if parsed is None:
            return self._err5(f"rejected: {why}",
                              required_shape=list(shape))
        st.r5_subs = {**(st.r5_subs or {}), fam: js}
        return json.dumps(dict(
            ok=True, instance=f"{fam}@i1", shape=list(shape),
            note="recorded; scored after the episode ends; resubmission "
                 "replaces"))

    # ------------------------------------------------ registration / mode
    _r5_mode = False   # set by setup_task before register (v1 default)

    async def setup_task(self, task) -> None:
        d = str(getattr(getattr(task, "data", None), "difficulty", ""))
        self._r5_mode = d.startswith("BLOB2v2")

    def register(self, mcp) -> None:
        """Advertise exactly one surface: the frozen v1 tool set for v1
        tags, the round-5 tool set for BLOB2v2 tags. Name collisions
        (status/wait/adjust/inject/submit) resolve by the mode filter."""
        from verifiers.v1.utils.decorators import discover_decorated
        want = V2_TOOL_NAMES if self._r5_mode else V1_TOOL_NAMES
        for fn in discover_decorated(self, "tool"):
            name = getattr(fn, "tool_name", None) or fn.__name__
            if bool(getattr(fn, "_r5_tool", False)) != self._r5_mode:
                continue
            if name not in want:
                continue
            mcp.add_tool(
                self._with_state(fn),
                name=name,
                description=(fn.__doc__ or "").strip() or None,
            )


def _active_salt() -> str:
    """Instance salt used by the reveal/scoring surface. Overridable by the
    reveal-leak gate (G-R1) to prove the Phase-A surface is byte-identical
    under an instance redraw."""
    from physim import blobround5 as R5
    return getattr(R5, "ACTIVE_SALT", R5.INSTANCE_SALT)



class BlobToolset(Blob5Mixin,
                  vf.Toolset[BlobToolsetConfig, BlobToolState]):
    TOOL_PREFIX = "probe"

    # ------------------------------------------------------------ internals
    def _ready(self) -> bool:
        return bool(self.state.world)

    def _ensure(self):
        st = self.state
        if not st.poses:
            sec = B.get_secrets(st.world, st.seed)
            st.poses = [[*sec["devices"][i]["center"], 1.0]
                        for i in range(len(B.ROSTER))]
        if not st.spent:
            st.spent = dict(sensor=0.0, adjust=0.0, injection=0.0)

    def _devices(self):
        st = self.state
        return [B.make_device(st.world, st.seed, i, center=st.poses[i][:2],
                              dilation=st.poses[i][2])
                for i in range(len(B.ROSTER))]

    def _left(self, key: str) -> float:
        return B.BUDGETS[key] - self.state.spent.get(key, 0.0)

    def _budget(self) -> dict:
        return {k: round(self._left(k), 1) for k in B.BUDGETS}

    @staticmethod
    def _parse_devices(devices) -> list[int]:
        if devices in ("all", None, ""):
            return [0, 1]
        if isinstance(devices, str):
            try:
                devices = json.loads(devices)
            except json.JSONDecodeError:
                return []
        if isinstance(devices, (int, float)):
            devices = [int(devices)]
        try:
            out = sorted({int(d) for d in devices})
        except (TypeError, ValueError):
            return []
        return [d for d in out if d in (0, 1)]

    def _k_of(self, dev_ids) -> int:
        ks = [len(B.agdev.lattice_offsets(B.ROSTER[i]["lattice"],
                                          B.ROSTER[i]["n_rings"]))
              for i in dev_ids]
        return int(sum(ks))

    def _sample_devices(self, i_ctrl: int, dev_ids, devs=None):
        st = self.state
        devs = devs or self._devices()
        return {i: B.sample_at(st.world, st.seed, i_ctrl, devs[i])
                for i in dev_ids}

    def _err(self, msg: str, **extra) -> str:
        out = {"error": msg, "t": self.state.i_ctrl * B.CTRL_TU,
               "budget": self._budget() if self.state.spent else None}
        out.update(extra)
        return json.dumps(out)

    # ----------------------------------------------------------------- tools
    @vf.tool(name="status")
    async def status(self) -> str:
        """Report episode time, budgets, interface counts, phase, announced
        contracts, injection pricing, and submission/lock state."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure()
        st = self.state
        st.turns += 1
        if st.round2:
            from physim import blobround2 as R2
            cc = R2.contracts2(st.world, st.seed, st.round2)["public"]
        else:
            cc = B.contracts(st.world, st.seed)["public"]
        nf = B.n_ports(st.world, st.seed)
        devs = self._devices()
        at_t0 = st.i_ctrl >= B.N_STEPS_MAIN
        return json.dumps(dict(
            t=st.i_ctrl * B.CTRL_TU,
            t_end_of_span=B.T0,
            phase=("replica_experiments" if at_t0 else "exploration"),
            step_tu=B.CTRL_TU,
            n_devices=len(devs),
            ports=nf,
            slots_per_device=[d.k for d in devs],
            n_actuator_channels=3,
            budget=self._budget(),
            costs=dict(
                sensor="slots_per_device[d] * 5 per read step per device",
                adjust="|u1|+|u2|+|u3| per adjust step",
                injection="amp*(1+4*max(0,amp-0.5)) per tu of emission",
            ),
            caps=dict(amp_max=B.AMP_CAP, amp_min=B.AMP_MIN,
                      dur_max=B.DUR_CAP, u_max=1.0,
                      replicas_left=B.MAX_REPLICAS - st.n_replicas),
            emission=("all emissions — yours and the announced protocol — "
                      "enter through the same fixed emission channel; where "
                      "and what it couples to is undisclosed"),
            contracts=cc,
            locked_p1p2=st.locked_p1p2,
            submitted=(
                {c: bool((st.subs2 or {}).get(c)) for c in cc["menu"]}
                if st.round2 else
                dict(P1=bool(st.sub_p1), P2=bool(st.sub_p2),
                     P3=bool(st.sub_p3))),
            notes=[
                "the main span replays a fixed trajectory to t_end_of_span "
                "and stops there; nothing after it is observable directly",
                "probe_inject only works once t = t_end_of_span; each call "
                "forks a fresh replica of the world from that instant",
                ("the first probe_inject locks these contracts (forecasts "
                 "issued from span information only): "
                 + ", ".join(c for c in cc["menu"]
                             if c in ("L1", "L2", "L3F", "L3E", "L3S"))
                 if st.round2 else
                 "the first probe_inject locks P1 and P2 (they are "
                 "forecasts issued from span information only)"),
                "contract truths are evaluated with each device at its "
                "t=0 configuration (as if you never adjusted it); your "
                "accepted probe_adjust commands are your only record of "
                "what you changed",
            ],
        ))

    @vf.tool(name="read_streams")
    async def read_streams(self, window: int = 1, devices="all",
                           ports="all", stride: int = 1,
                           include_global: bool = True) -> str:
        """Advance up to `window` 5tu steps on the main span, reading the
        selected devices' sensor streams every `stride`-th step (each read
        step costs slots*5 sensor per device read). ports filters returned
        ports (no cost change). Returns per-read-step values[device][port]
        [slot] plus free per-port global mean/var at the last step."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure()
        st = self.state
        st.turns += 1
        window = int(window)
        stride = max(int(stride), 1)
        if window < 1:
            return self._err("window must be >= 1")
        left_steps = B.N_STEPS_MAIN - st.i_ctrl
        if left_steps <= 0:
            return self._err(
                "the span has ended (t = t_end_of_span); reads now only "
                "happen inside probe_inject replicas")
        window = min(window, left_steps)
        dev_ids = self._parse_devices(devices)
        if not dev_ids:
            return self._err("devices must be 'all' or a list of device ids")
        nf = B.n_ports(st.world, st.seed)
        if ports in ("all", None, ""):
            port_ids = list(range(nf))
        else:
            if isinstance(ports, str):
                try:
                    ports = json.loads(ports)
                except json.JSONDecodeError:
                    return self._err("ports must be 'all' or a list")
            try:
                port_ids = [int(x) for x in ports]
            except (TypeError, ValueError):
                return self._err("ports must be 'all' or a list of ints")
            if any(x < 0 or x >= nf for x in port_ids):
                return self._err(f"port ids must be in [0, {nf - 1}]")
        read_steps = list(range(stride - 1, window, stride))
        k_read = self._k_of(dev_ids)
        cost = len(read_steps) * k_read * B.CTRL_TU
        n_numbers = len(read_steps) * len(port_ids) * k_read
        if n_numbers > 60000:
            return self._err(
                f"response too large ({n_numbers} numbers > 60000); lower "
                "window, raise stride, or filter ports/devices")
        if cost > self._left("sensor") + 1e-9:
            return self._err(
                f"sensor budget too low for this read (cost {cost:.0f}, "
                f"left {self._left('sensor'):.0f}); use probe_wait or "
                "reduce the read")
        st.spent["sensor"] = st.spent.get("sensor", 0.0) + cost
        devs = self._devices()
        out_steps = []
        for j in range(window):
            st.i_ctrl += 1
            if j in read_steps:
                sm = self._sample_devices(st.i_ctrl, dev_ids, devs)
                out_steps.append(dict(
                    t=st.i_ctrl * B.CTRL_TU,
                    values={str(i): _r(sm[i][port_ids]) for i in dev_ids}))
        resp = dict(t=st.i_ctrl * B.CTRL_TU, steps=out_steps,
                    ports=port_ids, sensor_cost=round(cost, 1),
                    budget=self._budget())
        if include_global:
            resp["global_stats"] = _r(
                B.global_stats(st.world, st.seed, st.i_ctrl))
        return json.dumps(resp)

    @vf.tool(name="wait")
    async def wait(self, steps: int = 1) -> str:
        """Advance up to `steps` 5tu steps on the main span without reading
        (no sensor cost). Returns the new time and free global stats."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure()
        st = self.state
        st.turns += 1
        steps = int(steps)
        if steps < 1:
            return self._err("steps must be >= 1")
        left_steps = B.N_STEPS_MAIN - st.i_ctrl
        if left_steps <= 0:
            return self._err("the span has ended (t = t_end_of_span)")
        steps = min(steps, left_steps)
        st.i_ctrl += steps
        return json.dumps(dict(
            t=st.i_ctrl * B.CTRL_TU,
            at_end_of_span=bool(st.i_ctrl >= B.N_STEPS_MAIN),
            global_stats=_r(B.global_stats(st.world, st.seed, st.i_ctrl)),
            budget=self._budget()))

    @vf.tool(name="adjust")
    async def adjust(self, device: int, u1: float, u2: float, u3: float,
                     steps: int = 1, read: bool = True) -> str:
        """Apply the 3-channel actuator (u1, u2, u3) to one device for
        `steps` 5tu steps. Each u is clipped to [-1, 1]; cost |u1|+|u2|+|u3|
        per step from the adjust budget. What the channels do to the device
        is fixed for the whole episode but undisclosed — discovering it is
        part of the task. The actuator may refuse a step (the response marks
        it "adjust_rejected", steps after it do not run); a refused step
        still costs its commanded effort. read=True samples the device after
        each completed step (costed). Only works on the main span."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure()
        st = self.state
        st.turns += 1
        try:
            device = int(device)
            u = np.clip([float(u1), float(u2), float(u3)], -1.0, 1.0)
            steps = int(steps)
        except (TypeError, ValueError):
            return self._err("device, u1, u2, u3, steps must be numeric")
        if device not in (0, 1):
            return self._err("device must be 0 or 1")
        if steps < 1:
            return self._err("steps must be >= 1")
        left_steps = B.N_STEPS_MAIN - st.i_ctrl
        if left_steps <= 0:
            return self._err("the span has ended; devices are parked")
        steps = min(steps, left_steps)
        adj_per_step = float(np.abs(u).sum())
        if adj_per_step * steps > self._left("adjust") + 1e-9:
            return self._err(
                f"adjust budget too low (cost {adj_per_step * steps:.1f}, "
                f"left {self._left('adjust'):.1f})")
        k_dev = self._k_of([device])
        read_per_step = k_dev * B.CTRL_TU if read else 0.0
        if read and read_per_step * steps > self._left("sensor") + 1e-9:
            read = False
            read_per_step = 0.0
        dev = self._devices()[device]
        M = np.asarray(B.get_secrets(st.world, st.seed)["adjust_mix"],
                       float)
        delta = M @ u                     # (dy, dx, dlog_spacing) per step
        out_steps = []
        applied = 0
        rejected = False
        charge = 0.0
        sensor_charge = 0.0
        for _ in range(steps):
            new_dil = dev.dilation * float(np.exp(delta[2]))
            if not (dev.dil_bounds[0] - 1e-12 <= new_dil
                    <= dev.dil_bounds[1] + 1e-12):
                # actuator refusal (R3-final: only u3/dlog can strike the
                # spacing bounds — pure-translation commands never land
                # here since delta[2] == 0). The whole step is the unit:
                # commanded translation in a refused step does not apply
                # either. Strain charge for the commanded effort; remaining
                # steps do not run and are not charged.
                rejected = True
                charge += adj_per_step
                break
            dev.center = (dev.center + delta[:2]) % dev.L
            dev.dilation = new_dil
            charge += adj_per_step
            applied += 1
            st.i_ctrl += 1
            if read:
                sensor_charge += read_per_step
                v = B.sample_at(st.world, st.seed, st.i_ctrl, dev)
                out_steps.append(dict(t=st.i_ctrl * B.CTRL_TU,
                                      values=_r(v)))
        st.spent["adjust"] = st.spent.get("adjust", 0.0) + charge
        st.spent["sensor"] = st.spent.get("sensor", 0.0) + sensor_charge
        st.poses[device] = [float(dev.center[0]), float(dev.center[1]),
                            float(dev.dilation)]
        return json.dumps(dict(
            t=st.i_ctrl * B.CTRL_TU, applied=[float(x) for x in u],
            steps_requested=steps, steps_applied=applied,
            result=("adjust_rejected" if rejected else "ok"),
            device=device,
            adjust_cost=round(charge, 2),
            sensor_cost=round(sensor_charge, 1),
            steps_read=out_steps, budget=self._budget()))

    @vf.tool(name="inject")
    async def inject(self, port: int, amp: float, dur: float,
                     lags="all", devices="all", ports="all") -> str:
        """Run ONE replica experiment: fork the world at t_end_of_span,
        drive the fixed emission channel with (port, amp) for `dur` tu, and
        read the selected devices at the requested lags (list of tu after
        the fork, multiples of 5, max 250; 'all' = the 13 announced P3
        lags). Where and what the emission channel couples to is
        undisclosed. Costs: injection amp*(1+4*max(0,amp-0.5))*dur + sensor
        slots*5 per lag per device. amp in [0.05, 1.0], or amp=0 for an
        emission-free CONTROL replica (sensor cost only). Requires
        t = t_end_of_span; the first call locks P1/P2. Replicas are
        independent forks: same start state, same world noise stream."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure()
        st = self.state
        st.turns += 1
        nf = B.n_ports(st.world, st.seed)
        try:
            port = int(port)
            amp = float(amp)
            dur = float(dur)
        except (TypeError, ValueError):
            return self._err("port, amp, dur must be numeric")
        if st.i_ctrl < B.N_STEPS_MAIN:
            return self._err(
                "probe_inject only works at t_end_of_span; advance the "
                f"span first ({(B.N_STEPS_MAIN - st.i_ctrl)} steps left, "
                "probe_wait is free)")
        if st.n_replicas >= B.MAX_REPLICAS:
            return self._err("replica limit reached")
        if port < 0 or port >= nf:
            return self._err(f"port must be in [0, {nf - 1}]")
        if amp != 0.0 and not (B.AMP_MIN <= amp <= B.AMP_CAP):
            return self._err(
                f"amp must be 0 (control) or in [{B.AMP_MIN}, {B.AMP_CAP}]"
                " — the apparatus cannot emit stronger; calibrate and "
                "extrapolate")
        if not (0.0 < dur <= B.DUR_CAP):
            return self._err(f"dur must be in (0, {B.DUR_CAP}] tu")
        dur = round(dur / B.CTRL_TU) * B.CTRL_TU
        dur = float(np.clip(dur, B.CTRL_TU, B.DUR_CAP))
        if lags in ("all", None, ""):
            lag_list = [float(x) for x in B.P3_LAGS]
        else:
            if isinstance(lags, str):
                try:
                    lags = json.loads(lags)
                except json.JSONDecodeError:
                    return self._err("lags must be 'all' or a list of tu")
            try:
                lag_list = sorted({float(x) for x in lags})
            except (TypeError, ValueError):
                return self._err("lags must be 'all' or a list of tu")
        if not lag_list:
            return self._err("need at least one lag")
        if any(x < B.CTRL_TU - 1e-9 or x > B.T_REPLICA + 1e-9
               or abs(x / B.CTRL_TU - round(x / B.CTRL_TU)) > 1e-6
               for x in lag_list):
            return self._err(
                f"lags must be multiples of {B.CTRL_TU:g} in "
                f"[{B.CTRL_TU:g}, {B.T_REPLICA:g}]")
        dev_ids = self._parse_devices(devices)
        if not dev_ids:
            return self._err("devices must be 'all' or a list of device ids")
        if ports in ("all", None, ""):
            port_ids = list(range(nf))
        else:
            if isinstance(ports, str):
                try:
                    ports = json.loads(ports)
                except json.JSONDecodeError:
                    return self._err("ports must be 'all' or a list")
            try:
                port_ids = [int(x) for x in ports]
            except (TypeError, ValueError):
                return self._err("ports must be 'all' or a list of ints")
            if any(x < 0 or x >= nf for x in port_ids):
                return self._err(f"port ids must be in [0, {nf - 1}]")
        inj_cost = B.inj_price(amp) * dur
        k_read = self._k_of(dev_ids)
        sensor_cost = len(lag_list) * k_read * B.CTRL_TU
        if inj_cost > self._left("injection") + 1e-9:
            return self._err(
                f"injection budget too low (cost {inj_cost:.1f}, left "
                f"{self._left('injection'):.1f})")
        if sensor_cost > self._left("sensor") + 1e-9:
            return self._err(
                f"sensor budget too low for the replica reads (cost "
                f"{sensor_cost:.0f}, left {self._left('sensor'):.0f})")
        n_numbers = len(lag_list) * len(port_ids) * k_read
        if n_numbers > 60000:
            return self._err(
                f"response too large ({n_numbers} numbers); fewer lags or "
                "filtered ports/devices")
        st.spent["injection"] = st.spent.get("injection", 0.0) + inj_cost
        st.spent["sensor"] = st.spent.get("sensor", 0.0) + sensor_cost
        st.n_replicas += 1
        st.locked_p1p2 = True
        st.replica_log = list(st.replica_log) + [dict(
            port=port, amp=amp, dur=dur, n_lags=len(lag_list))]
        n_ctrl = int(round(max(lag_list) / B.CTRL_TU))
        frames = B.replica_frames(st.world, st.seed, port, amp, dur, n_ctrl)
        perm = np.asarray(B.get_secrets(st.world, st.seed)["port_perm"],
                          int)
        dx = B.get_cached(st.world, st.seed).meta["dx"]
        devs = self._devices()
        reads = []
        for lag in lag_list:
            i = int(round(lag / B.CTRL_TU))
            f = frames[i][perm]
            reads.append(dict(
                lag=lag,
                values={str(d): _r(devs[d].sample(f, dx)[port_ids])
                        for d in dev_ids},
                global_stats=_r(np.stack([f.mean(axis=(1, 2)),
                                          f.var(axis=(1, 2))], axis=1))))
        return json.dumps(dict(
            replica=st.n_replicas, port=port, amp=amp, dur=dur,
            injection_cost=round(inj_cost, 2),
            sensor_cost=round(sensor_cost, 1),
            ports=port_ids, reads=reads,
            replicas_left=B.MAX_REPLICAS - st.n_replicas,
            locked_p1p2=True, budget=self._budget()))

    @vf.tool(name="submit")
    async def submit(self, contract: str, payload) -> str:
        """Submit or revise one contract payload (ids and required shapes:
        see probe_status contracts). payload = {"mean": nested list in the
        contract's shape, "sigma": scalar or same-shape list} (sigma = your
        predictive sd; scoring is CRPS-based, so honest spread beats
        overconfidence). Forecast contracts lock at the first probe_inject;
        emission contracts stay open. The LAST accepted submission per
        contract scores."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure()
        st = self.state
        st.turns += 1
        c = str(contract).strip().upper()
        if isinstance(payload, str):
            js = payload
        else:
            try:
                js = json.dumps(payload)
            except (TypeError, ValueError):
                return self._err("payload not JSON-serializable")
        if st.round2:
            from physim import blobround2 as R2
            menu = R2.MENUS[st.round2]
            if c not in menu:
                return self._err(
                    "contract must be one of " + ", ".join(menu))
            if st.locked_p1p2 and c in R2.LOCK_AT_INJECT:
                return self._err(
                    f"{c} is locked (forecasts must be issued before the "
                    "first probe_inject)")
            shape = R2.payload_shapes2(st.world, st.seed, st.round2)[c]
            parsed, why = B._parse_payload(js, shape)
            if parsed is None:
                return self._err(f"rejected: {why}",
                                 required_shape=list(shape))
            st.subs2 = {**(st.subs2 or {}), c: js}
            return json.dumps(dict(
                ok=True, contract=c, shape=list(shape),
                note="recorded; scored after the episode ends; "
                     "resubmission replaces", budget=self._budget()))
        if c not in ("P1", "P2", "P3"):
            return self._err("contract must be one of P1, P2, P3")
        if st.locked_p1p2 and c in ("P1", "P2"):
            return self._err(
                f"{c} is locked (forecasts must be issued before the first "
                "probe_inject)")
        shape = B.payload_shapes(st.world, st.seed)[c]
        parsed, why = B._parse_payload(js, shape)
        if parsed is None:
            return self._err(f"rejected: {why}",
                             required_shape=list(shape))
        setattr(st, f"sub_{c.lower()}", js)
        return json.dumps(dict(
            ok=True, contract=c, shape=list(shape),
            note="recorded; scored after the episode ends; resubmission "
                 "replaces", budget=self._budget()))


if __name__ == "__main__":
    BlobToolset.run()
