"""Level-1 renderers (labenv python: matplotlib). Designer-only views of h1, never shown to the agent."""
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "level0"))
from render import to_rgb   # noqa: E402

FEAT = ["present", "mass", "frac_c1", "x_cos", "x_sin", "y_cos", "y_sin", "rg", "q1", "q2", "vx", "vy"]
NF = len(FEAT)
CMAP = plt.get_cmap("tab20")


def decode_slots(y, K, H=128, W=128):
    """y (K*NF,) -> list of dicts for present slots."""
    S = y.reshape(K, NF)
    out = []
    for s in range(K):
        if S[s, 0] < 0.5:
            continue
        cx = np.arctan2(S[s, 4], S[s, 3]) * W / (2 * np.pi) % W
        cy = np.arctan2(S[s, 6], S[s, 5]) * H / (2 * np.pi) % H
        out.append({"slot": s, "mass": S[s, 1], "f1": S[s, 2], "cx": cx, "cy": cy, "rg": S[s, 7],
                    "theta": 0.5 * np.arctan2(S[s, 9], S[s, 8]), "e": float(np.hypot(S[s, 8], S[s, 9])),
                    "vx": S[s, 10], "vy": S[s, 11]})
    return out


def slot_color(s):
    return CMAP((2 * s) % 20 if s < 10 else (2 * (s - 10) + 1) % 20)


def coarse_rgb(yc, C=2, G=8, H=128, gain=1.6):
    mean = yc[:C * G * G].reshape(C, G, G)
    f = H // G
    up = np.repeat(np.repeat(mean, f, 1), f, 2)
    img = to_rgb(up * gain)
    # faint block grid
    img[::f, :, :] *= 0.55
    img[:, ::f, :] *= 0.55
    return img


def draw_objects(ax, objs, trails=None, H=128, W=128, scale=0.55, lw=1.4, alpha=1.0, color=None,
                 label=True, fill=True):
    """Glyph per slot: disc sized by mass (radius = scale*sqrt(mass)), orientation tick along the
    nematic axis (length grows with elongation), velocity arrow, short trail."""
    for o in objs:
        c = slot_color(o["slot"]) if color is None else color
        r = scale * np.sqrt(max(o["mass"], 0.0))
        for oy in (-H, 0, H):
            for ox in (-W, 0, W):
                x, y = o["cx"] + ox, o["cy"] + oy
                if x < -r - 2 or x > W + r + 2 or y < -r - 2 or y > H + r + 2:
                    continue
                ax.add_patch(Circle((x, y), r, facecolor=c if fill else "none", edgecolor=c,
                                    alpha=(0.35 if fill else 0.9) * alpha, lw=lw))
                ax.add_patch(Circle((x, y), r, facecolor="none", edgecolor=c, alpha=alpha, lw=lw))
                L = r * (0.35 + 1.3 * o["e"])
                dx, dy = L * np.cos(o["theta"]), L * np.sin(o["theta"])
                ax.plot([x - dx, x + dx], [y - dy, y + dy], color="white", lw=lw, alpha=0.9 * alpha)
                ax.annotate("", xy=(x + 4 * o["vx"], y + 4 * o["vy"]), xytext=(x, y),
                            arrowprops=dict(arrowstyle="->", color=c, lw=lw, alpha=alpha))
                if label and ox == 0 and oy == 0:
                    ax.text(x + r * 0.75, y - r * 0.75, str(o["slot"]), color=c, fontsize=7, alpha=alpha,
                            ha="left", va="bottom", family="monospace")
    if trails:
        for s, P in trails.items():
            if len(P) < 2:
                continue
            c = slot_color(s) if color is None else color
            P = np.array(P)
            seg = [0] + [i for i in range(1, len(P)) if abs(P[i, 0] - P[i - 1, 0]) > W / 2
                         or abs(P[i, 1] - P[i - 1, 1]) > H / 2] + [len(P)]
            for a, b in zip(seg[:-1], seg[1:]):
                if b - a >= 2:
                    ax.plot(P[a:b, 0], P[a:b, 1], color=c, lw=1.0, alpha=0.6 * alpha)


def setup_ax(ax, H=128, W=128, bg="black"):
    ax.set_xlim(-0.5, W - 0.5)
    ax.set_ylim(H - 0.5, -0.5)
    ax.set_facecolor(bg)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("0.3")
