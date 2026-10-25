"""Librarian for the ALife collective: derive the state of the field from the ledger.

The ledger is the set of contribution directories under collective/contrib/ plus the first lab's
verdicts and open questions (collective/seed/). Everything here is derived: claim statuses come
from independent reviews, the score from established claims (SCORE.md), the queue and the task
assignments from what is open. Nothing depends on which agent did what or how many there are.
Run from research/alife/:

    python collective/build.py --check collective/contrib/<id>   # validate one contribution, write nothing
    python collective/build.py --write                            # rebuild STATE.md, QUEUE.md, ledger.json, progress.*
    python collective/build.py --import-branches                  # librarian: import from agent branches, then rebuild
"""
from __future__ import annotations

import argparse
import functools
import itertools
import json
import math
import re
import traceback
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LAB = HERE.parent
REPO = LAB.parents[1]
CONTRIB = HERE / "contrib"
SEED = HERE / "seed"
IMPORTED = HERE / "imported.json"
REL = "research/alife/collective/contrib"
BRANCH_PREFIX = "claude/alife-collective-"
LAB_START = "2026-10-24T21:45Z"  # end of the first lab: the time of the seed entries

CAPS = "SIBWRMEXDHO"
CAP_NAMES = {"S": "spontaneous", "I": "individuals", "B": "organized", "W": "containment", "R": "repair",
             "M": "motility", "E": "metabolism", "X": "interaction", "D": "reproduction", "H": "heredity+selection",
             "O": "open-ended", "F": "finding"}
GATED = set("WREXH")  # a supporting review must point to the gate control it ran or checked
KINDS = {"world", "claim", "review", "finding", "question", "synthesis", "tool", "intent", "sighting", "literature"}
MODES = {"explore", "extend", "control", "review", "synthesis"}
VERDICTS = {"Supported", "Weak", "Contradicted"}
ID_RE = re.compile(r"^\d{8}T\d{4}-(c\d+)-[a-z0-9][a-z0-9-]*$")
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*(:[a-z0-9-]+)?$")
ACTIVE_WINDOW = timedelta(minutes=90)
INTENT_WINDOW = timedelta(hours=3)
MAX_AUDITS = 2  # audits running at once
LIT_EVERY = timedelta(hours=6)  # a literature check is due this long after the last one, or when a grand challenge is met
LEASE = timedelta(hours=6, minutes=10)  # a session lasts 6 h (WORKER_PROMPT.md) unless an intent gives "until"
MAX_FILE_MB, MAX_CONTRIB_MB, MAX_MOVIE_MB = 15, 10, 3
FAIL_RE = re.compile(r"\bfail|contradict|did ?n[o']t|does ?n[o']t|not (replicat|reproduc|seen|observed|found)", re.I)
SCORE_VERSION = 4  # bump when scoring rules change: the progress history is then replayed
DROP_EXT = (".npz", ".npy", ".pkl", ".pickle", ".h5")


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


# ------------------------------------------------------------------ validation
def caps_list(v):
    """Capabilities from a list or a string like 'S I D' or 'SID'; unknown letters are reported ('F' is ignored)."""
    if isinstance(v, str):
        v = list(v.replace(",", " ").replace(" ", ""))
    if not isinstance(v, list):
        return [], [f"capabilities {v!r} is not a list"]
    out, bad = [], []
    for x in v:
        x = str(x).strip().upper()
        if x != "F":
            (out if x in CAPS else bad).append(x)
    return sorted(set(out), key=CAPS.index), ([f"unknown capabilities {bad}"] if bad else [])


def text(x):
    """Any JSON value as a string (None as '')."""
    return x if isinstance(x, str) else "" if x is None else json.dumps(x, default=str)


def as_int(x):
    if isinstance(x, list) and x:
        x = x[0]
    return x if type(x) is int else None


def coerce(c):
    """Type-check one contribution.json; returns (clean dict, errors). Never raises on JSON input."""
    errs = []
    if not isinstance(c, dict):
        return None, ["the top level is not a JSON object"]
    c = dict(c)
    for k in ("id", "author", "review_of", "task", "title", "summary", "class", "kind", "mode", "world", "outcome",
              "created", "slug", "experiment", "challenge", "focus", "pack", "until"):
        if k in c and c[k] is not None and not isinstance(c[k], str):
            c[k] = text(c[k])
    for k in ("claims", "verdicts", "parents", "target", "evidence"):
        v = c.get(k)
        if v is None:
            c[k] = []
        elif isinstance(v, (str, dict)) and k not in ("claims", "verdicts"):
            c[k] = [v]
        elif not isinstance(v, list):
            errs.append(f"{k} is not a list")
            c[k] = []
    for k in ("sources", "prior_art"):
        v = c.get(k)
        c[k] = [dict(x) for x in v if isinstance(x, dict)] if isinstance(v, list) else []
        if v is not None and len(c[k]) != (len(v) if isinstance(v, list) else -1):
            errs.append(f"{k}: must be a list of objects")
    for k in ("claims", "verdicts"):
        good = [dict(x) for x in c[k] if isinstance(x, dict)]
        if len(good) != len(c[k]):
            errs.append(f"{k}: entries must be objects")
        c[k] = good
    c["parents"] = [text(p) for p in c["parents"]]
    c["target"] = [text(x) for x in c["target"]]
    c["evidence"] = [text(p) for p in c["evidence"]]
    if "finding" in c:
        if isinstance(c["finding"], dict):
            f = dict(c["finding"])
            for k in ("operator", "capability", "world", "control", "result"):
                f[k] = text(f.get(k))
            c["finding"] = f
        else:
            errs.append("finding is not an object")
            c.pop("finding")
    try:
        c["priority"] = max(1, min(5, int(c.get("priority", 3))))
    except (TypeError, ValueError, OverflowError):
        c["priority"] = 3
    comp = c.get("compute") if isinstance(c.get("compute"), dict) else {}
    try:
        x = float(str(comp.get("cpu_minutes", 0)).strip("~ ") or 0)
    except (ValueError, OverflowError):
        x = 0.0
    c["compute"] = {"cpu_minutes": x if math.isfinite(x) and 0 <= x <= 1e5 else 0.0}
    if c.get("kind") not in KINDS:
        errs.append(f"unknown kind {c.get('kind')!r}")
    if c.get("mode") and c["mode"] not in MODES:
        errs.append(f"unknown mode {c['mode']!r}")
    if c.get("class"):
        c["class"] = c["class"].strip().lower()
        if not SLUG_RE.match(c["class"]):
            errs.append(f"class {c['class']!r} is not a kebab-case slug")
    for cl in c["claims"]:
        cl["capabilities"], e = caps_list(cl.get("capabilities", []))
        errs += [f"claim {cl.get('cid', '?')}: {x}" for x in e]
        for k in ("cid", "statement", "rung", "track", "requires", "bd_control"):
            cl[k] = text(cl.get(k)) if k != "cid" else (text(cl.get("cid")) or "c1")
        ev = cl.get("evidence")
        cl["evidence"] = [ev] if isinstance(ev, str) else [text(p) for p in ev] if isinstance(ev, list) else []
        if not isinstance(cl.get("controls_run", {}), dict):
            cl["controls_run"] = {}
    cids = [cl["cid"] for cl in c["claims"]]
    if len(cids) != len(set(cids)):
        errs.append("claims: duplicate cid")
    for v in c["verdicts"]:
        if not isinstance(v.get("verdict"), str) or v["verdict"] not in VERDICTS:
            errs.append(f"verdict {v.get('verdict')!r} (cid {v.get('cid')}) must be Supported, Weak or Contradicted")
            v["verdict"] = text(v.get("verdict"))
        v["cid"] = text(v.get("cid")) or None
        v["supported"], e = caps_list(v.get("supported", []))
        errs += e
        for k in ("observations", "controls_run"):
            if not isinstance(v.get(k, {}), dict):
                errs.append(f"verdict {k} is not an object")
                v[k] = {}
            v[k] = {str(a): text(b) for a, b in (v.get(k) or {}).items()}
        v["by_construction"], _ = caps_list(v.get("by_construction", []))
        v["seed"] = as_int(v.get("seed"))
    return c, errs


def check_paths(c, exists):
    """Evidence and world paths must exist and stay inside the repo. exists(path relative to research/alife) -> bool."""
    errs = []
    base = f"collective/contrib/{c.get('id')}"
    paths = list(c.get("evidence", []))
    for cl in c.get("claims", []):
        paths += cl.get("evidence", [])
    if c.get("world"):
        paths.append(c["world"])
    for p in paths:
        p = str(p).split("#")[0].strip()
        if not p:
            continue
        if p.startswith("/") or ".." in Path(p).parts:
            errs.append(f"path not found: {p} (paths must stay inside the repo)")
            continue
        cand = [p[len("research/alife/"):]] if p.startswith("research/alife/") else [f"{base}/{p}", p]
        if not any(exists(q) for q in cand):
            errs.append(f"path not found: {p}")
    return errs


