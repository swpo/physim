"""pack_rollout -- the PUBLICATION FOLDER of one rollout of the request route, finished or interrupted.

    python -B tools/pack_rollout.py --request JOB.json --pilot DIR [--out DIR]

Reads <pilot>/rollouts/<job_id>/ (what tools/vfrun.py wrote) and the job's instance in <pilot>/store, and writes
a NEW folder (default <pilot>/publish/<job_id>/; it must not exist):

  status.json             what ran and how it ended: stages, stop condition, error types, reward, laboratory
                          counters, box caps, limits, the counted cost and its bound, what is missing
  transcript.md           the whole conversation, readable (every message, tool call and tool result)
  trace.redacted.jsonl    the saved trace with credential-like FIELDS removed by name
  lab_log.jsonl           the laboratory's own log: one line per request (operation, verdict, ticks, nats, time)
  grades.json             per exam item: failed or not, the fallback reason, the energy score per cell, CPU seconds
  reference.json          the reference table of the scripted policies on the same instance
  usage.json              every HTTP attempt to the provider as the spend meter counted it, the totals, the prices
                          as listed at run start and the bounds
  submission/, submission.json   the frozen submission that was graded (regular files; the capture's manifest)
  request.json, config.toml, resolved.toml, model_entry.json     what was asked for and what it resolved to
  key_scan.json           the key scan: file names and counts only
  PILOT_NEVER_REUSE_AS_EXAM.txt, MANIFEST.json (sha256 and size of every file; what was left out and why)

Rules:
  * The model's text is DATA: nothing from the trace or from submission/ is executed, imported or evaluated.
  * Before anything is written, every candidate file is scanned for (a) the VALUES of PRIME_API_KEY, HF_TOKEN and
    WANDB_API_KEY of this process's environment, plain and base64, (b) generic credential shapes (bearer tokens,
    private keys, well-known key prefixes), (c) the instance's secret and hidden parameters. A file with a hit
    is LEFT OUT and listed in MANIFEST.json and key_scan.json (names and counts; never the value); it stays in
    the pilot folder. No credential file is opened, `~/.prime` least of all.
  * Machine details are replaced by value in every text file: the home folder, the pilot folder, the study
    folder, the host name, and the value of PRIME_TEAM_ID.
  * At most 20 MB per file and 50 MB in all; what does not fit is left out and listed.
  * Nothing is deleted or changed in the pilot folder; the output folder is created and never overwritten.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import socket
import stat
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

MARK = "PILOT_NEVER_REUSE_AS_EXAM"
MAX_FILE, MAX_TOTAL = 20 << 20, 50 << 20
CRED_ENV = ("PRIME_API_KEY", "HF_TOKEN", "WANDB_API_KEY")
CRED_KEY = re.compile(r"(?i)(api[-_]?key|authorization|bearer|passw(or)?d|cookie|credential|private[-_]?key|"
                      r"(access|refresh|auth|id|session)[-_]?token|secret|x-prime-team-id|team[-_]?id|user[-_]?id|user[-_]?name)")
CRED_KEY_KEEP = {"secret_commitment", "api_key_var", "has_authorization"}
REMOVED = "[removed: credential-like field]"
GENERIC = {
    "bearer token": re.compile(rb"(?i)bearer\s+[A-Za-z0-9._~+/=-]{24,}"),
    "private key block": re.compile(rb"-----BEGIN [A-Z ]{0,30}PRIVATE KEY-----"),
    "sk- key": re.compile(rb"\bsk-[A-Za-z0-9_-]{24,}"),
    "hf_ token": re.compile(rb"\bhf_[A-Za-z0-9]{30,}"),
    "github token": re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{36,}"),
    "aws access key id": re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    "slack token": re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    "json web token": re.compile(rb"\beyJ[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{8,}"),
    "basic auth in a url": re.compile(rb"[a-z][a-z0-9+.-]{1,12}://[^/\s:@]{1,64}:[^/\s:@]{8,}@"),
}


# ----------------------------------------------------------------------------- needles and redaction
def credential_needles(environ=None) -> dict:
    """{label: bytes} of the credentials this process can see in its ENVIRONMENT (never printed, never written)."""
    environ = os.environ if environ is None else environ
    out = {}
    for name in CRED_ENV:
        v = environ.get(name, "")
        if len(v) >= 8:
            out[name] = v.encode()
            out[name + " (base64)"] = base64.b64encode(v.encode()).rstrip(b"=")
    return out


def hidden_needles(hidden: str) -> dict:
    """The instance's secret and the first ten characters of each hidden parameter (as tools/run_report.py)."""
    try:
        with open(os.path.join(hidden, "instance.json")) as f:
            inst = json.load(f)
    except (OSError, ValueError):
        return {}
    out = {"instance secret": str(inst.get("secret_hex", "")).encode()} if len(str(inst.get("secret_hex", ""))) >= 16 else {}
    for i, v in enumerate(inst.get("theta") or []):
        try:
            out[f"hidden parameter {i}"] = repr(float(v))[:10].encode()
        except (TypeError, ValueError):
            pass
    return out


