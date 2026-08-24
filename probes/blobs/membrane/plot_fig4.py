import os, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BASE = os.path.dirname(os.path.abspath(__file__))
d = np.load(f"{BASE}/data/R3_film_film.npz")
t, u1, u2 = d["t"], d["u1"].astype(float), d["u2"].astype(float)
u0 = -0.7035399190279488
print("film frames:", len(t), "t range", t[0], t[-1])
# static frames strip: 8 frames across the run
idx = np.linspace(0, len(t) - 1, 8).astype(int)
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
for ax, i in zip(axes.ravel(), idx):
    m = ax.imshow(u2[i] - u0, origin="lower", extent=[0, 96, 0, 96], cmap="Blues",
                  vmin=0, vmax=1.9, alpha=1.0)
    cargo = np.ma.masked_where(u1[i] - u0 < 0.3, u1[i] - u0)
    ax.imshow(cargo, origin="lower", extent=[0, 96, 0, 96], cmap="Reds",
              vmin=0, vmax=1.9, alpha=0.9)
    ax.set_title(f"t={t[i]:.0f} tu", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("R3 MONEY SHOT: cargo (red) confined inside a closed 10-blob membrane (blue) — "
             "etaw12=0.9, working noise, cargo tau=5.8 bounces around the cell", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(f"{BASE}/strips/fig4_R3_cargo_in_cell_frames.png", dpi=110)

# animated gif
try:
    from matplotlib import animation
    fig2, ax2 = plt.subplots(figsize=(5.6, 5.6))
    ax2.set_xticks([]); ax2.set_yticks([])
    im_m = ax2.imshow(u2[0] - u0, origin="lower", extent=[0, 96, 0, 96], cmap="Blues", vmin=0, vmax=1.9)
    cargo0 = np.ma.masked_where(u1[0] - u0 < 0.3, u1[0] - u0)
    im_c = ax2.imshow(cargo0, origin="lower", extent=[0, 96, 0, 96], cmap="Reds", vmin=0, vmax=1.9, alpha=0.9)
    tt = ax2.set_title("t=0")
    step = 2
    def upd(k):
        i = k * step
        im_m.set_data(u2[i] - u0)
        im_c.set_data(np.ma.masked_where(u1[i] - u0 < 0.3, u1[i] - u0))
        tt.set_text(f"cargo-in-cell   t={t[i]:.0f} tu")
        return im_m, im_c, tt
    ani = animation.FuncAnimation(fig2, upd, frames=len(t) // step, interval=50, blit=False)
    ani.save(f"{BASE}/strips/film_R3_cargo_in_cell.gif", writer="pillow", fps=20, dpi=80)
    print("gif saved")
except Exception as e:
    print("gif failed:", e)
print("fig4 saved")
