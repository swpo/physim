"""Checker: steering numbers recomputed from results/steer.npz (tracker tables), and run1 vs rerun."""
import json
import math

import numpy as np

R0 = "/home/user/evalwork/vecworld/vw1/fresh/inputs/results"
J = json.load(open(f"{R0}/steer.json"))
J1 = json.load(open(f"{R0}/steer_run1.json"))
z = np.load(f"{R0}/steer.npz")
tabs = z["tabs"].astype(np.float64)
targets = z["targets"]
NT = int(z["NT"])
print("tabs", tabs.shape, "targets", len(targets), "admissible all", bool(z["admissible"].all()))
# run1 vs rerun
r0, r1 = J["rows"], J1["rows"]
dif = 0
for a, b in zip(r0, r1):
    for k in a:
        if k in b and a[k] != b[k]:
            dif += 1
print("rows equal run1 vs rerun:", len(r0) == len(r1), "differing fields", dif)
print("summary 'all' equal:", J["summary"]["all"] == J1["summary"]["all"])
print("null", J["summary"]["null_check_max_abs_x"], J["summary"]["null_check_max_abs_table"],
      "null table from npz", float(np.abs(tabs[-1] - tabs[0]).max()))
NF, UID, CY, EVC = 12, 16, 12, 15


def mi(d, L):
    return (d + L / 2) % L - L / 2


def unwrap(P, start):
    L = np.array([128, 128])
    dd = np.vstack([mi(P[0] - start, L)[None], mi(np.diff(P, axis=0), L)])
    return np.cumsum(dd, 0)


ST = ["flank+", "flank-", "lead+", "lead-"]
rows = []
for i, (s0, s) in enumerate(targets):
    tb = tabs[5 * i]
    uid0 = tb[0, s, UID]
    v0 = tb[0, s, 10:12]
    u0 = v0 / np.linalg.norm(v0)
    n0 = np.array([-u0[1], u0[0]])
    for j, st in enumerate(ST, start=1):
        ts = tabs[5 * i + j]
        sg = 1 if st.endswith("+") else -1
        al = lambda T: [k for k in range(NT) if T[k + 1, s, 0] > 0.5 and T[k + 1, s, UID] == uid0]  # noqa: E731
        a1, a2 = al(ts), al(tb)
        kend = min(max(a1) if a1 else -1, max(a2) if a2 else -1)
        r = {"st": st, "kend": kend, "s0": int(s0), "s": int(s)}
        # also: first loss of identity (contiguous survival) to check whether 'max' hides gaps
        first_loss = next((k for k in range(NT) if not (ts[k + 1, s, 0] > 0.5 and ts[k + 1, s, UID] == uid0)), NT)
        first_loss_b = next((k for k in range(NT) if not (tb[k + 1, s, 0] > 0.5 and tb[k + 1, s, UID] == uid0)), NT)
        r["contig"] = min(first_loss, first_loss_b)
        if kend >= 7:
            start = tb[0, s, CY:CY + 2]
            Us = unwrap(ts[1:kend + 2, s, CY:CY + 2], start)
            Ub = unwrap(tb[1:kend + 2, s, CY:CY + 2], start)
            ds, db = Us[-1] - Us[-8], Ub[-1] - Ub[-8]
            ang = math.degrees(math.atan2(ds[0], ds[1]) - math.atan2(db[0], db[1]))
            r["ang"] = sg * ((ang + 180) % 360 - 180)
            off = Us[-1] - Ub[-1]
            r["lat"] = sg * (off[1] * n0[0] + off[0] * n0[1])
            ev = any(np.any(T[1:kend + 2, s, EVC] != 0) or np.any(np.abs(T[1:kend + 2, s, 1] / T[0, s, 1] - 1) > 0.2)
                     for T in (tb, ts))
            r["clean"] = not ev
        rows.append(r)
ok = [r for r in rows if "ang" in r]
h = np.array([r["ang"] for r in ok])
print("usable", len(ok), "of", len(rows), "toward -n", int((h < 0).sum()), "frac", (h < 0).mean(),
      "SE", math.sqrt((h < 0).mean() * (1 - (h < 0).mean()) / len(h)), "signed median", np.median(h),
      "abs median", np.median(np.abs(h)))
for g in ("flank", "lead"):
    hh = np.array([r["ang"] for r in ok if r["st"].startswith(g)])
    print(g, len(hh), int((hh < 0).sum()), np.median(hh))
for c in (True, False):
    hh = np.array([r["ang"] for r in ok if r["clean"] == c])
    print("clean" if c else "event", len(hh), int((hh < 0).sum()), np.median(hh))
# survival gaps: runs whose identity was lost and came back (max-based kend > first loss)
gap = [(r["s0"], r["st"], r["kend"], r["contig"]) for r in ok if r["kend"] + 1 > r["contig"]]
print("runs where identity reappears after a loss (kend+1 > contiguous survival):", len(gap), gap[:10])
# drop reasons
print("dropped:", [(r["s0"], r["st"], r["kend"]) for r in rows if "ang" not in r])
# turn direction by target: are the four strategies of a target all the same direction?
by_t = {}
for r in ok:
    by_t.setdefault(r["s0"], []).append(np.sign(r["ang"]))
print("per target signs", {k: [int(x) for x in v] for k, v in by_t.items()})
# per-sign strategy: flank+ vs flank- (if the effect is real, both signs should turn toward -n in their own frame)
for st in ST:
    hh = np.array([r["ang"] for r in ok if r["st"] == st])
    print(st, len(hh), int((hh < 0).sum()), round(float(np.median(hh)), 1))
lat = np.array([r["lat"] for r in ok])
print("lateral toward -n frac", (lat < 0).mean(), "median", np.median(lat))
print("video run", {k: J["summary"]["video_run"][k] for k in ("state", "slot", "strategy", "survived_ticks", "heading_change_deg_signed",
                                                                "lateral_offset_px_signed", "mass_ratio_end", "steered_ticks")})