def machine_values(pilot: str, environ=None) -> list[tuple[bytes, bytes]]:
    """(value, replacement) pairs for details of this machine and account, longest first."""
    environ = os.environ if environ is None else environ
    pairs = [(os.path.abspath(pilot), "<pilot>"), (ROOT, "<vfport>"), (os.path.realpath(ROOT), "<vfport>"),
             (os.path.expanduser("~"), "<home>"), (os.path.realpath(os.path.expanduser("~")), "<home>")]
    host = socket.gethostname()
    if len(host) >= 4:
        pairs.append((host, "<host>"))
    if len(environ.get("PRIME_TEAM_ID", "")) >= 6:
        pairs.append((environ["PRIME_TEAM_ID"], "[removed: account identifier]"))
    seen, out = set(), []
    for value, to in sorted(pairs, key=lambda x: -len(x[0])):
        if len(value) >= 4 and value != "/" and value not in seen:
            seen.add(value)
            out.append((value.encode(), to.encode()))
    return out


def scrub(data: bytes, pairs) -> tuple[bytes, int]:
    n = 0
    for value, to in pairs:
        c = data.count(value)
        if c:
            n += c
            data = data.replace(value, to)
    return data, n


def scan(data: bytes, cred: dict, hidden: dict) -> dict:
    """{label: count} of everything found in one blob; empty = clean."""
    hits = {}
    for label, v in {**cred, **hidden}.items():
        c = data.count(v) if v else 0
        if c:
            hits[label] = c
    for label, pattern in GENERIC.items():
        c = len(pattern.findall(data))
        if c:
            hits[label] = c
    return hits


def redact(o, removed: list, path=""):
    """A copy of a JSON value in which every value under a credential-like KEY is replaced (rollouts/tools/
    extract.py). Token counts are not credentials; `secret_commitment` is public."""
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            if isinstance(k, str) and CRED_KEY.search(k) and k not in CRED_KEY_KEEP and not re.search(r"(?i)tokens?(_|$)|_tokens", k) \
                    and v not in (None, "", [], {}) and not isinstance(v, bool):
                removed.append(f"{path}/{k}")
                out[k] = REMOVED
            else:
                out[k] = redact(v, removed, f"{path}/{k}")
        return out
    if isinstance(o, list):
        return [redact(v, removed, f"{path}[]") for v in o]
    return o


# ----------------------------------------------------------------------------- the transcript (the model's text is data)
def fence(text) -> str:
    text = "" if text is None else str(text)
    n = max([3] + [len(m) + 1 for m in re.findall(r"`{3,}", text)])
    return "`" * n + "\n" + text + ("" if text.endswith("\n") else "\n") + "`" * n


def content_text(c) -> str:
    if c is None:
        return ""
    if isinstance(c, str):
        return c
    parts = []
    for p in c if isinstance(c, list) else [c]:
        if isinstance(p, dict) and p.get("type") == "text":
            parts.append(str(p.get("text", "")))
        else:
            parts.append(f"[content part of type {p.get('type') if isinstance(p, dict) else type(p).__name__}]")
    return "\n".join(parts)


