"""smoke_blob2v2.py — round-5 scripted actor (spec PART 5). EVALUATOR-side
driver, AGENT-side policy: speaks ONLY through the round-5 tool functions.

Two-phase play. Phase A is a GENERIC fixed calibration program (no adaptive
timing, no fork-ensembling, no domain sweeps):
  record   burst-read the FULL base record (duty ~0.45, window 5 / gap 6)
           on both roster devices + the free global stats; persist the log
           to files (Phase B has no re-reads).
  adjust   a brief per-channel calibration walk inside a throwaway fork
           (exercises the tool + meter; its data is deliberately unused —
           the L1 policy below is law-ignorant BY POLICY).
  inject   one control fork + calibration injections PER PORT (amps
           0.3/0.6/1.0, dur 10) read on the 5tu lag grid covering
           [5, 250]; fit a per-(port, lag) linear-in-amp template; keep
           residuals.
  ready    probe_ready() right after the fixed program — deliberately
           early; its time-to-ready is the reference point on that Pareto
           axis.
Phase B: classical statistics evaluated at the revealed instances from the
actor's own pre-reveal record:
  L1   nearest logged device-0 reading at/before t_a + drift-inflated
       sigma (NO actuator model: L1 prices exactly the capability this
       reference refuses to have; expect |skill| ~ 0).
  L2   per-port global mean at t_a + spatial-spread sigma.
  L3F  AR(2)/climatology blend fit on the logged pre-t_a history of the
       revealed device.
  L3E/L3S  the v1 estimators windowed to logged pre-t_a data.
  L4/L4D   the template at the revealed (port, lags), scaled linearly in
       amp and first-order in dur; sigma = fit residual inflated by the
       scale factor.

Run (repo root):
  .venv/bin/python environments/physim/tools/smoke_blob2v2.py --world E1 --seed-idx 0
  .venv/bin/python environments/physim/tools/smoke_blob2v2.py --all
Writes probes/blobs/agentenv/results/smoke_blob2v2_{tag}_s{seed}.json
(+ smoke_blob2v2_aggregate.json with --all / --aggregate).
"""
import argparse
import asyncio
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "environments", "physim"))

from physim import blobcore as B                     # noqa: E402
from physim import blobround5 as R5                  # noqa: E402
from physim.blobstate import BlobToolState           # noqa: E402
from physim.servers import blob as S                 # noqa: E402

sys.path.insert(0, B.AGENTENV)
import refpipes as R                                 # noqa: E402

WORLDS = dict(E1=("p4g2_044", (928, 929, 930), "E1", "BLOB2v2-E1"),
              E2=("p6g8_033", (942, 943, 944), "E2", "BLOB2v2-E2"))

CAL_T = 1500.0            # calibration fork anchor (generic constant)
CAL_AMPS = (0.3, 0.6, 1.0)
CAL_DUR = 10.0
LOG_DIR = os.path.join(B.AGENTENV, "results", "actor_logs")


