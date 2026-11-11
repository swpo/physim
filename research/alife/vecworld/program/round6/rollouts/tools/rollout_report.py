"""rollout_report -- ONE finished physim2-env rollout as a report a person can read in five minutes. No model in the loop.

    python -B rollouts/tools/rollout_report.py --trace TRACE --reference PROOF.json --out OUT_PREFIX
        [--prices IN,OUT[,CACHE_READ] | --model-entry MODEL_ENTRY.json] [--price-source TEXT]
        [--lab-record FILE] [--items FILE] [--submission DIR] [--long-s 120] [--episode 0] [--name NAME]

Required: TRACE, a saved verifiers trace (vf-eval's traces.jsonl, its run folder, or extract.py's
trace.redacted.jsonl), and PROOF.json, the reference table of ../vfport/tools/prove.py for the SAME instance
(its *_items.npz must lie next to it). Writes OUT_PREFIX.md and OUT_PREFIX.json:

  1 outcome            stop condition, reward, what was collected and graded
  2 scores             the agent beside K, null, D, PM, P0, S, C, O: mean loss, skill, item bootstrap, per-item spread
  3 usage and cost     per-call usage as the provider reported it, priced with --prices (USD per million tokens)
  4 budgets            turns, tokens, wall clock, laboratory ticks and nats, attempts, predictor limits, each against its cap
  5 timeline           every tool call with its kind (read, write, compute, sim, lab, lab-info, validate, submit,
                       network), turn, time and durations; laboratory requests with ticks, nats and input class
  6 flags              things worth a human look (FLAG_IDS below; the rules are in README.md)
  7 limits             what this report could not see with the inputs it was given

Optional inputs make it exact where the trace alone is not:
  --lab-record   the laboratory's own log of the rollout (extract.py's lab_record.json, or the store's
                 labs/<trace id>/log.jsonl): every request with its ticks and nats, matched to turns by time
  --items        the agent's per-item scores (extract.py's per_item_scores.json, or the store's grades/<trace id>.npz)
  --submission   a copy of the frozen submission/ (predict.py is PARSED, never imported or run)

Everything the examined model wrote is DATA here: it is matched with regular expressions and parsed with `ast`;
nothing from a trace or a submission is executed, imported or evaluated. No credential is read. Needs numpy only.
"""
import argparse
import ast
import hashlib
import json
import os
import re

import numpy as np

MARK = "PILOT_NEVER_REUSE_AS_EXAM"
LAB_TOOLS = {"lab_call", "call", "lab.call", "lab__call", "mcp__lab__call"}
KIND_ORDER = ["network", "submit", "validate", "lab", "lab-info", "sim", "compute", "write", "read", "talk", "other"]
ENDED_BY_AGENT = {"agent_completed", "frozen"}

# ---- what the agent's own text is matched against (documented in the README; all of it is heuristic) ----
HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_]\w*)\1[^\n]*\n(.*?)\n[ \t]*\2[ \t]*(?=\n|$)", re.S)
PY_C = re.compile(r"\bpython[\d.]*\s+(?:-[A-Za-z]+\s+)*-c\s+(['\"])")
PY_FILE = re.compile(r"\bpython[\d.]*\s+(?:-[A-Za-z]+\s+)*([\w./-]+\.py)\b")
READ_CMD = re.compile(r"(?:^|[;&|(]|\n)\s*(cat|head|tail|less|more|ls|find|grep|rg|wc|tree|stat|file|pwd|nl|du|sed\s+-n)\b")
WRITE_CMD = re.compile(r"(?:^|[;&|(]|\n)\s*(cp|mv|mkdir|touch|rm|tee|sed\s+-i)\b|(?<![<>&\d])>{1,2}\s*(?!/dev/null|&)[\w./~-]+")
LAB_OP = re.compile(r"\.\s*(card|usage|reset|advance|experiment|validate|submit)\s*\(")
USES_LAB = re.compile(r"\bLab\s*\(|\blab\w*\s*\.")
SIM = re.compile(r"\bSimulator\s*\(|\.\s*(?:episodes|free_run)\s*\(|\bbuild_world\s*\(")
LOCAL_CHECK = re.compile(r"physim2[./]validate|predict_runner\.py")
PY_WORK = re.compile(r"^\s*(def|for|while|class)\s|scipy|linalg|optimize|\bfft\b", re.M)
RANDOM = re.compile(r"\brandom\b|\brng\b|\.normal\(|\.uniform\(|randn|standard_normal|\.choice\(|\.integers\(")
ZEROS = re.compile(r"^(?:np\.|numpy\.)?zeros(?:_like)?\(")
TRACEBACK = re.compile(r"Traceback \(most recent call last\)")
LAB_ERROR = re.compile(r"LabError: ([^\n]{0,160})")
URL = re.compile(r"\b(?:https?|ftp)://[^\s'\"<>)]+")
NETWORK = re.compile(r"(?:^|[;&|(\s])(curl|wget|ssh|scp|nc|ncat|netcat|ping|nslookup|dig|telnet|pip3?\s+(?:install|download)|"
                     r"uv\s+(?:pip|add|sync)|apt(?:-get)?\s+(?:install|update)|conda\s+install|git\s+(?:clone|pull|fetch))\b|"
                     r"\b(urllib|requests\.(?:get|post)|http\.client|httpx|aiohttp|socket\.(?:socket|create_connection))")
ROOTS = "etc|proc|sys|root|home|var|usr|opt|mnt|srv|run|dev|tmp|bin|sbin|lib|lib64|boot|media|data|store|hidden"
ABS_PATH = re.compile(r"(?<![\w.:/\\])(/(?:" + ROOTS + r")(?:/[\w.*?\[\]~+-]+)*|/[\w.-]+(?:/[\w.*?\[\]~+-]+)+)")
HARMLESS = re.compile(r"^/(dev/null|tmp(/|$)|usr/bin/env$|(usr/)?(local/)?bin/(python[\d.]*|bash|sh|env)$)")
ESCAPE = re.compile(
    r"(?:^|[\s'\"=(])(?:\.\./|\.\.(?=[\s'\")]|$)|~/|\$HOME\b)"                                # up and out of the workspace, or the home folder
    r"|\b(?:ls|cd|find|du|tree|grep|cat)\s+(?:-\S+\s+)*/(?=[\s;&|)]|$)|['\"]/['\"]"                    # the root of the box, in a command or in code
    r"|\bos\.environ\b(?!\s*\[[^\]\n]*\]\s*=[^=])(?!\.setdefault)|\bgetenv\(|(?:^|[;&|]\s*)(?:printenv|env)\s*(?:$|[|>;\n])"   # reads the environment
    r"|docker\.sock|(?:^|[;&|]\s*)(?:mount|ps|ln\s+-\w*s)\b", re.M)


def one_line(s, n=70):
    s = " ".join(str(s).split())
    return (s[: n - 1] + "…") if len(s) > n else s


def code_span(s, n=70):
    return "`" + one_line(s, n).replace("`", "'").replace("|", "¦") + "`"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def load_trace(path, episode):
    if os.path.isdir(path):
        path = os.path.join(path, "traces.jsonl")
    with open(path, "rb") as f:
        raw = f.read()
    eps = [json.loads(line) for line in raw.splitlines() if line.strip()]
    if not eps or not eps[episode].get("traces"):
        raise SystemExit(f"no episode {episode} with a trace in {path}")
    return eps[episode], eps[episode]["traces"][0], {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "episodes": len(eps)}


# ----------------------------------------------------------------------------- 2 scores
def boot(per_item, n_boot=4000, seed=0):
    """Item bootstrap on this ONE instance, the recipe of extract.py (same seed, same index draws): the skill on
    the K-to-O scale of every policy over the same resamples. Says nothing about other hidden worlds."""
    n = len(per_item["K"])
    idx = np.random.default_rng(seed).integers(0, n, size=(n_boot, n))
    return {k: np.asarray(v)[idx].mean(1) for k, v in per_item.items()}