def pretty_args(arguments) -> str:
    try:
        a = json.loads(arguments)
    except (ValueError, TypeError):
        return fence(arguments)
    if isinstance(a, dict):
        blocks = []
        for k, v in a.items():
            if isinstance(v, str) and ("\n" in v or len(v) > 100):
                blocks.append(f"`{k}`:\n\n{fence(v)}")
            elif isinstance(v, (dict, list)):
                blocks.append(f"`{k}`:\n\n{fence(json.dumps(v, indent=1))}")
            else:
                blocks.append(f"`{k}`: `{json.dumps(v)}`")
        return "\n\n".join(blocks) if blocks else "(no arguments)"
    return fence(json.dumps(a, indent=1))


def transcript(tr: dict, head: str) -> tuple[str, dict]:
    nodes, calls = tr.get("nodes") or [], tr.get("calls") or []
    call_of = {c.get("node"): (i, c) for i, c in enumerate(calls) if isinstance(c, dict) and c.get("node") is not None}
    t0 = (tr.get("timing") or {}).get("start") or 0
    out, tool_counts, turn = [head], {}, 0
    tools = tr.get("tools") or []
    if tools:
        out.append("## Tools offered to the model\n")
        for t in tools:
            name = (str(t.get("namespace")) + "." if t.get("namespace") else "") + str(t.get("name"))
            out.append(f"### `{name}`\n\n{fence(t.get('description') or '')}\n\nparameters:\n\n{fence(json.dumps(t.get('parameters'), indent=1))}\n")
    out.append("## Conversation\n")
    for i, n in enumerate(nodes):
        m = (n or {}).get("message") or {}
        role, ts = m.get("role"), (n or {}).get("timestamp")
        when = f"t = {ts - t0:.0f} s" if isinstance(ts, (int, float)) and t0 else ""
        if role == "assistant":
            if n.get("sampled"):
                turn += 1
            ci = call_of.get(i)
            u = (ci[1].get("usage") or {}) if ci else {}
            usage = (f"; call {ci[0] + 1}: {(u.get('prompt_tokens') or 0) + (u.get('cached_input_tokens') or 0)} tokens in "
                     f"({u.get('cached_input_tokens') or 0} cached), {u.get('completion_tokens')} out"
                     f"{', ' + str(u.get('reasoning_tokens')) + ' reasoning' if u.get('reasoning_tokens') else ''}, "
                     f"finish `{ci[1].get('finish_reason')}`") if ci else ""
            out.append(f"### [{i}] assistant, turn {turn} ({when}{usage})\n")
            if m.get("reasoning_content"):
                out.append("reasoning:\n\n" + fence(m["reasoning_content"]) + "\n")
            if m.get("content"):
                out.append(fence(content_text(m["content"])) + "\n")
            for c in m.get("tool_calls") or []:
                name = (str(c.get("namespace")) + "." if c.get("namespace") else "") + str(c.get("name"))
                tool_counts[name] = tool_counts.get(name, 0) + 1
                out.append(f"**tool call** `{name}` (id `{c.get('id')}`)\n\n{pretty_args(c.get('arguments'))}\n")
            if not (m.get("content") or m.get("tool_calls") or m.get("reasoning_content")):
                out.append("(empty message)\n")
        elif role == "tool":
            out.append(f"### [{i}] tool result{' `' + str(m['name']) + '`' if m.get('name') else ''} (for `{m.get('tool_call_id')}`; {when})\n\n"
                       + fence(content_text(m.get("content"))) + "\n")
        else:
            out.append(f"### [{i}] {role} ({when})\n\n" + fence(content_text(m.get("content"))) + "\n")
    failed = [(i, c) for i, c in enumerate(calls) if isinstance(c, dict) and c.get("error")]
    if failed:
        out.append("## Model calls that ended in an error\n")
        for i, c in failed:
            out.append(f"- call {i + 1}: `{(c.get('error') or {}).get('type')}` (status {(c.get('error') or {}).get('status_code')})\n")
    return "\n".join(out), {"turns": turn, "tool_calls_by_name": tool_counts, "nodes": len(nodes), "model_calls": len(calls),
                            "model_calls_with_error": len(failed)}


