"""physim.traces — trace-viewer gallery: rollouts as human-readable lab reports.

Builds docs/rollouts.html from outputs/*/traces.jsonl. For each rollout:
  1. a NARRATIVE experiment log — tool calls parsed, classified (noise floor,
     port probes, uniform drives, pin->release, closed-loop policies, ...),
     merged into phases, and rendered as prose + a lab-notebook timeline figure
     (drive profile over world time + observed sensor tracks);
  2. the agent-written workspace files (theories, data libraries);
  3. preparation-contract and theory results where present;
  4. contracts truth-vs-answer table;
  5. the verbatim log (collapsed).

Usage: .venv/bin/python -m physim.traces [--out docs/rollouts.html] [--max-per-pair N]
"""
from __future__ import annotations

import base64
import glob
import html as _html
import io
import json
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

MAX_PER_PAIR = 3
LOG_LINE_CAP = 200
FILE_RENDER_CAP = 20_000
FIG_MIN_EVENTS = 4          # skip figures for near-empty rollouts

plt.rcParams.update({
    "figure.facecolor": "white", "axes.titlesize": 8.5, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.spines.top": False,
    "axes.spines.right": False, "font.family": "sans-serif", "legend.fontsize": 6.5,
})


def esc(s: str) -> str:
    return _html.escape(str(s), quote=False)


# ------------------------------------------------------------------ loading
def load_rollouts(outputs_glob: str) -> list[dict]:
    rolls = []
    for d in sorted(glob.glob(outputs_glob), key=os.path.getmtime):
        tp = os.path.join(d, "traces.jsonl")
        if not os.path.exists(tp):
            continue
        pair = d.split("outputs/")[-1].split("/")[0]
        for line in open(tp):
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            for itr in rec.get("traces", []):
                info = (itr.get("info") or {}).get("physim") or {}
                rew = (itr.get("rewards") or {}).get("accuracy", {}).get("score")
                if rew is None or not info:
                    continue
                rolls.append(dict(pair=pair, run=d, trace=itr, info=info,
                                  reward=rew, rewards=itr.get("rewards") or {},
                                  metrics=itr.get("metrics") or {}))
    return rolls


def node_text(msg) -> str:
    c = msg.get("content")
    if isinstance(c, list):
        c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
    return c or ""


def _try_json(s):
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return None


# ------------------------------------------------------- experiment parsing
def _tool_result_payload(text: str):
    """Tool node content -> the physim response dict, if any."""
    if "Output:" in text:
        text = text.split("Output:", 1)[1]
    obj = _try_json(text.strip())
    if isinstance(obj, dict) and "result" in obj:
        inner = obj["result"]
        obj = _try_json(inner) if isinstance(inner, str) else inner
    return obj if isinstance(obj, dict) else None


def parse_events(itr: dict) -> list[dict]:
    """Ordered physim interaction events with parsed args + responses.

    Handles the tools tier (tool_calls + tool nodes) and the chat tier
    (assistant JSON command -> user JSON response)."""
    nodes = itr.get("nodes") or []
    # map tool_call_id -> tool response payload
    responses = {}
    for n in nodes:
        msg = n.get("message") or {}
        if msg.get("role") == "tool" and msg.get("tool_call_id"):
            payload = _tool_result_payload(node_text(msg))
            if payload is not None:
                responses[msg["tool_call_id"]] = payload
    events = []
    for n in nodes:
        msg = n.get("message") or {}
        role = msg.get("role")
        if role == "assistant":
            for tc in (msg.get("tool_calls") or []):
                name = (tc.get("name") or "").replace("mcp__physim__", "")
                if name not in ("run", "run_policy", "reset", "ready",
                                "answer", "answer_prep", "submit_theory", "status"):
                    continue
                args = _try_json(tc.get("arguments") or "{}") or {}
                events.append(dict(op=name, args=args,
                                   resp=responses.get(tc.get("id"))))
            # chat tier: the command is the message text
            if not msg.get("tool_calls"):
                cmd = _try_json_last(node_text(msg))
                if isinstance(cmd, dict) and cmd.get("op"):
                    events.append(dict(op=cmd["op"], args=cmd, resp=None,
                                       _chat=True))
        elif role == "user" and events and events[-1].get("_chat") and events[-1]["resp"] is None:
            payload = _try_json_last(node_text(msg))
            if isinstance(payload, dict):
                events[-1]["resp"] = payload
    return events