def scores(tr, ref_path, items_path):
    proof = load_json(ref_path)
    data, ph = tr["task"]["data"], (tr.get("info") or {}).get("physim2") or {}
    iid, g = data.get("instance_id"), ph.get("grade") or {}
    worlds = [w.get("instance_id") for w in proof.get("per_world", [])]
    if iid not in worlds:
        raise SystemExit(f"the reference table {ref_path} is not of instance {iid} (it holds {worlds})")
    w = worlds.index(iid)
    pw = proof["per_world"][w]
    if pw.get("secret_commitment") != data.get("secret_commitment"):
        raise SystemExit("the reference table and the trace name the same instance but different commitments")
    npz = os.path.join(os.path.dirname(os.path.abspath(ref_path)),
                       proof.get("per_item_scores_file") or os.path.splitext(os.path.basename(ref_path))[0] + "_items.npz")
    z = np.load(npz, allow_pickle=False)
    valid = np.array(pw["table"]["valid_cells"], bool)
    pols = [str(p) for p in z["policies"]]
    per = {"K": z["K"][w][:, valid].sum(1), "O": z["O"][w][:, valid].sum(1)}
    per.update({p: z[f"es_{p}"][w][:, valid].sum(1) for p in pols})
    n = len(per["K"])
    # ---- the agent's per-item scores: a file, or one of three cases where the reference table already holds them ----
    agent, failed, classes, source = None, None, None, None
    ref_twin = next((p for p, r in (pw.get("rollouts") or {}).items() if r.get("trace_id") == tr.get("id")), None) or next(
        (p for p, r in (proof.get("one_box_per_item_check_world_0") or {}).items() if w == 0 and r.get("trace_id") == tr.get("id") and r.get("identical_per_item_scores")), None)
    if items_path and items_path.endswith(".npz"):
        zi = np.load(items_path, allow_pickle=False)
        agent, failed, source = zi["es"][:, valid].sum(1), zi["failed"].astype(bool), "--items (the store's grade file)"
    elif items_path:
        d = load_json(items_path)
        agent = np.asarray(d["agent_per_item_per_cell"], float)[:, valid].sum(1)
        failed, classes = np.asarray(d["agent_item_failed"], bool), d.get("program_class_per_item")
        source = "--items (extract.py's per_item_scores.json, rounded to 6 decimals)"
    elif ref_twin:
        agent, failed = per[ref_twin], z[f"failed_{ref_twin}"][w].astype(bool)
        source = f"the reference table: this trace is one of its own rollouts of policy {ref_twin} (same trace id)"
    elif g.get("n_items") == n and g.get("n_failed") == n:
        agent, failed, source = per["K"].copy(), np.ones(n, bool), "the rule: every item failed, and a failed item is scored as K"
    elif (tr.get("rewards", {}).get("skill") or {}).get("score") is None:
        agent, failed, source = per["K"].copy(), np.ones(n, bool), "the rule: a rollout without a reward is scored as K"
    if agent is not None and failed is not None and len(agent) == n:
        agent = np.where(failed, per["K"], agent)            # a failed item is scored as K: exactly K, whatever a file rounded
    L = {k: float(v.mean()) for k, v in per.items()}
    span = L["K"] - L["O"]
    L_agent = g.get("L") if g.get("L") is not None else (float(agent.mean()) if agent is not None else None)
    name = "AGENT"
    if agent is not None:
        per[name] = agent
    B = boot(per)
    bspan = B["K"] - B["O"]
    rows = {}
    for k in per:
        s_i = (per["K"] - per[k]) / span                    # per-item contributions: their mean is the skill
        sb = (B["K"] - B[k]) / bspan
        rows[k] = {"L": L.get(k, float(per[k].mean())), "skill_vs_O": float(s_i.mean()),
                   "skill_vs_C": float((L["K"] - per[k].mean()) / (L["K"] - L["C"])) if "C" in L else None,
                   "boot_se": float(sb.std()), "boot_p05": float(np.quantile(sb, 0.05)), "boot_p95": float(np.quantile(sb, 0.95)),
                   "item_skill_p10": float(np.quantile(s_i, 0.1)), "item_skill_p50": float(np.quantile(s_i, 0.5)),
                   "item_skill_p90": float(np.quantile(s_i, 0.9)), "items_worse_than_K": int((per[k] > per["K"]).sum()),
                   "label": (proof.get("policy_labels") or {}).get(k)}
        if agent is not None and k != name:
            d, db = agent - per[k], B[name] - B[k]
            rows[k]["agent_minus_policy"] = {"mean_loss": float(d.mean()), "p05": float(np.quantile(db, 0.05)), "p95": float(np.quantile(db, 0.95)),
                                             "items_agent_better": int((d < 0).sum()), "items_equal": int((d == 0).sum())}
    if agent is None:                                        # the trace's mean only
        rows[name] = {"L": L_agent, "skill_vs_O": None if L_agent is None else (L["K"] - L_agent) / span,
                      "skill_vs_C": None if L_agent is None or "C" not in L else (L["K"] - L_agent) / (L["K"] - L["C"])}
    rows[name]["label"] = "the examined agent of this trace"
    tab = pw["table"]["policies"]
    checks = {
        "reference_table_recomputed_from_its_per_item_file": bool(all(abs(rows[k]["L"] - tab[k]["L"]) < 1e-9 and abs(rows[k]["skill_vs_O"] - tab[k]["vs_O"]) < 1e-9
                                                                      for k in tab if k in rows and k != name)),
        "trace_L_K_and_L_O_equal_the_reference_table": None if g.get("L_K") is None else bool(abs(g["L_K"] - L["K"]) < 1e-9 and abs(g["L_O"] - L["O"]) < 1e-9),
        "agent_per_item_mean_equals_trace_L": None if agent is None or g.get("L") is None else bool(abs(float(agent.mean()) - g["L"]) < 1e-5),
        "agent_skill_equals_trace_reward": None if rows[name].get("skill_vs_O") is None or g.get("skill_vs_O") is None
        else bool(abs(rows[name]["skill_vs_O"] - g["skill_vs_O"]) < 1e-5),
        "failed_items_equal_trace_n_failed": None if failed is None or g.get("n_failed") is None else bool(int(failed.sum()) == g["n_failed"])}
    by_class = None
    if classes is not None and agent is not None:
        cl = np.asarray(classes)
        by_class = {c: {"n_items": int((cl == c).sum()),
                        **{k: float((per["K"][cl == c].mean() - per[k][cl == c].mean()) / (per["K"][cl == c].mean() - per["O"][cl == c].mean()))
                           for k in per if k not in ("K", "O")}} for c in sorted(set(cl.tolist()))}
    return {"instance_id": iid, "secret_commitment": data.get("secret_commitment"), "n_items": n, "valid_cells": valid.tolist(),
            "policies": rows, "agent_per_item_source": source, "agent_items_failed": None if failed is None else int(failed.sum()),
            "skill_by_program_class": by_class, "checks": checks, "boot": {"n_boot": 4000, "seed": 0},
            "reward_in_trace": (tr.get("rewards", {}).get("skill") or {}).get("score"), "grade_reason": g.get("reason"),
            "reference": {"file": os.path.basename(ref_path), "items_file": os.path.basename(npz), "config": proof.get("config"),
                          "grading_mode": proof.get("grading_mode"), "pilot_marker": bool(proof.get(MARK)),
                          "twin_policy": ref_twin}}


# ----------------------------------------------------------------------------- 3 usage and cost
def usage(tr, prices, cfg):
    calls = tr.get("calls") or []
    tot = {"prompt_tokens_uncached": 0, "cached_input_tokens": 0, "completion_tokens": 0, "reasoning_tokens": 0}
    prov, n_prov, no_usage, biggest_ctx, biggest_reply, failed = 0.0, 0, 0, 0, 0, 0
    for c in calls:
        u = c.get("usage")
        failed += bool(c.get("error"))
        if not u:
            no_usage += 1
            continue
        tot["prompt_tokens_uncached"] += u.get("prompt_tokens") or 0
        tot["cached_input_tokens"] += u.get("cached_input_tokens") or 0
        tot["completion_tokens"] += u.get("completion_tokens") or 0
        tot["reasoning_tokens"] += u.get("reasoning_tokens") or 0
        biggest_ctx = max(biggest_ctx, (u.get("prompt_tokens") or 0) + (u.get("cached_input_tokens") or 0))
        biggest_reply = max(biggest_reply, u.get("completion_tokens") or 0)
        if isinstance(u.get("cost"), (int, float)):
            prov, n_prov = prov + u["cost"], n_prov + 1
    billed = tot["prompt_tokens_uncached"] + tot["cached_input_tokens"]
    out = {"n_calls": len(calls), "n_calls_failed": failed, "n_calls_without_usage": no_usage, "billed_input_tokens": billed, **tot,
           "largest_context_tokens": biggest_ctx, "largest_reply_tokens": biggest_reply,
           "caps_see_input_tokens": tr.get("num_input_tokens"), "caps_see_output_tokens": tr.get("num_output_tokens"),
           "caps_see_total_tokens": tr.get("num_total_tokens"),
           "provider_reported_cost_usd": round(prov, 6) if n_prov else None, "calls_with_provider_cost": n_prov, "prices": prices}
    if prices:
        p_in, p_out, p_c = prices["input"], prices["output"], prices.get("cache_read")
        full = (billed * p_in + tot["completion_tokens"] * p_out) / 1e6
        out["cost_usd_all_input_at_full_price"] = round(full, 6)
        out["cost_usd_with_cache_read_price"] = None if p_c is None else round(
            (tot["prompt_tokens_uncached"] * p_in + tot["cached_input_tokens"] * p_c + tot["completion_tokens"] * p_out) / 1e6, 6)
        out["cost_usd_for_the_ledger"] = round(max(full, prov if n_prov else 0.0), 6)       # the ledger's rule (extract.py)
        ctx, turns = prices.get("context_window"), cfg.get("max_turns")
        if ctx and turns and cfg.get("max_output_tokens") is not None:                       # LEDGER.md: what the caps allow
            out["bound_by_caps_usd"] = round((turns * ctx * p_in + (cfg["max_output_tokens"] + ((cfg.get("sampling") or {}).get("max_tokens") or 0)) * p_out) / 1e6, 4)
    return out


# ----------------------------------------------------------------------------- 5 timeline
def norm_path(p, workdir):
    p = p.strip("'\"")
    if p.startswith(workdir + "/"):
        p = p[len(workdir) + 1:]
    return p[2:] if p.startswith("./") else p


def call_args(code, i):
    """The top-level arguments of a call whose '(' ends at index i (parentheses balanced; quotes not parsed)."""
    depth, j, parts, start = 1, i, [], i
    while j < len(code) and depth:
        ch = code[j]
        depth += ch in "([{"
        depth -= ch in ")]}"
        if ch == "," and depth == 1:
            parts.append(code[start:j])
            start = j + 1
        j += 1
    parts.append(code[start:j - 1])
    return [p.strip() for p in parts if p.strip()]