# ----------------------------------------------------------------------------- reading the run
def read_json(path: str):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def read_jsonl(path: str) -> list:
    rows = []
    try:
        with open(path) as f:
            for line in f:
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    rows.append({"unreadable_line": True})
    except OSError:
        return []
    return rows


def plain_file(path: str, limit: int = MAX_FILE) -> bytes | None:
    """The bytes of a regular file that is not a link, or None (missing, special, or above `limit`)."""
    try:
        st = os.lstat(path)
        if not stat.S_ISREG(st.st_mode) or st.st_size > limit:
            return None
        with open(path, "rb") as f:
            return f.read(limit + 1)[:limit]
    except OSError:
        return None


def lab_lines(path: str) -> list[dict]:
    """The laboratory's log, one compact line per request. The worker-side detail (tracebacks, paths) stays in
    the store; the error text of a rejected request is what the agent itself was told."""
    keep = ("t", "op", "ok", "kind", "ticks", "ticks_used", "total_nats", "seconds")
    out = []
    for r in read_jsonl(path):
        row = {k: r.get(k) for k in keep if k in r}
        if r.get("error") and r.get("kind") != "infrastructure":
            row["error"] = str(r["error"])[:200]
        out.append(row)
    return out


def grades(hidden: str, name: str) -> dict | None:
    rec = read_json(os.path.join(hidden, "grades", f"{name}.json"))
    if rec is None:
        return None
    out = {"record": {k: rec[k] for k in sorted(rec) if k not in ("detail", "errors", "fallback_items")},
           "n_errors": len(rec.get("errors") or [])}
    reasons = {int(r["item"]): str(r.get("reason"))[:60] for r in rec.get("fallback_items") or [] if isinstance(r, dict) and "item" in r}
    try:
        import numpy as np
        z = np.load(os.path.join(hidden, "grades", f"{name}.npz"))
        es, failed, cpu = np.asarray(z["es"], float), np.asarray(z["failed"], bool), np.asarray(z["cpu"], float)
        out["items"] = [{"item": i, "failed": bool(failed[i]), "fallback_reason": reasons.get(i),
                         "energy_score_by_cell": [round(float(x), 6) for x in es[i]], "cpu_s": round(float(cpu[i]), 4)}
                        for i in range(es.shape[0])]
    except Exception as e:                                   # no numpy here, or no per-item file: the record alone
        out["items"], out["items_unavailable"] = None, type(e).__name__
        out["fallback_items"] = [{"item": i, "reason": r} for i, r in sorted(reasons.items())]
    return out


def usage_record(spend_rows: list, entry, bounds: dict | None) -> dict:
    meter = next((r for r in spend_rows if r.get("event") == "meter"), None)
    sent = {r.get("n"): r for r in spend_rows if r.get("event") == "sent"}
    settled = {r.get("n"): r for r in spend_rows if r.get("event") == "settled"}
    calls = []
    for n in sorted(sent):
        s, e = sent[n], settled.get(n)
        row = {"attempt": n, "prompt_bound_tokens": s.get("prompt_bound"), "bound_from": s.get("bound_from")}
        if e is None:
            row.update(settled=False, usd=meter["worst_call_usd"] if meter else None, basis="worst case: never settled (the process ended with it in flight)")
        else:
            row.update(settled=True, **{k: e.get(k) for k in ("usd", "basis", "outcome", "prompt_tokens", "cached_tokens", "completion_tokens",
                                                              "reasoning_tokens", "seconds", "over_the_reply_cap", "over_the_prompt_bound") if k in e})
        calls.append(row)
    total = sum(c["usd"] or 0.0 for c in calls)
    return {"marker": MARK, "meter": meter, "attempts": len(calls), "counted_usd": total if meter else None,
            "worst_case_calls": sum(1 for c in calls if str(c.get("basis", "")).startswith("worst case")),
            "tokens": {k: sum(c.get(k) or 0 for c in calls) for k in ("prompt_tokens", "cached_tokens", "completion_tokens", "reasoning_tokens")},
            "refused": [{"condition": r.get("condition"), "detail": r.get("detail")} for r in spend_rows if r.get("event") == "refused"][:20],
            "bounds": bounds, "model_entry": entry,
            "within_the_bound": None if not meter else total <= meter["bound_on_the_bill_usd"] + 1e-9,
            "how_to_reconcile": "counted_usd is the sum of the per-attempt figures above: listed prices times reported tokens, the provider's own "
                                "cost field where it was higher, one worst-case call for every attempt without complete usage. The provider's "
                                "bill may be lower, never higher if it bills what its usage says; a bill above counted_usd by more than "
                                "10 percent + $0.05 means the count is wrong: stop accepting requests.",
            "calls": calls}