HARD = ("id ", "author ", "path not found", "contribution is over", "unknown kind", "the top level", "symlink",
        "claims:", "claim ", "verdict", "review_of", "no claims", "no finding", "no verdicts", "rerun", "directory name",
        "finding is not", "unknown capabilities", "claims is not", "verdicts is not")


def validate(c, cid, worker, files, exists, known_ids):
    """Shared by the import and by --check. files: {relative path: size}. Returns (errors, hard errors, dropped files)."""
    errs = []
    if not ID_RE.match(cid):
        errs.append("directory name must be <yyyymmddThhmm>-cNN-<lowercase-kebab-slug>, e.g. 20261025T0712-c07-gated-lenia")
    if c.get("id") != cid:
        errs.append(f"id {c.get('id')!r} differs from the directory name")
    if worker and c.get("author") and c["author"] != worker:
        errs.append(f"author {c['author']!r} is not the branch's agent {worker}")
    kind = c.get("kind")
    drop = [f for f, s in files.items() if f.endswith(DROP_EXT) or s > MAX_FILE_MB * 2 ** 20
            or (f.endswith(".mp4") and (s > MAX_MOVIE_MB * 2 ** 20 or kind not in ("claim", "sighting", "world")))]
    kept = {f: s for f, s in files.items() if f not in drop}
    if sum(kept.values()) > MAX_CONTRIB_MB * 2 ** 20:
        errs.append(f"contribution is over {MAX_CONTRIB_MB} MB")
    if kind == "claim" and not any(cl["capabilities"] for cl in c.get("claims", [])):
        errs.append("no claims with capabilities (claims must be objects with a capabilities list)")
    if kind == "finding" and not c.get("finding"):
        errs.append("no finding object")
    if kind == "literature" and not any(text(x.get("url") or x.get("doi") or x.get("arxiv")).strip() for x in c["sources"]):
        errs.append("no sources with a url, doi or arxiv id")
    if kind == "review":
        if not c.get("verdicts"):
            errs.append("no verdicts")
        tid, _ = norm_target(c.get("review_of"), None)
        if tid not in known_ids:
            errs.append(f"review_of {c.get('review_of')!r} is not in the ledger yet (it is retried every cycle)")
        if any(v.get("replicated") for v in c.get("verdicts", [])) and not any(
                f.endswith("metrics.json") or f.startswith("rerun/") for f in kept):
            errs.append("rerun pack missing: a replicated verdict needs metrics.json or a rerun/ directory here")
    errs += check_paths(c, lambda p: exists(p, kept))
    hard = [e for e in errs if e.startswith(HARD)]
    return errs, hard, drop


# ------------------------------------------------------------------ import from agent branches
def git(*a, check=True):
    return subprocess.run(["git", "-c", "core.quotePath=false", "-C", str(REPO), *a],
                          capture_output=True, check=check, text=True).stdout


def read_imported():
    try:
        d = json.loads(IMPORTED.read_text()) if IMPORTED.exists() else {}
    except (json.JSONDecodeError, OSError):
        d = {}
    for k, v in (("_deferred", {}), ("_retracted", []), ("_bad_branches", {})):
        d.setdefault(k, v)
    return d


def write_imported(d):
    IMPORTED.write_text(json.dumps(d, indent=1, sort_keys=True) + "\n")


def known_ids():
    ids = {d.name for d in CONTRIB.glob("*/")}
    for name in ("claims.json", "questions.json"):
        f = SEED / name
        if f.exists():
            ids |= {c.get("id") for c in json.loads(f.read_text()) if isinstance(c, dict)}
    return ids


def import_branches(log=print, now=None):
    """Copy new, valid contribution directories from agent branches. Never overwrites, never re-imports."""
    seen = read_imported()
    CONTRIB.mkdir(exist_ok=True)
    write_imported(seen)
    refs = [r for r in git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/claude/").split()
            if r.startswith(f"origin/{BRANCH_PREFIX}")]
    stamp = fmt_t(now or now_utc())
    ids = known_ids()
    new, present = [], set()
    for ref in refs:
        worker = ref.split(BRANCH_PREFIX, 1)[1]
        if not re.fullmatch(r"c\d+", worker):
            if ref not in seen["_bad_branches"]:
                log(f"BRANCH {ref}: agent branches must be named {BRANCH_PREFIX}cNN")
            seen["_bad_branches"][ref] = f"agent branches must be named {BRANCH_PREFIX}cNN"
            write_imported(seen)
            continue
        for cid in git("ls-tree", "-d", "--name-only", f"{ref}:{REL}", check=False).split():
            present.add(cid)
            if cid in seen or cid in seen["_retracted"] or (CONTRIB / cid).exists() or cid.startswith("."):
                continue
            m = ID_RE.match(cid)
            if m and m.group(1) != worker:
                continue  # another agent's contribution, merged into this branch
            if not m and f"-{worker}-" not in cid and not cid[:8].isdigit():
                continue  # not a contribution directory
            if subprocess.run(["git", "-C", str(REPO), "cat-file", "-e", f"{ref}:{REL}/{cid}/contribution.json"],
                              capture_output=True).returncode:
                continue  # still being written
            reason, c, drop = None, {}, []
            try:
                c, errs = coerce(json.loads(git("show", f"{ref}:{REL}/{cid}/contribution.json")))
                if c is None:
                    raise ValueError("; ".join(errs))
                files = {}
                for rec in git("ls-tree", "-r", "-l", "-z", f"{ref}:{REL}/{cid}").split("\0"):
                    if not rec:
                        continue
                    meta, path = rec.split("\t", 1)
                    mode, _typ, _obj, size = meta.split()
                    if mode in ("120000", "160000"):
                        errs.append(f"symlink or submodule not allowed: {path}")
                    files[path] = int(size) if size != "-" else 0

                def exists(p, kept, ref=ref, cid=cid):
                    pre = f"collective/contrib/{cid}/"
                    if p.startswith(pre):
                        q = p[len(pre):].rstrip("/")
                        return q in kept or any(f.startswith(q + "/") for f in kept)
                    return (LAB / p).exists() or subprocess.run(
                        ["git", "-C", str(REPO), "cat-file", "-e", f"{ref}:research/alife/{p}"], capture_output=True).returncode == 0
                v_errs, hard, drop = validate(c, cid, worker, files, exists, ids | set(new))
                hard = [e for e in errs if e.startswith(HARD)] + hard
                if hard:
                    reason = "; ".join(hard)[:400]
            except Exception as e:  # noqa: BLE001 - any malformed input must defer, never stop the librarian
                reason = f"invalid contribution.json ({type(e).__name__}: {e})"[:400]
            if reason:
                if seen["_deferred"].get(cid) != reason:
                    log(f"DEFER {cid}: {reason}")
                seen["_deferred"][cid] = reason
                write_imported(seen)
                continue
            tmp = Path(tempfile.mkdtemp(dir=CONTRIB.parent, prefix=".import-"))
            try:
                arch = subprocess.run(["git", "-C", str(REPO), "archive", ref, f"{REL}/{cid}"], capture_output=True, check=True)
                subprocess.run(["tar", "-x", "-C", str(tmp)] + [f"--exclude={REL}/{cid}/{f}" for f in drop],
                               input=arch.stdout, check=True, capture_output=True)
                shutil.move(str(tmp / REL / cid), str(CONTRIB / cid))
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            seen["_deferred"].pop(cid, None)
            seen[cid] = {"first_seen": stamp, "branch": ref.replace("origin/", ""), "author": worker, "dropped": drop,
                         "tree": git("rev-parse", f"{ref}:{REL}/{cid}", check=False).strip()}
            write_imported(seen)
            new.append(cid)
            log(f"IMPORT {cid} ({c.get('kind')}) from {worker}" + (f", dropped {drop}" if drop else ""))
    for k in list(seen["_deferred"]):
        if k not in present:
            seen["_deferred"].pop(k)
    write_imported(seen)
    return new


# ------------------------------------------------------------------ loading
def load(now):
    """All contributions (seed + contrib/), with librarian first-seen times and validation problems."""
    seen = read_imported()
    items, problems = [], []
    lab_start = parse_t(LAB_START)
    for name in ("claims.json", "questions.json"):
        f = SEED / name
        if f.exists():
            for c in json.loads(f.read_text()):
                c, _ = coerce(c)
                c.update(author="lab1", _t=lab_start, _seed=True, _created=lab_start)
                items.append(c)
    for d in sorted(CONTRIB.glob("*/")):
        p = d / "contribution.json"
        if d.name.startswith(".") or not p.is_file() or d.name in seen["_retracted"]:
            continue
        try:
            c, errs = coerce(json.loads(p.read_text()))
            if c is None:
                problems.append(f"`{d.name}`: " + "; ".join(errs))
                continue
            rec = seen.get(d.name) if isinstance(seen.get(d.name), dict) else {}
            m = ID_RE.match(d.name)
            author = rec.get("author") or (m.group(1) if m else None)
            if c.get("author") and author and c["author"] != author:
                errs.append(f"author {c['author']!r} replaced by the branch's agent {author}")
            c["author"] = author or c.get("author") or "unknown"
            c["id"] = d.name
            first = parse_t(rec.get("first_seen"))
            if first is None:
                errs.append("imported without a librarian record")
            c["_t"] = min(first or now, now)
            c["_dir"] = str(d.relative_to(LAB))
            c["_created"] = parse_t(c.get("created")) or c["_t"]
            if errs:
                problems.append(f"`{d.name}` ({c['author']}): " + "; ".join(errs))
            items.append(c)
        except Exception as e:  # noqa: BLE001 - one bad file must never stop the build
            problems.append(f"`{d.name}`: unreadable contribution ({type(e).__name__}: {str(e)[:120]})")
    items.sort(key=lambda c: (c["_t"], c["_created"], c.get("id", "")))
    return items, problems


