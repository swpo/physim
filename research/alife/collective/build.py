"""Librarian for the ALife collective: derive the state of the field from the ledger.

The ledger is the set of contribution directories under collective/contrib/ plus the claims and
questions carried over from the first lab (collective/seed/). Everything here is derived: claim
statuses come from reviews, the score from established claims (SCORE.md), the queue from what is
open. Nothing depends on which agent did what or on how many agents there are. Run from
research/alife/:

    python collective/build.py                    # rebuild STATE.md, QUEUE.md, ledger.json, progress.*
    python collective/build.py --import-branches  # first import new contributions from worker branches
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from itertools import combinations
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LAB = HERE.parent
REPO = LAB.parents[1]
CONTRIB = HERE / "contrib"
SEED = HERE / "seed"
IMPORTED = HERE / "imported.json"
LAB_START = "2026-10-24T21:45Z"  # end of the first lab: the seed claims' time

CAPS = "SIBRMEXDHO"
CAP_NAMES = {"S": "spontaneous", "I": "individuals", "B": "organized boundary", "R": "repair", "M": "motility",
             "E": "metabolism", "X": "interaction", "D": "reproduction", "H": "heredity+selection",
             "O": "open-ended"}
CLASSES = ["lenia", "flow-lenia", "particle", "active-emulsion", "keller-segel", "phase-field",
           "reaction-diffusion", "physim-genome", "other"]
KINDS = {"world", "claim", "review", "finding", "question", "synthesis", "tool", "intent"}
VERDICTS = {"Supported", "Weak", "Contradicted"}
ACTIVE_WINDOW = timedelta(minutes=90)
MAX_FILE_MB = 15


# ------------------------------------------------------------------ time
def parse_t(s):
    if not s:
        return None
    s = str(s).strip().replace(" ", "T")
    for fmt in ("%Y-%m-%dT%H:%MZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    try:
        t = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def fmt_t(t):
    return t.strftime("%Y-%m-%dT%H:%MZ") if t else "?"


def now_utc():
    return datetime.now(timezone.utc).replace(second=0, microsecond=0)


# ------------------------------------------------------------------ import from worker branches
def git(*a, check=True):
    return subprocess.run(["git", "-C", str(REPO), *a], capture_output=True, text=True, check=check).stdout


def import_branches(prefix="claude/alife-c-", log=print):
    """Copy new contribution directories from worker branches (never overwrite existing ones)."""
    seen = json.loads(IMPORTED.read_text()) if IMPORTED.exists() else {}
    CONTRIB.mkdir(exist_ok=True)
    rel = "research/alife/collective/contrib"
    refs = [r.strip() for r in git("for-each-ref", "--format=%(refname:short)", f"refs/remotes/origin/{prefix}*").split()]
    stamp = fmt_t(now_utc())
    new = []
    for ref in refs:
        out = git("ls-tree", "-d", "--name-only", f"{ref}:{rel}", check=False)
        for cid in out.split():
            if (CONTRIB / cid).exists():
                continue
            if subprocess.run(["git", "-C", str(REPO), "cat-file", "-e", f"{ref}:{rel}/{cid}/contribution.json"],
                              capture_output=True).returncode:
                continue  # still being written
            sizes = git("ls-tree", "-r", "-l", f"{ref}:{rel}/{cid}").split("\n")
            big = [ln.split()[-1] for ln in sizes if ln.strip() and ln.split()[3] != "-"
                   and int(ln.split()[3]) > MAX_FILE_MB * 2 ** 20]
            arch = subprocess.run(["git", "-C", str(REPO), "archive", ref, f"{rel}/{cid}"], capture_output=True, check=True)
            subprocess.run(["tar", "-x", "-C", str(REPO)] + [f"--exclude={rel}/{cid}/{b}" for b in big],
                           input=arch.stdout, check=True)
            seen[cid] = {"first_seen": stamp, "branch": ref.replace("origin/", ""), "dropped_large_files": big}
            new.append(cid)
            log(f"IMPORT {cid} from {ref.replace('origin/', '')}" + (f" (dropped {big})" if big else ""))
    IMPORTED.write_text(json.dumps(seen, indent=1, sort_keys=True) + "\n")
    return new


# ------------------------------------------------------------------ loading
def load(now):
    """All contributions (seed + contrib/), with first-seen times and validation problems."""
    seen = json.loads(IMPORTED.read_text()) if IMPORTED.exists() else {}
    items, problems = [], []
    lab_start = parse_t(LAB_START)
    for f in sorted(SEED.glob("*.json")):
        for c in json.loads(f.read_text()):
            c.setdefault("author", "lab1")
            c["_t"] = lab_start
            c["_seed"] = True
            items.append(c)
    for d in sorted(CONTRIB.glob("*/")):
        p = d / "contribution.json"
        if not p.exists():
            continue
        try:
            c = json.loads(p.read_text())
        except json.JSONDecodeError as e:
            problems.append(f"`{d.name}`: contribution.json is not valid JSON ({e})")
            continue
        errs = []
        if c.get("id") != d.name:
            errs.append(f"id {c.get('id')!r} differs from the directory name")
            c["id"] = d.name
        if c.get("kind") not in KINDS:
            errs.append(f"unknown kind {c.get('kind')!r}")
        if not c.get("author"):
            errs.append("no author")
        if c.get("class") and c["class"] not in CLASSES:
            errs.append(f"unknown class {c['class']!r} (counted as other)")
            c["class"] = "other"
        for cl in c.get("claims") or []:
            bad = [x for x in cl.get("capabilities", []) if x not in CAPS]
            if bad:
                errs.append(f"claim {cl.get('cid')}: unknown capabilities {bad}")
        for v in c.get("verdicts") or []:
            if v.get("verdict") not in VERDICTS:
                errs.append(f"verdict {v.get('verdict')!r} for {v.get('cid')}")
        first = parse_t((seen.get(d.name) or {}).get("first_seen")) or parse_t(c.get("created")) or now
        c["_t"] = min(first, now)
        c["_dir"] = str(d.relative_to(LAB))
        if errs:
            problems.append(f"`{d.name}`: " + "; ".join(errs))
        items.append(c)
    items.sort(key=lambda c: (c["_t"], c.get("id", "")))
    return items, problems


# ------------------------------------------------------------------ derivation
def mask(caps):
    m = 0
    for x in caps:
        if x in CAPS:
            m |= 1 << CAPS.index(x)
    return m


def caps_of(m):
    return "".join(x for i, x in enumerate(CAPS) if m >> i & 1)


def submasks(m):
    s = m
    while s:
        yield s
        s = (s - 1) & m


def derive(items, until=None):
    """Claims with statuses and established capability sets, from contributions seen up to `until`."""
    items = [c for c in items if until is None or c["_t"] <= until]
    by_id = {c["id"]: c for c in items if c.get("id")}
    claims = {}
    for c in items:
        units = list(c.get("claims") or [])
        if c.get("finding"):
            units.append({"cid": "finding", "capabilities": [], "statement": c["finding"].get("result", ""),
                          "_finding": True})
        for cl in units:
            key = f"{c['id']}#{cl.get('cid', 'c1')}"
            claims[key] = {
                "key": key, "contribution": c["id"], "author": c.get("author"), "class": c.get("class", "other"),
                "title": c.get("title", ""), "rung": cl.get("rung", ""), "statement": cl.get("statement", ""),
                "claimed": mask(cl.get("capabilities", [])), "finding": bool(cl.get("_finding")),
                "outcome": c.get("outcome", "positive"), "world": c.get("world", ""), "t": c["_t"],
                "dir": c.get("_dir", ""), "seed_status": cl.get("seed_status") if c.get("_seed") else None,
                "evidence": cl.get("evidence", []), "reviews": [],
            }
    for c in items:
        if c.get("kind") != "review":
            continue
        target = by_id.get(c.get("review_of"))
        for v in c.get("verdicts") or []:
            key = f"{c.get('review_of')}#{v.get('cid', 'c1')}"
            cl = claims.get(key)
            if cl is None or target is None:
                continue
            if c.get("author") == cl["author"]:
                cl.setdefault("self_reviews", []).append(c["id"])
                continue
            sup = v.get("supported")
            cl["reviews"].append({"review": c["id"], "author": c.get("author"), "verdict": v.get("verdict"),
                                  "replicated": bool(v.get("replicated")), "t": c["_t"],
                                  "supported": mask(sup) if sup is not None else None,
                                  "observation": v.get("observation", "")})
    for cl in claims.values():
        latest = {}
        for r in cl["reviews"]:  # one vote per reviewer: their latest
            latest[r["author"]] = r
        votes = list(latest.values())
        sup = [r for r in votes if r["verdict"] == "Supported"]
        con = [r for r in votes if r["verdict"] == "Contradicted"]
        n_sup, n_rep_sup = len(sup), sum(r["replicated"] for r in sup)
        n_con, n_rep_con = len(con), sum(r["replicated"] for r in con)
        if cl["seed_status"] == "established":  # the first lab's committee: 3 judges, a re-run, a director
            n_sup, n_rep_sup = n_sup + 2, n_rep_sup + 1
        elif cl["seed_status"] == "provisional":
            n_sup, n_rep_sup = n_sup + 1, n_rep_sup + 1
        elif cl["seed_status"] == "contradicted":
            n_con, n_rep_con = n_con + 2, n_rep_con + 1
        if n_sup >= 2 and n_rep_sup >= 1 and n_sup >= 2 * n_con + 1:
            status = "established"
        elif (n_con >= 2 and n_con >= n_sup) or (n_rep_con >= 1 and n_rep_sup == 0 and n_sup <= 1):
            status = "contradicted"
        elif n_sup and n_con:
            status = "disputed"
        elif n_rep_sup >= 1:
            status = "provisional"
        else:
            status = "submitted"
        m = cl["claimed"]
        for r in sup:
            if r["supported"] is not None:
                m &= r["supported"]
        cl.update(status=status, held=m, n_sup=n_sup, n_rep_sup=n_rep_sup, n_con=n_con, n_rep_con=n_rep_con,
                  reviewers=sorted(latest))
    return claims, items


def score(claims, which=("established",)):
    cells = {}
    for cl in claims.values():
        if cl["status"] in which and not cl["finding"] and cl["held"] & ~mask("S"):
            for s in submasks(cl["held"]):
                if s & ~mask("S"):  # S alone is a modifier, not a capability
                    cells.setdefault(s, set()).add(cl["class"])
    P = len(cells)
    Q = sum(min(3, len(v)) for v in cells.values())
    K = sum(1 for cl in claims.values() if cl["finding"] and cl["status"] == "established" and cl["outcome"] == "positive")
    C = (sum(1 for cl in claims.values() if cl["status"] == "contradicted")
         + sum(1 for cl in claims.values() if cl["finding"] and cl["status"] == "established" and cl["outcome"] == "negative"))
    return {"P": P, "Q": Q, "K": K, "C": C}, cells


def frontier(claims):
    est = {}
    for cl in claims.values():
        if cl["status"] == "established" and not cl["finding"] and cl["held"]:
            est.setdefault(cl["held"], []).append(cl)
    maxi = [m for m in est if not any(o != m and (o & m) == m for o in est)]
    maxi.sort(key=lambda m: (-bin(m).count("1"), caps_of(m)))
    return maxi, est


def gaps(maxi, cells):
    """Sets one capability beyond a frontier set that no established claim illuminates yet."""
    out = {}
    for m in maxi:
        for i, x in enumerate(CAPS):
            g = m | 1 << i
            if g != m and g not in cells and x != "O":
                out.setdefault(g, []).append(m)
    return sorted(out.items(), key=lambda kv: (-bin(kv[0]).count("1"), -len(kv[1]), caps_of(kv[0])))


def potential(cl, cells):
    """Subsets a claim would newly illuminate if established as claimed."""
    return sum(1 for s in submasks(cl["claimed"]) if s not in cells and s & ~mask("S"))


# ------------------------------------------------------------------ outputs
def rel(path):
    return path if not path else str(path)


def write_outputs(items, problems, now, log=print):
    claims, _ = derive(items)
    sc, cells = score(claims)
    sc_prov, _ = score(claims, ("established", "provisional"))
    maxi, est = frontier(claims)
    gp = gaps(maxi, cells)
    recent = [c for c in items if not c.get("_seed")]
    active = sorted({c["author"] for c in recent if now - c["_t"] <= ACTIVE_WINDOW and c.get("author")})
    pending = [cl for cl in claims.values() if cl["status"] in ("submitted", "provisional", "disputed")]
    intents = [c for c in recent if c.get("kind") == "intent" and now - c["_t"] <= ACTIVE_WINDOW]
    busy = {}
    for c in intents:
        busy.setdefault(c.get("task", ""), []).append(c["author"])
    pressure = len([cl for cl in pending if not cl["seed_status"]]) / max(1, len(active))
    syn = [c for c in recent if c.get("kind") == "synthesis"]
    last_syn = syn[-1] if syn else None
    decided_since = sum(1 for cl in claims.values() if not cl["seed_status"] and cl["status"] in ("established", "contradicted")
                        and (last_syn is None or cl["t"] > last_syn["_t"]))
    syn_due = (last_syn is None and len(recent) >= 12) or (last_syn is not None and (
        now - last_syn["_t"] > timedelta(hours=3) or decided_since >= 8))
    cpu = sum(float((c.get("compute") or {}).get("cpu_minutes") or 0) for c in recent) / 60

    # progress replay: the score as a function of time, from first-seen times only
    times = sorted({c["_t"] for c in items})
    series = []
    for t in times:
        cl_t, _ = derive(items, until=t)
        s, _ = score(cl_t)
        s_prov, _ = score(cl_t, ("established", "provisional"))
        series.append({"t": fmt_t(t), **s, "P_prov": s_prov["P"],
                       "contributions": sum(1 for c in items if c["_t"] <= t and not c.get("_seed")),
                       "cpu_hours": round(sum(float((c.get("compute") or {}).get("cpu_minutes") or 0)
                                              for c in items if c["_t"] <= t and not c.get("_seed")) / 60, 2)})
    (HERE / "progress.json").write_text(json.dumps(series, indent=0) + "\n")
    plot(series)

    # ledger.json: machine-readable state for agents
    ledger = {
        "generated": fmt_t(now), "score": sc, "score_with_provisional": sc_prov, "active_agents": active,
        "claims": [{k: (caps_of(v) if k in ("claimed", "held") else fmt_t(v) if k == "t" else v)
                    for k, v in cl.items() if k not in ("reviews",)} | {"reviews": [
                        {**r, "t": fmt_t(r["t"]), "supported": caps_of(r["supported"]) if r["supported"] is not None else None}
                        for r in cl["reviews"]]} for cl in sorted(claims.values(), key=lambda c: c["t"])],
        "contributions": [{k: v for k, v in c.items() if not k.startswith("_")} | {"first_seen": fmt_t(c["_t"])}
                          for c in recent],
        "frontier": [caps_of(m) for m in maxi],
        "gaps": [caps_of(g) for g, _ in gp],
        "problems": problems,
    }
    (HERE / "ledger.json").write_text(json.dumps(ledger, indent=1, default=str) + "\n")

    def claim_line(cl):
        loc = cl["dir"] or cl["world"] or ""
        who = "lab 1 committee" if cl["seed_status"] else cl["author"]
        return (f"| `{caps_of(cl['held'] if cl['status'] == 'established' else cl['claimed'])}` | {cl['class']} | "
                f"{cl['title'] or cl['statement'][:80]} | {cl['status']} | {who} | `{loc}` |")

    # STATE.md
    L = [f"# State of the field", "",
         f"Generated {fmt_t(now)} from the ledger by `collective/build.py`. Do not edit by hand.", "",
         f"**Score.** Reach P = **{sc['P']}** illuminated capability sets; breadth Q = **{sc['Q']}**; "
         f"mechanisms K = **{sc['K']}**; corrections C = **{sc['C']}**. With provisional claims P would be "
         f"{sc_prov['P']}. Definitions: [SCORE.md](SCORE.md).", "",
         f"**Activity.** {len(recent)} contributions since the collective started; {len(active)} agents active in the "
         f"last 90 minutes ({', '.join(active) or 'none'}); {cpu:.1f} CPU hours reported. "
         f"{len(pending)} claims await review.", "",
         "![progress](progress.png)", ""]
    if last_syn:
        L += [f"## Latest synthesis ({fmt_t(last_syn['_t'])}, {last_syn.get('author')})", "",
              last_syn.get("summary", "").strip(), ""]
        body = REPO / "research/alife" / last_syn.get("_dir", "") / "synthesis.md"
        if body.exists():
            L += [body.read_text().strip(), ""]
    L += ["## Frontier", "",
          "The largest established capability sets (codes in [SCORE.md](SCORE.md)). Each row is one organism-level result.", "",
          "| Set | Class | Result | Status | By | Where |", "|---|---|---|---|---|---|"]
    for m in maxi:
        for cl in est[m][:2]:
            L.append(claim_line(cl))
    L += ["", "## Recently decided", "", "| Set | Class | Result | Status | By | Where |", "|---|---|---|---|---|---|"]
    dec = sorted([cl for cl in claims.values() if not cl["seed_status"] and cl["status"] in ("established", "contradicted")],
                 key=lambda c: max([r["t"] for r in c["reviews"]] or [c["t"]]), reverse=True)[:15]
    L += [claim_line(cl) for cl in dec] or ["| | | nothing decided yet | | | |"]
    mech = [cl for cl in claims.values() if cl["finding"] and cl["status"] == "established"]
    L += ["", "## Established mechanisms and negative results", ""]
    L += [f"- **{cl['title']}** ({cl['outcome']}): {cl['statement']} `{cl['dir']}`" for cl in mech] or ["- none yet"]
    neg = [cl for cl in claims.values() if cl["status"] == "contradicted"]
    L += ["", f"## Corrections ({len(neg)} contradicted claims)", ""]
    L += [f"- `{caps_of(cl['claimed'])}` {cl['title'] or cl['statement'][:100]} ({'lab 1' if cl['seed_status'] else cl['author']})"
          for cl in neg[-12:]] or ["- none"]
    L += ["", "## Toolbox", "", "Reusable operators and trackers: [TOOLBOX.md](TOOLBOX.md). Published tools:", ""]
    L += [f"- `{c['_dir']}`: {c.get('title', '')}" for c in recent if c.get("kind") == "tool"] or ["- none yet"]
    if problems:
        L += ["", "## Problems in contributions", ""] + [f"- {p}" for p in problems]
    (HERE / "STATE.md").write_text("\n".join(L) + "\n")

    # QUEUE.md
    def needs(cl):
        if cl["status"] == "disputed":
            return "tie-break review with replication"
        if cl["status"] == "provisional":
            return "1 more independent Supported review"
        return "2 independent reviews, at least 1 with a fresh-seed re-run"
    Q = ["# Work queue", "", f"Generated {fmt_t(now)}. Pick by the rules in [PROTOCOL.md](PROTOCOL.md).", "",
         f"**Review pressure: {pressure:.1f}** claims waiting per active agent. "
         + ("High: take a review unless you authored every waiting claim." if pressure >= 0.5 else
            "Low: push the frontier; review when you see a claim you can check quickly."), ""]
    if syn_due:
        Q += ["**Synthesis due** (task `SYN`): the state-of-the-field narrative is stale. The first agent to see this writes it.", ""]
    Q += ["## Claims waiting for review", "", "Ranked by how many new capability sets each would add if it holds.", "",
          "| Task | Claimed | Class | Claim | Author | Status | Needs | Reviewing |", "|---|---|---|---|---|---|---|---|"]
    for cl in sorted(pending, key=lambda c: (-potential(c, cells), c["t"]))[:25]:
        task = f"R:{cl['key']}"
        Q.append(f"| `{task}` | `{caps_of(cl['claimed'])}` (+{potential(cl, cells)}) | {cl['class']} | "
                 f"{cl['title'] or cl['statement'][:70]} | {cl['author'] if not cl['seed_status'] else 'lab 1'} | "
                 f"{cl['status']} | {needs(cl)} | {', '.join(busy.get(task, [])) or '-'} |")
    if not pending:
        Q.append("| | | | nothing waiting | | | | |")
    Q += ["", "## Frontier gaps", "", "Capability sets one step beyond an established result. Nobody has established these yet.", "",
          "| Task | Target set | Missing | Extends |", "|---|---|---|---|"]
    for g, ms in gp[:14]:
        add = [x for x in caps_of(g) if not any(x in caps_of(m) for m in ms)]
        ext = "; ".join(f"`{caps_of(m)}` ({est[m][0]['title'] or est[m][0]['statement'][:40]})" for m in ms[:2])
        Q.append(f"| `G:{caps_of(g)}` | `{caps_of(g)}` | {', '.join(CAP_NAMES[x] for x in add)} | {ext} |")
    qs = [c for c in items if c.get("kind") == "question"]
    took = {}
    for c in recent:
        if c.get("task"):
            took.setdefault(c["task"], []).append(c)
    Q += ["", "## Open questions", "", "Highest priority first. Attempts are contributions that named the task.", ""]
    for c in sorted(qs, key=lambda c: (-int(c.get("priority", 3)), c["_t"])):
        task = f"Q:{c.get('slug') or c['id']}"
        done = [a for a in took.get(task, []) if a.get("kind") != "intent"]
        prog = f"; in progress: {', '.join(busy[task])}" if task in busy else ""
        Q.append(f"- `{task}` (priority {c.get('priority', 3)}, target `{''.join(c.get('target', []))}`, "
                 f"{c.get('class', 'any')}, {len(done)} attempts{prog}) **{c.get('title', '')}** "
                 f"{c.get('experiment') or c.get('summary', '')}")
    cov = {k: 0 for k in CLASSES}
    for cl in claims.values():
        if cl["status"] == "established" and not cl["finding"]:
            cov[cl["class"]] = cov.get(cl["class"], 0) + 1
    tries = {k: 0 for k in CLASSES}
    for c in recent:
        if c.get("class") in tries:
            tries[c["class"]] += 1
    Q += ["", "## Class coverage", "", "Established claims and new contributions per dynamical class. Thin classes are "
          "where exploration pays most.", "", "| Class | Established | Contributions since start |", "|---|---|---|"]
    Q += [f"| {k} | {cov[k]} | {tries[k]} |" for k in sorted(CLASSES, key=lambda k: (cov[k] + tries[k], k))]
    Q += ["", "## In progress", ""]
    Q += [f"- `{c.get('task', '?')}` by {c['author']} since {fmt_t(c['_t'])}: {c.get('title', '')}" for c in intents] or ["- nothing announced"]
    (HERE / "QUEUE.md").write_text("\n".join(Q) + "\n")
    log(f"SCORE P={sc['P']} Q={sc['Q']} K={sc['K']} C={sc['C']} P_prov={sc_prov['P']} "
        f"contributions={len(recent)} pending={len(pending)} active={len(active)}")
    return claims, sc


def plot(series):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if not series:
        return
    t = [parse_t(s["t"]) for s in series]
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.2))
    for k, c in (("P", "#0d7480"), ("Q", "#b0561b"), ("P_prov", "#9aa5ab")):
        ax[0].step(t, [s[k] for s in series], where="post", color=c, label={"P_prov": "P incl. provisional"}.get(k, k))
    ax[0].set_title("reach P and breadth Q")
    ax[0].legend(frameon=False, fontsize=8)
    for k, c in (("K", "#1d7a45"), ("C", "#a33b3b")):
        ax[1].step(t, [s[k] for s in series], where="post", color=c, label={"K": "mechanisms K", "C": "corrections C"}[k])
    ax[1].set_title("knowledge")
    ax[1].legend(frameon=False, fontsize=8)
    for a in ax:
        a.spines[["top", "right"]].set_visible(False)
        a.tick_params(labelsize=7)
        for lab in a.get_xticklabels():
            lab.set_rotation(30)
    fig.tight_layout()
    fig.savefig(HERE / "progress.png", dpi=90)
    plt.close(fig)


def status_map(claims):
    return {k: (v["status"], caps_of(v["held"])) for k, v in claims.items()}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--import-branches", action="store_true")
    ap.add_argument("--now", help="override the clock (UTC, e.g. 2026-10-25T07:30Z)")
    a = ap.parse_args()
    now = parse_t(a.now) if a.now else now_utc()
    prev = {}
    if (HERE / "ledger.json").exists():
        try:
            prev = {c["key"]: (c["status"], c["held"]) for c in json.loads((HERE / "ledger.json").read_text())["claims"]}
        except (KeyError, json.JSONDecodeError):
            prev = {}
    if a.import_branches:
        import_branches()
    items, problems = load(now)
    claims, sc = write_outputs(items, problems, now)
    for k, (st, held) in status_map(claims).items():
        if prev.get(k, ("new", ""))[0] != st:
            print(f"STATUS {k} {prev.get(k, ('new', ''))[0]} -> {st} `{held}`")
