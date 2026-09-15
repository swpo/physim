"""smoke_blob2.py — round-2 scripted actor (B8). EVALUATOR-side driver,
AGENT-side policy: speaks ONLY through the MCP tool functions.

Strategy per contract (the 'informed scripted reference', A0-grade):
  L1  execute each announced sequence ON THE MAIN SPAN near its end (walk
      out, read, walk back with the inverse command), and predict that
      reading with a small drift sigma. The span read is ~n steps earlier
      than the fork read — persistence over <=15tu at the walked pose.
  L2  no spatial model (the honest scripted gap): predict the per-port
      global mean with cross-slot climatology sigma. If informed spatial
      nowcasting is beyond the script, THAT is the measurement — L2 skill
      ~0 vs the global-aggregate baseline documents the gap.
  L3F AR(2) per channel on burst-sampled device-0 history + climatology
      blend at long horizons (sigma widened by horizon backtest).
  L3E duty-corrected windowed crossing rates + trend (round-1 logic).
  L3S persistence of the last 200tu windowed global mean/var.
  L4  control replica + sub-cap calibration emissions at the 6 lags ->
      linear template scaled to amp 3 (round-1 logic, slimmed lags).
  L4D the SAME calibration replicas at the 3 dose lags -> per-amp table:
      response scales linearly from calibration; sigma = fit residual.

Run: .venv/bin/python environments/physim/tools/smoke_blob2.py --world E1
Writes probes/blobs/agentenv/results/smoke_blob2_{tag}.json
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
from physim import blobround2 as R2                  # noqa: E402
from physim.blobstate import BlobToolState           # noqa: E402
from physim.servers import blob as S                 # noqa: E402

sys.path.insert(0, B.AGENTENV)
import refpipes as R                                 # noqa: E402

WORLDS = dict(E1=("p4g2_044", 928, "E1", "BLOB2-E1"),
              E2=("p6g8_033", 942, "E2", "BLOB2-E2"))


class Agent2:
    def __init__(self, ts):
        self.ts = ts
        self.t, self.v0, self.v1, self.glob = [], [], [], []
        self.status = None

    async def call(self, fn, **kw):
        out = json.loads(await fn(**kw))
        if "error" in out:
            raise RuntimeError(f"tool error: {out['error']}")
        return out

    async def explore(self, duty=0.45, burst=10, l1_reserve=24):
        st = await self.call(self.ts.status)
        self.status = st
        self.cc = st["contracts"]["contracts"]
        n_steps = int(round(st["t_end_of_span"] / st["step_tu"]))
        target = n_steps - l1_reserve          # leave room for L1 walks
        gap = max(int(round(burst / duty - burst)), 0)
        i = 0
        while i < target:
            take = min(burst, target - i)
            r = await self.call(self.ts.read_streams, window=take,
                                devices="all", include_global=True)
            for stp in r["steps"]:
                self.t.append(stp["t"])
                self.v0.append(np.asarray(stp["values"]["0"], float))
                self.v1.append(np.asarray(stp["values"]["1"], float))
            if "global_stats" in r:
                self.glob.append((r["t"],
                                  np.asarray(r["global_stats"], float)))
            i += take
            if gap and i < target:
                w = min(gap, target - i)
                await self.call(self.ts.wait, steps=w)
                i += w
        return n_steps - i                     # steps left for L1

    async def do_l1(self, steps_left):
        """Execute each announced sequence in place: walk out (n steps),
        read on the last step, walk back with -u (n steps). Uses the span's
        final steps; prediction = the walked read."""
        seqs = self.cc["L1"]["sequences"]
        preds = []
        for seq in seqs:
            u = seq["u"]; n = int(seq["steps"])
            r = await self.call(self.ts.adjust, device=0, u1=u[0], u2=u[1],
                                u3=u[2], steps=n, read=True)
            if r["result"] != "ok" or not r["steps_read"]:
                preds.append(None)
            else:
                preds.append(np.asarray(r["steps_read"][-1]["values"],
                                        float))
            # walk back (torus + exp symmetry: -u inverts exactly if no
            # wall was struck; sequences are wall-safe by construction)
            await self.call(self.ts.adjust, device=0, u1=-u[0], u2=-u[1],
                            u3=-u[2], steps=n, read=False)
            steps_left -= 2 * n
        # burn the rest of the span
        st = await self.call(self.ts.status)
        left = int(round((st["t_end_of_span"] - st["t"]) / st["step_tu"]))
        if left > 0:
            await self.call(self.ts.wait, steps=left)
        M0 = np.stack(self.v0)
        sig0 = np.abs(np.diff(M0[-24:], axis=0)).std(axis=0) * 3 + 1e-3
        k = self.cc["L1"]["slots"]; nf = self.cc["L1"]["ports"]
        clim_mu = M0.mean(0); clim_sd = M0.std(0) + 1e-3
        mu = np.stack([pr if pr is not None else clim_mu for pr in preds])
        sig = np.stack([sig0 if pr is not None else clim_sd
                        for pr in preds])
        return dict(mean=mu.tolist(), sigma=sig.tolist())

    def p_l2(self):
        """Honest scripted floor: global mean per port + spread that covers
        spatial variation (the cross-slot std of OWN devices ~ upper bound
        of spatial dispersion)."""
        nf = self.cc["L2"]["ports"]; kh = self.cc["L2"]["slots"]
        t_last, g_last = self.glob[-1]
        mu = np.repeat(g_last[:, 0][:, None], kh, axis=1)
        # spatial spread estimate: max(own-device slot std, sqrt(global var))
        own = np.stack(self.v0[-12:])
        slot_sd = own.std(axis=(0, 2))
        sig = np.maximum(slot_sd[:, None], np.sqrt(g_last[:, 1])[:, None])
        sig = np.repeat(sig, kh, axis=1) + 1e-3
        return dict(mean=mu.tolist(), sigma=sig.tolist())

    def p_l3f(self):
        Hs = np.array(self.cc["L3F"]["horizons"], float)
        M = np.stack(self.v0)
        Tn = M.shape[0]
        flat = M.reshape(Tn, -1)
        clim_mu, clim_sd = flat.mean(0), flat.std(0) + 1e-3
        mu, sig = [], []
        for H in Hs:
            n = max(int(round(H / 5.0)), 1)
            ar = R._ar2_forecast(flat, n)
            w = float(np.exp(-H / 100.0))      # blend to climatology
            mu.append(w * ar + (1 - w) * clim_mu)
            sig.append(np.maximum(clim_sd * (1.0 - 0.5 * w), 1e-3))
        shp = (len(Hs),) + M.shape[1:]
        return dict(mean=np.stack(mu).reshape(shp).tolist(),
                    sigma=np.stack(sig).reshape(shp).tolist())

    def p_l3e(self):
        cc = self.cc["L3E"]
        pt, thr, sgn = cc["port"], cc["thr"], float(cc["sign"])
        M = np.stack(self.v0)[:, pt, :] * sgn
        t = np.asarray(self.t)
        win = float(cc["window_tu"])
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
        last_r = float(valid[-1]) if len(valid) else 0.0
        n_win = cc["n_windows"]
        if len(valid) >= 4:
            v = valid[-6:]
            slope = np.polyfit(np.arange(len(v)), v, 1)[0]
            mu = np.clip(last_r + slope * np.arange(1, n_win + 1), 0, None)
        else:
            mu = np.full(n_win, last_r)
        sig = float(max(np.std(valid[-8:]) if len(valid) >= 3 else 1.0,
                        1.0))
        return dict(mean=mu.tolist(), sigma=sig)

    def p_l3s(self):
        cc = self.cc["L3S"]
        fpw = int(round(cc["window_tu"] / 5.0))
        G = [g for _, g in self.glob]
        Gw = np.stack(G[-max(fpw // 10, 4):])   # ~last window's snapshots
        mu1 = Gw.mean(0)
        n_ep = len(cc["epochs"])
        mu = np.tile(mu1[None], (n_ep, 1, 1))
        blocks = np.stack(G)
        sd = blocks.std(0) * 1.5 + 1e-4
        sig = np.tile(sd[None], (n_ep, 1, 1))
        return dict(mean=mu.tolist(), sigma=sig.tolist())

    async def do_l4(self):
        cc = self.cc["L4"]
        port, ann_amp, dur = cc["port"], cc["amp"], float(cc["dur_tu"])
        lags4 = [float(x) for x in cc["lags"]]
        ccd = self.cc["L4D"]
        lagsd = [float(x) for x in ccd["lags"]]
        all_lags = sorted(set(lags4) | set(lagsd))
        ctrl = await self.call(self.ts.inject, port=port, amp=0.0,
                               dur=dur, lags=all_lags, devices=[1])
        Call = {rd["lag"]: np.asarray(rd["values"]["1"], float)
                for rd in ctrl["reads"]}
        amps = (0.3, 0.6, 1.0)
        resps = []
        for a in amps:
            r = await self.call(self.ts.inject, port=port, amp=a,
                                dur=dur, lags=all_lags, devices=[1])
            A = {rd["lag"]: np.asarray(rd["values"]["1"], float)
                 for rd in r["reads"]}
            resps.append((a, {lg: A[lg] - Call[lg] for lg in all_lags}))
        # linear template per lag
        T = {lg: np.mean([dR[lg] / a for a, dR in resps], axis=0)
             for lg in all_lags}
        res = {lg: np.std([dR[lg] / a for a, dR in resps], axis=0)
               for lg in all_lags}
        noise = np.median(np.abs(np.diff(np.stack(self.v1[-20:]), axis=0)))
        mu4 = np.stack([Call[lg] + T[lg] * ann_amp for lg in lags4])
        sig4 = np.stack([np.maximum(res[lg] * ann_amp, noise + 1e-3)
                         for lg in lags4])
        p4 = dict(mean=mu4.tolist(), sigma=sig4.tolist())
        # dose table over announced amps
        grid = [float(a) for a in ccd["amps"]]
        mud = np.stack([np.stack([Call[lg] + T[lg] * a for lg in lagsd])
                        for a in grid])
        sigd = np.stack([np.stack([np.maximum(res[lg] * a, noise + 1e-3)
                                   for lg in lagsd]) for a in grid])
        p4d = dict(mean=mud.tolist(), sigma=sigd.tolist())
        return p4, p4d

    async def run(self, menu):
        steps_left = await self.explore()
        p1 = await self.do_l1(steps_left)
        subs = {"L1": p1, "L2": self.p_l2(), "L3F": self.p_l3f()}
        if "L3E" in self.cc:
            subs["L3E"] = self.p_l3e()
        if "L3S" in self.cc:
            subs["L3S"] = self.p_l3s()
        for cid, pl in subs.items():
            await self.call(self.ts.submit, contract=cid,
                            payload=json.dumps(pl))
        p4, p4d = await self.do_l4()
        await self.call(self.ts.submit, contract="L4",
                        payload=json.dumps(p4))
        await self.call(self.ts.submit, contract="L4D",
                        payload=json.dumps(p4d))
        return len(self.t)


async def main(tag):
    world, seed, menu, diff = WORLDS[tag]
    t0 = time.time()
    ts = S.BlobToolset(S.BlobToolsetConfig())
    st = BlobToolState()
    st.world, st.seed, st.round2 = world, seed, menu
    ts._inert_state = st
    agent = Agent2(ts)
    n_reads = await agent.run(menu)
    res = R2.score_episode2(world, seed, menu, dict(st.subs2))
    out = dict(
        world=world, seed=seed, menu=menu, difficulty=diff,
        reward_skill=round(res["reward_skill"], 4),
        skills={k: round(v, 4) for k, v in res["skills"].items()},
        crps={k.replace("_crps", ""): v for k, v in res["detail"].items()
              if k.endswith("_crps")},
        baselines=res["detail"]["baselines"],
        spend=dict(st.spent), n_replicas=st.n_replicas, n_reads=n_reads,
        wall_s=round(time.time() - t0, 1),
    )
    gates = dict(
        budgets_respected=all(st.spent[k] <= B.BUDGETS[k] + 1e-6
                              for k in B.BUDGETS),
        all_submitted=all(res["skills"][c] > -1.0 or
                          f"{c.lower()}_error" not in res["detail"]
                          for c in R2.MENUS[menu]),
        l1_positive=bool(res["skills"]["L1"] > 0.1),
        l4_positive=bool(res["skills"]["L4"] > 0.3),
        l4d_positive=bool(res["skills"]["L4D"] > 0.3),
        no_contract_at_floor=all(v > -1.0 for v in res["skills"].values()),
    )
    out["gates"] = gates
    out["smoke_pass"] = all(gates.values())
    path = os.path.join(B.AGENTENV, "results", f"smoke_blob2_{tag}.json")
    json.dump(out, open(path, "w"), indent=1)
    print(json.dumps(out, indent=1))
    print("SMOKE2", tag, "PASS" if out["smoke_pass"] else "FAIL", "->", path)
    return 0 if out["smoke_pass"] else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--world", choices=("E1", "E2"), default="E1")
    a = ap.parse_args()
    sys.exit(asyncio.run(main(a.world)))
