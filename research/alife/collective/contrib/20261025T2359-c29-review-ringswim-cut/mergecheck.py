"""(c29) For each cut arm: step at which closure first reaches the twin's median closure over 0-400, first area jump (>25% in 20 steps, i.e. a merge), and whether area regained pre-cut before that jump."""
import sys, json, numpy as np
for f in sys.argv[1:]:
    for c in json.load(open(f))["cells"]:
        if c["mode"] != "front": continue
        tw = c["tracks"]["twin"]; cu = c["tracks"]["cut"]
        tw_med = np.median([r[6] for r in tw if r[0] <= 400 and r[6] is not None])
        rec = next((r[0] for r in cu if r[6] is not None and r[6] >= tw_med), None)
        A0 = c["twin"]["area_start"]
        jump = next((cu[i][0] for i in range(1, len(cu)) if cu[i-1][1] and cu[i][1] > 1.25 * cu[i-1][1]), None)
        back = next((r[0] for r in cu[1:] if r[1] >= A0), None)
        print(f.split("/")[0], c["cell"], "keepS" if c["damage"].get("keep_S") else "bathS", f"twin closure med {tw_med:.2f}", "cut reaches it at", rec,
              "| first merge jump", jump, "| area>=precut at", back, "| grown before merge:", back is not None and (jump is None or back < jump), "| lost", c["cut"]["lost_at"], "twin lost", c["twin"]["lost_at"])