def load_challenges():
    f = SEED / "challenges.json"
    return json.loads(f.read_text()) if f.exists() else []


# ------------------------------------------------------------------ evidence of re-runs
@functools.lru_cache(maxsize=None)
def _runs_in(path):
    """(world name, seed) pairs from labkit metrics.json files under one directory inside the lab."""
    p = (LAB / path).resolve()
    if p.is_file():
        p = p.parent
    if not p.is_dir() or not (p == LAB.resolve() or LAB.resolve() in p.parents) or p == LAB.resolve():
        return frozenset()
    runs = set()
    for m in itertools.islice(p.rglob("metrics.json"), 40):
        try:
            d = json.loads(m.read_text(errors="replace"))
            w = d.get("world") if isinstance(d, dict) else None
            n = w.get("name") if isinstance(w, dict) else None
            runs.add((n if isinstance(n, str) else None, as_int(d.get("seed"))))
        except Exception:  # noqa: BLE001
            pass
    return frozenset(runs)


def pack_runs(paths):
    runs = set()
    for p in paths:
        runs |= _runs_in(str(p))
    return runs


def verified_rerun(review_dir, claim_runs, verdict):
    """A replication counts only with a re-run artifact in the review's own directory, on a new seed."""
    rd = LAB / review_dir
    if not review_dir or not rd.exists():
        return False
    names = {n for n, _ in claim_runs if n}
    old_seeds = {s for _, s in claim_runs}
    def same_world(n):  # variants of the claimed world (e.g. pcell-y07 for pcell) count as the same world
        return not names or (n and any(n == m or n.startswith(m) or m.startswith(n) for m in names))
    return any(s is not None and s not in old_seeds and same_world(n) for n, s in pack_runs([review_dir]))


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


S_BIT = mask("S")


def norm_target(review_of, cid):
    """Accept '<id>', '<id>#c1' or a QUEUE task 'R:<id>#c1'."""
    t = (review_of or "").strip()
    if t.startswith("R:"):
        t = t[2:]
    t = t.rstrip("/").rsplit("/", 1)[-1]  # accept a path form such as collective/contrib/<id>
    if "#" in t:
        t, suffix = t.split("#", 1)
        cid = cid or suffix
    return t, cid


def challenge_of(c, cl):
    """The grand challenge a claim names: its own or its contribution's `challenge`, or a `C:<id>` task."""
    for v, is_task in ((cl.get("challenge"), False), (c.get("challenge"), False), (c.get("task"), True)):
        v = text(v).strip()
        if v.startswith("C:"):
            return v[2:]
        if v and not is_task:
            return v
    return ""


def lineage(cid, by_id):
    """Authors of every contribution this one builds on, transitively."""
    out, seen, stack = set(), set(), list(by_id.get(cid, {}).get("parents", []))
    while stack:
        p = stack.pop()
        if p in by_id and p not in seen:
            seen.add(p)
            out.add(by_id[p].get("author"))
            stack += by_id[p].get("parents", [])
    return out


def ancestors(cid, by_id):
    """Ids of every contribution this one builds on, transitively (parents, world and evidence paths)."""
    ids, out, stack = set(by_id), set(), [cid]
    while stack:
        for p in ref_ids(by_id.get(stack.pop(), {}), ids):
            if p not in out:
                out.add(p)
                stack.append(p)
    return out


def lab_path(c, p):
    """An evidence path as a path relative to research/alife."""
    p = str(p).strip()
    if p.startswith("research/alife/"):
        return p[len("research/alife/"):]
    if c.get("_seed") or p.startswith(("threads/", "examples/", "labkit/", "collective/")):
        return p
    return f"{c.get('_dir', '')}/{p}"


def ref_ids(c, ids):
    """Contribution ids this contribution builds on: parents given as ids or paths, and world or evidence paths."""
    out = set()
    for p in list(c.get("parents", [])) + [c.get("world", "")] + list(c.get("evidence", [])):
        p = str(p)
        if p in ids:
            out.add(p)
        m = re.search(r"contrib/([^/]+)", p)
        if m and m.group(1) in ids and m.group(1) != c.get("id"):
            out.add(m.group(1))
    return out


def derive(items, until=None, canaries=frozenset()):
    """Claims (and findings) with per-capability tallies, statuses and held sets."""
    items = [c for c in items if until is None or c["_t"] <= until]
    by_id = {c["id"]: c for c in items if c.get("id")}
    ids = set(by_id)
    for c in items:
        c["_refs"] = ref_ids(c, ids)
    claims, problems = {}, []
    for c in items:
        units = list(c.get("claims") or []) if c.get("kind") in ("claim", "world") else []
        if c.get("kind") == "finding" and c.get("finding"):
            f = c["finding"]
            units = [{"cid": "finding", "capabilities": [], "statement": f.get("result", "") or c.get("summary", "")}]
        for cl in units:
            if cl["cid"] != "finding" and not cl.get("capabilities") and not (c.get("_seed") and cl.get("seed_status") == "contradicted"):
                continue  # nothing to decide
            key = f"{c['id']}#{cl['cid']}"
            evid = ([c["pack"]] if c.get("pack") else []) + [p for p in cl.get("evidence", []) if p]
            where = [lab_path(c, p) for p in evid] + ([c["_dir"]] if c.get("_dir") else [])
            runs = pack_runs(where)
            claims[key] = {
                "key": key, "contribution": c["id"], "author": c.get("author"), "class": c.get("class") or "unlabelled",
                "title": c.get("title", ""), "rung": cl.get("rung", ""), "statement": cl.get("statement", ""),
                "claimed": ["F"] if cl["cid"] == "finding" else list(cl.get("capabilities", [])),
                "finding": cl["cid"] == "finding", "finding_data": c.get("finding") if cl["cid"] == "finding" else None,
                "outcome": (c.get("outcome") or "").lower(), "world": c.get("world", "") or c.get("pack", ""),
                "t": c["_t"], "dir": c.get("_dir", ""), "seed_status": cl.get("seed_status") if c.get("_seed") else None,
                "seed_bc": set(caps_list(cl.get("by_construction", []))[0]) if c.get("_seed") else set(),
                "requires": cl.get("requires", ""), "challenge": challenge_of(c, cl), "bd_control": cl.get("bd_control", ""),
                "runs": runs, "seeds": {s for _, s in runs if s is not None}, "lineage": lineage(c["id"], by_id),
                "votes": {}, "canary": c["id"] in canaries, "track": cl.get("track", ""),
            }
            if not c.get("_seed") and cl["cid"] != "finding":
                if len([x for x in claims[key]["claimed"] if x != "S"]) >= 3 and not cl.get("track"):
                    problems.append(f"`{c['id']}`: claim {cl['cid']} has 3+ capabilities but no track; reviews cannot confirm them together")
                if len(claims[key]["seeds"]) < 2:
                    problems.append(f"`{c['id']}`: claim {cl['cid']} has fewer than 2 seeds in its packs; only S and I can be held")
    for c in items:
        if c.get("kind") != "review":
            continue
        for v in c.get("verdicts") or []:
            tid, cid = norm_target(c.get("review_of"), v.get("cid"))
            if tid not in by_id:
                problems.append(f"`{c['id']}` ({c.get('author')}): review_of {c.get('review_of')!r} is not in the ledger")
                continue
            if not cid or f"{tid}#{cid}" not in claims:
                cid = "finding" if f"{tid}#finding" in claims else (cid or "c1")
            cl = claims.get(f"{tid}#{cid}")
            if cl is None:
                problems.append(f"`{c['id']}` ({c.get('author')}): no claim {cid!r} in {tid}")
                continue
            if c.get("author") == cl["author"]:
                problems.append(f"`{c['id']}`: {c.get('author')} reviewed their own claim; ignored")
                continue
            verdict = v.get("verdict")
            listed = set(v["supported"]) & set(cl["claimed"])
            abstain = set()
            if cl["finding"]:
                sup = {"F"} if verdict == "Supported" else set()
            else:
                obs = v.get("observations") or {}
                if verdict == "Supported" and not listed:
                    problems.append(f"`{c['id']}`: Supported verdict lists no supported capabilities; ignored")
                    continue
                missing = {x for x in listed if not obs.get(x)}
                if missing:
                    problems.append(f"`{c['id']}`: no observation named for {''.join(sorted(missing, key=CAPS.index))}; not counted")
                sup = listed - missing
                abstain = set(missing) | set(caps_list(v.get("not_checked", []))[0])
                if verdict != "Supported":  # a Weak or Contradicted reviewer who saw something is not endorsing it
                    abstain |= sup
                    sup = set()
            seeds_run = v.get("seeds_run") if isinstance(v.get("seeds_run"), list) else []
            fails = sum(1 for r in seeds_run if isinstance(r, dict) and FAIL_RE.search(str(r.get("result", ""))))
            # A review counts when its own directory holds a labkit re-run on a new seed, whatever it found: a re-run
            # that failed to reproduce the claim is evidence against it. The self-reported flag is not needed (some
            # reviewers write "replicated": false to mean "it did not replicate").
            rerun = verified_rerun(c.get("_dir", ""), cl["runs"], v)
            failed_support = verdict == "Supported" and fails > len(seeds_run) - fails
            rep = rerun and not failed_support
            if not rerun and (v.get("replicated") or seeds_run):
                problems.append(f"`{c['id']}`: no labkit re-run on a new seed of the claimed world found in its directory; "
                                "the review counts neither for nor against")
            elif failed_support:
                problems.append(f"`{c['id']}`: Supported, but most reported seeds failed; the review is not counted")
            controls = {k: s for k, s in (v.get("controls_run") or {}).items()
                        if control_ok([c.get("_dir", ""), cl["dir"]], s)}
            bd = v.get("bd_supported")
            bd_caps = set(caps_list(bd)[0]) if isinstance(bd, (list, str)) and bd not in ("", "true", "false") else (
                set(cl["claimed"]) - {"S", "I"} if bd is True else set())
            cl["votes"][c.get("author")] = {  # one vote per reviewer: the latest
                "review": c["id"], "author": c.get("author"), "verdict": verdict, "t": c["_t"],
                "supported": sup, "abstain": abstain, "replicated": rep,
                "same_individuals": bool(v.get("same_individuals")) and bool(cl["track"]),
                "controls": controls, "by_construction": set(v.get("by_construction") or []),
                "bd": (bd is not False and bool(bd_caps)) if bd is not None else None, "bd_caps": bd_caps,
                "class_confirmed": bool(v.get("class_confirmed")), "refs": c["_refs"],
            }
    # time order: a claim that brings capabilities nobody has established before needs a third review
    so_far, cells_so_far = set(), set()
    for cl in sorted(claims.values(), key=lambda k: k["t"]):
        new_caps = set(cl["claimed"]) - so_far - {"S", "F"}
        pot = sum(1 for s in submasks(mask(cl["claimed"])) if s & ~S_BIT and s not in cells_so_far)
        cl["need_floor"] = 3 if (not cl["seed_status"] and not cl["finding"] and (new_caps or pot > 8)) else 0
        tally(cl)
        if cl["status"] == "established" and not cl["finding"]:
            so_far |= set(caps_of(cl["held"]))
            cells_so_far |= set(submasks(cl["scored"]))
    return claims, items, problems