class Agent5:
    """The scripted reference. All world access via tool calls; everything
    it knows in Phase B lives in self.* (persisted to its log file)."""

    def __init__(self, ts):
        self.ts = ts
        self.t, self.v0, self.v1 = [], [], []
        self.gt, self.glob = [], []
        self.template = {}
        self.resid = {}
        self.dose_p = {}
        self.per_amp = {}
        self.ctrl = {}
        self.nf = None

    async def call(self, fn, **kw):
        out = json.loads(await fn(**kw))
        if "error" in out:
            raise RuntimeError(f"tool error: {out['error']} ({kw})")
        return out

    # ------------------------------------------------------------- phase A
    async def record(self, chunk=10):
        """Full-rate base-record read (both devices, every 5tu step).
        v2 has no budgets — the record is the portable artifact Phase B
        answers from, and the L1/L3E floor gates need rung-grade freshness
        (<=5tu staleness at any anchor). Meters stay far under caps
        (~80k node-tu sensor vs the 1M safety cap)."""
        st = await self.call(self.ts.status5)
        self.status = st
        self.nf = st["ports"]
        n_steps = int(round(st["T_BASE"] / st["step_tu"]))
        i = 0
        while i < n_steps:
            take = min(chunk, n_steps - i)
            r = await self.call(self.ts.read5, ctx="base", window=take,
                                devices="all", include_global=True)
            for stp in r["steps"]:
                self.t.append(stp["t"])
                self.v0.append(np.asarray(stp["values"]["0"], float))
                self.v1.append(np.asarray(stp["values"]["1"], float))
            self.gt.append(r["t"])
            self.glob.append(np.asarray(r["global_stats"], float))
            i += take

    async def adjust_bullet(self):
        f = await self.call(self.ts.fork5, t=800.0)
        fid = f["fork"]
        for ch in range(3):
            u = [0.0, 0.0, 0.0]
            u[ch] = 0.5 if ch < 2 else -0.3
            await self.call(self.ts.adjust5, device=0, u1=u[0], u2=u[1],
                            u3=u[2], ctx=fid, steps=1, read=True)
        await self.call(self.ts.reset5, fork=fid)

    async def calibrate(self):
        lag_steps = 50                              # 5tu grid to 250tu
        f = await self.call(self.ts.fork5, t=CAL_T)
        r = await self.call(self.ts.read5, ctx=f["fork"], window=lag_steps,
                            devices=[1], include_global=False)
        self.ctrl = {round(stp["t"] - CAL_T, 1):
                     np.asarray(stp["values"]["1"], float)
                     for stp in r["steps"]}
        await self.call(self.ts.reset5, fork=f["fork"])
        lags = sorted(self.ctrl)
        # baseline for response deltas: average of the control fork and the
        # base record at the same times (two independent realizations of
        # the undisturbed field -> ~sqrt(2) less baseline noise)
        self.base_ctrl = {}
        for lg in lags:
            i = self._last_idx(CAL_T + lg)
            self.base_ctrl[lg] = 0.5 * (self.ctrl[lg] + self.v1[i])
        for port in range(self.nf):
            per_amp = []
            for amp in CAL_AMPS:
                f = await self.call(self.ts.fork5, t=CAL_T)
                await self.call(self.ts.inject5, ctx=f["fork"], port=port,
                                amp=amp, dur=CAL_DUR)
                r = await self.call(self.ts.read5, ctx=f["fork"],
                                    window=lag_steps, devices=[1],
                                    include_global=False)
                A = {round(stp["t"] - CAL_T, 1):
                     np.asarray(stp["values"]["1"], float)
                     for stp in r["steps"]}
                await self.call(self.ts.reset5, fork=f["fork"])
                per_amp.append((amp, {lg: A[lg] - self.base_ctrl[lg]
                                      for lg in lags}))
            self.per_amp[port] = per_amp
            # least-squares through the origin: T = sum(a*D)/sum(a^2)
            # (weights the high-SNR amps; mean(D/a) would upweight the
            # noisiest low-amp run)
            ssq = sum(a * a for a, _ in per_amp)
            self.template[port] = {
                lg: sum(a * d[lg] for a, d in per_amp) / ssq for lg in lags}
            rms_a = np.sqrt(ssq / len(per_amp))
            self.resid[port] = {
                lg: np.sqrt(np.mean(
                    [(d[lg] - a * self.template[port][lg]) ** 2
                     for a, d in per_amp], axis=0)) / rms_a for lg in lags}
            # dose-law exponent per lag: project each amp's delta onto the
            # amp-1.0 response shape, fit log(gain) ~ p*log(amp). p<1 =
            # saturating response — the classical in-range calibration of
            # the dose LAW that L4 extrapolation is priced on. p clipped to
            # [0, 1.15]; weak responses fall back to p=1 (masked anyway).
            self.dose_p[port] = {}
            ref = {lg: per_amp[-1][1][lg] for lg in lags}
            for lg in lags:
                R2ref = float((ref[lg] ** 2).sum()) + 1e-12
                num = den = 0.0
                usable = True
                for a, d in per_amp[:-1]:
                    g = float((d[lg] * ref[lg]).sum()) / R2ref
                    if g < 0.02:
                        usable = False
                        break
                    num += np.log(a) * np.log(g)
                    den += np.log(a) ** 2
                self.dose_p[port][lg] = float(np.clip(num / den, 0.0, 1.15)) \
                    if (usable and den > 0) else 1.0

    def persist(self, tag):
        os.makedirs(LOG_DIR, exist_ok=True)
        np.savez_compressed(
            os.path.join(LOG_DIR, f"{tag}.npz"),
            t=np.asarray(self.t), v0=np.stack(self.v0),
            v1=np.stack(self.v1), gt=np.asarray(self.gt),
            glob=np.stack(self.glob),
            template=json.dumps({p: {lg: T.tolist() for lg, T in d.items()}
                                 for p, d in self.template.items()}),
            dose_p=json.dumps(self.dose_p),
            per_amp=json.dumps({p: [[a, {lg: dd.tolist()
                                         for lg, dd in d.items()}]
                                    for a, d in pa]
                                for p, pa in self.per_amp.items()}))

    # ------------------------------------------------------------- phase B
    def _last_idx(self, t_a):
        t = np.asarray(self.t)
        idx = np.searchsorted(t, t_a + 1e-9) - 1
        return max(int(idx), 0)

    def _step_sigma(self, M):
        """Per-channel rms of one-step diffs inside bursts (5tu apart)."""
        t = np.asarray(self.t)
        D = np.diff(np.stack(M), axis=0)
        ok = np.diff(t) <= 5.0 + 1e-9
        return np.sqrt(np.mean(D[ok] ** 2, axis=0)) + 1e-4

    def p_l1(self, inst):
        """Law-ignorant BY POLICY: nearest logged reading + drift-inflated
        sigma. The read is stale (log duty < 1) and the hidden command walk
        re-poses the device, so the honest classical spread is the
        climatology sd floored under a staleness-drift term — anything
        tighter is overconfidence against a hidden-pose truth."""
        i = self._last_idx(inst["anchor_t"])
        t_read = inst["anchor_t"] + 5.0 * len(inst["sequence"])
        gap = max((t_read - self.t[i]) / 5.0, 1.0)
        drift = self._step_sigma(self.v0) * np.sqrt(gap) * 1.5
        M0 = np.stack(self.v0)
        clim_sd = M0.std(0) + 1e-3
        return dict(mean=self.v0[i].tolist(),
                    sigma=np.maximum(drift, clim_sd).tolist())

    def p_l2(self, inst):
        t_a = inst["anchor_t"]
        gi = int(np.searchsorted(np.asarray(self.gt), t_a + 1e-9) - 1)
        gi = max(gi, 0)
        g = self.glob[gi]
        kh = inst["payload_shape"][1]
        mu = np.repeat(g[:, 0][:, None], kh, axis=1)
        i = self._last_idx(t_a)
        own = np.stack(self.v0[max(i - 12, 0):i + 1])
        slot_sd = own.std(axis=(0, 2))
        sig = np.maximum(slot_sd[:, None], np.sqrt(g[:, 1])[:, None])
        sig = np.repeat(sig, kh, axis=1) + 1e-3
        return dict(mean=mu.tolist(), sigma=sig.tolist())

    def p_l3f(self, inst):
        t_a = inst["anchor_t"]
        Hs = np.asarray(inst["horizons"], float)
        V = self.v0 if inst["device"] == 0 else self.v1
        i = self._last_idx(t_a)
        M = np.stack(V[:i + 1])
        Tn = M.shape[0]
        flat = M.reshape(Tn, -1)
        clim_mu, clim_sd = flat.mean(0), flat.std(0) + 1e-3
        t_last = self.t[i]
        mu, sig = [], []
        for H in Hs:
            n = max(int(round((t_a + H - t_last) / 5.0)), 1)
            ar = R._ar2_forecast(flat, n)
            w = float(np.exp(-H / 100.0))
            mu.append(w * ar + (1 - w) * clim_mu)
            sig.append(np.maximum(clim_sd * (1.0 - 0.5 * w), 1e-3))
        shp = (len(Hs),) + M.shape[1:]
        return dict(mean=np.stack(mu).reshape(shp).tolist(),
                    sigma=np.stack(sig).reshape(shp).tolist())

    def p_l3e(self, inst):
        t_a = inst["anchor_t"]
        pt, thr, sgn = inst["port"], inst["thr"], float(inst["sign"])
        i = self._last_idx(t_a)
        M = np.stack(self.v0[:i + 1])[:, pt, :] * sgn
        t = np.asarray(self.t[:i + 1])
        win = float(inst["window_tu"])
        fpw = max(int(round(win / 5.0)), 1)
        x = M > thr
        up = (~x[:-1] & x[1:]).sum(axis=1)
        consec = np.diff(t) <= 5.0 + 1e-9
        up = up * consec
        edges = np.arange(t[0], t[-1] + win, win)
        rates = []
        for w0, w1 in zip(edges[:-1], edges[1:]):
            sel = (t[:-1] >= w0) & (t[:-1] < w1)
            n_pairs = int((sel & consec).sum())
            rates.append(up[sel].sum() * fpw / n_pairs if n_pairs else
                         np.nan)
        rates = np.asarray(rates, float)
        valid = rates[np.isfinite(rates)]
        n_win = inst["n_windows"]
        # constant pre-anchor mean rate (no trend extrapolation: 800tu of
        # extrapolated slope from a windowed sample is not a classical
        # reference play and can blow past the floor on early anchors)
        rate = float(valid.mean()) if len(valid) else 0.0
        sig = float(valid.std() + 0.5) if len(valid) >= 3 else 1.5
        return dict(mean=np.full(n_win, rate).tolist(), sigma=sig)

    def p_l3s(self, inst):
        t_a = inst["anchor_t"]
        gt = np.asarray(self.gt)
        gi = int(np.searchsorted(gt, t_a + 1e-9))
        G = np.stack(self.glob[:max(gi, 2)])
        w_sel = gt[:max(gi, 2)] >= t_a - 200.0
        mu1 = G[w_sel].mean(0) if w_sel.any() else G[-4:].mean(0)
        n_ep = len(inst["epochs"])
        mu = np.tile(mu1[None], (n_ep, 1, 1))
        sd = G.std(0) * 1.5 + 1e-4
        sig = np.tile(sd[None], (n_ep, 1, 1))
        return dict(mean=mu.tolist(), sigma=sig.tolist())

    def p_l4(self, inst):
        """Template at the revealed (port, lags): least-squares linear-in-
        amp shape, dose-law exponent p fit from the in-range calibration
        (resp ~ T * (amp*dur/10)^p), with classical safeguards validated
        against the frozen truth offline:
        (a) significance shrinkage — entries below 2x their fit residual
            contribute spread, not mean;
        (b) dose-trust fade — full trust of the calibrated law up to 2x the
            calibrated dose, fading to a base-record answer by 4x (beyond
            the validated range the prior wins; the not-taken response
            moves into sigma);
        (c) extrapolation widening for the p-vs-linear ambiguity."""
        t_a, port = inst["anchor_t"], inst["port"]
        amp, dur = float(inst["amp"]), float(inst["dur_tu"])
        scale = amp * (dur / CAL_DUR)
        wgt = float(np.clip((4.0 - scale) / 2.0, 0.0, 1.0))
        lags = [float(x) for x in inst["lags"]]
        M1 = np.stack(self.v1)
        clim_mu, clim_sd = M1.mean(0), M1.std(0) + 1e-3
        mu, sig = [], []
        for lg in lags:
            t_read = t_a + lg
            if t_read <= self.t[-1] + 1e-9:
                base = self.v1[self._last_idx(t_read)]
            else:
                base = clim_mu
            T = self.template[port][lg]
            Rres = self.resid[port][lg]
            ok = np.abs(T) > 2.0 * Rres
            T_eff = np.where(ok, T, 0.0)
            p = self.dose_p[port][lg]
            se = float(scale ** p)
            resp = T_eff * se
            m = base + wgt * resp
            s_resp = np.where(ok, Rres, np.abs(T)) * se * max(wgt, 0.3)
            s_hedge = (1.0 - wgt) * np.abs(resp)
            s_extrap = np.abs(T_eff) * 0.5 * abs(
                scale ** min(p + 0.15, 1.15) - se) * wgt
            s = np.clip(np.sqrt(s_resp ** 2 + s_hedge ** 2 + s_extrap ** 2),
                        0.004, 3.0 * clim_sd)
            s = np.maximum(s, np.where(np.abs(m - base) > clim_sd,
                                       clim_sd * 0.5, 0.004))
            mu.append(m)
            sig.append(s)
        return dict(mean=np.stack(mu).tolist(),
                    sigma=np.stack(sig).tolist())

    # ---------------------------------------------------------------- play
    async def run(self, tag):
        await self.record()
        await self.adjust_bullet()
        await self.calibrate()
        self.persist(tag)
        rr = await self.call(self.ts.ready5)
        inst = {d["id"].split("@")[0]: d for d in rr["instances"]}
        subs = {"L1": self.p_l1(inst["L1"]), "L2": self.p_l2(inst["L2"]),
                "L3F": self.p_l3f(inst["L3F"])}
        if "L3E" in inst:
            subs["L3E"] = self.p_l3e(inst["L3E"])
        if "L3S" in inst:
            subs["L3S"] = self.p_l3s(inst["L3S"])
        subs["L4"] = self.p_l4(inst["L4"])
        subs["L4D"] = self.p_l4(inst["L4D"])
        for cid, pl in subs.items():
            await self.call(self.ts.submit5, instance=cid,
                            payload=json.dumps(pl))
        return len(self.t)


