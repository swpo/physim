"""Collect w_measure.json (measure_w.py), claim_def.json (claim_def.py) and the claim script's printed
lines (claim_cargo_contrast.txt) for every arm into w_table.txt."""
import json, os, re

OUT = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/fch-gated-micelles"
ARMS = [("unchanged", 51, "rerun/seed51"), ("unchanged", 52, "rerun/seed52"),
        ("walloff (chi_q=0)", 51, "controls/walloff_seed51"), ("walloff (chi_q=0)", 52, "controls/walloff_seed52"),
        ("homgate (gate by domain-mean q)", 51, "controls/homgate_seed51"),
        ("smoothgate (gate by q blurred sigma 4px)", 51, "controls/smoothgate_seed51"),
        ("betaoff (beta=0)", 51, "controls/betaoff_seed51")]
L = ["W audit, fch-gated-micelles#c1. 100 frames x 200 steps, 128x128, dt 0.02 (claim settings). Body-frames = labkit components",
     ">= 12 px at frames 5..100. in/out = mean c in the body interior beyond ~2 px of the contour / mean c in the 2.5-5.5 px band",
     "outside the contour assigned to this body (measure_w.py). claim-def = the claim's own cargo_contrast.py definition (whole body",
     "u+1.6>0.8 vs beyond a 3-px dilation) applied to all frames >= 5; claim-script = its own printout (11 frames).",
     "daughters = surviving children of labkit persistent splits, measured 5 frames after the split.", ""]
hdr = f"{'arm':42s} {'seed':>4s} {'n_bf':>5s} {'med in/out':>10s} {'share>=2':>8s} {'t>=120 med/share':>17s} {'daughters>=2 @+5':>17s} {'dau med':>7s} {'q in/out':>11s} {'claim-def med/share':>20s} {'claim-script contrast f10..f100':>32s}"
L += [hdr, "-" * len(hdr)]
for arm, seed, rel in ARMS:
    p = os.path.join(OUT, rel)
    if not os.path.exists(p + "/w_measure.json"):
        L.append(f"{arm:42s} {seed:>4d}  (not run)")
        continue
    w = json.load(open(p + "/w_measure.json"))
    cd = json.load(open(p + "/claim_def.json"))
    cs = open(p + "/claim_cargo_contrast.txt").read()
    con = [float(x) for x in re.findall(r"contrast ([0-9.]+),", cs)]
    sh = [float(x) for x in re.findall(r">=2x ([0-9.]+),", cs)]
    con, sh = con[1:-1], sh[1:-1]  # drop frame 0 (nan) and the repeated last line
    L.append(f"{arm:42s} {seed:>4d} {w['n_body_frames']:>5d} {w['median_in_out']:>10.2f} {w['share_ge2']:>8.3f} "
             f"{w['late_median']:>8.2f}/{w['late_share_ge2']:.3f} {w['daughters_ge2']:>8d}/{w['daughters_n']:<3d} ({w['daughters_ge2'] / max(w['daughters_n'], 1):.2f}) "
             f"{(w['daughters_median'] or 0):>6.2f} {w['median_q_in']:>5.3f}/{w['median_q_out']:.3f} "
             f"{cd['claim_def_median']:>11.2f}/{cd['claim_def_share_ge2']:.3f}  "
             f"{min(con):.1f}-{max(con):.1f}x, bodies>=2x {min(sh):.2f}-{max(sh):.2f}")
L.append("")
L.append("bodies identical to the unchanged run (u channel, every frame; labkit lineage summary): see bodies_identical.txt")
open(os.path.join(OUT, "w_table.txt"), "w").write("\n".join(L) + "\n")
print("\n".join(L))
