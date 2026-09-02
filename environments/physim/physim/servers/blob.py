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
  probe_adjust(device, u1, u2, u3)   3-channel actuator (costed; per-world
                                     secret linear mix — R2: the control
                                     factorization itself is undisclosed)
  probe_inject(port, amp, dur, ...)  ONLY at the end of the span: fork a
                                     live replica with the agent's emission
                                     at the fixed emitter; returns replica
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


class BlobToolset(vf.Toolset[BlobToolsetConfig, BlobToolState]):
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
            submitted=dict(P1=bool(st.sub_p1), P2=bool(st.sub_p2),
                           P3=bool(st.sub_p3)),
            notes=[
                "the main span replays a fixed trajectory to t_end_of_span "
                "and stops there; nothing after it is observable directly",
                "probe_inject only works once t = t_end_of_span; each call "
                "forks a fresh replica of the world from that instant",
                "the first probe_inject locks P1 and P2 (they are forecasts "
                "issued from span information only)",
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
                # actuator refusal: the step does not apply (its translation
                # component included — entanglement intended); strain charge
                # for the commanded effort; remaining steps do not run and
                # are not charged.
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
        """Submit or revise one contract payload. contract in {'P1','P2',
        'P3'}. payload = {"mean": nested list in the contract's shape,
        "sigma": scalar or same-shape list} (sigma = your predictive sd;
        scoring is CRPS, so honest spread beats overconfidence). Shapes:
        P1 [n_horizons][ports][slots_A], P2 [n_windows], P3 [n_lags][ports]
        [slots_B]. P1/P2 lock at the first probe_inject; P3 stays open.
        The LAST accepted submission per contract scores."""
        if not self._ready():
            return json.dumps({"error": "world not initialized; retry"})
        self._ensure()
        st = self.state
        st.turns += 1
        c = str(contract).strip().upper()
        if c not in ("P1", "P2", "P3"):
            return self._err("contract must be one of P1, P2, P3")
        if st.locked_p1p2 and c in ("P1", "P2"):
            return self._err(
                f"{c} is locked (forecasts must be issued before the first "
                "probe_inject)")
        if isinstance(payload, str):
            js = payload
        else:
            try:
                js = json.dumps(payload)
            except (TypeError, ValueError):
                return self._err("payload not JSON-serializable")
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