async def main_one(tag, seed_idx):
    world, seeds, menu, diff = WORLDS[tag]
    seed = seeds[seed_idx]
    t0 = time.time()
    ts = S.BlobToolset(S.BlobToolsetConfig())
    st = BlobToolState()
    st.world, st.seed, st.round5 = world, seed, menu
    ts._inert_state = st
    agent = Agent5(ts)
    n_reads = await agent.run(f"{tag}_s{seed}")
    res = R5.score_episode5(world, seed, menu, dict(st.r5_subs))
    meters = {**st.r5_meters, "fork_spawns": st.r5_fork_seq,
              "open_forks_peak": st.r5_open_peak, "resets": st.r5_n_resets,
              "reads_base": st.r5_reads_base,
              "reads_fork": st.r5_reads_fork, "turns": st.turns}
    out = dict(
        world=world, seed=seed, menu=menu, difficulty=diff,
        reward_skill=round(res["reward_skill"], 4),
        skills={k: round(v, 4) for k, v in res["skills"].items()},
        crps={k.replace("_crps", ""): v for k, v in res["detail"].items()
              if k.endswith("_crps")},
        ladders=res["detail"]["ladders"],
        instances=res["detail"]["instances"],
        meters={k: round(float(v), 2) for k, v in meters.items()},
        cap_hits=dict(st.r5_cap_hits),
        time_to_ready=dict(sim_tu=st.r5_t_ready_sim,
                           turns=st.r5_t_ready_turns),
        n_reads=n_reads,
        wall_s=round(time.time() - t0, 1),
    )
    sk = res["skills"]
    gates = dict(
        all_submitted=all(f"{c.lower()}_error" not in res["detail"]
                          for c in R5.MENUS5[menu]),
        none_at_floor=all(v > -1.0 for v in sk.values()),
        l1_near_floor=bool(abs(sk["L1"]) <= 0.15),
        l4_positive=bool(sk["L4"] > 0.05),
        l4d_positive=bool(sk["L4D"] > 0.05),
        zero_cap_hits=(sum(st.r5_cap_hits.values()) == 0),
    )
    out["gates"] = gates
    out["smoke_pass"] = all(gates.values())
    path = os.path.join(B.AGENTENV, "results",
                        f"smoke_blob2v2_{tag}_s{seed}.json")
    json.dump(out, open(path, "w"), indent=1)
    print(json.dumps(dict(world=world, seed=seed,
                          reward=out["reward_skill"], skills=out["skills"],
                          gates=gates), indent=1))
    print("SMOKE2v2", tag, seed,
          "PASS" if out["smoke_pass"] else "FAIL", "->", path)
    return out["smoke_pass"]