def _try_json_last(text: str):
    """Last parsable {...} block in a text (chat tier tolerance)."""
    obj = _try_json(text)
    if obj is not None:
        return obj
    depth, start, cands = 0, None, []
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None:
                cands.append(text[start:i + 1])
    for c in reversed(cands):
        obj = _try_json(c)
        if isinstance(obj, dict):
            return obj
    return None


def _seg_profile(args: dict):
    """[(duration, mean_u)] per segment; None for unparseable."""
    segs = args.get("segments")
    if isinstance(segs, str):
        segs = _try_json(segs)
    if not isinstance(segs, list):
        return None
    prof = []
    for s in segs:
        if not isinstance(s, dict):
            return None
        t = s.get("t")
        if not isinstance(t, (int, float)):
            return None
        if "u" in s and isinstance(s["u"], list):
            u = [x for x in s["u"] if isinstance(x, (int, float))]
            prof.append((int(t), float(np.mean(u)) if u else 0.0,
                         [i for i, x in enumerate(s["u"])
                          if isinstance(x, (int, float)) and abs(x) > 0.02]))
        elif "u_start" in s and "u_end" in s:
            a = [x for x in s.get("u_start", []) if isinstance(x, (int, float))]
            b = [x for x in s.get("u_end", []) if isinstance(x, (int, float))]
            ma = float(np.mean(a)) if a else 0.0
            mb = float(np.mean(b)) if b else 0.0
            prof.append((int(t), (ma + mb) / 2, ["ramp"]))
        else:
            return None
    return prof


def classify_run(args: dict) -> tuple[str, str]:
    """(label, detail) for a run event."""
    prof = _seg_profile(args)
    if prof is None:
        return "experiment", ""
    total = sum(p[0] for p in prof)
    amps = [p[1] for p in prof]
    ports_sets = [p[2] for p in prof]
    all_quiet = all(abs(a) <= 0.02 for a in amps)
    if all_quiet:
        return "free run", f"{total} ticks, all inputs 0"
    has_ramp = any(p == ["ramp"] for p in ports_sets)
    ends_quiet = abs(amps[-1]) <= 0.02 and len(prof) > 1
    drive_ports = set()
    for p in ports_sets:
        if p != ["ramp"]:
            drive_ports.update(p)
    peak = max(amps, key=abs)
    if has_ramp:
        return "ramp sweep", f"{total} ticks, peak mean drive {peak:+.2f}"
    if ends_quiet:
        return "drive → release", (f"drive {peak:+.2f} for "
                                   f"{sum(p[0] for p in prof[:-1])}t, release {prof[-1][0]}t")
    if len(drive_ports) == 1:
        return "single-port probe", f"port {next(iter(drive_ports))} at {peak:+.2f}, {total}t"
    if len(drive_ports) <= 4 and drive_ports:
        return "multi-port probe", f"ports {sorted(drive_ports)} at {peak:+.2f}, {total}t"
    return "uniform drive", f"{peak:+.2f} held {total}t"


def _first_comment(code: str) -> str:
    for line in (code or "").splitlines():
        s = line.strip()
        if s.startswith("#"):
            return s.lstrip("# ")
        if s and not s.startswith(("def ", "import ", "from ")):
            break
    return ""