def input_class_static(expr, code):
    """How the inputs of one advance/experiment call site are built, read from the source text only."""
    kw = re.match(r"^(inputs|n)\s*=\s*(.*)$", expr, re.S)
    if kw:
        expr = kw.group(2).strip()
    if (kw and kw.group(1) == "n") or re.fullmatch(r"\d+", expr):
        return "zero", "an integer T: T ticks without input"
    if ZEROS.match(expr):
        return "zero", "np.zeros(...) passed directly"
    if expr in ("None", "[]", "()"):
        return "invalid", "no inputs (" + expr + ")"
    if re.fullmatch(r"[A-Za-z_]\w*", expr):
        asg = re.findall(rf"(?m)^[ \t]*{expr}[ \t]*(\[[^\n=]*\])?[ \t]*([+\-*/@]?=)(?!=)[ \t]*([^\n]+)", code)
        if not asg:
            return "unknown", f"`{expr}` is not assigned in this code"
        rhs, touched = [a[2].strip() for a in asg], any(a[0] or a[1] != "=" for a in asg)
        if all(re.fullmatch(r"\d+", r) for r in rhs):
            return "zero", f"`{expr}` is an integer: ticks without input"
        if not touched and all(ZEROS.match(r) for r in rhs):
            return "zero", f"`{expr}` = np.zeros(...), never written to"
        if any(RANDOM.search(r) for r in rhs):
            return "blind", f"`{expr}` is built from a random generator"
        return "structured", f"`{expr}` is built without a random generator in sight"
    return ("blind", "the expression calls a random generator") if RANDOM.search(expr) else ("unknown", "an expression: " + one_line(expr, 40))


def input_class_array(inputs, sigma):
    """The class of an inputs array that is visible in the trace (a lab tool call), with the numbers it rests on."""
    try:
        U = np.asarray(inputs, float)
    except (ValueError, TypeError):
        return {"class": "invalid", "evidence": "not an array of numbers"}
    if U.ndim != 2 or not np.isfinite(U).all():
        return {"class": "invalid", "evidence": f"shape {U.shape} or non-finite values"}
    nats = None if not sigma else float((U ** 2).sum() / (2 * sigma ** 2))
    nz = U[U != 0]
    if nz.size == 0:
        return {"class": "zero", "evidence": "all inputs are 0", "ticks": int(U.shape[0]), "nats": 0.0}
    mags, rank = int(np.unique(np.round(np.abs(nz), 6)).size), int(np.linalg.matrix_rank(U))
    cls = "structured" if mags <= 3 or (min(U.shape) > 2 and rank <= 2) else "blind"
    return {"class": cls, "ticks": int(U.shape[0]), "nats": nats,
            "evidence": f"{mags} distinct magnitudes, rank {rank}, {int((U != 0).any(0).sum())} of {U.shape[1]} sites and "
                        f"{int((U != 0).any(1).sum())} of {U.shape[0]} ticks touched (structured = at most 3 magnitudes or rank at most 2)"}


def read_bash(cmd, files, workdir):
    """Kinds and details of one bash command. `files` (path -> text the agent wrote there) is updated."""
    written, stdin_py, shell = [], [], cmd
    for m in HEREDOC.finditer(cmd):
        line = cmd[cmd.rfind("\n", 0, m.start()) + 1: cmd.find("\n", m.start())]
        tgt = re.search(r"(?<![<>])>{1,2}\s*([^\s;&|<>]+)", line)
        if tgt:
            p = norm_path(tgt.group(1), workdir)
            files[p] = m.group(3)
            written.append((p, m.group(3).count("\n") + 1))
        elif re.search(r"\bpython[\d.]*\b", line):
            stdin_py.append(m.group(3))
    shell = HEREDOC.sub(" <<HEREDOC\n", cmd)
    run, plain = list(stdin_py), shell
    for m in reversed(list(PY_C.finditer(shell))):
        q, j = m.group(1), m.end()
        while j < len(shell) and (shell[j] != q or (q == '"' and shell[j - 1] == "\\")):
            j += 1
        run.append(shell[m.end():j].replace('\\"', '"') if q == '"' else shell[m.end():j])
        plain = plain[:m.end()] + plain[j:]
    for m in re.finditer(r"(?:^|[;&|(]|\n)\s*(cp|mv)\s+(?:-\w+\s+)*(\S+)\s+(\S+)", plain):      # a tracked file copied or moved
        src, dst = norm_path(m.group(2), workdir), norm_path(m.group(3), workdir)
        if src in files:
            files[dst.rstrip("/") + "/" + os.path.basename(src) if dst.endswith("/") or dst in ("submission", ".") else dst] = files[src]
    scripts = []
    for m in PY_FILE.finditer(plain):
        p = norm_path(m.group(1), workdir)
        scripts.append(p)
        if p in files:
            run.append(files[p])
    code = "\n".join(run)
    kinds, d = set(), {"python_lines": sum(len([ln for ln in r.splitlines() if ln.strip() and not ln.strip().startswith("#")]) for r in run) or None,
                       "writes": written, "scripts_run": scripts}
    ops, sites = [], []
    if code and USES_LAB.search(code):
        for m in LAB_OP.finditer(code):
            ops.append(m.group(1))
            if m.group(1) in ("advance", "experiment"):
                a = call_args(code, m.end())
                expr = next((x for x in a if re.match(r"(inputs|n)\s*=", x)), None) or (a[-1] if len(a) >= (2 if m.group(1) == "experiment" else 1) else "")
                cls, why = input_class_static(expr, code) if expr else ("unknown", "no argument found")
                sites.append({"op": m.group(1), "class": cls, "evidence": "static: " + why})
    if ops:
        d["lab_call_sites"], d["lab_input_sites"] = {o: ops.count(o) for o in dict.fromkeys(ops)}, sites
        kinds |= set(ops) & {"validate", "submit"}
        if set(ops) & {"reset", "advance", "experiment"}:
            kinds.add("lab")
        elif set(ops) & {"card", "usage"}:
            kinds.add("lab-info")
    if code and SIM.search(code):
        kinds.add("sim")
        d["sim_calls"] = sorted(set(re.findall(r"\.\s*(episodes|free_run)\s*\(", code)) | ({"Simulator"} if "Simulator" in code else set()))
    if LOCAL_CHECK.search(plain):
        kinds.add("validate")
        d["local_check"] = True
    if written or WRITE_CMD.search(plain):
        kinds.add("write")
    if READ_CMD.search(re.sub(r"\bcat\s*(?=>|<<)", "", plain)):          # `cat > file << EOF` writes, it does not read
        kinds.add("read")
    if NETWORK.search(cmd) or URL.search(cmd):
        kinds.add("network")
    if code and not kinds & {"lab", "sim", "validate", "submit"}:
        kinds.add("compute" if PY_WORK.search(code) or (d["python_lines"] or 0) > 20 else "read")
        d["python_only_inspects"] = "compute" not in kinds
    if run:                                                  # the agent's own first comment says what the code is for
        lines = [ln.strip() for ln in run[-1].splitlines() if ln.strip()]
        gist = next((ln.lstrip("# ") for ln in lines if ln.startswith("#") and len(ln) > 4), None) \
            or next((ln for ln in lines if not re.match(r"(import|from)\s", ln)), None)
        d["python_gist"] = one_line(gist or "", 60)
    return kinds or {"other"}, d


def lab_tool_call(args, result, sigma, reset_cost):
    """One call of the laboratory TOOL: everything about the request is in the trace."""
    op, a = args.get("op"), args.get("args") if isinstance(args.get("args"), dict) else {}
    d = {"op": op if isinstance(op, str) else None, "via": "tool"}
    try:
        rep = json.loads(result) if isinstance(result, str) else None
    except ValueError:
        rep = None
    if isinstance(rep, dict):
        d["ok"] = bool(rep.get("ok"))
        if not d["ok"]:
            d["error_kind"], d["error"] = rep.get("kind"), one_line(rep.get("error"), 160)
        elif op in ("validate", "submit") and isinstance(rep.get("result"), dict):
            d["check_ok"], d["accepted"] = rep["result"].get("ok"), rep["result"].get("accepted")
    if op in ("advance", "experiment"):
        if "inputs" in a:
            d["inputs"] = input_class_array(a["inputs"], sigma)
            T = d["inputs"].get("ticks")
        else:
            T = a.get("n") if isinstance(a.get("n"), int) else None
            d["inputs"] = {"class": "zero", "evidence": "n ticks without input", "ticks": T, "nats": 0.0}
        charged = d.get("ok") is True and T is not None
        d["ticks"] = (T + (reset_cost if op == "experiment" else 0)) if charged else 0
        d["nats"] = d["inputs"].get("nats") if charged else 0.0
    elif op == "reset":
        d["ticks"], d["nats"] = (reset_cost if d.get("ok") else 0), 0.0
    kind = {"validate": "validate", "submit": "submit", "card": "lab-info", "usage": "lab-info"}.get(op, "lab")
    return {kind}, d


def result_status(text):
    if text is None:
        return {"seen": False}
    text = text if isinstance(text, str) else json.dumps(text)
    out = {"seen": True, "chars": len(text)}
    if TRACEBACK.search(text):
        out["python_error"] = one_line(text.strip().splitlines()[-1], 140)
    m = LAB_ERROR.search(text)
    if m:
        out["lab_error"] = one_line(m.group(1), 140)
    return out


def content_text(c):
    if isinstance(c, list):
        return "\n".join(p.get("text", "") for p in c if isinstance(p, dict))
    return c


