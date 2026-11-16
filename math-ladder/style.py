"""Style for the math-ladder series; reuses the layout helpers of ../cognition-evolution/common.py."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "cognition-evolution"))

import common  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import to_rgb  # noqa: E402
from common import (BG, GRID, INK, MUTED, PALETTE, arrow, box, cells, clean, clean3d, note, panel,  # noqa: E402,F401
                    plotstyle, rk4, split)

OUT = os.path.join(HERE, "output")
os.makedirs(OUT, exist_ok=True)

STRAND = {
    "nt": ("Number theory", "#2a5d9f"),
    "alg": ("Algebra", "#6a4c93"),
    "geo": ("Geometry", "#3d8b5a"),
    "comb": ("Combinatorics", "#c4512c"),
    "ana": ("Analysis", "#b8860b"),
    "prob": ("Probability", "#2b8a9e"),
    "meta": ("Thinking skills", "#a23b72"),
}
OLY = "#d4a017"


def lighten(c, f=0.86):
    r, g, b = to_rgb(c)
    return (r + (1 - r) * f, g + (1 - g) * f, b + (1 - b) * f)


C = {k: v[1] for k, v in STRAND.items()}
L = {k: lighten(v[1]) for k, v in STRAND.items()}
common.DOMAIN.update(C)
common.SOFT.update(L)


def figure(title, subtitle, w=18, h=12.5, keys=("nt", "alg", "geo", "comb", "ana", "prob"), flow=True,
           flow_labels=("primary school", "research frontier")):
    fig = common.figure(title, subtitle, w=w, h=h, legend=False, flow=False)
    x, yl = 0.975, 1 - 0.45 / h
    for k in reversed(keys or ()):
        label = STRAND[k][0]
        fig.text(x, yl, label, fontsize=10.5, ha="right", va="center", color=INK)
        x -= len(label) * 10.5 * 0.52 / 72 / w + 0.004
        fig.text(x, yl, "●", fontsize=13, ha="right", va="center", color=C[k])
        x -= 0.02
    if flow:
        from matplotlib.patches import FancyArrowPatch
        y = 1 - 1.28 / h
        fig.patches.append(FancyArrowPatch((0.13, y), (0.87, y), transform=fig.transFigure,
                                           arrowstyle="-|>,head_length=8,head_width=4.5", color="#b5b0a6", lw=1.4,
                                           mutation_scale=1))
        fig.text(0.125, y, flow_labels[0], ha="right", va="center", fontsize=10, color=MUTED)
        fig.text(0.875, y, flow_labels[1], ha="left", va="center", fontsize=10, color=MUTED)
    return fig


def footer(fig, text="Drawings are schematic; every plotted curve, table and number is computed by the script."):
    fig.text(0.978, 0.008, text, fontsize=9, color=MUTED, ha="right", va="bottom", style="italic")


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig)
    print("saved", path)
    return path
