import json, re
OUT = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-marangoni"
rows = [json.loads(l) for l in open(OUT + "/w_results.jsonl")]
log = open(OUT + "/measure_log.txt").read()
arms = [("unchanged", 51, "rerun/seed51", "-"), ("unchanged", 52, "rerun/seed52", "-"),
        ("walloff_shadow", 51, "controls/walloff_seed51", "cmp_walloff51.txt"), ("walloff_shadow", 52, "controls/walloff_seed52", "cmp_walloff52.txt"),
        ("chis0", 51, "controls/chis0_seed51", "cmp_chis0_51.txt"), ("kappa0", 51, "controls/kappa0_seed51", "cmp_kappa0_51.txt"),
        ("res15_unchanged", 51, "controls/res15_seed51", "-")]
def ident(f):
    if f == "-": return "reference"
    try: t = open(OUT + "/" + f).read()
    except FileNotFoundError: return "?"
    m = re.search(r"matter frames .* max \|diff\| (\S+) identical (\w+)", t)
    return ("yes (phi, |Q|, s bitwise equal, 201 frames)" if m.group(2) == "True" else f"no (max |dphi| {float(m.group(1)):.2f})")
L = []
L.append("W audit table: cargo (ch3) inside/outside per body-frame by signed distance to the phi=0 contour; claim 20261026T0505-c34-nematic-marangoni#c1")
L.append("own A = measure_w.py, inside d<=-1.5 px (>= 2 px in), outside 3<=d<=6 px (beyond the s ring, which sits at -1<d<1.5); own B = measure_w.py, inside d<=-1, outside 2<=d<=4 (claim's bands, periodic labels)")
L.append("claim = the claim's own sd_individuals.py ch3 (every 5th render frame >= 20) and inherit.py (daughters >= 12 frames, exactly start+5 when rendered)")
L.append("daughters = labkit tracks born by split living >= 12 frames, ratio at start+5 (or +6 if +5 not rendered); 'tracks maj' = share of tracks (>= 5 measured frames) with > 50% of their frames >= 2")
L.append("")
hdr = f"{'arm':16} {'seed':>4} | {'A median':>8} {'A >=2':>6} {'A dau>=2':>12} {'A trk maj':>9} | {'B median':>8} {'B >=2':>6} {'B dau>=2':>12} | {'claim med':>9} {'claim >=2':>9} {'claim dau>=2':>14} | bodies identical to unchanged | run dir"
L.append(hdr); L.append("-" * len(hdr))
for arm, seed, rd, cmpf in arms:
    A = [r for r in rows if rd in r["frames"] and r["bands"]["outside"] == [3.0, 6.0]]
    B = [r for r in rows if rd in r["frames"] and r["bands"]["outside"] == [2.0, 4.0]]
    if not A: continue
    A, B = A[-1], B[-1]
    blk = log.split(f"({rd})")[-1].split("#####")[0] if f"({rd})" in log else ""
    m1 = re.search(r"ch3: inside/outside \(d<=-1 vs 2<=d<=4\) median (\S+), fraction >= 2: (\S+)", blk)
    m2 = re.search(r"5 frames after birth: n=(\d+), median in/out (\S+), fraction >= 2: (\S+)", blk)
    da = A["daughters_ge12"]; db = B["daughters_ge12"]
    L.append(f"{arm:16} {seed:>4} | {A['median_in_out']:>8.2f} {A['share_ge2']:>6.3f} {da['ge2']:>3}/{da['n']:<3}={da['share']:<4.2f} {A['tracks_life']['share_tracks_majority_ge2']:>9.2f} | "
             f"{B['median_in_out']:>8.2f} {B['share_ge2']:>6.3f} {db['ge2']:>3}/{db['n']:<3}={db['share']:<4.2f} | "
             f"{(m1.group(1) if m1 else 'n/a'):>9} {(m1.group(2) if m1 else 'n/a'):>9} {(m2.group(3) + ' (n=' + m2.group(1) + ')') if m2 else 'n/a':>14} | {ident(cmpf)} | {rd}")
open(OUT + "/w_table.txt", "w").write("\n".join(L) + "\n")
print("\n".join(L))