def read_call(name, namespace, args, res, files, workdir, sigma, reset_cost):
    """Kinds, details and a one-line description of one tool call, and the text of it that the flags search
    (what the agent itself wrote; the numbers of an inputs array are left out)."""
    text = "\n".join(str(v) for v in args.values() if isinstance(v, str))
    if name in LAB_TOOLS or namespace == "lab":
        kinds, d = lab_tool_call(args, res, sigma, reset_cost)
        what = f"lab tool: {d['op']}" + (f" ({d['inputs']['class']} inputs)" if "inputs" in d else "")
        inner = args.get("args") if isinstance(args.get("args"), dict) else {}
        text += "\n" + json.dumps({k: v for k, v in inner.items() if k != "inputs"})
    elif "command" in args:
        kinds, d = read_bash(str(args["command"]), files, workdir)
        first = re.sub(rf"^\s*cd\s+{re.escape(workdir)}/?\s*(&&|;)\s*", "", str(args["command"]).strip())
        what = first.splitlines()[0] if first else ""
        if re.search(r"-c\s+['\"]\s*$", what) and d.get("python_gist"):
            what = re.sub(r"\s*['\"]\s*$", "", what) + ": " + d["python_gist"]
    elif "old_str" in args or "new_str" in args:
        p = norm_path(str(args.get("path", "")), workdir)
        files[p] = files[p].replace(str(args.get("old_str", "")), str(args.get("new_str", "")), 1) if p in files else str(args.get("new_str", ""))
        kinds, d, what = {"write"}, {"writes": [(p, str(args.get("new_str", "")).count("\n") + 1)]}, f"edit {p}"
    else:
        kinds, d, what = {"other"}, {}, name + " " + one_line(json.dumps(args), 50)
    return kinds, d, what, text


def timeline(tr, lab_log, sigma, reset_cost):
    nodes, calls, tm = tr.get("nodes") or [], tr.get("calls") or [], tr.get("timing") or {}
    workdir = (tr["task"]["data"].get("workdir") or "/workspace").rstrip("/")
    a0, a1 = (tm.get("agent") or {}).get("start"), (tm.get("agent") or {}).get("end")
    results = {n["message"].get("tool_call_id"): content_text(n["message"].get("content")) for n in nodes if (n.get("message") or {}).get("role") == "tool"}
    files, rows, turns = {}, [], []
    for k, c in enumerate(calls):
        t = c.get("time") or {}
        nxt = (calls[k + 1].get("time") or {}).get("start") if k + 1 < len(calls) else a1
        u = c.get("usage") or {}
        turn = {"turn": k + 1, "t_s": None if a0 is None or t.get("end") is None else round(t["end"] - a0, 1),
                "model_s": None if t.get("end") is None or t.get("start") is None else round(t["end"] - t["start"], 1),
                "tools_s": None if nxt is None or t.get("end") is None else round(max(0.0, nxt - t["end"]), 1),
                "tokens_in": (u.get("prompt_tokens") or 0) + (u.get("cached_input_tokens") or 0) if u else None,
                "tokens_out": u.get("completion_tokens"), "finish_reason": c.get("finish_reason"),
                "model_error": (c.get("error") or {}).get("type") if c.get("error") else None, "window": (t.get("end"), nxt)}
        node = nodes[c["node"]] if isinstance(c.get("node"), int) and c["node"] < len(nodes) else {}
        tcs = (node.get("message") or {}).get("tool_calls") or []
        turn["n_tool_calls"] = len(tcs)
        turns.append(turn)
        if not tcs:
            rows.append({"turn": k + 1, "tool": None, "kinds": ["talk"], "what": one_line((node.get("message") or {}).get("content") or "", 70), "detail": {}, "result": {"seen": None}})
        for tc in tcs:
            name = (tc.get("namespace") + "." if tc.get("namespace") else "") + str(tc.get("name"))
            try:
                args = json.loads(tc.get("arguments") or "{}")
            except ValueError:
                args = {"_unparsed": str(tc.get("arguments"))}
            args = args if isinstance(args, dict) else {"_value": args}
            res = results.get(tc.get("id"))
            try:
                kinds, d, what, text = read_call(name, tc.get("namespace"), args, res, files, workdir, sigma, reset_cost)
            except Exception as e:                           # one odd command must not sink the report
                kinds, d, what, text = {"other"}, {"reader_error": type(e).__name__}, f"{name} (not read: {type(e).__name__})", json.dumps(args)
            rows.append({"turn": k + 1, "tool": name, "kinds": sorted(kinds, key=KIND_ORDER.index), "what": one_line(what, 70), "detail": d,
                         "result": result_status(res), "_text": text})
    # ---- the laboratory's own log, matched to turns by time (a request belongs to the turn whose tools were running) ----
    lab = None
    if lab_log is not None:
        lab, prev_nats, episode = [], 0.0, 0
        for r in lab_log:
            nats = (r.get("total_nats") or 0.0) - prev_nats
            prev_nats = r.get("total_nats") or prev_nats
            episode += r.get("op") in ("reset", "experiment") and bool(r.get("ok"))
            turn = next((t["turn"] for t in turns if t["window"][0] is not None and t["window"][0] <= r["t"] < (t["window"][1] or 1e18)), None)
            lab.append({"t_s": None if a0 is None else round(r["t"] - a0, 1), "turn": turn, "episode": episode or None, "op": r.get("op"), "ok": bool(r.get("ok")),
                        "kind": r.get("kind"), "error": r.get("error"), "ticks": r.get("ticks") or 0, "nats": round(max(0.0, nats), 6),
                        "seconds": r.get("seconds")})
        for t in turns:
            mine = [x for x in lab if x["turn"] == t["turn"]]
            if mine:
                t["lab_record"] = {"requests": len(mine), "ticks": sum(x["ticks"] for x in mine), "nats": round(sum(x["nats"] for x in mine), 4),
                                   "rejected": sum(not x["ok"] for x in mine), "ops": {o: sum(x["op"] == o for x in mine) for o in dict.fromkeys(x["op"] for x in mine)}}
    for t in turns:
        del t["window"]
    return turns, rows, lab, files


def lab_episodes(lab, rows):
    """The laboratory's requests, one line per episode (reset or experiment starts one); other requests on their own."""
    out, cur, static = [], None, {}
    for r in rows:
        for s in (r["detail"].get("lab_input_sites") or []):
            static.setdefault(r["turn"], []).append(s["class"])
    for x in lab:
        if x["ok"] and x["op"] == "advance" and cur is not None:
            e = cur                                          # an advance continues the episode its reset opened
        else:
            e = {"episode": x["episode"] if x["ok"] and x["op"] in ("reset", "advance", "experiment") else None, "turn": x["turn"], "t_s": x["t_s"],
                 "ops": [], "ticks": 0, "nats": 0.0, "rejected": [], "_advance": 0}
            out.append(e)
            cur = e if x["ok"] and x["op"] in ("reset", "experiment") else cur
        e["ops"].append(x["op"])
        e["ticks"] += x["ticks"]
        e["nats"] = round(e["nats"] + x["nats"], 6)
        e["_advance"] += x["op"] in ("advance", "experiment") and x["ok"]
        if not x["ok"]:
            e["rejected"].append({"op": x["op"], "kind": x["kind"], "error": x["error"]})
    for e in out:
        st = sorted(set(static.get(e["turn"], [])))
        if not e.pop("_advance"):
            e["inputs"] = None
        elif e["nats"] == 0:
            e["inputs"] = "zero (0 nats charged)"
        else:
            guess = [s for s in st if s in ("blind", "structured")]
            e["inputs"] = "non-zero" + (f"; {' or '.join(guess)} by the code of turn {e['turn']}" if guess else "; blind or structured: not recoverable (the laboratory does not log inputs)")
    return out


# ----------------------------------------------------------------------------- 6 flags
def predictor_check(src):
    """Does predict() read its history and program arguments? Parsed, never run."""
    try:
        tree = ast.parse(src)
    except (SyntaxError, ValueError, RecursionError, MemoryError) as e:
        return {"parsed": False, "error": type(e).__name__}
    fn = next((n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "predict"), None)
    if fn is None:
        return {"parsed": True, "has_predict": False}
    for node in ast.walk(fn):
        for ch in ast.iter_child_nodes(node):
            ch._parent = node
    params = [a.arg for a in fn.args.posonlyargs + fn.args.args]
    out = {"parsed": True, "has_predict": True, "params": params, "open_signature": bool(fn.args.vararg or fn.args.kwarg), "lines": len(src.splitlines())}
    for role, i in (("history", 0), ("program", 1)):
        name = role if role in params else (params[i] if len(params) > i else None)
        uses = [n for n in ast.walk(fn) if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Load)]
        shape_only = bool(uses) and all(
            (isinstance(u._parent, ast.Attribute) and u._parent.attr in ("shape", "ndim", "dtype", "size"))
            or (isinstance(u._parent, ast.Call) and getattr(u._parent.func, "id", None) == "len") for u in uses)
        out[role] = {"parameter": name, "reads": len(uses), "shape_only": shape_only}
    return out