# ------------------------------------------------------------- narrative
def narrate(events: list[dict]) -> tuple[list[str], list[dict]]:
    """(paragraph list, enriched timeline for figures)."""
    story, timeline = [], []
    tick = 0
    last_obs: dict[int, float] = {}
    group = None  # (label, count, ticks, details, movers)

    def flush():
        nonlocal group
        if not group:
            return
        label, count, ticks, detail, movers = group
        head = f"{count}× {label}" if count > 1 else label.capitalize()
        s = f"{head} ({ticks:,} ticks{'; ' + detail if detail else ''})"
        if movers:
            tops = sorted(movers.items(), key=lambda kv: -abs(kv[1][1] - kv[1][0]))[:3]
            frag = ", ".join(f"ch{c} {a:+.2f}→{b:+.2f}" for c, (a, b) in tops
                             if abs(b - a) > 0.15)
            if frag:
                s += f" — {frag}"
        story.append(s + ".")
        group = None

    for ev in events:
        op, args, resp = ev["op"], ev.get("args") or {}, ev.get("resp")
        err = (resp or {}).get("error")
        if op == "status":
            continue
        if op == "run" or op == "run_policy":
            if op == "run_policy":
                label = "closed-loop policy"
                t = args.get("t") or 0
                detail = f"{t}t"
                note = _first_comment(args.get("code", ""))
                if note:
                    detail += f' — "{note[:80]}"'
                prof = None
            else:
                label, detail = classify_run(args)
                prof = _seg_profile(args)
                t = sum(p[0] for p in prof) if prof else 0
            if err:
                flush()
                msg = f"✗ {label} rejected: {err[:110]}."
                if story and story[-1].startswith(msg[:40]):
                    # collapse repeats: "... (xN)"
                    import re as _re
                    m = _re.search(r" \(x(\d+)\)$", story[-1])
                    n_ = (int(m.group(1)) + 1) if m else 2
                    story[-1] = msg + f" (x{n_})"
                else:
                    story.append(msg)
                continue
            # observations
            movers = {}
            if isinstance(resp, dict) and isinstance(resp.get("tail_mean"), dict):
                for cs, v in resp["tail_mean"].items():
                    try:
                        c = int(cs); v = float(v)
                    except (TypeError, ValueError):
                        continue
                    old = last_obs.get(c)
                    if old is not None:
                        movers[c] = (old, v)
                    last_obs[c] = v
            timeline.append(dict(kind=op, t0=tick, t1=tick + t, prof=prof,
                                 obs=dict(last_obs)))
            tick += t
            if group and group[0] == label:
                group = (label, group[1] + 1, group[2] + t,
                         group[3] or detail, {**group[4], **movers})
            else:
                flush()
                group = (label, 1, t, detail, movers)
        elif op == "reset":
            flush()
            if not err:
                story.append("Reset to fresh initial conditions (−200 ticks).")
                timeline.append(dict(kind="reset", t0=tick, t1=tick + 200))
                tick += 200
                last_obs.clear()
        elif op == "ready":
            flush()
            if err:
                story.append(f"✗ ready refused: {err[:110]}.")
            else:
                n_c = len((resp or {}).get("contracts") or [])
                n_p = len((resp or {}).get("preparation_contracts") or [])
                s = f"Ended exploration → received {n_c} prediction contracts"
                if n_p:
                    s += f" + {n_p} preparation contracts"
                story.append(s + ".")
                timeline.append(dict(kind="ready", t0=tick, t1=tick))
        elif op == "answer_prep":
            flush()
            code = args.get("code", "")
            intent = _first_comment(code)
            s = f"Submitted preparation policy for contract {args.get('id')}" \
                + (f' ("{intent[:90]}")' if intent else f" ({len(code)} chars)")
            if err:
                s += f" — ✗ {err[:80]}"
            story.append(s + ".")
        elif op == "submit_theory":
            flush()
            code = args.get("code", "")
            s = f"Submitted an executable theory ({len(code):,} chars)"
            if err:
                s += f" — ✗ {err[:80]}"
            story.append(s + ".")
        elif op == "answer":
            flush()
            n = len((args.get("answers") or []))
            story.append(f"Submitted {n} contract answers.")
    flush()
    return story, timeline