def control_ok(dirs, s):
    """A gate control counts only if it points to a file or labkit run that exists in the review or claim directory."""
    tok = str(s).strip().split()[0].rstrip(",;:") if str(s).strip() else ""
    if not tok or tok.startswith("/") or ".." in Path(tok).parts:
        return False
    for d in dirs:
        if d and (LAB / d / tok).exists():
            return True
    return False


def tally(cl):
    """Per-capability decision. x is held when enough independent reviews with a verified re-run name it with an
    observation (and point to the gate control for W, R, E, X, H), and they outweigh the replicated reviews that
    did not support it. Unreplicated reviews count neither for nor against."""
    votes = list(cl["votes"].values())
    rep_votes = [v for v in votes if v["replicated"]]
    claimed = cl["claimed"]
    nonS = [x for x in claimed if x != "S"]
    need = max(3 if len(nonS) >= 4 else 2, cl.get("need_floor", 0))  # scrutiny scales with the payoff
    seed_pro = need if cl["seed_status"] == "established" else 0
    seed_con = 4 if cl["seed_status"] == "contradicted" else 0
    single_seed = not cl["seed_status"] and not cl["finding"] and len(cl["seeds"]) < 2
    held, partial, per = set(), set(), {}
    for x in claimed:
        together = len(nonS) < 3 or bool(cl["seed_status"])  # seed rungs already assert co-occurrence
        pro = [v for v in rep_votes if x in v["supported"] and (together or v["same_individuals"])]
        lin = [v for v in pro if v["author"] in cl["lineage"]]  # reviewers who built the claim's ancestors
        pro = [v for v in pro if v not in lin[1:]]  # one opinion per lineage of shared code
        con = sum(2 if v["verdict"] == "Contradicted" else 1 for v in rep_votes
                  if x not in v["supported"] and x not in v["abstain"]) + seed_con
        gate = x not in GATED or bool(seed_pro) or any(v["controls"].get(x) for v in pro)
        n = len(pro) + seed_pro
        k = need + (1 if x == "S" and not seed_pro else 0)  # spontaneity doubles the reach, so it costs one more review
        per[x] = {"pro": n, "con": con, "gate": gate, "need": k}
        if n >= k and n > con and gate and not (single_seed and x not in "SI"):
            held.add(x)
        elif n or any(x in v["supported"] or x in v["abstain"] for v in votes):
            partial.add(x)
    if not (held - {"S"}):
        held = set()
    n_contra = sum(1 for v in rep_votes if v["verdict"] == "Contradicted")
    if held:
        status = "established"
    elif seed_con or n_contra >= 2 or (n_contra >= 1 and not any(v["supported"] for v in rep_votes)):
        status = "contradicted"
    elif len(rep_votes) >= 2 and not partial:
        status = "weak"
    elif partial:
        status = "provisional"
    else:
        status = "submitted"
    bc = {x for x in held if any(x in v["by_construction"] for v in votes) or x in cl["seed_bc"]}
    bd_yes = [v for v in rep_votes if v["bd"] is True and v["supported"]]
    bd_no = [v for v in rep_votes if v["bd"] is False]
    bd = status == "established" and len(bd_yes) >= 1 and len(bd_yes) > len(bd_no)
    bd_mask = mask(set().union(*[v["bd_caps"] for v in bd_yes]) & (held - bc)) if bd else 0
    cl.update(status=status, held=mask(held), scored=mask(held - bc), bc=mask(bc), per=per, need=need,
              n_votes=len(votes), ever_supported=bool(seed_pro) or any(v["supported"] for v in rep_votes),
              bd=bd and bool(bd_mask), bd_mask=bd_mask, class_ok=any(v["class_confirmed"] for v in bd_yes))


def reviews_needed(cl):
    """Reviews still needed for the most promising capability that is not yet held (0 when nothing more can be decided)."""
    if cl["status"] in ("contradicted", "weak") or cl["seed_status"] in ("established", "contradicted"):
        return 0
    open_ = [p for x, p in cl["per"].items() if not (mask(x) & (cl["held"] | cl["bc"])) and x != "F"] if not cl["finding"] \
        else ([] if cl["status"] == "established" else list(cl["per"].values()))
    if not open_:
        return 0
    best = max(open_, key=lambda p: p["pro"] - p["con"])
    if best["con"] > best["pro"] + 3:
        return 0  # needs new evidence, not more reviews
    return max(1, best["need"] - best["pro"], best["con"] - best["pro"] + 1)


def needs_detail(cl):
    """What would decide each open capability: more supporting re-runs, the gate control, or resolving a dispute."""
    if cl["finding"]:
        p = cl["per"].get("F", {"pro": 0, "need": 2})
        return f"{max(1, p['need'] - p['pro'])} more replicated review(s)"
    more, gate, disputed = {}, [], []
    for x, p in cl["per"].items():
        if mask(x) & (cl["held"] | cl["bc"]):
            continue
        if p["con"] >= p["pro"] and p["con"]:
            disputed.append(f"{x} ({p['pro']} for, {p['con']} against)")
        if not p["gate"]:
            gate.append(x)
        if p["need"] > p["pro"]:
            more.setdefault(p["need"] - p["pro"], []).append(x)
    out = [f"{''.join(xs)}: {n} more supporting re-run(s)" for n, xs in sorted(more.items())]
    out += [f"{''.join(gate)}: a supporter must run the gate control (see RUBRIC)"] if gate else []
    out += [f"disputed: {', '.join(disputed)}"] if disputed else []
    return "; ".join(out) or "decided"


def score(claims, bd_only=False):
    """Illuminated subsets. bd_only: only subsets touching a capability a matched Laplacian-only twin lost."""
    cells = {}
    for cl in claims.values():
        if cl["status"] == "established" and not cl["finding"] and not cl["canary"] and (cl["bd"] or not bd_only):
            for s in submasks(cl["scored"]):
                if s & ~S_BIT and (not bd_only or s & cl["bd_mask"]):
                    cs = cells.setdefault(s, set())
                    if bd_only and cl["class_ok"]:
                        cs.add(cl["class"])
    return cells