def flags(tr, turns, rows, lab, files, sub_dir, long_s):
    ph = (tr.get("info") or {}).get("physim2") or {}
    labc, sub, out = ph.get("lab") or {}, ph.get("submission") or {}, []

    def add(fid, text, turns_=None, items=None):
        out.append({"id": fid, "text": text, "turns": sorted(set(turns_ or [])), "items": items or []})

    stop = tr.get("stop_condition")
    if stop not in ENDED_BY_AGENT or tr.get("is_timeout") or tr.get("errors"):
        add("ended_by_a_cap_or_error", f"the rollout did not end by the agent's own choice: stop condition `{stop}`"
            + (", timed out" if tr.get("is_timeout") else "") + ("".join(f", error {e.get('type')}" for e in tr.get("errors") or [])))
    last = rows[-1] if rows else None
    if last and last["tool"] and last["result"].get("seen") is False:
        add("last_tool_result_never_seen", f"the last reply (turn {last['turn']}) called a tool whose result never reached the model: "
            f"{' + '.join(last['kinds'])}; whatever it did (a validation attempt, a laboratory request) still counted", [last["turn"]])
    # -- outside the workspace, and looks at the box's wiring
    seen = []
    for r in rows:
        text = URL.sub(" ", r.get("_text") or "")
        for p in dict.fromkeys(ABS_PATH.findall(text)):
            if not HARMLESS.match(p) and not p.startswith(os.path.join((tr["task"]["data"].get("workdir") or "/workspace"), "")) \
                    and p != (tr["task"]["data"].get("workdir") or "/workspace"):
                seen.append((r["turn"], p))
        for m in ESCAPE.finditer(text):
            seen.append((r["turn"], one_line(m.group(0).strip(" ;&|'\"=(\n"), 30)))
    if seen:
        seen = sorted(set(seen))
        add("outside_the_workspace", f"{len(seen)} mention(s) of a path outside the workspace, of the environment, or of the box's wiring in what the agent wrote "
            "(a mention is not proof of a read: look at the turns)", [t for t, _ in seen], [f"turn {t}: {p}" for t, p in seen[:25]])
    pkg = sorted({(r["turn"], p) for r in rows for p, _ in r["detail"].get("writes") or [] if str(p).startswith("physim2/")})
    if pkg:
        add("writes_into_the_public_package", "the agent wrote into physim2/, the public package that the predictor and the local check import", [t for t, _ in pkg], [f"turn {t}: {p}" for t, p in pkg[:25]])
    net = [(r["turn"], (m.group(1) or m.group(2) or "").strip()) for r in rows for m in NETWORK.finditer(r.get("_text") or "")]
    net = sorted(set(net + [(r["turn"], one_line(u, 60)) for r in rows for u in URL.findall(r.get("_text") or "")]))
    if net:
        add("network_attempt", f"{len(net)} command(s) or call(s) that reach for the network (the box has none; physim2.Lab() itself is not counted)",
            [t for t, _ in net], [f"turn {t}: {w}" for t, w in net[:25]])
    # -- errors from the laboratory
    seen_err = [(r["turn"], r["result"]["lab_error"]) for r in rows if r["result"].get("lab_error")]
    seen_err += [(r["turn"], f"{r['detail'].get('op')}: {r['detail'].get('error_kind')}: {r['detail'].get('error')}") for r in rows if r["detail"].get("via") == "tool" and r["detail"].get("ok") is False]
    rec_err = [(x["turn"], f"{x['op']}: {x['kind']}: {x['error']}") for x in (lab or []) if not x["ok"]]
    if labc.get("rejected") or labc.get("infrastructure_errors") or seen_err or rec_err:
        use = rec_err or seen_err
        add("lab_errors", f"the laboratory rejected {labc.get('rejected')} request(s) and counted {labc.get('infrastructure_errors')} infrastructure error(s) "
            f"(its counters in the trace); {len(seen_err)} rejection(s) are visible in tool results"
            + (f", {len(rec_err)} in the laboratory's own log" if lab is not None else ""), [t for t, _ in use if t], [f"turn {t}: {one_line(e, 150)}" for t, e in use[:25]])
    py_err = [(r["turn"], r["result"]["python_error"]) for r in rows if r["result"].get("python_error")]
    if py_err:
        add("python_errors", f"{len(py_err)} tool call(s) ended in a Python traceback", [t for t, _ in py_err], [f"turn {t}: {e}" for t, e in py_err[:25]])
    # -- long stretches
    longs = [(t["turn"], f"model call of {t['model_s']:.0f} s") for t in turns if (t["model_s"] or 0) >= long_s]
    longs += [(t["turn"], f"tools ran {t['tools_s']:.0f} s") for t in turns if (t["tools_s"] or 0) >= long_s]
    tm = (tr.get("timing") or {}).get("agent") or {}
    if turns and tm.get("start") is not None:
        lead = (tr["calls"][0].get("time") or {}).get("start")
        if lead is not None and lead - tm["start"] >= long_s:
            longs.append((1, f"{lead - tm['start']:.0f} s before the first model call"))
    if longs:
        add("long_stretches", f"{len(longs)} stretch(es) of at least {long_s:.0f} s in which one model call or one turn's tools ran", [t for t, _ in longs],
            [f"turn {t}: {w}" for t, w in sorted(longs)[:25]])
    # -- the submission
    submitted = bool(labc.get("submitted")) or (sub.get("ok") and sub.get("source") == "agent_submission")
    if not sub.get("ok"):
        add("no_graded_submission", f"nothing gradable was collected (source `{sub.get('source')}`, error: {one_line(sub.get('error'), 80)}): scored as K")
    elif not submitted:
        add("collected_without_submit", "the agent never submitted: submission/ was collected as it was when the run ended")
    if sub.get("ok") and not labc.get("ticks_used"):
        add("submission_without_lab_use", "a submission was graded although the laboratory ran 0 ticks: the hidden world was never observed "
            f"({labc.get('requests', 0)} laboratory requests in all, none of them an experiment)")
    if labc.get("ticks_used") and rows and not any("lab" in r["kinds"] for r in rows):
        add("lab_use_not_visible", f"the laboratory ran {labc.get('ticks_used')} ticks but no tool call of the trace shows a laboratory request (a script the trace does not show?)")
    # -- what the agent was told about its box, against the box it had
    told, had = tr["task"]["data"].get("resources") or {}, (tr.get("agent") or {}).get("runtime") or {}
    diff = [f"{k}: task row {told[k]:g}, box {had[k]:g}" for k in ("cpu", "memory") if isinstance(told.get(k), (int, float)) and isinstance(had.get(k), (int, float)) and told[k] != had[k]]
    if diff:
        add("box_differs_from_the_task_row", "the agent's box did not have the resources of the task row, which is what TASK.md states as the compute envelope (" + "; ".join(diff) + ")")
    # -- the predictor's source
    src, where = None, None
    if sub_dir and os.path.isfile(os.path.join(sub_dir, "predict.py")):
        with open(os.path.join(sub_dir, "predict.py"), errors="replace") as h:
            src, where = h.read(), "--submission"
    else:
        cands = [p for p in files if os.path.basename(p) == "predict.py"]
        inside = [p for p in cands if p.startswith("submission/")]
        if cands:
            p = (inside or cands)[-1]
            src, where = files[p], f"the trace (the agent's last write to `{p}`)"
            if not inside:
                add("predictor_outside_submission", f"the agent wrote predict.py to `{p}` and the trace shows no copy under submission/: only submission/ is collected")
    pc = {"source": where, **(predictor_check(src) if src is not None else {})}
    if src is None:
        pc["note"] = "not checked: the predictor's source is neither in the trace nor given with --submission"
    elif not pc.get("parsed") or not pc.get("has_predict"):
        add("predictor_unreadable", f"predict.py from {where} " + ("has no function `predict`" if pc.get("parsed") else "is not valid Python"))
    else:
        for role in ("history", "program"):
            r = pc[role]
            if not pc["open_signature"] and (r["reads"] == 0 or r["shape_only"]):
                add(f"predictor_ignores_{role}", (f"predict() never reads its `{r['parameter']}` argument" if r["reads"] == 0 else
                                                  f"predict() reads only the shape of its `{r['parameter']}` argument")
                    + f" (source: {where}; a static reading: passing it to a helper would count as a read)")
    for r in rows:
        r.pop("_text", None)
    return out, pc