# ------------------------------------------------------------------ figures
def timeline_figure(timeline: list[dict]) -> str | None:
    runs = [e for e in timeline if e["kind"] in ("run", "run_policy")]
    if len(runs) < FIG_MIN_EVENTS:
        return None
    # choose up to 4 channels observed most often
    counts: dict[int, int] = defaultdict(int)
    for e in runs:
        for c in (e.get("obs") or {}):
            counts[c] += 1
    chans = [c for c, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:4]]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 3.1), sharex=True,
                                   height_ratios=[1, 1.6])
    fig.subplots_adjust(hspace=0.25)
    for e in timeline:
        if e["kind"] == "run" and e.get("prof"):
            t = e["t0"]
            for dur, amp, _ in e["prof"]:
                ax1.fill_between([t, t + dur], 0, amp, step="pre",
                                 color="#1f77b4", alpha=0.75, linewidth=0)
                t += dur
        elif e["kind"] == "run_policy":
            ax1.axvspan(e["t0"], e["t1"], color="#8250df", alpha=0.30)
        elif e["kind"] == "reset":
            for ax in (ax1, ax2):
                ax.axvline(e["t0"], color="#d62728", lw=0.8, ls=":")
        elif e["kind"] == "ready":
            for ax in (ax1, ax2):
                ax.axvline(e["t0"], color="black", lw=1.2, ls="--")
    ax1.set_ylabel("mean drive")
    ax1.set_ylim(-1.05, 1.05)
    ax1.axhline(0, color="gray", lw=0.4)
    ax1.set_title("agent's experiment timeline — blue: open-loop drive, "
                  "purple: closed-loop policy, red dots: reset, dashes: ready",
                  loc="left")
    colors = plt.cm.tab10.colors
    for i, c in enumerate(chans):
        xs, ys = [], []
        for e in runs:
            if c in (e.get("obs") or {}):
                xs.append(e["t1"]); ys.append(e["obs"][c])
        ax2.plot(xs, ys, "o-", ms=2.5, lw=0.8, color=colors[i % 10], label=f"ch{c}")
    ax2.set_ylabel("observed tail mean")
    ax2.set_xlabel("world time (ticks)")
    ax2.axhline(0, color="gray", lw=0.4)
    if chans:
        ax2.legend(ncol=min(4, len(chans)), loc="best")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=88, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------- workspace
def workspace_from_tool_calls(itr: dict) -> dict:
    files: dict[str, str] = {}
    for n in itr.get("nodes") or []:
        msg = n.get("message") or {}
        if msg.get("role") != "assistant":
            continue
        for tc in (msg.get("tool_calls") or []):
            name = tc.get("name") or ""
            args = _try_json(tc.get("arguments") or "{}") or {}
            if name == "Write" and "file_path" in args:
                files[args["file_path"]] = str(args.get("content", ""))
            elif name == "Edit" and args.get("file_path") in files:
                o, nw = str(args.get("old_string", "")), str(args.get("new_string", ""))
                if o:
                    files[args["file_path"]] = files[args["file_path"]].replace(o, nw, 1)
    return files


# ---------------------------------------------------------------- tables
def answers_vs_truth(info: dict) -> str:
    detail = info.get("detail") or []
    if not detail:
        return ""
    rows = ["<tr><th>id</th><th>stratum</th><th>truth μ</th><th>scale</th>"
            "<th>|z|</th><th>accuracy</th><th>covered</th></tr>"]
    for d in detail:
        z = d.get("z")
        rows.append(
            f"<tr><td>{d.get('id')}</td><td>{d.get('stratum')}</td>"
            f"<td>{d.get('mu'):+.3f}</td><td>{d.get('scale', 0):.3f}</td>"
            f"<td>{'—' if z is None else f'{z:.1f}'}</td>"
            f"<td>{d.get('accuracy'):.3f}</td>"
            f"<td>{'✓' if d.get('covered') else '✗'}</td></tr>")
    return "<table>" + "".join(rows) + "</table>"