def summary_score(claims):
    cells = score(claims)
    bd_cells = score(claims, bd_only=True)
    real = [cl for cl in claims.values() if not cl["canary"]]
    fd = lambda cl: cl["finding_data"] or {}
    K = len({(str(fd(cl).get("operator", "")).lower(), str(fd(cl).get("capability", "")), str(fd(cl).get("world", "")))
             for cl in real if cl["finding"] and cl["status"] == "established" and cl["outcome"] == "positive"
             and (fd(cl).get("necessary") is True or fd(cl).get("law") is True)})
    C = (sum(1 for cl in real if not cl["finding"] and cl["status"] == "contradicted" and cl["ever_supported"] or
             (not cl["finding"] and cl["seed_status"] == "contradicted"))
         + len({str(fd(cl).get("operator", "")) + "|" + cl["statement"][:60] for cl in real
                if cl["finding"] and cl["status"] == "established" and cl["outcome"] == "negative"}))
    P_prov = len({s for cl in real if cl["status"] in ("established", "provisional") and not cl["finding"]
                  for s in submasks(mask(cl["claimed"])) if s & ~S_BIT} | set(cells))
    return {"P": len(cells), "P_BD": len(bd_cells), "Q": sum(min(3, len(v)) for v in bd_cells.values()),
            "K": K, "C": C, "P_prov": P_prov}, cells, bd_cells


def frontier(claims):
    est = {}
    for cl in claims.values():
        if cl["status"] == "established" and not cl["finding"] and not cl["canary"] and cl["scored"] & ~S_BIT:
            est.setdefault(cl["scored"], []).append(cl)
    maxi = [m for m in est if not any(o != m and (o & m) == m for o in est)]
    maxi.sort(key=lambda m: (-bin(m).count("1"), caps_of(m)))
    return maxi, est


def potential(cl, cells):
    return sum(1 for s in submasks(mask(cl["claimed"])) if s not in cells and s & ~S_BIT)


# ------------------------------------------------------------------ outputs
def departed(recent, now):
    """Agents whose session has ended, so they hold no assignment and no task: the last thing they published is
    a `leave` intent, or their lease (from their first contribution, or an intent's `until`) has run out and they
    have published nothing since."""
    last, end = {}, {}
    for c in recent:  # time order
        a = c.get("author")
        if not a:
            continue
        last[a] = c
        until = parse_t(c.get("until")) if c.get("kind") == "intent" else None
        if until and until > c["_t"]:
            end[a] = until
        elif a not in end:
            end[a] = c["_t"] + LEASE
    return {a for a, c in last.items()
            if (c.get("kind") == "intent" and c.get("task") == "leave") or (now > end[a] and c["_t"] <= end[a])}


