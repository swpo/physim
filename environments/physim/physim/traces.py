"""physim.traces — trace-viewer gallery: rollouts as human-readable lab reports.

Builds docs/rollouts.html from outputs/*/traces.jsonl: for each tools-tier
rollout a condensed experiment log (tool calls + world responses), the agent's
written workspace files (MODEL.md etc.), final answers vs truth, and metrics.
Chat-tier rollouts get the conversation log. Self-contained HTML.

Usage: .venv/bin/python -m physim.traces [--out docs/rollouts.html] [--max-per-pair N]
"""
from __future__ import annotations

import glob
import html as _html
import json
import os
from collections import defaultdict

MAX_PER_PAIR = 3          # best/median/worst per (pairing, difficulty)
LOG_LINE_CAP = 200
FILE_RENDER_CAP = 20_000


def esc(s: str) -> str:
    return _html.escape(str(s), quote=False)


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
                                  reward=rew, metrics=itr.get("metrics") or {}))
    return rolls


def node_text(msg) -> str:
    c = msg.get("content")
    if isinstance(c, list):
        c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
    return c or ""


def condensed_log(itr: dict) -> list[tuple[str, str]]:
    """(kind, line) entries: tool calls with args, tool results, assistant notes."""
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
                    try:
                        fp = json.loads(args).get("file_path", "?")
                    except json.JSONDecodeError:
                        fp = "?"
                    out.append(("file", f"{name}: {fp}"))
                else:
                    out.append(("other", f"{name}({args[:80]})"))
            txt = node_text(msg).strip()
            if txt and len(txt) > 60:
                out.append(("note", txt[:400]))
        elif role == "tool":
            txt = node_text(msg)
            if '"result"' in txt:
                try:
                    inner = json.loads(txt.split("Output:\n", 1)[-1])
                    res = inner.get("result", "")
                    obj = json.loads(res) if isinstance(res, str) else res
                    keep = {k: obj[k] for k in
                            ("ticks_run", "budget_left", "error", "phase", "received")
                            if isinstance(obj, dict) and k in obj}
                    if keep:
                        out.append(("result", json.dumps(keep)))
                except (json.JSONDecodeError, AttributeError):
                    pass
        elif role == "user" and itr_is_chat(itr):
            txt = node_text(msg)[:LOG_LINE_CAP]
            if txt:
                out.append(("world", txt))
    return out


def workspace_from_tool_calls(itr: dict) -> dict:
    """Fallback for rollouts predating artifact collection: reconstruct files
    from Write/Edit tool-call arguments (claude_code) or heredocs are skipped."""
    files: dict[str, str] = {}
    for n in itr.get("nodes") or []:
        msg = n.get("message") or {}
        if msg.get("role") != "assistant":
            continue
        for tc in (msg.get("tool_calls") or []):
            name = tc.get("name") or ""
            try:
                args = json.loads(tc.get("arguments") or "{}")
            except json.JSONDecodeError:
                continue
            if name == "Write" and "file_path" in args:
                files[args["file_path"]] = str(args.get("content", ""))
            elif name == "Edit" and args.get("file_path") in files:
                old_s = str(args.get("old_string", ""))
                new_s = str(args.get("new_string", ""))
                if old_s:
                    files[args["file_path"]] = files[args["file_path"]].replace(old_s, new_s, 1)
    return files


def itr_is_chat(itr) -> bool:
    return (((itr.get("info") or {}).get("physim") or {}).get("tier")) == "chat"


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


def render_rollout(r: dict, idx: int) -> str:
    itr, info = r["trace"], r["info"]
    met = r["metrics"]
    model = (itr.get("calls") or [{}])[0].get("model", "?")
    seed = info.get("world_seed")
    parts = [f'<details class="roll"><summary><b>{esc(model)}</b> · '
             f'{info.get("difficulty")} seed {seed} · tier {info.get("tier")} · '
             f'reward <b>{r["reward"]:.3f}</b> · '
             f'budget {met.get("budget_used_frac", 0):.0%}</summary>']
    strata = " · ".join(f"{k[4:]}={met.get(k, 0):.2f}"
                        for k in ("acc_S1", "acc_S2", "acc_S3", "acc_S4") if k in met)
    parts.append(f'<p class="meta">{strata} · coverage {met.get("coverage", 0):.2f} · '
                 f'{len(itr.get("nodes") or [])} nodes</p>')
    ws = info.get("workspace") or workspace_from_tool_calls(itr)
    if ws:
        parts.append("<h4>Agent-written files (its theory &amp; data)</h4>")
        for path in sorted(ws, key=lambda p: (not p.lower().endswith(".md"), p)):
            body = ws[path]
            shown = body[:FILE_RENDER_CAP]
            more = f" … [+{len(body) - len(shown):,} chars]" if len(body) > len(shown) else ""
            parts.append(f"<details><summary><code>{esc(path)}</code> "
                         f"({len(body):,} chars)</summary>"
                         f"<pre>{esc(shown)}{more}</pre></details>")
    log = condensed_log(itr)
    if log:
        parts.append(f"<h4>Experiment log ({len(log)} entries)</h4><pre class='log'>")
        for kind, line in log:
            cls = {"call": "c", "result": "r", "file": "f",
                   "note": "n", "world": "w", "other": "o"}[kind]
            parts.append(f'<span class="{cls}">{esc(line)}</span>')
        parts.append("</pre>")
    tbl = answers_vs_truth(info)
    if tbl:
        parts.append("<h4>Contracts: truth vs answer</h4>" + tbl)
    parts.append("</details>")
    return "\n".join(parts)


