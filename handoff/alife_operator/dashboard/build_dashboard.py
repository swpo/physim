#!/usr/bin/env python3
"""Build the ALife dashboard page: overview, score facts, one clip card per met grand challenge,
the open challenges, and three interactive charts (challenges met, capability reach, knowledge).

Inputs (all regenerated or edited between publishes):
  REPO/research/alife/collective/{STATE.md, progress.json, seed/challenges.json}
  SCRATCH/challenge_history.json   status of every challenge after each STATE.md change (git history)
  SCRATCH/dashboard/cards.json     per challenge: clip files, watch_for, settings, notes (hand-curated)
Output: SCRATCH/artifact/alife_lab.html and SCRATCH/artifact/media/challenges/<id>.{mp4,jpg}
"""
import html, json, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/user/physim")
COL = REPO / "research/alife/collective"
SCRATCH = Path("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad")
ART = SCRATCH / "artifact"
GH = "https://github.com/swpo/physim/tree/claude/fisim-agent-world-research-hepmlz/research/alife/"
STATE_URL = "https://github.com/swpo/physim/blob/claude/fisim-agent-world-research-hepmlz/research/alife/collective/STATE.md"
EQ_URL = "https://claude.ai/artifact/B3yhNbfmE4QSzbboQWoXMf"

E = html.escape


def history():
    """Status of every challenge row after each change of STATE.md (from the librarian clone's git log)."""
    out, prev = [], None
    log = subprocess.run(["git", "-C", "/home/user/librarian", "log", "--reverse", "--format=%H %cI", "--",
                          "research/alife/collective/STATE.md"], capture_output=True, text=True).stdout
    for line in log.splitlines():
        h, t = line.split()
        s = subprocess.run(["git", "-C", "/home/user/librarian", "show", f"{h}:research/alife/collective/STATE.md"],
                           capture_output=True, text=True).stdout
        rows = table(s)
        if rows and rows != prev:
            out.append({"t": t, "rows": rows})
            prev = rows
    (SCRATCH / "challenge_history.json").write_text(json.dumps(out, indent=1))
    return out


def table(s):
    i = s.find("## Grand challenges")
    if i < 0:
        return {}
    j = s.find("\n## ", i + 5)
    rows = {}
    for r in s[i:j if j > 0 else len(s)].splitlines():
        m = re.match(r"\| (.+?) \| `([A-Z]+)`( \(BD\))? \| (.+?) \|$", r)
        if m and m.group(1) != "Challenge":
            rows[m.group(1)] = m.group(4)
    return rows


def fmt_t(t):
    d = datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(timezone.utc)
    return f"{d.day} Oct {d:%H:%M}"


