"""(c45) Per-setting summary of extract.py tables for Q:marangoni-swim-screen.
D = net displacement over the track's median rod length 4 sqrt(lambda_max) (extract.py disp_rl);
D_A = net over sqrt(mean area) (PROTOCOL's floor unit). Dividing = split-born, >= 2 daughters living >= 20 frames.
usage: stats.py out.txt name:table.json:metrics.json [...]"""
import sys, json, numpy as np
out = open(sys.argv[1], "w")
def P(s): print(s); out.write(s + "\n")
P("setting        ndiv psplit  medD  p90D  sh>=2.5 sh>=3 | medD_A sh>=3_A | v_path straight cycle  Lbirth  growL  v/growL  ring_contrast")
for arg in sys.argv[2:]:
    name, tab, met = arg.split(":")
    rows = json.load(open(tab))["rows"]; m = json.load(open(met))
    ps = len(m.get("persistent_splits", []))
    dv = [r for r in rows if r["dividing"]]
    if not dv:
        P(f"{name:14s} 0 {ps}"); continue
    D = np.array([r["disp_rl"] for r in dv]); DA = np.array([r["net"] / np.sqrt(r["A_mean"]) for r in dv])
    vp = np.array([r["vpath"] for r in dv]); st = np.array([r["straight"] for r in dv]); cy = np.array([r["cycle"] for r in dv])
    Lb = np.array([r["L_birth"] for r in dv]); gL = np.array([(r["L_end"] - r["L_birth"]) / r["cycle"] for r in dv])
    rc = np.array([r.get("ring_contrast", np.nan) for r in dv])
    ratio = np.median(vp) / max(np.median(gL), 1e-9)
    P(f"{name:14s} {len(dv):4d} {str(ps):>6s} {np.median(D):5.2f} {np.percentile(D, 90):5.2f} {np.mean(D >= 2.5):7.2f} {np.mean(D >= 3):5.2f} | "
      f"{np.median(DA):6.2f} {np.mean(DA >= 3):7.2f} | {np.median(vp):6.3f} {np.median(st):8.2f} {np.median(cy):5.0f} {np.median(Lb):7.1f} {np.median(gL):6.3f} {ratio:8.1f} {np.nanmedian(rc):8.2f}")