HEAD = """<!doctype html><html><head><meta charset="utf-8"/>
<title>physim rollouts — trace gallery</title><style>
body { font-family: -apple-system, Segoe UI, Helvetica, Arial, sans-serif;
       max-width: 1080px; margin: 24px auto; padding: 0 16px; color: #1a1a1a; }
h1 { font-size: 24px; } h2 { font-size: 19px; margin-top: 36px;
     border-bottom: 2px solid #eee; padding-bottom: 6px; }
h4 { margin: 14px 0 6px; }
details.roll { border: 1px solid #d0d7de; border-radius: 8px; margin: 10px 0;
               padding: 8px 14px; background: #fbfcfd; }
details.roll > summary { cursor: pointer; font-size: 14px; }
details details { margin: 6px 0 6px 12px; }
pre { background: #f6f8fa; border-radius: 6px; padding: 10px; font-size: 11.5px;
      overflow-x: auto; white-space: pre-wrap; word-break: break-word; }
pre.log span { display: block; }
pre.log .c { color: #0550ae; } pre.log .r { color: #57606a; }
pre.log .f { color: #8250df; font-weight: 600; } pre.log .n { color: #1a7f37; }
pre.log .w { color: #9a6700; } pre.log .o { color: #6e7781; }
table { border-collapse: collapse; font-size: 12px; margin: 8px 0; }
td, th { border: 1px solid #d0d7de; padding: 3px 8px; text-align: center; }
.meta { color: #57606a; font-size: 12.5px; margin: 4px 0; }
.note { background: #f6f8fa; border-left: 4px solid #0969da; padding: 10px 14px;
        border-radius: 4px; margin: 12px 0; font-size: 14px; }
code { background: #f6f8fa; padding: 1px 5px; border-radius: 4px; }
</style></head><body>
<h1>physim rollouts — what the agents actually did</h1>
<p class="note">Every rollout below is reconstructed from the complete trace:
the agent's tool calls (its experiments), the files it wrote in its sandbox
(its instruments, data libraries, and theories), and its final contract answers
scored against ground truth. Expand a rollout, then expand its files — reading
an agent's <code>MODEL.md</code> is the fastest way to judge whether it did
science or guessed. Best/median/worst rollout shown per pairing.</p>
"""


def build(out_path="docs/rollouts.html",
          outputs_glob="outputs/*/*", max_per_pair=MAX_PER_PAIR) -> str:
    rolls = load_rollouts(outputs_glob)
    groups = defaultdict(list)
    for r in rolls:
        groups[(r["pair"], r["info"].get("difficulty"))].append(r)
    parts = [HEAD]
    for (pair, diff), rs in sorted(groups.items(),
                                   key=lambda kv: (kv[0][1] or "", kv[0][0])):
        rs = sorted(rs, key=lambda r: -r["reward"])
        if len(rs) <= max_per_pair:
            pick = rs
        else:
            # best / median / worst, then swap the median for the most
            # artifact-rich rollout not already picked (theories > scores).
            pick = [rs[0], rs[len(rs) // 2], rs[-1]]
            def richness(r):
                ws = (r["info"].get("workspace") or
                      workspace_from_tool_calls(r["trace"]))
                return sum(len(v) for v in ws.values())
            richest = max(rs, key=richness)
            if richness(richest) > 0 and richest not in pick:
                pick[1] = richest
            pick = sorted(set(map(id, pick)) and pick, key=lambda r: -r["reward"])
        import numpy as np
        parts.append(f"<h2>{esc(pair.replace('physim--', ''))} — {diff} "
                     f"({len(rs)} rollouts, mean {np.mean([x['reward'] for x in rs]):.3f})</h2>")
        for i, r in enumerate(pick):
            parts.append(render_rollout(r, i))
    parts.append("<p class='meta'>Generated by <code>python -m physim.traces</code>. "
                 "Workspace files present only for rollouts run since artifact "
                 "collection landed (v0.1.3).</p></body></html>")
    html = "\n".join(parts)
    from pathlib import Path
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return str(out)


if __name__ == "__main__":
    import sys
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "docs/rollouts.html"
    mpp = int(sys.argv[sys.argv.index("--max-per-pair") + 1]) if "--max-per-pair" in sys.argv else MAX_PER_PAIR
    print("wrote", build(out, max_per_pair=mpp))