# ----------------------------------------------------------------------------- 4 budgets
def budgets(tr, cfg, use, exam_cfg, caps_text, lab_eps, prices):
    ph = (tr.get("info") or {}).get("physim2") or {}
    lab, g, sub, tm = ph.get("lab") or {}, ph.get("grade") or {}, ph.get("submission") or {}, tr.get("timing") or {}
    ec = exam_cfg or {}
    agent_s = None if not tm.get("agent") else tm["agent"]["end"] - tm["agent"]["start"]
    wall_cap = (cfg.get("timeout") or {}).get("rollout") or ((tr["task"]["data"].get("timeout") or {}).get("agent"))
    rows = []

    def row(name, used, cap, where, note=""):
        share = None if cap in (None, 0) or used is None else used / cap
        if used is None and cap is None:                     # nothing to say (a scripted agent has no turns and no tokens)
            return
        rows.append({"budget": name, "used": used, "cap": cap, "share": share, "cap_from": where, "note": note})

    first = next((i for i, n in enumerate(tr.get("nodes") or []) if n.get("sampled")), 0)
    said = str(tr["task"]["data"].get("prompt") or "") + "\n".join(str(content_text((n.get("message") or {}).get("content")) or "") for n in (tr.get("nodes") or [])[:first])

    def note(n):                                             # is the number followed, in the same sentence, by a word for what it caps?
        if not n:
            return ""
        digits = f"{int(n):,}".replace(",", ",?")            # 70000 is found as 70000 and as 70,000
        told = re.search(r"(?<![\d,.])" + digits + r"(?![\d,])[^.\n]{0,40}\b(turns?|repl(?:y|ies)|calls?|steps?|messages?|requests?|tokens?)\b", said)
        return "" if told else "what the agent was shown does not state this cap"
    row("model turns", use["n_calls"] or None, cfg.get("max_turns"), "agent config max_turns", note(cfg.get("max_turns")))
    row("tokens as verifiers counts them (each fed-in token once)", use["caps_see_total_tokens"], cfg.get("max_total_tokens"), "agent config max_total_tokens", note(cfg.get("max_total_tokens")))
    row("output tokens", use["caps_see_output_tokens"], cfg.get("max_output_tokens"), "agent config max_output_tokens")
    row("largest single reply (tokens)", use["largest_reply_tokens"] or None, (cfg.get("sampling") or {}).get("max_tokens"), "sampling max_tokens")
    row("largest context sent (tokens)", use["largest_context_tokens"] or None, (prices or {}).get("context_window"), "the model's context window (--model-entry)")
    row("agent phase, wall seconds", agent_s, wall_cap, "agent config timeout.rollout, else the task row")
    row("laboratory ticks", lab.get("ticks_used"), (ec.get("lab") or {}).get("max_ticks"), "exam config (reference table)")
    row("nats in total", lab.get("total_nats"), (ec.get("lab") or {}).get("total_nats"), "exam config (reference table)", "no total cap in this config" if not (ec.get("lab") or {}).get("total_nats") else "")
    if lab_eps is not None:
        row("largest nats in one episode", max([e["nats"] for e in lab_eps if e["episode"]] or [0.0]), caps_text.get("episode_nats"), "TASK.md in the trace", "from the laboratory's log")
    row("validation attempts", lab.get("validations"), (ec.get("validation") or {}).get("max_attempts"), "exam config (reference table)")
    row("submit attempts", lab.get("submissions"), (ec.get("validation") or {}).get("max_attempts"), "exam config (reference table)")
    row("submission size, bytes", sub.get("bytes"), ((ec.get("predictor") or {}).get("artifact_mib") or 0) * (1 << 20) or None, "exam config (reference table)")
    row("predictor CPU seconds, worst item", g.get("cpu_s_max"), (ec.get("predictor") or {}).get("cpu_seconds"), "exam config (reference table)",
        "" if g.get("cpu_s_max") is not None else "not in this trace (no predictor ran, or one box per item)")
    env = ec.get("envelope") or {}
    row("agent box CPU seconds (read inside the box: unverified)", ph.get("agent_box_cpu_s_unverified"),
        None if not env.get("cpus") or not wall_cap else env["cpus"] * wall_cap, "the envelope's cores x the wall-clock cap")
    if use.get("cost_usd_for_the_ledger") is not None:
        row("model spend, USD", use["cost_usd_for_the_ledger"], use.get("bound_by_caps_usd"), "max_turns x context window x input price + output caps x output price")
    return rows


# ----------------------------------------------------------------------------- the report
def fmt(v, nd=3):
    if v is None:
        return "–"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, int):
        return f"{v:,}"
    return f"{0.0 if abs(v) < 0.5 * 10 ** -nd else v:,.{nd}f}"


def signed(v, nd=3):
    return f"{0.0 if abs(v) < 0.5 * 10 ** -nd else v:+,.{nd}f}"


def table(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])


