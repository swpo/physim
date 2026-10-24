import sys; from screen import *
g = load(sys.argv[1] if len(sys.argv)>1 else "m4")
sn, ts, w = run(g, N=128, T=300, seed=0)
na=len(g["acts"])
print("wall", w, [blobs(s[0], g["acts"][0]["u0"]) for s in sn], front_width(sn[-1][0], g["acts"][0]["u0"]))
strip(sn, ts, ["u"]+[f"x{c}" for c in range(len(g["chans"]))], f"screens/base_{sys.argv[1]}.png", sys.argv[1])