def prep_table(info: dict) -> str:
    pd_ = info.get("prep_detail") or []
    if not pd_:
        return ""
    rows = ["<tr><th>id</th><th>channel</th><th>band</th><th>success</th>"
            "<th>released finals</th></tr>"]
    for d in pd_:
        finals = ", ".join(f"{v:+.2f}" for v in (d.get("finals") or []) if v is not None)
        err = (d.get("errors") or [None])[0]
        rows.append(f"<tr><td>{d['id']}</td><td>{d.get('channel')}</td>"
                    f"<td>[{d['band'][0]:+.2f}, {d['band'][1]:+.2f}]</td>"
                    f"<td>{d['success_rate']:.0%}</td>"
                    f"<td>{esc(finals) or esc(str(err)[:60] if err else '—')}</td></tr>")
    return "<h4>Preparation contracts</h4><table>" + "".join(rows) + "</table>"


def theory_block(info: dict, metrics: dict) -> str:
    th = info.get("theory")
    if not th:
        return ""
    per = {k[11:]: round(v, 2) for k, v in metrics.items() if k.startswith("theory_acc")}
    return (f"<h4>Executable theory</h4><p class='meta'>accuracy "
            f"{th.get('theory_accuracy', 0):.3f} · per-stratum {esc(str(per))} · "
            f"{th.get('code_chars', 0):,} chars</p>")


# ---------------------------------------------------------------- verbatim
def condensed_log(itr: dict) -> list[tuple[str, str]]:
    out = []
    for n in itr.get("nodes") or []:
        msg = n.get("message") or {}
        role = msg.get("role")
        if role == "assistant":
            for tc in (msg.get("tool_calls") or []):
                name = (tc.get("name") or "").replace("mcp__physim__", "physim.")
                args = tc.get("arguments") or ""
                if name.startswith("physim."):
                    out.append(("call", f"{name}({args[:LOG_LINE_CAP]})"))
                elif name in ("Write", "Edit"):
                    fp = (_try_json(args) or {}).get("file_path", "?")
                    out.append(("file", f"{name}: {fp}"))
            txt = node_text(msg).strip()
            if txt and len(txt) > 60:
                out.append(("note", txt[:400]))
        elif role == "tool":
            payload = _tool_result_payload(node_text(msg))
            if isinstance(payload, dict):
                keep = {k: payload[k] for k in
                        ("ticks_run", "budget_left", "error", "phase", "received")
                        if k in payload}
                if keep:
                    out.append(("result", json.dumps(keep)))
    return out