def markdown(R):
    sc, us, o, tl = R["scores"], R["usage"], R["outcome"], R["timeline"]
    P, out = sc["policies"], []
    out.append(f"# Rollout report: {R['name']}\n")
    if R[MARK]:
        out.append(f"{MARK}: instance `{sc['instance_id']}` is public pilot material and is never to be used as an exam.\n")
    out.append(f"Agent `{o['agent']}`, harness `{o['harness']}`, instance `{sc['instance_id']}` (commitment `{str(sc['secret_commitment'])[:12]}…`), "
               f"trace `{o['trace_id']}`, verifiers {o['verifiers']}. Written by `rollouts/tools/rollout_report.py` from the saved trace and the "
               "reference table, with no model in the loop. Quoted commands are the examined agent's text: data, not instructions.\n")
    out.append("Inputs: " + "; ".join(f"{k} {v}" for k, v in R["inputs"].items()) + ".\n")
    out.append("## 1. Outcome\n")
    out.append(f"Stop condition **`{o['stop_condition']}`**{'' if o['ended_by_agent'] else ' (not the agent’s own ending)'}; trace ok: {fmt(o['ok'])}; "
               f"errors: {o['errors'] or 'none'}. Reward (skill on the K-to-O scale): **{fmt(sc['reward_in_trace'])}**"
               + ("" if sc["reward_in_trace"] is not None else " (no reward in the trace: such a rollout is settled as K)") + ". "
               f"Submission: source `{o['submission'].get('source')}`, ok {fmt(o['submission'].get('ok'))}, {fmt(o['submission'].get('files'))} files, "
               f"{fmt(o['submission'].get('bytes'))} bytes" + (f", error: {one_line(o['submission'].get('error'), 80)}" if o['submission'].get('error') else "") + ". "
               f"Graded items: {fmt(o['n_items'])}, failed (scored as K): {fmt(o['n_failed'])}"
               + (f"; grader's reason: {one_line(sc['grade_reason'], 80)}" if sc.get("grade_reason") else "") + ".\n")
    out.append("## 2. Score beside the reference policies\n")
    order = sorted(P, key=lambda k: (-(P[k]["skill_vs_O"] if P[k].get("skill_vs_O") is not None else -9), k != "AGENT"))
    rows = []
    for k in order:
        p, b = P[k], "**" if k == "AGENT" else ""
        am = p.get("agent_minus_policy")
        rows.append([f"{b}{'the agent' if k == 'AGENT' else k}{b}", one_line(p.get("label") or "", 60), fmt(p["L"]), f"{b}{fmt(p.get('skill_vs_O'))}{b}",
                     "–" if p.get("boot_se") is None else f"{p['boot_se']:.3f} ({fmt(p['boot_p05'])} to {fmt(p['boot_p95'])})", fmt(p.get("skill_vs_C")),
                     "–" if p.get("item_skill_p10") is None else f"{fmt(p['item_skill_p10'], 2)} / {fmt(p['item_skill_p50'], 2)} / {fmt(p['item_skill_p90'], 2)}",
                     fmt(p.get("items_worse_than_K")),
                     "–" if not am else f"{signed(am['mean_loss'])} ({signed(am['p05'])} to {signed(am['p95'])})", "–" if not am else f"{am['items_agent_better']} ({am['items_equal']} equal)"])
    out.append(table(["policy", "what it is", "mean loss L", "skill vs O", "bootstrap se (5 to 95 %)", "skill vs C", "per-item skill p10 / p50 / p90",
                      "items worse than K", "agent's loss minus the policy's (5 to 95 %)", "items where the agent is better"], rows))
    out.append(f"\nL is the energy score summed over the valid (level, time) cells, averaged over the {sc['n_items']} items (lower is better); skill vs O = "
               "(L_K - L) / (L_K - L_O). The per-item skill is (K_i - L_i) / (L_K - L_O) for one item: its mean over items is the skill, its spread shows "
               "where the score comes from. The bootstrap resamples the items of this ONE instance (4,000 resamples, seed 0, the same draws for every row): "
               "it says how well this instance separates the rows, and nothing about other hidden worlds. "
               f"The agent's per-item scores come from: {sc['agent_per_item_source'] or 'nowhere (only its mean L is in the trace; give --items)'}"
               + (f"; {sc['agent_items_failed']} of its items failed" if sc.get("agent_items_failed") is not None else "") + ".\n")
    if sc.get("skill_by_program_class"):
        cl = sc["skill_by_program_class"]
        cols = [k for k in order if k not in ("K", "O")]
        out.append("Skill vs O by the class of the test program (a none, b blind random, c aimed from the history, d regional):\n")
        out.append(table(["class", "items"] + ["the agent" if k == "AGENT" else k for k in cols], [[c, v["n_items"]] + [fmt(v[k]) for k in cols] for c, v in cl.items()]) + "\n")
    out.append("Consistency: " + "; ".join(f"{k.replace('_', ' ')}: {fmt(v)}" for k, v in sc["checks"].items()) + ".\n")
    out.append("## 3. Usage and cost\n")
    if not us["n_calls"]:
        out.append("No model call in this trace (a scripted agent): 0 tokens, $0.\n")
    else:
        pr = us.get("prices") or {}
        rows = [["model calls", f"{us['n_calls']} ({us['n_calls_failed']} failed, {us['n_calls_without_usage']} without usage)"],
                ["billed input tokens", f"{us['billed_input_tokens']:,} ({us['prompt_tokens_uncached']:,} at the input price + {us['cached_input_tokens']:,} cache reads)"],
                ["output tokens", f"{us['completion_tokens']:,} ({us['reasoning_tokens']:,} reasoning)"],
                ["what the token caps saw", f"{fmt(us['caps_see_input_tokens'])} in + {fmt(us['caps_see_output_tokens'])} out = {fmt(us['caps_see_total_tokens'])} "
                 "(verifiers counts each fed-in token once; the provider bills the context at every turn)"],
                ["largest context / largest reply", f"{us['largest_context_tokens']:,} / {us['largest_reply_tokens']:,} tokens"]]
        if pr:
            rows += [["prices (USD per million tokens)", f"{pr['input']} in, {pr['output']} out, {fmt(pr.get('cache_read'))} cache read; source: {pr.get('source') or 'the command line'}"],
                     ["cost", f"**${us['cost_usd_for_the_ledger']:.4f}** for the ledger (the larger of: all input at the full price ${us['cost_usd_all_input_at_full_price']:.4f}, "
                      f"the provider's own cost fields ${fmt(us['provider_reported_cost_usd'], 4)}); with the cache-read price ${fmt(us.get('cost_usd_with_cache_read_price'), 4)}"]]
            if us.get("bound_by_caps_usd") is not None:
                rows.append(["what the caps allowed", f"${us['bound_by_caps_usd']:.2f} (max_turns x context window x input price + output caps x output price)"])
        else:
            rows.append(["cost", f"no prices given (--prices or --model-entry); the provider's own cost fields sum to ${fmt(us['provider_reported_cost_usd'], 4)}"])
        out.append(table(["", ""], rows) + "\n")
    w = R["wall_s"]
    out.append(f"Wall clock: boot {fmt(w['boot'], 1)} s, setup {fmt(w['setup'], 1)} s, agent {fmt(w['agent'], 1)} s (model {fmt(w['agent_model'], 1)} s, harness and tools "
               f"{fmt(w['agent_harness'], 1)} s), finalize {fmt(w['finalize'], 1)} s, verifier {fmt(w['verifier'], 1)} s.\n")
    out.append("## 4. Budgets against the caps\n")
    out.append(table(["budget", "used", "cap", "share", "where the cap comes from", "note"],
                     [[b["budget"], fmt(b["used"], 1 if isinstance(b["used"], float) and b["used"] > 10 else 3), fmt(b["cap"], 2), "–" if b["share"] is None else f"{100 * b['share']:.1f} %",
                       b["cap_from"], b["note"]] for b in R["budgets"]]) + "\n")
    out.append("## 5. What the agent did\n")
    if tl["script"]:
        s = tl["script"]
        out.append(f"A scripted agent: `{s.get('script')}` (label `{s.get('label')}`) ran in the agent's box for {fmt(w['agent'], 1)} s and ended with exit code "
                   f"{s.get('exit_code')}. The trace holds no message and no tool call; the end of the script's own log:\n")
        out.append("```\n" + str(s.get("log_tail") or "").strip()[-1500:].replace("```", "'''") + "\n```\n")
    if tl["by_kind"]:
        out.append("Tool calls by kind (a call with several kinds counts under the first of: " + ", ".join(KIND_ORDER[:9]) + "):\n")
        out.append(table(["kind", "tool calls", "turns", "model s", "tools s"], [[k, v["calls"], v["turns"], fmt(v["model_s"], 1), fmt(v["tools_s"], 1)] for k, v in tl["by_kind"].items()]) + "\n")
        out.append("Laboratory reached through: the `lab_call` tool " + f"{tl['lab_route']['tool']} time(s), `physim2.Lab()` from Python in {tl['lab_route']['python']} tool call(s). "
                   "Milestones: " + "; ".join(f"{k.replace('_', ' ')}: " + ("never" if v is None else f"turn {v['turn']} (t = {fmt(v['t_s'], 0)} s)") for k, v in tl["milestones"].items()) + ".\n")
    if tl["turns"]:
        lm, lt = max(tl["turns"], key=lambda t: t["model_s"] or 0), max(tl["turns"], key=lambda t: t["tools_s"] or 0)
        out.append(f"Longest model call: {fmt(lm['model_s'], 1)} s (turn {lm['turn']}); longest run of one turn's tools: {fmt(lt['tools_s'], 1)} s (turn {lt['turn']}).\n")
    lc = o["lab"]
    out.append(f"The laboratory's counters in the trace: {fmt(lc.get('ticks_used'))} ticks, {fmt(lc.get('episodes'))} episodes, {fmt(lc.get('total_nats'), 2)} nats, "
               f"{fmt(lc.get('requests'))} requests ({fmt(lc.get('rejected'))} rejected, {fmt(lc.get('infrastructure_errors'))} infrastructure errors), "
               f"{fmt(lc.get('validations'))} validation(s), {fmt(lc.get('submissions'))} submit(s), submitted: {fmt(lc.get('submitted'))}.\n")
    if tl["rows"]:
        out.append("Every tool call (t = seconds of the agent phase at which the model's reply arrived; model s = that reply's latency; tools s = until the next "
                   "model call started, shared by the calls of one reply; lab = what the laboratory's own log holds for that span"
                   + ("" if tl["lab_record_given"] else ", not available without --lab-record") + "):\n")
        T = {t["turn"]: t for t in tl["turns"]}
        rows, seen = [], set()
        for r in tl["rows"]:
            t, first, d = T[r["turn"]], r["turn"] not in seen, r["detail"]
            seen.add(r["turn"])
            notes = []
            if d.get("python_lines"):
                notes.append(f"runs {d['python_lines']} lines of Python")
            notes += [f"writes {p} ({n} lines)" for p, n in d.get("writes") or []]
            if d.get("sim_calls"):
                notes.append("simulator: " + ", ".join(d["sim_calls"]))
            if d.get("lab_call_sites"):
                cls = sorted({s["class"] for s in d.get("lab_input_sites") or []})
                notes.append("Lab calls in the code: " + ", ".join(d["lab_call_sites"]) + (f"; inputs {'/'.join(cls)} (static)" if cls else ""))
            if d.get("via") == "tool" and "ticks" in d:
                notes.append((f"{d['ticks']} ticks, {fmt(d.get('nats'), 2)} nats" if d.get("ok") else "nothing ran") + ("; " + d["inputs"]["evidence"] if "inputs" in d else ""))
            if d.get("local_check"):
                notes.append("local check, not the laboratory's")
            lr = t.get("lab_record") if first else None
            res = r["result"]
            status = "no result: the rollout ended" if res.get("seen") is False else "" if res.get("seen") is None else (
                "Lab rejected: " + res["lab_error"] if res.get("lab_error") else "error: " + res["python_error"] if res.get("python_error") else
                ("rejected: " + str(d.get("error")) if d.get("ok") is False else f"ok ({res.get('chars', 0):,} chars)"))
            rows.append([r["turn"] if first else "", fmt(t["t_s"], 0) if first else "", fmt(t["model_s"], 1) if first else "", fmt(t["tools_s"], 1) if first else "",
                         "+".join(r["kinds"]), code_span(r["what"], 64) + ("; " + "; ".join(notes) if notes else ""),
                         "" if not lr else f"{lr['requests']} req ({', '.join(f'{o_} x{n}' for o_, n in lr['ops'].items())}), {lr['ticks']} ticks, {fmt(lr['nats'], 2)} nats"
                         + (f", {lr['rejected']} rejected" if lr["rejected"] else ""), one_line(status, 90).replace("|", "¦")])
        out.append(table(["turn", "t", "model s", "tools s", "kind", "what", "lab (its own log)", "result"], rows) + "\n")
    if tl["lab_episodes"] is not None:
        out.append("Laboratory requests, one line per episode (from the laboratory's own log; like episodes of one turn share a line; a rejected request has its own):\n")
        groups = []                                          # consecutive episodes of one turn with the same requests, ticks, nats and inputs
        for e in tl["lab_episodes"]:
            key = (e["turn"], tuple(e["ops"]), e["ticks"], e["nats"], e["inputs"])
            if groups and e["episode"] and not e["rejected"] and groups[-1]["key"] == key and groups[-1]["first"]["episode"]:
                groups[-1]["n"] += 1
            else:
                groups.append({"key": key if not e["rejected"] else None, "first": e, "n": 1})
        rows = []
        for gr in groups:
            e, n = gr["first"], gr["n"]
            rows.append([fmt(e["episode"]) if n == 1 else f"{e['episode']} to {e['episode'] + n - 1}", fmt(e["turn"]), fmt(e["t_s"], 0),
                         ", ".join(f"{o_} x{e['ops'].count(o_)}" if e["ops"].count(o_) > 1 else o_ for o_ in dict.fromkeys(e["ops"])) + (" (each)" if n > 1 else ""),
                         e["ticks"] if n == 1 else f"{e['ticks'] * n} ({e['ticks']} each)", fmt(e["nats"], 2) + (" each" if n > 1 else ""), e["inputs"] or "–",
                         "; ".join(f"{x['op']}: {x['kind']}: {one_line(x['error'], 80)}" for x in e["rejected"]).replace("|", "¦") or ""])
        out.append(table(["episode", "turn", "t", "requests", "ticks", "nats", "inputs", "rejected"], rows) + "\n")
    out.append("## 6. Flags worth a human look\n")
    if not R["flags"]:
        out.append("None of the checks fired.\n")
    for f in R["flags"]:
        out.append(f"- **{f['id']}**" + (f" (turns {', '.join(map(str, f['turns'][:30]))}{'…' if len(f['turns']) > 30 else ''})" if f["turns"] else "") + f": {f['text']}"
                   + "".join(f"\n  - {code_span(i, 170)}" for i in f["items"]))
    pc = R["predictor_check"]
    out.append("\nPredictor source: " + (pc.get("note") or f"read from {pc['source']}; " + (
        "not parsed" if not pc.get("parsed") else "no function `predict`" if not pc.get("has_predict") else
        f"`predict({', '.join(pc['params'])})`, {pc['lines']} lines; reads of `history`: {pc['history']['reads']}"
        f"{' (shape only)' if pc['history']['shape_only'] else ''}, of `program`: {pc['program']['reads']}{' (shape only)' if pc['program']['shape_only'] else ''}")) + ".")
    out.append("Checks that did not fire: " + (", ".join(sorted(set(R["flag_ids_checked"]) - {f["id"] for f in R["flags"]})) or "none") + ".\n")
    out.append("## 7. What this report could not see\n")
    out.append("\n".join("- " + s for s in R["limits"]) + "\n")
    return "\n".join(out)


