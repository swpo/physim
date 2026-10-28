"""Classify pulse outcomes from out/pulse_log.txt (+ strict blow-up re-runs in out/pulse_strict_log.txt).
Target outcome from its descendant tracking against the twin (twin's target splits at t=85; the 1e-4 null pulse
leaves that unchanged), site outcome from body presence at the injection site, spread from |dphi| > 0.25."""
import json, sys
from pathlib import Path

D = Path(__file__).resolve().parent
rows = [json.loads(l) for l in open(D / "out" / "pulse_log.txt") if l.startswith("{")]
strict = {}
sp = D / "out" / "pulse_strict_log.txt"
if sp.exists():
    for l in open(sp):
        if l.startswith("{"):
            r = json.loads(l)
            strict[(r["field"], r["site"], r["amp"])] = r
marks = ["t20", "t50", "t100"]


def first_split(ev):
    for t, a, b in ev:
        if b > a:
            return t
    return None


def classify(r):
    key = (r["field"], r["site"], r["amp"])
    blown = [k for k in marks if "blowup_at" in r[k]]
    if blown:
        rs = strict.get(key)
        if rs is not None:
            sb = [k for k in marks if "blowup_at" in rs[k]]
            if sb:
                return [f"numerical blow-up (non-finite) at t={rs[sb[0]]['blowup_at']}"], rs
            return [f"|phi|>50 at t={r[blown[0]]['blowup_at']} but stays finite to t=100"], rs
        return [f"blow-up flag at t={r[blown[0]]['blowup_at']} (|phi|>50 or non-finite; strict re-run pending)"], r
    tags = []
    ts, tt = first_split(r["events"]), first_split(r["twin_events"])
    if any(b == 0 for _, a, b in r["events"]):
        tags.append("target killed")
    if ts is not None and (tt is None or ts < tt - 5):
        tags.append(f"division triggered (t={ts} vs twin {tt})")
    elif ts is None and tt is not None:
        tags.append("division suppressed/delayed past t=100")
    elif ts is not None and tt is not None and ts > tt + 5:
        tags.append(f"division delayed (t={ts} vs {tt})")
    if r["t100"]["target_maxdesc"] >= 3:
        tags.append(f"target fragmented ({r['t100']['target_maxdesc']} pieces)")
    if r["site"] == "bath" and any(r[k]["body_at_site"] and not r[k]["body_at_site_twin"] for k in marks[:2]):
        tags.append("body created at site")
    elif r["t20"]["bodies"] > r["t20"]["bodies_twin"]:
        tags.append("extra body by t=20")
    if not tags:
        tags.append("absorbed" if r["t20"]["changed_px"] == 0 else "absorbed (target reshaped)")
    return tags, r


out = []
print(f"{'field':5} {'site':6} {'amp':>7} | spread rmax(|dphi|>.25) t20/t50/t100 | changed px t20/t50/t100 | r90_c t20 | class")
for r in rows:
    tags, rr = classify(r)
    sp_, cp = [], []
    for k in marks:
        v = rr[k]
        sp_.append(str(v.get("changed_rmax", "X")))
        cp.append(str(v.get("changed_px", "X")))
    print(f"{r['field']:5} {r['site']:6} {r['amp']:>7g} | {'/'.join(sp_):22} | {'/'.join(cp):16} | "
          f"{rr['t20'].get('r90_c', 'X')} | " + "; ".join(tags))
    out.append(dict(field=r["field"], site=r["site"], amp=r["amp"], cls=tags, **{k: rr[k] for k in marks},
                    events=rr["events"], twin_events=rr["twin_events"]))
(D / "out" / "pulse_table.json").write_text(json.dumps(out, indent=1))