# ---------------------------------------------------------------- rendering
def render_rollout(r: dict) -> str:
    itr, info, met = r["trace"], r["info"], r["metrics"]
    model = (itr.get("calls") or [{}])[0].get("model", "?")
    rews = {k: v.get("score") for k, v in r["rewards"].items() if isinstance(v, dict)}
    rew_str = " · ".join(f"{k} <b>{v:.2f}</b>" for k, v in rews.items() if v is not None)
    parts = [f'<details class="roll"><summary><b>{esc(model)}</b> · '
             f'{info.get("difficulty")} seed {info.get("world_seed")} · '
             f'tier {info.get("tier")} · {rew_str} · '
             f'budget {met.get("budget_used_frac", 0):.0%}</summary>']
    strata = " · ".join(f"{k[4:]}={met.get(k, 0):.2f}"
                        for k in ("acc_S1", "acc_S2", "acc_S3", "acc_S4") if k in met)
    parts.append(f'<p class="meta">{strata} · coverage {met.get("coverage", 0):.2f} · '
                 f'{len(itr.get("nodes") or [])} nodes</p>')

    events = parse_events(itr)
    story, timeline = narrate(events)
    if story:
        parts.append("<h4>Narrative experiment log</h4>")
        fig = timeline_figure(timeline)
        if fig:
            parts.append(f'<img src="data:image/png;base64,{fig}" alt="timeline"/>')
        parts.append("<ol class='story'>")
        parts.extend(f"<li>{esc(s)}</li>" for s in story)
        parts.append("</ol>")

    ws = info.get("workspace") or workspace_from_tool_calls(itr)
    if ws:
        parts.append("<h4>Agent-written files (its instruments &amp; theories)</h4>")
        for path in sorted(ws, key=lambda p: (not p.lower().endswith(".md"), p)):
            body = ws[path]
            shown = body[:FILE_RENDER_CAP]
            more = f" … [+{len(body) - len(shown):,} chars]" if len(body) > len(shown) else ""
            parts.append(f"<details><summary><code>{esc(path)}</code> "
                         f"({len(body):,} chars)</summary>"
                         f"<pre>{esc(shown)}{more}</pre></details>")

    parts.append(prep_table(info))
    parts.append(theory_block(info, met))
    tbl = answers_vs_truth(info)
    if tbl:
        parts.append("<h4>Prediction contracts: truth vs answer</h4>" + tbl)

    log = condensed_log(itr)
    if log:
        parts.append(f"<details><summary>Verbatim log ({len(log)} entries)</summary>"
                     "<pre class='log'>")
        for kind, line in log:
            cls = {"call": "c", "result": "r", "file": "f", "note": "n"}[kind]
            parts.append(f'<span class="{cls}">{esc(line)}</span>')
        parts.append("</pre></details>")
    parts.append("</details>")
    return "\n".join(parts)


HEAD = """<!doctype html><html><head><meta charset="utf-8"/>
<title>physim rollouts — trace gallery</title><style>
body { font-family: -apple-system, Segoe UI, Helvetica, Arial, sans-serif;
       max-width: 1080px; margin: 24px auto; padding: 0 16px; color: #1a1a1a; }
h1 { font-size: 24px; } h2 { font-size: 19px; margin-top: 36px;
     border-bottom: 2px solid #eee; padding-bottom: 6px; }
h4 { margin: 16px 0 6px; }
details.roll { border: 1px solid #d0d7de; border-radius: 8px; margin: 10px 0;
               padding: 8px 14px; background: #fbfcfd; }
details.roll > summary { cursor: pointer; font-size: 14px; }
details details { margin: 6px 0 6px 12px; }
pre { background: #f6f8fa; border-radius: 6px; padding: 10px; font-size: 11.5px;
      overflow-x: auto; white-space: pre-wrap; word-break: break-word; }
pre.log span { display: block; }
pre.log .c { color: #0550ae; } pre.log .r { color: #57606a; }
pre.log .f { color: #8250df; font-weight: 600; } pre.log .n { color: #1a7f37; }
ol.story { font-size: 13.5px; line-height: 1.5; margin: 8px 0; padding-left: 26px; }
ol.story li { margin: 2px 0; }
img { max-width: 100%; height: auto; border: 1px solid #e1e4e8; border-radius: 6px;
      margin: 6px 0; }
table { border-collapse: collapse; font-size: 12px; margin: 8px 0; }
td, th { border: 1px solid #d0d7de; padding: 3px 8px; text-align: center; }
.meta { color: #57606a; font-size: 12.5px; margin: 4px 0; }
.note { background: #f6f8fa; border-left: 4px solid #0969da; padding: 10px 14px;
        border-radius: 4px; margin: 12px 0; font-size: 14px; }
code { background: #f6f8fa; padding: 1px 5px; border-radius: 4px; }
</style></head><body>
<nav style="font-size:14px;margin-bottom:18px;">
<a href="index.html">home</a> · <a href="results.html">results</a> ·
<a href="worlds.html">worlds</a> ·
<a href="scoring.html">scoring</a> ·
rollouts: <a href="rollouts-bulk.html"><b>bulk</b></a> ·
<a href="rollouts-chemistry.html"><b>chemistry</b></a> ·
<a href="rollouts-life.html"><b>life</b></a> ·
<a href="https://github.com/swpo/physim">github</a></nav>
<h1>physim rollouts — what the agents actually did</h1>
<p class="note">Each rollout below is reconstructed from its complete trace.
The <b>narrative log</b> translates the agent's raw tool calls into a readable
experiment sequence, with a lab-notebook timeline (top: drive the agent applied;
bottom: what its most-watched sensors read). Then: the files it wrote (its
instruments and theories), preparation-contract outcomes, its executable theory
score, and every prediction contract vs ground truth. The verbatim call log is
collapsed at the bottom. Best/median/worst rollout per pairing, plus the most
artifact-rich.</p>
"""


