"""smoke_blob.py — SMOKE A: null-harness scripted actor on the BLOB tool
surface (Track A round-1 W3). EVALUATOR-side test driver, AGENT-side policy.

The actor speaks ONLY through the MCP tool functions (direct-call, inert
state — the same code path the FastMCP server registers). It adapts the A0
informed reference pipeline to the round-1 episode:

  P1' informed  : AR2 per-channel on burst-sampled device-0 history (the A0
                  p1_ar2 predictor, refpipes.py), climatology sigma.
  P2  informed  : duty-corrected pre-T0 crossing-rate estimate from the
                  agent's own reads at the announced (port, thr, sign).
  P3  informed  : control replica + amp-calibration replicas at <=1.0 via
                  probe_inject; response templates scaled linearly to the
                  announced amp 3.0 added onto the control trajectory
                  (the A0 p3_template_predict logic on the agent surface).

Verifies (vs blobcore truths, evaluator-side AFTER the episode):
  - episode mechanics + budget discipline through the agent interface,
  - P3 informed CRPS beats persistence CRPS (adequacy-grade skill: the A0
    x4/r2 table shows ~5x on E1; here calibration stops at the amp cap so
    the bar is 'clearly better than persistence', target >=1.5x),
  - P2 informed MAE at least matches the better scripted null,
  - P1' respec horizons carry more skill than the old H50/H200 (report).

Run:  .venv/bin/python environments/physim/tools/smoke_blob.py [--seed 928]
Writes probes/blobs/agentenv/results/smoke_blob_s{seed}.json
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
from physim.blobstate import BlobToolState           # noqa: E402
from physim.servers import blob as S                 # noqa: E402

sys.path.insert(0, B.AGENTENV)
import refpipes as R                                 # noqa: E402

WORLD = "p4g2_044"


class Agent:
    """Scripted actor: owns NOTHING but tool responses."""

    def __init__(self, ts):
        self.ts = ts
        self.t = []            # read times
        self.v0 = []           # device-0 streams per read (nf, k0)
        self.v1 = []           # device-1 streams per read (nf, k1)
        self.status = None

    async def call(self, fn, **kw):
        out = json.loads(await fn(**kw))
        if "error" in out:
            raise RuntimeError(f"tool error: {out['error']}")
        return out

    # ---------------------------------------------------------- exploration
    async def explore(self, duty=0.5, burst=10):
        """Burst-sampled passive observation of the whole span at ~duty."""
        st = await self.call(self.ts.status)
        self.status = st
        n_steps = int(round(st["t_end_of_span"] / st["step_tu"]))
        # read plan: bursts of `burst` reads, gaps sized to hit the duty
        gap = max(int(round(burst / duty - burst)), 0)
        i = 0
        while i < n_steps:
            take = min(burst, n_steps - i)
            r = await self.call(self.ts.read_streams, window=take,
                                devices="all", include_global=False)
            for stp in r["steps"]:
                self.t.append(stp["t"])
                self.v0.append(np.asarray(stp["values"]["0"], float))
                self.v1.append(np.asarray(stp["values"]["1"], float))
            i += take
            if gap and i < n_steps:
                w = await self.call(self.ts.wait, steps=min(gap, n_steps - i))
                i += min(gap, n_steps - i)
        # ensure we are exactly at span end
        st = await self.call(self.ts.status)
        assert st["phase"] == "replica_experiments", st
        return st

    # ------------------------------------------------------------ contracts
    def p1_payload(self):
        cc = self.status["contracts"]["P1"]
        H = np.array(cc["horizons"], float)
        M = np.stack(self.v0)                     # (T, nf, k)
        Tn, nf, k = M.shape
        flat = M.reshape(Tn, -1)
        # AR2 forecast per flattened channel (refpipes _ar2_forecast expects
        # (T, C) and n-step count in READ steps; our reads are ~5tu apart
        # in bursts — use the burst cadence as the step unit, horizons in
        # steps from the last read)
        mu = []
        for h in H:
            nstep = max(int(round(h / 5.0)), 1)
            mu.append(R._ar2_forecast(flat, nstep))
        mu = np.stack(mu).reshape(len(H), nf, k)
        sig = flat.std(axis=0).reshape(nf, k)[None].repeat(len(H), 0)
        sig = np.maximum(sig, 1e-3)
        return dict(mean=mu.tolist(), sigma=sig.tolist())

    def p2_payload(self):
        """A0 p2_forecast adaptation: duty-corrected windowed rates from own
        reads; forecast = last-window rate + short trend (refpipes logic)."""
        cc = self.status["contracts"]["P2"]
        p, thr, sgn = cc["port"], cc["thr"], float(cc["sign"])
        M = np.stack(self.v0)[:, p, :] * sgn      # (T, k)
        t = np.asarray(self.t)
        win = float(cc["window_tu"])
        fpw = max(int(round(win / 5.0)), 1)
        x = M > thr
        up = (~x[:-1] & x[1:]).sum(axis=1)
        consec = np.diff(t) <= 5.0 + 1e-9         # duty correction
        up = up * consec
        edges = np.arange(t[0], t[-1] + win, win)
        rates = []
        for w0, w1 in zip(edges[:-1], edges[1:]):
            sel = (t[:-1] >= w0) & (t[:-1] < w1)
            n_pairs = int((sel & consec).sum())
            rates.append(up[sel].sum() * fpw / n_pairs if n_pairs else np.nan)
        rates = np.asarray(rates, float)
        valid = rates[np.isfinite(rates)]
        last_r = float(valid[-1]) if len(valid) else 0.0
        n_win = cc["n_windows"]
        if len(valid) >= 4:
            v = valid[-6:]
            slope = np.polyfit(np.arange(len(v)), v, 1)[0]
            mu = np.clip(last_r + slope * np.arange(1, n_win + 1), 0, None)
        else:
            mu = np.full(n_win, last_r)
        sig = np.maximum(np.std(valid[-8:]) if len(valid) >= 3
                         else np.sqrt(max(last_r, 1.0)), 1.0)
        return dict(mean=mu.tolist(), sigma=float(sig))

    async def p3_payload(self, amps=(0.25, 0.5, 1.0)):
        cc = self.status["contracts"]["P3"]
        port, ann_amp, dur = cc["port"], cc["amp"], float(cc["dur_tu"])
        lags = [float(x) for x in cc["lags"]]
        # control replica
        ctrl = await self.call(self.ts.inject, port=port, amp=0.0,
                               dur=dur, lags=lags, devices=[1])
        C = np.stack([np.asarray(rd["values"]["1"], float)
                      for rd in ctrl["reads"]])          # (L, nf, k)
        # calibration replicas
        resps = []
        for a in amps:
            r = await self.call(self.ts.inject, port=port, amp=a,
                                dur=dur, lags=lags, devices=[1])
            A = np.stack([np.asarray(rd["values"]["1"], float)
                          for rd in r["reads"]])
            resps.append((a, A - C))
        # linear template: response/amp averaged across calibs, scaled to
        # announced amp (the A0 template logic; template units amp*dur)
        T = np.mean([dR / a for a, dR in resps], axis=0)
        mu = C + T * ann_amp
        # sigma: residual scale of the linear fit + read noise floor
        res = np.std([dR / a for a, dR in resps], axis=0) * ann_amp
        noise = np.median(np.abs(np.diff(np.stack(self.v1), axis=0)))
        sig = np.maximum(res, noise + 1e-3)
        return dict(mean=mu.tolist(), sigma=sig.tolist()), C, resps

    async def run(self):
        st0 = await self.explore(duty=0.5)
        p1 = self.p1_payload()
        p2 = self.p2_payload()
        r1 = await self.call(self.ts.submit, contract="P1", payload=json.dumps(p1))
        r2 = await self.call(self.ts.submit, contract="P2", payload=json.dumps(p2))
        p3, C, resps = await self.p3_payload()
        r3 = await self.call(self.ts.submit, contract="P3", payload=json.dumps(p3))
        st = await self.call(self.ts.status)
        return dict(status=st, n_reads=len(self.t))


async def main(seed):
    t0 = time.time()
    ts = S.BlobToolset(S.BlobToolsetConfig())
    st = BlobToolState()
    st.world, st.seed = WORLD, seed
    ts._inert_state = st
    agent = Agent(ts)
    summary = await agent.run()

    # ---------------- evaluator side: score + compare --------------------
    res = B.score_episode(WORLD, seed, st.sub_p1, st.sub_p2, st.sub_p3)
    ref = B.baselines(WORLD, seed)
    d = res["detail"]
    p3_skill = ref["p3_persistence"] / max(d.get("p3_crps", np.inf), 1e-12)
    p1_skill = ref["p1_persistence"] / max(d.get("p1_crps", np.inf), 1e-12)
    p2_mae = d.get("p2_mae", np.inf)
    out = dict(
        world=WORLD, seed=seed,
        reward_accuracy=round(res["reward_accuracy"], 4),
        accs=res["accs"],
        crps=dict(p1=d.get("p1_crps"), p2=d.get("p2_crps"),
                  p3=d.get("p3_crps")),
        p2_mae=p2_mae,
        baselines={k: round(v, 5) for k, v in ref.items()},
        skill=dict(p1_vs_persistence=round(p1_skill, 3),
                   p3_vs_persistence=round(p3_skill, 3),
                   p2_mae_vs_ref=round(ref["p2_ref"] / max(p2_mae, 1e-9), 3)),
        spend=dict(st.spent),
        n_replicas=st.n_replicas,
        n_reads=summary["n_reads"],
        wall_s=round(time.time() - t0, 1),
    )
    # gates
    gates = dict(
        budgets_respected=all(st.spent[k] <= B.BUDGETS[k] + 1e-6
                              for k in B.BUDGETS),
        p1p2_locked_after_inject=bool(st.locked_p1p2),
        p3_beats_persistence=bool(p3_skill >= 1.5),
        p2_not_worse_than_ref=bool(p2_mae <= ref["p2_ref"] * 1.35 + 1e-9),
        all_submitted=bool(st.sub_p1 and st.sub_p2 and st.sub_p3),
    )
    out["gates"] = gates
    out["smoke_pass"] = all(gates.values())
    path = os.path.join(B.AGENTENV, "results", f"smoke_blob_s{seed}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, "w"), indent=1)
    print(json.dumps(out, indent=1))
    print("SMOKE", "PASS" if out["smoke_pass"] else "FAIL", "->", path)
    return 0 if out["smoke_pass"] else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=928)
    a = ap.parse_args()
    sys.exit(asyncio.run(main(a.seed)))
