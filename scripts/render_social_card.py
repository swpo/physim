"""Render the site's link-preview card: the PhySim name beside an abstract measured path.

One bright path carries a few measurements, then fans out into many predicted futures,
with soft out-of-focus bundles behind. Every curve is synthetic and seeded: the card shows
no PhySim world, apparatus or result. Run from the repository root:

    uv run --with matplotlib python scripts/render_social_card.py

The 1200 x 630 PNG is written to docs/assets/social-card.png, which the Open Graph and
Twitter tags in docs_source/template.html name as the preview image.
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties, findfont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W, H = 1200, 630
GROUND = np.array([0x1D, 0x20, 0x1C]) / 255  # the landing film's dark ground
CREAM, BLUE, ORANGE, YELLOW = "#f2efd9", "#3c7bd4", "#ec7a36", "#e6d75c"
TITLE, LINES = "PhySim", ("A virtual science environment", "for agents")


def font(weight, size):
    return ImageFont.truetype(findfont(FontProperties(family="Liberation Sans", weight=weight)), size)


def smoothstep(a, b, v):
    t = np.clip((v - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def render(output, seed=11):
    rng = np.random.default_rng(seed)
    x = np.linspace(-0.05, 1.05, 900)

    def path(offset=0.0, lift=0.0):
        """A meandering path rising from the lower left to the upper right, in figure fractions."""
        return 0.14 + lift + 0.6 * np.clip(x, 0, None) ** 1.25 + 0.045 * np.sin(2 * np.pi * (1.4 * x + offset))

    def fan(base, n, spread, start, phase):
        """Smooth random futures that agree before `start` and fan out after it."""
        grow = 0.012 + spread * smoothstep(start, 1.05, x)
        curves = []
        for _ in range(n):
            a, b, c = rng.normal(0, 0.75, 3)
            wiggle = a * np.sin(2 * np.pi * (0.9 * x + phase)) + b * np.sin(2 * np.pi * (1.7 * x + 2 * phase)) + c
            curves.append(base + grow * wiggle / 1.6)
        return curves

    def layer(draw):
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
        fig.patch.set_alpha(0)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        draw(ax)
        fig.canvas.draw()
        image = Image.fromarray(np.asarray(fig.canvas.buffer_rgba()).copy())
        plt.close(fig)
        return image

    def far(ax):
        """Out-of-focus bundles and motes behind everything."""
        for lift, color, phase in ((0.22, BLUE, 0.35), (-0.12, ORANGE, 0.8), (0.4, BLUE, 0.1)):
            for curve in fan(path(phase, lift), 26, 0.18, 0.2, phase):
                ax.plot(x, curve, color=color, lw=2.2, alpha=0.10, solid_capstyle="round")
        motes = rng.uniform(0, 1, (70, 2))
        ax.scatter(motes[:, 0] * 0.7 + 0.3, motes[:, 1], s=rng.uniform(4, 60, 70), color=CREAM, alpha=0.08, lw=0)

    reality = path(0.0) + 0.03 * np.sin(2 * np.pi * (2.6 * x + 0.15)) * (1 - 0.35 * np.clip(x, 0, 1))
    sample = np.linspace(0.14, 0.64, 12) + rng.normal(0, 0.008, 12)
    measured = np.interp(sample, x, reality) + rng.normal(0, 0.012, sample.size)

    def near(ax):
        for curve in fan(reality, 90, 0.26, 0.5, 0.2):
            ax.plot(x, curve, color=BLUE, lw=1.3, alpha=0.16, solid_capstyle="round")
        ax.plot(x, reality, color=CREAM, lw=3.2, solid_capstyle="round")
        colors = [YELLOW if k % 3 == 0 else ORANGE for k in range(sample.size)]
        ax.scatter(sample, measured, s=420, color=colors, alpha=0.10, zorder=4, lw=0)  # halos
        ax.scatter(sample, measured, s=150, color=colors, alpha=0.22, zorder=4, lw=0)
        ax.scatter(sample, measured, s=62, color=colors, zorder=5, lw=0)

    yy, xx = np.mgrid[0:H, 0:W]
    light = np.exp(-(((xx - 0.78 * W) / (0.55 * W)) ** 2 + ((yy - 0.38 * H) / (0.75 * H)) ** 2))
    tone = np.clip(GROUND[None, None] + 0.035 * light[..., None] * np.array([1.0, 1.05, 1.0]), 0, 1)
    canvas = Image.fromarray((tone * 255).astype(np.uint8)).convert("RGBA")
    canvas = Image.alpha_composite(canvas, layer(far).filter(ImageFilter.GaussianBlur(7)))
    front = layer(near)
    for radius in (14, 5):  # soft light around the bright strokes
        canvas = Image.alpha_composite(canvas, front.filter(ImageFilter.GaussianBlur(radius)))
    canvas = Image.alpha_composite(canvas, front)

    # A soft shade behind the text block keeps the name legible over the far bundles.
    shade = np.exp(-(((xx - 0.22 * W) / (0.30 * W)) ** 2 + ((yy - 0.36 * H) / (0.26 * H)) ** 2))
    veil = np.zeros((H, W, 4), np.uint8)
    veil[..., :3] = (GROUND * 255).astype(np.uint8)
    veil[..., 3] = (150 * shade).astype(np.uint8)
    canvas = Image.alpha_composite(canvas, Image.fromarray(veil))
    draw = ImageDraw.Draw(canvas)
    draw.text((76, 292), TITLE, font=font("bold", 118), fill=(242, 239, 217, 255), anchor="ls")
    for k, line in enumerate(LINES):
        draw.text((82, 352 + 40 * k), line, font=font("normal", 32), fill=(242, 239, 217, 215), anchor="ls")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, optimize=True)
    print("wrote", output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--output", type=Path, default=ROOT / "docs/assets/social-card.png")
    render(parser.parse_args().output)
