"""(c29) Table of the 128^2 kernel-drive screen (seed 0, t=10000, labkit). All runs: drive=kernel, N=128, plus the overrides listed."""
import re, os
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screen")
RUNS = {"base": "mu .75", "chi3": "mu .75 chi 3", "chi4": "mu .75 chi 4", "DL24": "mu .75 DL .24", "chi3DL24": "mu .75 chi 3 DL .24",
        "chi3kd08": "mu .75 chi 3 kd .08", "chi4kd08": "mu .75 chi 4 kd .08", "chi4kd12": "mu .75 chi 4 kd .12",
        "chi4kd08dL01": "mu .75 chi 4 kd .08 dL .01", "chi5kd08": "mu .75 chi 5 kd .08", "chi5kd12": "mu .75 chi 5 kd .12",
        "chi5mu10": "mu 1 chi 5 kd .08", "chi5mu10kd12": "mu 1 chi 5 kd .12", "chi5mu125": "mu 1.25 chi 5 kd .08",
        "chi6mu10": "mu 1 chi 6 kd .08", "chi7mu10": "mu 1 chi 7 kd .08"}
print("| run | params | L rim/core | membrane-like | bodies final | persistent splits | max gen | merges | tracks >= 1 BL | max BL |")
print("|---|---|---|---|---|---|---|---|---|---|")
for r, p in RUNS.items():
    f = open(os.path.join(H, r, "FACTS.md")).read()
    L = re.search(r"radial L link.*?rim/core ([0-9.]+).*?(\d+/\d+) membrane-like", f)
    g = lambda pat: (re.search(pat, f) or [None, "-"])[1]
    print(f"| {r} | {p} | {L[1] if L else '-'} | {L[2] if L else '-'} | {g(r'components: final (\d+)')} | {g(r'persistent splits (\d+)')} | "
          f"{g(r'max generation (\d+)')} | {g(r'merges (\d+)')} | {g(r'(\d+) long-lived tracks moved')} | {g(r'max body lengths ([0-9.]+)')} |")