def aggregate():
    rows = {}
    rdir = os.path.join(B.AGENTENV, "results")
    for tag, (world, seeds, menu, diff) in WORLDS.items():
        per = []
        for seed in seeds:
            p = os.path.join(rdir, f"smoke_blob2v2_{tag}_s{seed}.json")
            if os.path.exists(p):
                per.append(json.load(open(p)))
        if not per:
            continue
        fams = list(per[0]["skills"])
        rows[tag] = dict(
            n=len(per),
            reward_mean=round(float(np.mean([r["reward_skill"]
                                             for r in per])), 4),
            skills_mean={f: round(float(np.mean([r["skills"][f]
                                                 for r in per])), 4)
                         for f in fams},
            all_pass=all(r["smoke_pass"] for r in per),
            zero_cap_hits=all(sum(r["cap_hits"].values()) == 0
                              for r in per),
        )
    if set(rows) == {"E1", "E2"}:
        # A0-style world separation (PART 6 step 5): menu split is
        # structural (L3E vs L3S); report the shared-family profile delta.
        shared = [f for f in rows["E1"]["skills_mean"]
                  if f in rows["E2"]["skills_mean"]]
        rows["separation"] = {
            f: round(rows["E1"]["skills_mean"][f]
                     - rows["E2"]["skills_mean"][f], 4) for f in shared}
    path = os.path.join(rdir, "smoke_blob2v2_aggregate.json")
    json.dump(rows, open(path, "w"), indent=1)
    print(json.dumps(rows, indent=1))
    print("aggregate ->", path)
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--world", choices=("E1", "E2"), default="E1")
    ap.add_argument("--seed-idx", type=int, default=0)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--aggregate", action="store_true")
    a = ap.parse_args()
    if a.aggregate:
        aggregate()
        sys.exit(0)
    ok = True
    if a.all:
        for tag in ("E1", "E2"):
            for si in range(3):
                ok = asyncio.run(main_one(tag, si)) and ok
        aggregate()
    else:
        ok = asyncio.run(main_one(a.world, a.seed_idx))
    sys.exit(0 if ok else 1)