def submission_files(folder: str) -> list[tuple[str, bytes | None]]:
    """(relative name, bytes or None) of the regular files of a captured submission folder (already sanitised by
    physim2_env/capture.py: plain names, no links). At most 2,000 files."""
    out = []
    for base, dirs, names in os.walk(folder):
        dirs[:] = sorted(d for d in dirs if not os.path.islink(os.path.join(base, d)))
        for nm in sorted(names):
            rel = os.path.relpath(os.path.join(base, nm), folder)
            if len(out) < 2000 and re.fullmatch(r"[A-Za-z0-9._+=@,/-]{1,300}", rel) and ".." not in rel.split("/"):
                out.append((rel, plain_file(os.path.join(base, nm))))
    return out


# ----------------------------------------------------------------------------- the pack
def pack(request_path: str, pilot: str, out_dir: str | None = None, environ=None) -> dict:
    import check_request as CR
    req = CR.read_request(request_path)
    p = dict(CR.require_pilot(pilot), **CR.pilot_paths(pilot, req["job_id"]))
    if not os.path.isdir(p["job"]) or os.path.islink(p["job"]):
        raise CR.Refused("this job has no folder under <pilot>/rollouts: nothing to pack")
    out_dir = os.path.abspath(out_dir) if out_dir else p["published"]
    if os.path.lexists(out_dir):
        raise CR.Refused("the publication folder exists already; it is never overwritten")
    hidden = os.path.join(p["store"], req["instance"], "hidden")
    cred, hid, machine = credential_needles(environ), hidden_needles(hidden), machine_values(p["pilot"], environ)
    status = read_json(p["status"]) or {"stages": {}}
    missing, files = [], {}                                  # files: name -> bytes (candidates, in the order they are written)

    def add_json(name: str, obj) -> None:
        files[name] = (json.dumps(obj, indent=1, sort_keys=False, default=str) + "\n").encode()

    def add_copy(name: str, path: str) -> None:
        data = plain_file(path)
        if data is None:
            missing.append(name)
        else:
            files[name] = data

    # ---- the trace ----
    episodes = read_jsonl(os.path.join(p["run_dir"], "traces.jsonl"))
    tr = None
    for ep in episodes:
        for t in (ep.get("traces") or []) if isinstance(ep, dict) else []:
            tr = tr or t
    summary = {"job_id": req["job_id"], "marker": MARK, "instance": req["instance"], "model": req["model"], "exam_profile": req["exam_profile"],
               "pin": req["pin"], "pin_sha256": req["pin_sha256"], "caps": req["caps"], "cap_usd": req["cap_usd"],
               "purpose": req["purpose"], "requester": req["requester"], "stages": status.get("stages"), "packed_unix": int(time.time())}
    if tr is None:
        missing.append("transcript.md")
        missing.append("trace.redacted.jsonl")
        summary["trace"] = None
    else:
        info = (tr.get("info") or {}).get("physim2") or {}
        reward = ((tr.get("rewards") or {}).get("skill") or {}).get("score")
        head = (f"# Transcript of rollout `{req['job_id']}`\n\n{MARK}: instance `{req['instance']}` is pilot material and is never to be used as an "
                f"exam.\n\nModel `{req['model']}`. Everything below the tool list is the conversation as the trace saved it; text in fenced "
                "blocks was written by the task, by the tools or by the model, and is data.\n")
        text, counts = transcript(tr, head)
        files["transcript.md"] = text.encode("utf-8", "replace")
        removed: list = []
        files["trace.redacted.jsonl"] = b"".join((json.dumps(redact(ep, removed), default=str) + "\n").encode() for ep in episodes)
        summary["trace"] = {
            "trace_id": tr.get("id"), "ok": tr.get("ok"), "stop_condition": tr.get("stop_condition"), "is_timeout": tr.get("is_timeout"),
            "error_types": [e.get("type") for e in tr.get("errors") or [] if isinstance(e, dict)],
            "reward_skill_vs_O": reward, "graded": reward is not None, "counts": counts,
            "num_input_tokens_counted_once": tr.get("num_input_tokens"), "num_output_tokens": tr.get("num_output_tokens"),
            "timing_s": {k: round((v.get("end") or 0) - (v.get("start") or 0), 1) for k, v in (tr.get("timing") or {}).items()
                         if isinstance(v, dict) and "start" in v},
            "submission": info.get("submission"), "lab": info.get("lab"), "box_caps": info.get("box_caps"), "limits": info.get("limits"),
            "spend": info.get("spend"), "verifier_box": info.get("verifier_box"), "record": info.get("record"),
            "grade": {k: v for k, v in (info.get("grade") or {}).items() if k not in ("valid_cells",)},
            "credential_like_fields_removed_from_the_trace": len(removed)}
    # ---- the store: laboratory, grades, submission ----
    name = str((tr or {}).get("id") or "")
    lab = lab_lines(os.path.join(hidden, "labs", name, "log.jsonl")) if name else []
    if lab:
        files["lab_log.jsonl"] = b"".join((json.dumps(r) + "\n").encode() for r in lab)
    else:
        missing.append("lab_log.jsonl")
    g = grades(hidden, name) if name else None
    if g is None:
        missing.append("grades.json")
    else:
        add_json("grades.json", dict(g, marker=MARK))
    add_copy("reference.json", p["reference"])
    spend_rows = read_jsonl(p["spend_log"])
    entry = read_json(p["model_entry"])
    ledger = [r for r in CR.ledger_rows(p) if r.get("job_id") == req["job_id"]]
    reserved = next((r for r in ledger if r.get("event") == "reserved"), None)
    add_json("usage.json", usage_record(spend_rows, entry, None if reserved is None else
                                        {k: reserved.get(k) for k in ("cap_usd", "worst_call_usd", "bound_usd", "crude_bound_usd", "prices_usd_per_mtok", "billed")}))
    summary["ledger"] = ledger
    final = os.path.join(p["store"], req["instance"], "captures", re.sub(r"[^A-Za-z0-9._-]", "_", name), "final") if name else ""
    sub_manifest = read_json(os.path.join(final, "submission.json")) if final else None
    if sub_manifest is None:
        missing.append("submission/")
    else:
        add_json("submission.json", sub_manifest)
        for rel, data in submission_files(os.path.join(final, "submission")):
            if data is None:
                missing.append("submission/" + rel)
            else:
                files["submission/" + rel] = data
    for fname, key in (("request.json", "request"), ("config.toml", "config"), ("resolved.toml", "resolved"), ("model_entry.json", "model_entry")):
        add_copy(fname, p[key])
    stopped = read_json(os.path.join(p["job"], "rollout.stopped.json"))
    if stopped is not None:
        summary["stopped"] = stopped
    summary["missing"] = sorted(set(missing))
    summary["complete"] = not summary["missing"] and bool(tr and tr.get("is_completed"))
    add_json("status.json", summary)
    files["PILOT_NEVER_REUSE_AS_EXAM.txt"] = (f"{MARK}: rollout {req['job_id']} ran on the pilot instance {req['instance']}. The instance and "
                                              "everything in this folder are public pilot material and are never to be used as an exam.\n").encode()

    # ---- scrub machine details, scan, apply the size caps ----
    kept, left_out, scan_rows, total, replaced = {}, [], [], 0, 0
    order = ["status.json", "PILOT_NEVER_REUSE_AS_EXAM.txt", "request.json", "config.toml", "resolved.toml", "model_entry.json", "usage.json",
             "grades.json", "reference.json", "lab_log.jsonl", "submission.json", "transcript.md", "trace.redacted.jsonl"]
    names = [n for n in order if n in files] + sorted(n for n in files if n not in order)
    for nm in names:
        data = files[nm]
        if not nm.startswith("submission/"):
            data, n = scrub(data, machine)
            replaced += n
        hits = scan(data, cred, hid)
        scan_rows.append({"file": nm, "bytes": len(data), "hits": hits})
        if hits:
            left_out.append({"file": nm, "why": "key scan: " + ", ".join(f"{k} x{v}" for k, v in sorted(hits.items()))})
        elif len(data) > MAX_FILE:
            left_out.append({"file": nm, "why": f"larger than {MAX_FILE} bytes"})
        elif total + len(data) > MAX_TOTAL:
            left_out.append({"file": nm, "why": f"the folder would exceed {MAX_TOTAL} bytes"})
        else:
            kept[nm] = data
            total += len(data)
    # everything else of the job folder is scanned too, for the report (it is not published)
    others = []
    for base, dirs, fnames in os.walk(p["job"]):
        dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(base, d))]
        for nm in fnames:
            data = plain_file(os.path.join(base, nm), 256 << 20)
            if data is not None:
                hits = {k: v for k, v in scan(data, cred, {}).items() if k in cred}
                if hits:
                    others.append({"file": os.path.relpath(os.path.join(base, nm), p["job"]), "hits": hits})
    key_scan = {"marker": MARK, "needles": {"credentials_from_the_environment": sorted(cred), "generic_shapes": sorted(GENERIC),
                                              "hidden_values_of_the_instance": len(hid)},
                "candidates_scanned": len(scan_rows), "candidates_with_hits": [r for r in scan_rows if r["hits"]],
                "machine_details_replaced": replaced, "left_out": left_out,
                "job_folder_files_with_a_credential": others,
                "verdict": "clean" if not any(r["hits"] for r in scan_rows) and not others else "HITS: see the lists; the files stay in the pilot folder"}
    kept["key_scan.json"] = (json.dumps(key_scan, indent=1) + "\n").encode()
    manifest = {"marker": MARK, "job_id": req["job_id"], "instance": req["instance"],
                "files": [{"path": nm, "bytes": len(d), "sha256": hashlib.sha256(d).hexdigest()} for nm, d in kept.items()],
                "left_out": left_out, "missing": summary["missing"], "total_bytes": sum(len(d) for d in kept.values()),
                "limits": {"max_file_bytes": MAX_FILE, "max_total_bytes": MAX_TOTAL}}
    # ---- write: a new folder, files created exclusively ----
    os.makedirs(os.path.dirname(out_dir), mode=0o700, exist_ok=True)
    os.mkdir(out_dir, 0o700)
    for nm, data in list(kept.items()) + [("MANIFEST.json", (json.dumps(manifest, indent=1) + "\n").encode())]:
        target = os.path.join(out_dir, *nm.split("/"))
        os.makedirs(os.path.dirname(target), mode=0o700, exist_ok=True)
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write(data)
    return {"out": out_dir, "files": len(kept) + 1, "total_bytes": manifest["total_bytes"], "left_out": left_out, "missing": summary["missing"],
            "key_scan": key_scan["verdict"], "credential_hits_in_candidates": sum(1 for r in scan_rows if any(k in cred for k in r["hits"])),
            "complete": summary["complete"]}


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="build the publication folder of one rollout (finished or interrupted)")
    ap.add_argument("--request", required=True)
    ap.add_argument("--pilot", required=True)
    ap.add_argument("--out", default=None, help="default: <pilot>/publish/<job_id> (must not exist)")
    a = ap.parse_args(argv)
    import check_request as CR
    try:
        got = pack(a.request, a.pilot, a.out)
    except CR.Refused as e:
        print("refused: " + str(e))
        return 2
    print(json.dumps({k: got[k] for k in ("files", "total_bytes", "left_out", "missing", "key_scan", "complete")}))
    return 0 if got["key_scan"] == "clean" else 3


if __name__ == "__main__":
    sys.exit(main())