def main():
    hist = history() if "--no-history" not in sys.argv else json.loads((SCRATCH / "challenge_history.json").read_text())
    chal = json.loads((COL / "seed/challenges.json").read_text())
    chal = chal if isinstance(chal, list) else chal.get("challenges", chal)
    by_title = {c["title"]: c for c in chal}
    state = (COL / "STATE.md").read_text()
    live = table(state)
    gen = re.search(r"Generated (\S+)", state).group(1)
    score = re.search(r"Reach P = \*\*(\d+)\*\*.*?P_BD = \*\*(\d+)\*\*.*?Q = \*\*(\d+)\*\*.*?K = \*\*(\d+)\*\*.*?C = \*\*(\d+)\*\*.*?P would be (\d+)", state, re.S).groups()
    act = re.search(r"\*\*Activity\.\*\* (\d+) contributions.*?([\d.]+) CPU hours", state, re.S).groups()
    cards = json.loads((SCRATCH / "dashboard/cards.json").read_text())

    # met time = the last transition of the row to "achieved"
    met_at, last = {}, {}
    for e in hist:
        for k, v in e["rows"].items():
            a = v.startswith("achieved")
            if a and not last.get(k):
                met_at[k] = e["t"]
            last[k] = a

    met, opened = [], []
    for title, status in live.items():
        c = by_title.get(title)
        if not c:
            continue
        (met if status.startswith("achieved") else opened).append((c, status, title))
    met.sort(key=lambda x: met_at.get(x[2], ""))

    media = ART / "media/challenges"
    media.mkdir(parents=True, exist_ok=True)
    card_html = []
    for c, status, title in met:
        cid = c["id"]
        info = cards.get(cid, {})
        holders = re.findall(r"([\w.-]+#c\d+) \(([^)]+)\)", status)
        audit = "; ".join(sorted({h[1] for h in holders}))
        note = info.get("status_note", "")
        video = ""
        if info.get("clip") and Path(info["clip"]).exists():
            shutil.copy(info["clip"], media / f"{cid}.mp4")
            shutil.copy(info["poster"], media / f"{cid}.jpg")
            w, h = info.get("width", 16), info.get("height", 9)
            video = (f'<div class="frame" style="aspect-ratio:{w} / {h}"><video muted loop playsinline controls preload="none" '
                     f'poster="media/challenges/{cid}.jpg" aria-label="{E(info.get("alt", title))}">'
                     f'<source src="media/challenges/{cid}.mp4" type="video/mp4"></video></div>')
        else:
            video = '<div class="frame pending"><span>clip being rendered</span></div>'
        claim = info.get("claim_dir", "")
        who = info.get("who", "")
        bd = ' <span class="tag">beyond diffusion</span>' if c.get("bd") else ""
        card_html.append(f"""      <article class="card" id="{E(cid)}">
        {video}
        <div class="text">
          <div class="tagrow"><span class="tag">{E(c['target'])}</span>{bd}<span class="when">met {E(fmt_t(met_at.get(title, gen)))}</span></div>
          <h3>{E(title)}</h3>
          <p>{E(info.get('watch_for', ''))}</p>
          <p class="status"><span class="dot {'ok' if 'audited' in audit or 'committee' in audit else 'wait'}"></span>{E(audit or 'held')}{(' · ' + E(note)) if note else ''}</p>
          <details class="settings"><summary>Run settings and colours</summary><p>{E(info.get('settings', ''))}</p></details>
          <p class="claim">{('<a href="' + E(GH + claim) + '">' + E(info.get('claim_label', claim)) + '</a>') if claim else ''}{(' · ' + E(who)) if who else ''}</p>
        </div>
      </article>""")

    open_html = []
    for c, status, title in opened:
        note = cards.get(c["id"], {}).get("open_note", "")
        open_html.append(f'<li><span class="tag">{E(c["target"])}</span> <b>{E(title)}</b>{(". " + E(note)) if note else ""}</li>')

    # chart data: score change points, challenge counts after each change
    prog = json.loads((COL / "progress.json").read_text())["series"]
    keys = ["P", "P_prov", "P_BD", "Q", "K", "C"]
    pts, pv = [], None
    for i, p in enumerate(prog):
        v = tuple(p[k] for k in keys)
        if v != pv or i == len(prog) - 1:
            pts.append([p["t"]] + list(v))
            pv = v
    cnt, events, last = [], [], {}
    for e in hist:
        m = sum(v.startswith("achieved") for v in e["rows"].values())
        cnt.append([e["t"], m, len(e["rows"])])
        for k, v in e["rows"].items():
            a = v.startswith("achieved")
            if k not in last and len(cnt) > 1:
                events.append([e["t"], "set", k])
            elif k in last and a != last[k]:
                events.append([e["t"], "met" if a else "reopened", k])
            last[k] = a
    cnt.append([gen if gen.endswith("Z") else gen + "Z", cnt[-1][1], cnt[-1][2]])
    data = {"score": pts, "keys": keys, "count": cnt, "events": events}

    tpl = (SCRATCH / "dashboard/template.html").read_text()
    page = (tpl.replace("{{SNAP}}", E(fmt_t(gen)))
               .replace("{{P}}", score[0]).replace("{{P_BD}}", score[1]).replace("{{Q}}", score[2])
               .replace("{{K}}", score[3]).replace("{{C}}", score[4]).replace("{{P_PROV}}", score[5])
               .replace("{{CONTRIB}}", act[0]).replace("{{CPU}}", str(round(float(act[1]))))
               .replace("{{MET}}", str(len(met))).replace("{{TOTAL}}", str(len(met) + len(opened)))
               .replace("{{CARDS}}", "\n".join(card_html)).replace("{{OPEN}}", "\n        ".join(open_html))
               .replace("{{STATE_URL}}", STATE_URL).replace("{{EQ_URL}}", EQ_URL)
               .replace("{{SESSIONS}}", str(cards.get("_sessions", "")))
               .replace("{{DATA}}", json.dumps(data, separators=(",", ":"))))
    (ART / "alife_lab.html").write_text(page)
    print(f"wrote {ART/'alife_lab.html'} ({len(page)} bytes): {len(met)} met, {len(opened)} open, "
          f"{len(pts)} score points, {len(events)} events; clips: "
          + ", ".join(c['id'] for c, _, _ in met if cards.get(c['id'], {}).get('clip')))


if __name__ == "__main__":
    main()
