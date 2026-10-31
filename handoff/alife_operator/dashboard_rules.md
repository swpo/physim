# Dashboard rules (ALife lab artifact)

Artifact: https://claude.ai/artifact/X3wa4n8wacbVmhzRJC8N4q
Source: scratchpad/artifact/alife_lab.html, media in scratchpad/artifact/media/ (clips under media/challenges/<slug>.mp4 + .jpg).

User's rule (2026-10-27, ~13:15Z): "When we get a new grand challenge we should add a clip of it to the
dashboard artifact. In fact that artifact should be mostly that plus the overview text and plots."

So the page is:
1. Overview text (what the collective is, how it scores) and the score facts.
2. Plots (librarian's progress.png, refreshed from research/alife/collective/progress.png).
3. One card per met grand challenge: a clip (H.264, <= 3 MB, 8-20 s, labelled panels, matched control
   side by side where the control is the point), title, target code, the claim and agent, when met,
   audit status, a 1-2 sentence "watch for" caption and a settings line.
4. A short list of the open challenges.
Nothing else (the old sprint gallery, ladder and long narrative were removed; they live in version 24).

When a challenge is newly met: run one job of the challenge-clips workflow script
(/root/.claude/projects/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/workflows/scripts/challenge-clips-wf_3914ed30-9b6.js,
make + verify stages), add the card, refresh score and plot, fact-check the new text, publish.
When an audit changes a challenge's status, update that card's audit line.

## How to rebuild (since version 25, 27 Oct 15:10Z)
- Generator: scratchpad/dashboard/build_dashboard.py (reads STATE.md, progress.json, challenges.json, the librarian
  clone's git history, dashboard/cards.json and dashboard/template.html; copies clips to artifact/media/challenges/<id>.*).
- Per challenge in cards.json: clip, poster, width, height, watch_for (<= ~70 words, checker-corrected), settings
  (shown in a collapsible "Run settings and colours"), claim_dir, claim_label, who, optional status_note; open
  challenges take open_note. Update ecology-with-reproduction's status_note when the outside audit lands.
- Then: cd /home/user/physim && git pull; python3 build_dashboard.py; node shot.js (screens desk/dark/phone);
  look at the screenshots; publish alife_lab.html with files {media/challenges/<id>.mp4/.jpg} for new clips only.