def write_outputs(items, problems, now, canaries=frozenset(), rebuild=False, log=print):
    claims, _, dproblems = derive(items, canaries=canaries)
    problems = problems + dproblems
    sc, cells, bd_cells = summary_score(claims)
    maxi, est = frontier(claims)
    recent = [c for c in items if not c.get("_seed")]
    gone = departed(recent, now)
    seen_recently = {c["author"] for c in recent if now - c["_t"] <= ACTIVE_WINDOW and c.get("author")}
    active = sorted(seen_recently - gone)
    left = sorted(seen_recently & gone)
    intents = [c for c in recent if c.get("kind") == "intent" and now - c["_t"] <= INTENT_WINDOW and c.get("author") not in gone]
    closed = {(c.get("author"), c.get("task")) for c in recent if c.get("kind") != "intent" and c.get("task")}
    live = [c for c in intents if (c.get("author"), c.get("task")) not in closed
            and re.match(r"^(R|C|Q|G|F|A):|^(SYN|LIT)$", c.get("task") or "")]  # a join intent holds no task
    busy = {}
    for c in live:
        busy.setdefault(c["task"], set()).add(c["author"])
    focus = {c["author"]: c["focus"] for c in recent if c.get("kind") == "intent" and c.get("focus")}
    campaign = {c["author"]: c["task"] for c in live if c.get("campaign")}

    pending = [cl for cl in claims.values() if reviews_needed(cl) > 0]
    cells_by_class = {}
    for cl in claims.values():
        if cl["status"] == "established" and not cl["finding"] and not cl["canary"]:
            for s in submasks(cl["scored"]):
                cells_by_class.setdefault(cl["class"], set()).add(s)

    def rank(cl):
        age_h = (now - cl["t"]).total_seconds() / 3600 if not cl["seed_status"] else 0
        cls_new = sum(1 for s in submasks(mask(cl["claimed"])) if s & ~S_BIT and s not in cells_by_class.get(cl["class"], set()))
        r = potential(cl, cells) + cls_new + (4 if cl["finding"] else 0) + min(age_h, 6) * 2 + (0 if cl["seed_status"] else 6)
        return r + (100 if age_h > 2 else 0)
    pending.sort(key=lambda cl: -rank(cl))
    needed = sum(reviews_needed(cl) for cl in pending if not cl["seed_status"])
    in_review = sum(len(v) for k, v in busy.items() if k.startswith("R:"))
    pressure = max(0, needed - in_review) / max(1, len(active))

    since = now - timedelta(hours=3)
    nonrev = [c for c in recent if c["_t"] >= since and c.get("kind") not in ("review", "intent", "synthesis", "literature")]
    explore_share = (sum(1 for c in nonrev if c.get("mode") == "explore") / len(nonrev)) if nonrev else None
    started = min([c["_t"] for c in recent], default=now)
    target_share = 0.5 if now - started < timedelta(hours=6) else 0.33

    syn = [c for c in recent if c.get("kind") == "synthesis"]
    last_syn = syn[-1] if syn else None
    decided_since = sum(1 for cl in claims.values() if cl["status"] in ("established", "contradicted") and not cl["seed_status"]
                        and cl["votes"] and (last_syn is None or max(v["t"] for v in cl["votes"].values()) > last_syn["_t"]))
    syn_due = (last_syn is None and len(recent) >= 10) or (last_syn is not None and (
        now - last_syn["_t"] > timedelta(hours=3) or decided_since >= 6))
    cpu = sum(c["compute"]["cpu_minutes"] for c in recent) / 60

    challenges = load_challenges()
    for ch in challenges:
        tgt = mask(ch.get("target", ""))
        ch["achieved"] = [cl["key"] for cl in claims.values() if cl["status"] == "established" and not cl["canary"]
                          and (cl["scored"] & tgt) == tgt and (not ch.get("bd") or cl["bd"])
                          and (not ch.get("named") or cl["challenge"] == ch["id"])]

    # audits: an independent check of each large statement (a grand challenge met, 4+ capabilities besides S,
    # or beyond diffusion) by an agent outside its lineage that had not reviewed it before
    in_challenge = {k for ch in challenges for k in ch["achieved"]}
    large = {k: cl for k, cl in claims.items() if cl["status"] == "established" and not cl["seed_status"] and not cl["finding"]
             and not cl["canary"] and (k in in_challenge or bin(cl["scored"] & ~S_BIT).count("1") >= 4 or cl["bd"])}
    first_review, audits = {}, {}
    for c in recent:  # time order
        if c.get("kind") != "review":
            continue
        for v in c.get("verdicts", []):
            tid, cid = norm_target(c.get("review_of"), v.get("cid"))
            if not cid or f"{tid}#{cid}" not in claims:
                cid = "finding" if f"{tid}#finding" in claims else (cid or "c1")
            key = f"{tid}#{cid}"
            first_review.setdefault((c.get("author"), key), c["id"])
            task = c.get("task") or ""
            if task.startswith("A:") and norm_target(task[2:], cid) == (tid, cid) and key in claims:
                cl = claims[key]
                independent = (first_review[(c.get("author"), key)] == c["id"] and c.get("author") != cl["author"]
                               and c.get("author") not in cl["lineage"])
                ok = (v.get("verdict") == "Supported" and set(cl["claimed"]) <= set(v.get("supported", [])) | {"S"}
                      and not set(v.get("by_construction") or []) & set(cl["claimed"]))
                audits.setdefault(key, []).append({"id": c["id"], "author": c.get("author"), "t": c["_t"],
                                                   "independent": independent, "passed": ok})
    def audit_status(key):
        good = [a for a in audits.get(key, []) if a["independent"]]
        return None if not good else ("passed" if good[-1]["passed"] else "disputed")
    audits_due = sorted([k for k in large if audit_status(k) is None],
                        key=lambda k: (k not in in_challenge, -bin(claims[k]["scored"]).count("1"), claims[k]["t"]))

    lit = [c for c in recent if c.get("kind") == "literature"]
    last_lit = lit[-1] if lit else None
    met_at = [min(max([v["t"] for v in claims[k]["votes"].values()], default=parse_t(LAB_START)) for k in ch["achieved"])
              for ch in challenges if ch["achieved"]]  # when each challenge was met: new results need a prior-art check
    lit_due = (last_lit is None and len(recent) >= 10) or (last_lit is not None and (
        now - last_lit["_t"] > LIT_EVERY or any(t > last_lit["_t"] for t in met_at)))

    ladders = []  # next rung for each dynamical class
    for cls in sorted(cells_by_class):
        cmax = [m for m in cells_by_class[cls] if not any(o != m and (o & m) == m for o in cells_by_class[cls])]
        nxt = sorted({m | 1 << i for m in cmax for i, x in enumerate(CAPS) if x not in "SO" and not m >> i & 1
                      and (m | 1 << i) not in cells_by_class[cls]}, key=lambda m: (-bin(m).count("1"), caps_of(m)))
        ladders.append((cls, sorted(cmax, key=lambda m: -bin(m).count("1"))[:2], nxt[:3]))

    # deterministic, collision-free assignments for the agents active now
    assign, taken = {}, {k: set(v) for k, v in busy.items()}
    review_slots = [[cl, min(2, reviews_needed(cl)) - len(busy.get(f"R:{cl['key']}", set()))]  # at most 2 at once
                    for cl in pending]
    max_reviewers = max(1, len(active) - max(1, len(active) // 4)) if pressure >= 1 else max(1, math.ceil(len(active) / 2))
    qs = [c for c in items if c.get("kind") == "question"]
    tried = {}
    for c in recent:
        if c.get("task") and c.get("kind") != "intent":
            tried.setdefault(c["task"], []).append(c)
    qs.sort(key=lambda c: (-c.get("priority", 3), len(tried.get(f"Q:{c.get('slug') or c['id']}", [])), c["_t"]))
    open_tasks = [f"C:{ch['id']}" for ch in challenges if not ch["achieved"]] + [f"Q:{c.get('slug') or c['id']}" for c in qs]
    syn_given = not syn_due or "SYN" in busy
    syn_order = sorted([a for a in active if a not in campaign],
                       key=lambda a: max([c["_t"] for c in syn if c["author"] == a], default=parse_t(LAB_START)))
    lit_given = not lit_due or "LIT" in busy
    lit_order = sorted([a for a in active if a not in campaign and (syn_given or a != syn_order[0])],
                       key=lambda a: (a in focus, max([c["_t"] for c in lit if c["author"] == a], default=parse_t(LAB_START)), a))
    n_rev = 0
    assigned_audits = set()
    n_audit = sum(1 for t in busy if t.startswith("A:"))
    for a in sorted(active, key=lambda a: (a in focus, a)):  # agents without an exploration focus review first
        if a in campaign:
            assign[a] = (campaign[a], "your campaign")
            continue
        if not syn_given and syn_order and a == syn_order[0]:
            assign[a] = ("SYN", "synthesis due")
            syn_given = True
            continue
        if n_audit < MAX_AUDITS:
            k = next((k for k in audits_due if f"A:{k}" not in busy and f"A:{k}" not in assigned_audits
                      and a != claims[k]["author"] and a not in claims[k]["lineage"] and a not in claims[k]["votes"]), None)
            if k is not None:
                assign[a] = (f"A:{k}", "audit of a large claim")
                assigned_audits.add(f"A:{k}")
                n_audit += 1
                continue
        if not lit_given and lit_order and a == lit_order[0]:
            assign[a] = ("LIT", "literature check due")
            lit_given = True
            continue
        if n_rev < max_reviewers:
            slot = next((s for s in review_slots if s[1] > 0 and s[0]["author"] != a and a not in s[0]["lineage"]
                         and a not in s[0]["votes"]), None)
            if slot is not None:
                slot[1] -= 1
                assign[a] = (f"R:{slot[0]['key']}", "review")
                n_rev += 1
                continue
        if a in focus:
            assign[a] = (f"F:{focus[a]}", "your exploration focus")
            continue
        t = next((t for t in open_tasks if t not in taken), None)
        if t:
            taken.setdefault(t, set()).add(a)
            assign[a] = (t, "open task")
        else:
            assign[a] = ("explore", "free exploration")

    # ---- progress replay (incremental: history is fixed by first-seen times)
    prog_f = HERE / "progress.json"
    try:
        stored = json.loads(prog_f.read_text()) if prog_f.exists() else {}
    except json.JSONDecodeError:
        stored = {}
    same = isinstance(stored, dict) and stored.get("version") == SCORE_VERSION
    series = stored["series"] if same and not rebuild else []  # scoring changed: replay the whole history
    last = parse_t(series[-1]["t"]) if series else None
    for t in sorted({c["_t"] for c in items}):
        if last is not None and t <= last:
            continue
        cl_t, _, _ = derive(items, until=t, canaries=canaries)
        s, _, _ = summary_score(cl_t)
        prior = [c for c in items if c["_t"] <= t and not c.get("_seed")]
        series.append({"t": fmt_t(t), **s, "contributions": len(prior),
                       "cpu_hours": round(sum(c["compute"]["cpu_minutes"] for c in prior) / 60, 2)})
    prog_f.write_text(json.dumps({"version": SCORE_VERSION, "series": series}, indent=0, allow_nan=False) + "\n")
    plot(series)

    # ---- how much of P rests on any single claim, and how often reviewers support planted false claims
    loo = sc["P"]
    for k, cl in claims.items():
        if cl["status"] == "established" and not cl["finding"] and not cl["canary"]:
            loo = min(loo, len(score({kk: v for kk, v in claims.items() if kk != k})))
    can = [cl for cl in claims.values() if cl["canary"] and cl["votes"]]
    can_rate = (sum(1 for cl in can if any(v["supported"] for v in cl["votes"].values())) / len(can)) if can else None

    # ---- ledger.json (compact; verdict contents of undecided claims are left out to limit anchoring)
    def claim_rec(cl):
        r = {k: cl[k] for k in ("key", "contribution", "author", "class", "title", "status", "rung", "world", "dir",
                                 "seed_status", "requires", "need", "n_votes")}
        r.update(claimed="".join(cl["claimed"]), t=fmt_t(cl["t"]), reviews_needed=reviews_needed(cl))
        if cl["status"] in ("established", "contradicted", "weak") and not cl["canary"]:
            r.update(held=caps_of(cl["held"]), scored=caps_of(cl["scored"]), by_construction=caps_of(cl["bc"]),
                     bd=cl["bd"], per=cl["per"])
            r["reviews"] = [{"review": v["review"], "author": v["author"], "verdict": v["verdict"],
                             "supported": "".join(sorted(v["supported"])), "replicated": v["replicated"]}
                            for v in cl["votes"].values()]
        return r
    ledger = {"generated": fmt_t(now), "score": sc, "P_leave_one_out": loo, "active_agents": active,
              "claims": [claim_rec(cl) for cl in sorted(claims.values(), key=lambda c: c["t"])],
              "contributions": [{"id": c["id"], "kind": c.get("kind"), "author": c.get("author"), "mode": c.get("mode"),
                                 "class": c.get("class"), "task": c.get("task"), "title": c.get("title", ""),
                                 "first_seen": fmt_t(c["_t"])} for c in recent],
              "assignments": {a: t for a, (t, _) in assign.items()},
              "frontier": [caps_of(m) for m in maxi], "problems": problems[-50:]}
    (HERE / "ledger.json").write_text(json.dumps(ledger, separators=(",", ":"), default=str) + "\n")

    def where(cl):
        return f"`{cl['dir'] or cl['world'] or ''}`"

    def who(cl):
        return "lab 1" if cl["seed_status"] or cl["author"] == "lab1" else cl["author"]

    def row(cl, s=None):
        st = s or (caps_of(cl["scored"]) if cl["status"] == "established" else "".join(cl["claimed"]))
        return (f"| `{st}` | {cl['class']} | {(cl['title'] or cl['statement'])[:90]} | "
                f"{cl['status']}{' (BD)' if cl['bd'] else ''} | {who(cl)} | {where(cl)} |")

    # ---- STATE.md
    S = ["# State of the field", "",
         f"Generated {fmt_t(now)} from the ledger by `collective/build.py`. Do not edit by hand. Syntheses are summaries, not evidence.", "",
         f"**Score.** Reach P = **{sc['P']}** illuminated capability sets; beyond diffusion P_BD = **{sc['P_BD']}**; "
         f"breadth Q = **{sc['Q']}**; mechanisms and laws K = **{sc['K']}**; corrections C = **{sc['C']}**. "
         f"With provisional claims P would be {sc['P_prov']}; removing the single most important established claim leaves "
         f"P = {loo}. Definitions: [SCORE.md](SCORE.md)." + (f" Canary false-support rate: {can_rate:.0%}." if can_rate is not None else ""), "",
         f"**Activity.** {len(recent)} contributions since the collective started; {len(active)} agents active (published in "
         f"the last 90 minutes, session not ended: {', '.join(active) or 'none'})"
         + (f"; sessions ended recently: {', '.join(left)}" if left else "")
         + f"; {cpu:.1f} CPU hours reported; {len(pending)} claims need reviews.", "",
         "![progress](progress.png)", ""]
    if last_syn:
        S += [f"## Latest synthesis ({fmt_t(last_syn['_t'])}, {last_syn.get('author')})", "", last_syn.get("summary", "").strip(), ""]
        cited = set(re.findall(r"\d{8}T\d{4}-c\d+-[a-z0-9-]+", json.dumps(last_syn, default=str)))
        unreviewed = sorted(k.split("#")[0] for k, cl in claims.items() if cl["contribution"] in cited and cl["status"] != "established")
        if unreviewed:
            S += [f"*Note: this synthesis cites claims that are not established: {', '.join(sorted(set(unreviewed))[:6])}.*", ""]
        body = LAB / last_syn.get("_dir", "") / "synthesis.md"
        if body.is_file() and not body.is_symlink():
            with body.open(errors="replace") as fh:
                S += [fh.read(6000).strip(), ""]
    # ---- literature: prior art for new results, and ideas that came from published work
    by_id = {c["id"]: c for c in items}
    lit_ids = {c["id"] for c in lit}
    lit_qs = [c for c in recent if c.get("kind") == "question" and ref_ids(c, set(by_id)) & lit_ids]
    lit_tasks = {f"Q:{q.get('slug') or q['id']}" for q in lit_qs}
    lit_roots = lit_ids | {q["id"] for q in lit_qs}
    from_lit = [cl for cl in claims.values() if cl["status"] == "established" and not cl["seed_status"] and (
        by_id.get(cl["contribution"], {}).get("task") in lit_tasks or ancestors(cl["contribution"], by_id) & lit_roots)]
    S += ["## Literature", ""]
    if last_lit:
        S += [f"Last check {fmt_t(last_lit['_t'])} by {last_lit.get('author')}: {last_lit.get('summary', '').strip()[:900]}", "",
              f"{len(lit)} literature checks; {len(lit_qs)} questions raised from them, {sum(1 for t in lit_tasks if tried.get(t))} "
              f"attempted; {len(from_lit)} established results descend from them.", ""]
        seen, rows = set(), []
        for c in reversed(lit):
            for x in c.get("prior_art", []):
                key = text(x.get("result")).strip()
                if key and key not in seen:
                    seen.add(key)
                    rows.append(f"| {key[:70]} | {text(x.get('relation'))[:12]} | {text(x.get('nearest'))[:110]} | `{c['_dir']}` |")
        if rows:
            S += ["Prior art for our results (latest check first):", "", "| Result | Relation | Nearest published work | Where |",
                  "|---|---|---|---|"] + rows[:12] + [""]
    else:
        S += ["No literature check yet" + (" (task `LIT` is due)." if lit_due else "."), ""]
    S += ["## Grand challenges", "", "| Challenge | Target | Status |", "|---|---|---|"]
    def met(k):
        st = audit_status(k)
        if st is None and claims[k]["seed_status"]:
            return f"{k} (lab 1 committee)"
        return f"{k} ({'audited' if st == 'passed' else 'disputed by audit' if st == 'disputed' else 'audit pending'})"
    S += [f"| {ch['title']} | `{ch.get('target', '')}`{' (BD)' if ch.get('bd') else ''} | "
          f"{'achieved: ' + ', '.join(met(k) for k in ch['achieved'][:2]) if ch['achieved'] else 'open'} |" for ch in challenges] or ["| none | | |"]
    n_pass = sum(1 for k in large if audit_status(k) == "passed")
    n_disp = [k for k in claims if audit_status(k) == "disputed"]
    S += ["", f"**Audits.** Large claims (a grand challenge met, 4 or more capabilities besides S, or beyond diffusion) get an "
          f"independent audit (PROTOCOL.md): {n_pass} passed, {len(audits_due)} pending"
          + (f"; disputed by audit: {', '.join(n_disp[:6])}" if n_disp else "") + "."]
    S += ["", "## Frontier", "", "The largest established capability sets, by-construction capabilities removed (codes: [SCORE.md](SCORE.md)).", "",
          "| Set | Class | Result | Status | By | Where |", "|---|---|---|---|---|---|"]
    for m in maxi[:20]:
        S += [row(cl, caps_of(m)) for cl in est[m][:2]]
    gal = [c for c in recent if c.get("kind") in ("sighting", "world") and now - c["_t"] <= timedelta(hours=6)]
    S += ["", "## New dynamics, last 6 hours", ""]
    for c in gal[-12:]:
        imgs = [p for p in c.get("evidence", []) if str(p).endswith((".png", ".jpg", ".gif"))]
        forks = sum(1 for o in recent if c["id"] in o.get("parents", []))
        img = f" ![]({c['_dir'].replace('collective/', '', 1)}/{imgs[0]})" if imgs else ""
        S.append(f"- **{c.get('title', c['id'])}** ({c.get('class', '?')}, {c['author']}, {forks} forks) "
                 f"{c.get('summary', '')[:220]} `{c['_dir']}`{img}")
    if not gal:
        S.append("- none yet")
    dec = sorted([cl for cl in claims.values() if not cl["seed_status"] and not cl["canary"] and cl["votes"]
                  and cl["status"] in ("established", "contradicted", "weak")],
                 key=lambda c: max(v["t"] for v in c["votes"].values()), reverse=True)[:15]
    S += ["", "## Recently decided", "", "| Set | Class | Result | Status | By | Where |", "|---|---|---|---|---|---|"]
    S += [row(cl) for cl in dec] or ["| | | nothing decided yet | | | |"]
    mech = [cl for cl in claims.values() if cl["finding"] and cl["status"] == "established" and not cl["canary"]]
    S += ["", "## Mechanisms, laws and negative results", ""]
    S += [f"- **{cl['title']}** ({cl['outcome'] or 'outcome not stated'}): {cl['statement'][:200]} {where(cl)}" for cl in mech[-15:]] or ["- none yet"]
    neg = [cl for cl in claims.values() if cl["status"] == "contradicted" and not cl["canary"]]
    S += ["", f"## Corrections ({len(neg)} contradicted claims)", ""]
    S += [f"- `{''.join(cl['claimed'])}` {(cl['title'] or cl['statement'])[:110]} ({who(cl)})" for cl in neg[-12:]] or ["- none"]
    tools = [c for c in recent if c.get("kind") == "tool"]
    S += ["", "## Toolbox", "", "Operators and trackers from the first lab: [TOOLBOX.md](TOOLBOX.md). Recently published tools:", ""]
    S += [f"- `{c['_dir']}`: {c.get('title', '')}" for c in tools[-10:]] or ["- none yet"]
    if problems:
        S += ["", "## Problems in contributions (latest 10)", ""] + [f"- {p}" for p in problems[-10:]]
    (HERE / "STATE.md").write_text("\n".join(S) + "\n")

    # ---- QUEUE.md
    Q = ["# Work queue", "", f"Generated {fmt_t(now)}. Rules: [PROTOCOL.md](PROTOCOL.md).", "",
         f"**Review pressure {pressure:.1f}** (reviews still needed per active agent). "
         + (f"**Exploration share {explore_share:.0%}** of non-review work in the last 3 hours (target {target_share:.0%})"
            + (": **exploration debt**, prefer new dynamics." if explore_share < target_share else ".")
            if explore_share is not None else "No exploration measured yet."), ""]
    if syn_due:
        Q += ["**Synthesis due** (task `SYN`), assigned below.", ""]
    if lit_due:
        Q += ["**Literature check due** (task `LIT`, see PROTOCOL.md), assigned below.", ""]
    Q += ["## Assignments", "", "One distinct task per active agent. Take yours. If you are not listed, or cannot do it, take "
          "the first open task nobody holds and publish an intent.", "", "| Agent | Task | Why |", "|---|---|---|"]
    Q += [f"| {a} | `{t}` | {why} |" for a, (t, why) in assign.items()] or ["| (no active agents yet) | | |"]
    if audits_due:
        Q += ["## Audits due", "", f"Independent audits of large claims, at most {MAX_AUDITS} at a time (PROTOCOL.md, Audit).", ""]
        Q += [f"- `A:{k}` `{caps_of(claims[k]['scored'])}` {claims[k]['class']}: {(claims[k]['title'] or '')[:90]}"
              + (f"; in progress: {', '.join(sorted(busy['A:' + k]))}" if f"A:{k}" in busy else "") for k in audits_due[:10]] + [""]
    Q += ["", "## Grand challenges", ""]
    Q += [f"- `C:{ch['id']}` **{ch['title']}** (target `{ch.get('target', '')}`{', diffusion-tested' if ch.get('bd') else ''}). "
          f"Route: {ch.get('route', '')}" for ch in challenges if not ch["achieved"]] or ["- none open"]
    Q += ["", "## Claims and findings needing review", "",
          "| Task | Claimed | Class | Claim | Author | Status | Needs | Reviewing |", "|---|---|---|---|---|---|---|---|"]
    for cl in pending[:30]:
        task = f"R:{cl['key']}"
        need = needs_detail(cl) + (f"; lab 1 asked for: {cl['requires'][:120]}" if cl["requires"] else "")
        Q.append(f"| `{task}` | `{''.join(cl['claimed'])}` (+{potential(cl, cells)}) | {cl['class']} | "
                 f"{(cl['title'] or cl['statement'])[:70]} | {who(cl)} | {cl['status']} | {need} | {', '.join(sorted(busy.get(task, []))) or '-'} |")
    if not pending:
        Q.append("| | | | nothing waiting | | | | |")
    Q += ["", "## Next rung for each class", "", "| Class | Has | Next |", "|---|---|---|"]
    Q += [f"| {cls} | {', '.join('`' + caps_of(m) + '`' for m in has)} | {', '.join('`G:' + caps_of(m) + '`' for m in nxt)} |"
          for cls, has, nxt in ladders if cls != "reaction-diffusion"]
    rd = next((h for c, h, _ in ladders if c == "reaction-diffusion"), [])
    Q += ["| reaction-diffusion (baseline, not a target) | " + ", ".join("`" + caps_of(m) + "`" for m in rd) + " | |"]
    Q += ["", "## Open questions", "", "Highest priority first. Full text in `seed/questions.json` or the question's contribution.", ""]
    for c in qs[:15]:
        task = f"Q:{c.get('slug') or c['id']}"
        att = len(tried.get(task, []))
        Q.append(f"- `{task}` p{c.get('priority', 3)} `{''.join(c.get('target', []))}` {c.get('title', '')}"
                 + (f" ({att} attempts)" if att else "") + (f"; in progress: {', '.join(sorted(busy[task]))}" if task in busy else ""))
    unforked = [c for c in recent if c.get("kind") == "sighting" and now - c["_t"] <= timedelta(hours=12)
                and not any(c["id"] in o.get("parents", []) for o in recent)]
    if unforked:
        Q += ["", "## Sightings nobody has forked yet", ""] + [f"- `{c['_dir']}` {c.get('title', '')} ({c.get('class', '?')})" for c in unforked[-10:]]
    rec = read_imported()
    if rec["_deferred"] or rec["_bad_branches"]:
        Q += ["", "## Not imported: fix on your branch", ""] + [f"- `{k}`: {v}" for k, v in sorted(rec["_deferred"].items())[-15:]]
        Q += [f"- branch `{k}`: {v}" for k, v in sorted(rec["_bad_branches"].items())[-5:]]
    mine = {}
    for p in problems:
        m = re.search(r"-(c\d+)-", p)
        if m:
            mine.setdefault(m.group(1), []).append(p)
    if mine:
        Q += ["", "## Problems with your recent contributions", "",
              "These were imported but parts did not count. Fix them with a new contribution that names the old one in `parents`.", ""]
        for a in sorted(mine):
            Q += [f"- **{a}**: " + " / ".join(x[:160] for x in mine[a][-3:])]
    Q += ["", "## In progress", ""]
    Q += [f"- `{c['task']}` by {c['author']} since {fmt_t(c['_t'])}{' (campaign)' if c.get('campaign') else ''}: {c.get('title', '')[:80]}"
          for c in live] or ["- nothing announced"]
    (HERE / "QUEUE.md").write_text("\n".join(Q) + "\n")
    log(f"SCORE P={sc['P']} P_BD={sc['P_BD']} Q={sc['Q']} K={sc['K']} C={sc['C']} P_prov={sc['P_prov']} "
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
    for k, c, lab in (("P", "#0d7480", "reach P"), ("P_BD", "#b0561b", "beyond diffusion P_BD"),
                      ("Q", "#7a4fb0", "breadth Q"), ("P_prov", "#9aa5ab", "P incl. provisional")):
        ax[0].step(t, [s.get(k, 0) for s in series], where="post", color=c, label=lab)
    ax[0].set_title("capability reach")
    ax[0].legend(frameon=False, fontsize=7)
    for k, c, lab in (("K", "#1d7a45", "mechanisms and laws K"), ("C", "#a33b3b", "corrections C")):
        ax[1].step(t, [s.get(k, 0) for s in series], where="post", color=c, label=lab)
    ax[1].set_title("knowledge")
    ax[1].legend(frameon=False, fontsize=7)
    for a in ax:
        a.spines[["top", "right"]].set_visible(False)
        a.tick_params(labelsize=7)
        for lab in a.get_xticklabels():
            lab.set_rotation(30)
    fig.tight_layout()
    fig.savefig(HERE / "progress.png", dpi=90)
    plt.close(fig)


def check(path):
    """Validate one contribution directory before pushing, with the import's own rules. Returns the number of problems."""
    d = Path(path).resolve()
    try:
        c, errs = coerce(json.loads((d / "contribution.json").read_text()))
    except Exception as e:  # noqa: BLE001
        print(f"PROBLEM contribution.json: {type(e).__name__}: {e}")
        return 1
    if c is None:
        print("PROBLEM " + "; ".join(errs))
        return 1
    branch = subprocess.run(["git", "-C", str(d.parent), "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    worker = branch.split(BRANCH_PREFIX, 1)[1] if branch.startswith(BRANCH_PREFIX) else None
    if not worker:
        errs.append(f"you are on branch {branch!r}; agents push from {BRANCH_PREFIX}cNN")
    files = {str(f.relative_to(d)): f.stat().st_size for f in d.rglob("*") if f.is_file() and not f.is_symlink()}
    errs += [f"symlink not allowed: {f.relative_to(d)}" for f in d.rglob("*") if f.is_symlink()]

    def exists(p, kept):
        pre = f"collective/contrib/{d.name}/"
        if p.startswith(pre):
            q = p[len(pre):].rstrip("/")
            return q in kept or any(f.startswith(q + "/") for f in kept)
        return (LAB / p).exists()
    try:
        ids = known_ids()
    except Exception:  # noqa: BLE001
        ids = set()
    v_errs, hard, drop = validate(c, d.name, worker, files, exists, ids)
    errs += v_errs
    if c.get("kind") == "review":
        for v in c.get("verdicts", []):
            for x in v.get("supported", []):
                if not (v.get("observations") or {}).get(x):
                    errs.append(f"no observation for supported capability {x}: it will not count")
    for cl in c.get("claims", []):
        if len([x for x in cl["capabilities"] if x != "S"]) >= 3 and not cl.get("track"):
            errs.append(f"track missing in claim {cl['cid']}: with 3+ capabilities, name one individual that shows all of them")
    for f in drop:
        print(f"WARN {f} will not be imported (size or type)")
    hard_all = [e for e in errs if e.startswith(HARD)]
    for e in errs:
        print(("BLOCKS IMPORT " if e in hard_all else "PROBLEM ") + e)
    print("OK" if not errs else f"{len(errs)} problem(s), {len(hard_all)} of them block the import")
    return len(errs)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", metavar="DIR", help="validate one contribution directory and exit")
    ap.add_argument("--write", action="store_true", help="rebuild STATE.md, QUEUE.md, ledger.json and progress")
    ap.add_argument("--import-branches", action="store_true", help="librarian: import from agent branches, then rebuild")
    ap.add_argument("--rebuild", action="store_true", help="recompute the whole progress history")
    ap.add_argument("--canaries", help="JSON list of canary contribution ids (kept outside the repo)")
    ap.add_argument("--now", help="override the clock (UTC, e.g. 2026-10-25T07:30Z)")
    a = ap.parse_args()
    if a.check:
        sys.exit(1 if check(a.check) else 0)
    if not (a.write or a.import_branches):
        ap.error("nothing to do: use --check DIR (agents) or --write / --import-branches (librarian)")
    now = parse_t(a.now) if a.now else now_utc()
    canaries = frozenset(json.loads(Path(a.canaries).read_text())) if a.canaries else frozenset()
    prev = {}
    if (HERE / "ledger.json").exists():
        try:
            prev = {c["key"]: (c["status"], c.get("scored", "")) for c in json.loads((HERE / "ledger.json").read_text())["claims"]}
        except (KeyError, json.JSONDecodeError, TypeError):
            prev = {}
    if a.import_branches:
        try:
            import_branches(now=now if a.now else None)
        except Exception:  # noqa: BLE001 - keep rebuilding the state even if an import cycle fails
            print("Error during import:\n" + traceback.format_exc())
    try:
        items, problems = load(now)
        claims, sc = write_outputs(items, problems, now, canaries=canaries, rebuild=a.rebuild)
    except Exception:  # noqa: BLE001 - make a stall visible to every agent instead of freezing silently
        tb = traceback.format_exc()
        print("Error during build:\n" + tb)
        banner = f"**Librarian error at {fmt_t(now)}; this file may be stale.** {tb.strip().splitlines()[-1][:200]}\n\n"
        for f in ("STATE.md", "QUEUE.md"):
            p = HERE / f
            old = p.read_text() if p.exists() else ""
            p.write_text(banner + re.sub(r"^\*\*Librarian error.*?\n\n", "", old, flags=re.S))
        sys.exit(1)
    for k, cl in claims.items():
        old = prev.get(k, ("new", ""))
        if cl["canary"] or (old[0] == "new" and cl["seed_status"]):
            continue
        if old[0] != cl["status"] or old[1] != caps_of(cl["scored"]):
            print(f"STATUS {k} {old[0]} -> {cl['status']} `{caps_of(cl['scored'])}`")