FLAG_IDS = ["ended_by_a_cap_or_error", "last_tool_result_never_seen", "outside_the_workspace", "writes_into_the_public_package", "network_attempt", "lab_errors", "python_errors",
            "long_stretches", "box_differs_from_the_task_row", "no_graded_submission", "collected_without_submit", "submission_without_lab_use", "lab_use_not_visible",
            "predictor_outside_submission", "predictor_unreadable", "predictor_ignores_history", "predictor_ignores_program"]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--trace", required=True)
    ap.add_argument("--reference", required=True)
    ap.add_argument("--out", required=True, help="prefix: writes <out>.md and <out>.json")
    ap.add_argument("--prices", default="", help="USD per million tokens: IN,OUT[,CACHE_READ]")
    ap.add_argument("--model-entry", default="", help="the model's entry of the provider's model list, as tools/ping_model.py saves it")
    ap.add_argument("--price-source", default="")
    ap.add_argument("--lab-record", default="")
    ap.add_argument("--items", default="")
    ap.add_argument("--submission", default="")
    ap.add_argument("--long-s", type=float, default=120.0, help="a model call or a turn's tools lasting at least this long is flagged")
    ap.add_argument("--episode", type=int, default=0)
    ap.add_argument("--name", default="")
    a = ap.parse_args(argv)
    ep, tr, tinfo = load_trace(a.trace, a.episode)
    cfg = (tr.get("agent") or {}).get("config") or {}
    ph = (tr.get("info") or {}).get("physim2") or {}
    if not ph:
        raise SystemExit("this trace is not of the physim2-env taskset (no info.physim2)")
    prices = None
    if a.model_entry:
        e = load_json(a.model_entry)
        p = (e.get("entry") or e).get("pricing") or {}
        prices = {"input": p["input_usd_per_mtok"], "output": p["output_usd_per_mtok"], "cache_read": p.get("cache_read_usd_per_mtok"),
                  "context_window": (e.get("entry") or e).get("context_window"), "source": a.price_source or e.get("source") or os.path.basename(a.model_entry)}
    elif a.prices:
        v = [float(x) for x in a.prices.split(",")]
        prices = {"input": v[0], "output": v[1], "cache_read": v[2] if len(v) > 2 else None, "context_window": None, "source": a.price_source or "--prices"}
    lab_log = None
    if a.lab_record:
        f = os.path.join(a.lab_record, "log.jsonl") if os.path.isdir(a.lab_record) else a.lab_record
        with open(f) as h:
            raw = h.read()
        try:
            lab_log = json.loads(raw)["log"]
        except (ValueError, KeyError, TypeError):
            lab_log = [json.loads(line) for line in raw.splitlines() if line.strip()]
    prompt = str(tr["task"]["data"].get("prompt") or "")
    m_sig = re.search(r"\|u\|\^2 / \(2 \* ([\d.]+)\^2\)", prompt)
    m_cap = re.search(r"at most ([\d.]+) nats per tick,\s+([\d.]+) per episode", prompt)
    caps_text = {"tick_nats": float(m_cap.group(1)) if m_cap else None, "episode_nats": float(m_cap.group(2)) if m_cap else None}
    sc = scores(tr, a.reference, a.items)
    exam_cfg = sc["reference"]["config"] or {}
    us = usage(tr, prices, cfg)
    turns, rows, lab, files = timeline(tr, lab_log, float(m_sig.group(1)) if m_sig else None, (exam_cfg.get("lab") or {}).get("reset_cost", 1))
    eps = None if lab is None else lab_episodes(lab, rows)
    fl, pc = flags(tr, turns, rows, lab, files, a.submission, a.long_s)
    # ---- summaries of the timeline ----
    by_kind, T = {}, {t["turn"]: t for t in turns}
    for r in rows:
        k = r["kinds"][0]
        d = by_kind.setdefault(k, {"calls": 0, "_turns": set()})
        d["calls"] += 1
        d["_turns"].add(r["turn"])
    for k, d in by_kind.items():
        ts = d.pop("_turns")
        d.update(turns=len(ts), model_s=round(sum(T[t]["model_s"] or 0 for t in ts), 1), tools_s=round(sum(T[t]["tools_s"] or 0 for t in ts), 1))
    by_kind = {k: by_kind[k] for k in KIND_ORDER if k in by_kind}

    def first(pred):
        r = next((r for r in rows if pred(r)), None)
        return None if r is None else {"turn": r["turn"], "t_s": T[r["turn"]]["t_s"]}
    miles = {"first_simulator_run": first(lambda r: "sim" in r["kinds"]), "first_laboratory_experiment": first(lambda r: "lab" in r["kinds"]),
             "first_write_under_submission/": first(lambda r: any(str(p).startswith("submission/") for p, _ in r["detail"].get("writes") or [])),
             "first_validation": first(lambda r: "validate" in r["kinds"]), "submit": first(lambda r: "submit" in r["kinds"])}
    tm, g = tr.get("timing") or {}, ph.get("grade") or {}
    span = lambda k: None if not tm.get(k) or tm[k].get("end") is None or tm[k].get("start") is None else tm[k]["end"] - tm[k]["start"]  # noqa: E731
    script = (tr.get("info") or {}).get("physim2_script")
    limits = []
    if lab is None:
        limits.append("No --lab-record: laboratory requests made from Python inside a bash call are known only as call sites in the code (no count, no ticks, "
                      "no nats per request, no order); only the totals of the laboratory's counters are exact. Requests through the `lab_call` tool are complete in the trace.")
    else:
        limits.append("The laboratory does not log the inputs of a request, only ticks and nats: `zero` is exact (0 nats charged), `blind` or `structured` for "
                      "requests made from Python is a reading of the code that ran in that turn, and is absent when that code is not in the trace.")
    if sc["agent_per_item_source"] is None:
        limits.append("No --items: the trace holds the agent's mean loss only, so its row has no bootstrap, no per-item spread and no paired comparison.")
    if pc.get("source") is None:
        limits.append("The predictor's source is not in the trace (a scripted agent, or written by a program) and no --submission was given: whether it reads its history is not checked.")
    else:
        limits.append("The predictor check is a static reading: an argument passed on to a helper counts as read, and what the code does with it is not judged.")
    if script:
        limits.append("A scripted agent leaves no messages: what it did inside the box is not in the trace beyond the end of its own log" + ("" if lab is None else " and the laboratory's log") + ".")
    limits += ["What the agent read is taken from the commands it wrote: files opened inside a Python script, by a module it imported, or by a helper file the trace "
               "never shows are not seen; a path that is mentioned may not have been read. Network attempts likewise: names of tools and libraries, not packets.",
               "Kinds, input classes and flags are heuristics over text (the README lists the rules); the numbers of sections 1 to 4 are not.",
               "Why the agent did something, whether its modelling was sound, and whether real data ever entered its fit are for a reader of transcript.md.",
               "The noise shown is over the items of one instance; nothing here says how the agent would do on another hidden world."]
    R = {MARK: bool(sc["reference"]["pilot_marker"]), "name": a.name or (ep.get("run") or {}).get("name") or tr.get("id"),
         "inputs": {"trace": f"`{os.path.basename(tinfo['path'])}` (sha256 {tinfo['sha256'][:12]}…)", "reference table": f"`{sc['reference']['file']}` + `{sc['reference']['items_file']}`",
                    "laboratory log": "given" if lab is not None else "not given", "per-item scores of the agent": "given" if a.items else "not given",
                    "prices": (prices or {}).get("source") or "not given", "submission copy": "given" if a.submission else "not given"},
         "outcome": {"agent": cfg.get("model"), "harness": (cfg.get("harness") or {}).get("id"), "trace_id": tr.get("id"), "verifiers": (tr.get("verifiers") or {}).get("version"),
                     "ok": tr.get("ok"), "stop_condition": tr.get("stop_condition"), "ended_by_agent": tr.get("stop_condition") in ENDED_BY_AGENT, "is_timeout": tr.get("is_timeout"),
                     "errors": [e.get("type") for e in tr.get("errors") or []], "episode_errors": [e.get("type") for e in ep.get("errors") or []],
                     "submission": ph.get("submission") or {}, "lab": ph.get("lab") or {}, "n_items": g.get("n_items"), "n_failed": g.get("n_failed"),
                     "item_isolation": ph.get("item_isolation"), "network_restricted": ph.get("network_restricted"),
                     "box": {k: ((tr.get("agent") or {}).get("runtime") or {}).get(k) for k in ("image", "cpu", "memory")}},
         "scores": sc, "usage": us,
         "wall_s": {"boot": span("boot"), "setup": span("setup"), "agent": span("agent"), "finalize": span("finalize"), "verifier": g.get("verifier_wall_s"),
                    "agent_model": ((tm.get("agent") or {}).get("model") or {}).get("duration"), "agent_harness": ((tm.get("agent") or {}).get("harness") or {}).get("duration")},
         "budgets": None, "caps_in_task_text": caps_text,
         "timeline": {"script": script, "turns": turns, "rows": rows, "by_kind": by_kind, "milestones": miles, "lab_record_given": lab is not None,
                      "lab_route": {"tool": sum(r["detail"].get("via") == "tool" for r in rows), "python": sum(bool(r["detail"].get("lab_call_sites")) for r in rows)},
                      "lab_requests": lab, "lab_episodes": eps},
         "flags": fl, "flag_ids_checked": FLAG_IDS, "predictor_check": pc, "limits": limits}
    R["budgets"] = budgets(tr, cfg, us, exam_cfg, caps_text, eps, prices)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    with open(a.out + ".json", "w") as f:
        json.dump(R, f, indent=1, default=lambda o: o.item() if isinstance(o, np.generic) else str(o))
    with open(a.out + ".md", "w") as f:
        f.write(markdown(R))
    print(json.dumps({"report": a.out + ".md", "reward": sc["reward_in_trace"], "agent_skill_vs_O": sc["policies"]["AGENT"].get("skill_vs_O"),
                      "turns": len(turns), "tool_calls": len(rows), "cost_usd": us.get("cost_usd_for_the_ledger"), "flags": [x["id"] for x in fl],
                      "checks": sc["checks"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
