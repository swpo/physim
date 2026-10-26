"""Collect w_mine.json (measure_w.py) and the claim's sd_individuals.py / inherit.py outputs per arm into w_table.txt."""
import json, re, os
OUT = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-cargo"
arms = [("unchanged", 51, "rerun/seed51"), ("unchanged", 52, "rerun/seed52"),
        ("wall-off chis=0", 51, "controls/walloff_seed51"), ("wall-off chis=0", 52, "controls/walloff_seed52"),
        ("coupling-off kappa=0", 51, "controls/kappa0_seed51"), ("unchanged 1.5x grid (dx 2/3)", 51, "controls/res15_seed51")]
L = []
L.append("W audit, nematic-cargo (20261026T0405-c34-nematic-cargo#c1). Own script: measure_w.py (sub-pixel signed distance to phi=0;")
L.append("inside sd<=-1, outside 2<=sd<=5, own pixels; every rendered frame >= 20; bodies >= 20 px). Claim's script: sd_individuals.py")
L.append("(inside d<=-1 vs 2<=d<=4, every 5th rendered frame) and inherit.py (daughters >= 12 frames, 5 frames after birth).")
L.append("")
hdr = f"{'arm':30s} {'seed':>4s} | {'mine: n':>7s} {'med in/out':>10s} {'>=2x':>6s} {'trk>50%':>7s} {'dau n':>5s} {'dau med':>7s} {'dau>=2x':>7s} | {'claim: med':>10s} {'>=2x':>5s} {'dau n':>5s} {'dau med':>7s} {'dau>=2x':>7s} | {'ring both>=1.5':>14s} {'cargo on body':>13s}"
L.append(hdr); L.append("-" * len(hdr))
for name, seed, d in arms:
    p = os.path.join(OUT, d)
    if not os.path.exists(os.path.join(p, "w_mine.json")):
        L.append(f"{name:30s} {seed:>4d} | (not run)"); continue
    m = json.load(open(os.path.join(p, "w_mine.json")))
    sd = open(os.path.join(p, "claim_sd.txt")).read() if os.path.exists(os.path.join(p, "claim_sd.txt")) else ""
    ih = open(os.path.join(p, "claim_inherit.txt")).read() if os.path.exists(os.path.join(p, "claim_inherit.txt")) else ""
    c = re.search(r"ch3: inside/outside .*? median ([\d.]+), fraction >= 2: ([\d.]+)", sd)
    r = re.search(r"ch2: body-frames \d+, both >= 1.5: ([\d.]+)", sd)
    di = re.search(r"5 frames after birth: n=(\d+), median in/out ([\d.na]+), fraction >= 2: ([\d.na]+)", ih)
    L.append(f"{name:30s} {seed:>4d} | {m['n_bodyframes']:>7d} {m['median_in_out']:>10.2f} {m['share_ge2']:>6.2f} {m['tracks_majority_ge2']:>7.2f} "
             f"{m['n_daughters']:>5d} {m['daughters_median']:>7.2f} {m['daughters_share_ge2']:>7.2f} | "
             f"{(c.group(1) if c else '-'):>10s} {(c.group(2) if c else '-'):>5s} {(di.group(1) if di else '-'):>5s} {(di.group(2) if di else '-'):>7s} {(di.group(3) if di else '-'):>7s} | "
             f"{(r.group(1) if r else '-'):>14s} {m['cargo_on_body_frac_2nd_half']:>13.3f}")
L.append("")
L.append("columns: 'mine: n' body-frames; 'trk>50%' share of tracks (>= 10 measured frames) holding >= 2x for more than half")
L.append("of their measured life; 'dau' = daughters born by a labkit split, in/out at the rendered frame nearest birth+5;")
L.append("'ring both>=1.5' = claim script, s rim/core and rim/out both >= 1.5; 'cargo on body' = share of all cargo on phi>0, 2nd half.")
L.append("")
L.append("sensitivity (mine): median in/out with inside sd<=-1.5 | with outside 3<=sd<=6; share < 1x")
for name, seed, d in arms:
    p = os.path.join(OUT, d, "w_mine.json")
    if os.path.exists(p):
        m = json.load(open(p))
        L.append(f"  {name:30s} {seed:>4d}: core1.5 {m['median_in_out_core15']:.2f} (>=2x {m['share_ge2_core15']:.2f}) | out3-6 {m['median_in_out_out36']:.2f} (>=2x {m['share_ge2_out36']:.2f}) | <1x {m['share_lt1']:.2f}")
fb = os.path.join(OUT, "far_band.txt")
if os.path.exists(fb):
    L.append(""); L.append("sensitivity (mine): outside band 6-10 px (far bath, past the cargo-depleted moat); daughters on the same band:")
    L += ["  " + x for x in open(fb).read().splitlines()]
L.append("")
L.append("compute: 5 runs at 128^2 x 200 frames x 100 spf (~8 min each) + 1 run at 192^2 (dx 2/3) x 120 frames (10.4 min) = ~50 min; claim settings, nothing shortened")
L.append("(the 1.5x run uses T=600 as the claim's res15/ does). Variants: variants/active-nematic-cargo-walloff.py (P['chis']=0), variants/active-nematic-cargo-kappa0.py (P['kappa']=0).")
extra = os.path.join(OUT, "bodies_identical.txt")
if os.path.exists(extra):
    L.append(""); L.append("bodies identical across arms (compare_bodies.py):"); L += ["  " + x for x in open(extra).read().splitlines()]
open(os.path.join(OUT, "w_table.txt"), "w").write("\n".join(L) + "\n")
print("\n".join(L))