def build(out_path="docs/rollouts.html",
          outputs_glob="outputs/*/*", max_per_pair=MAX_PER_PAIR,
          track: str | None = None) -> str:
    rolls = load_rollouts(outputs_glob)
    # keep only the LATEST rollout per (pair, difficulty, seed) — reruns supersede
    latest: dict[tuple, dict] = {}
    for r in rolls:                      # rolls are in mtime order
        key = (r["pair"], r["info"].get("difficulty"), r["info"].get("world_seed"))
        latest[key] = r
    groups = defaultdict(list)
    for r in latest.values():
        diff = r["info"].get("difficulty") or ""
        if track == "bulk" and not diff.startswith("D"):
            continue
        if track == "chemistry" and not diff.startswith("C"):
            continue
        if track == "life" and not (diff.startswith("B") or diff.startswith("E")):
            continue
        groups[(r["pair"], diff)].append(r)
    parts = [HEAD]
    for (pair, diff), rs in sorted(groups.items(),
                                   key=lambda kv: (kv[0][1] or "", kv[0][0])):
        rs = sorted(rs, key=lambda r: -r["reward"])
        if len(rs) <= max_per_pair:
            pick = rs
        else:
            pick = [rs[0], rs[len(rs) // 2], rs[-1]]
            def richness(r):
                ws = (r["info"].get("workspace") or
                      workspace_from_tool_calls(r["trace"]))
                return sum(len(v) for v in ws.values())
            richest = max(rs, key=richness)
            if richness(richest) > 0 and richest not in pick:
                pick[1] = richest
            pick = sorted(pick, key=lambda r: -r["reward"])
        parts.append(f"<h2>{esc(pair.replace('physim--', ''))} — {diff} "
                     f"({len(rs)} rollouts, mean acc "
                     f"{np.mean([x['reward'] for x in rs]):.3f})</h2>")
        for r in pick:
            parts.append(render_rollout(r))
    parts.append("<p class='meta'>Generated by <code>python -m physim.traces</code>. "
                 "Narratives and figures are parsed from the raw traces; workspace "
                 "files come from artifact collection (v0.1.3+) or Write/Edit "
                 "reconstruction for older rollouts.</p></body></html>")
    html = "\n".join(parts)
    from pathlib import Path
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return str(out)


if __name__ == "__main__":
    import sys
    mpp = int(sys.argv[sys.argv.index("--max-per-pair") + 1]) if "--max-per-pair" in sys.argv else MAX_PER_PAIR
    if "--out" in sys.argv:
        print("wrote", build(sys.argv[sys.argv.index("--out") + 1], max_per_pair=mpp))
    else:
        print("wrote", build("docs/rollouts-bulk.html", max_per_pair=mpp, track="bulk"))
        print("wrote", build("docs/rollouts-chemistry.html", max_per_pair=mpp, track="chemistry"))
        print("wrote", build("docs/rollouts-life.html", max_per_pair=mpp, track="life"))
