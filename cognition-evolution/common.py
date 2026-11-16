"""Shared style and layout helpers for the cognition-evolution figure series."""
import os
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT, exist_ok=True)

MATH = "#2a5d9f"
PHYS = "#c4512c"
BOTH = "#6a4c93"
INK = "#1f1f1f"
MUTED = "#6b6b6b"
GRID = "#d8d4cb"
BG = "#faf8f3"
PANEL = "#ffffff"
SOFT = {"math": "#e6eef8", "phys": "#f8e9e3", "both": "#eee8f5"}
DOMAIN = {"math": MATH, "phys": PHYS, "both": BOTH}
PALETTE = ["#2a5d9f", "#c4512c", "#3d8b5a", "#b8860b", "#6a4c93", "#2b8a9e", "#a23b72", "#555555"]

plt.rcParams.update({
    "font.family": ["Arial", "Arial Unicode MS", "DejaVu Sans"],
    "mathtext.fontset": "dejavusans",
    "axes.edgecolor": "#9a968e",
    "axes.linewidth": 0.8,
    "axes.labelcolor": INK,
    "axes.labelsize": 9.5,
    "xtick.color": "#555",
    "ytick.color": "#555",
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8.5,
    "legend.frameon": False,
    "text.color": INK,
})


def figure(title, subtitle, w=18, h=12.5, legend=True, flow=True):
    fig = plt.figure(figsize=(w, h), facecolor=BG)
    fig.text(0.025, 1 - 0.32 / h, title, fontsize=25, weight="bold", color=INK, va="top")
    fig.text(0.025, 1 - 0.85 / h, subtitle, fontsize=12.5, color=MUTED, va="top")
    if legend:
        x, yl = 0.975, 1 - 0.45 / h
        for key, label in [("both", "Both"), ("phys", "Physical cognition"), ("math", "Mathematical cognition")]:
            fig.text(x, yl, label, fontsize=10.5, ha="right", va="center", color=INK)
            x -= len(label) * 10.5 * 0.52 / 72 / w + 0.004
            fig.text(x, yl, "●", fontsize=13, ha="right", va="center", color=DOMAIN[key])
            x -= 0.022
    if flow:
        y = 1 - 1.28 / h
        fig.patches.append(FancyArrowPatch((0.11, y), (0.89, y), transform=fig.transFigure,
                                           arrowstyle="-|>,head_length=8,head_width=4.5",
                                           color="#b5b0a6", lw=1.4, mutation_scale=1))
        fig.text(0.105, y, "simple", ha="right", va="center", fontsize=10, color=MUTED)
        fig.text(0.895, y, "complex · abstract", ha="left", va="center", fontsize=10, color=MUTED)
    return fig


def cells(fig, rows, cols, top=None, bottom=0.03, left=0.022, right=0.978, hgap=0.024, vgap=0.035):
    h = fig.get_size_inches()[1]
    if top is None:
        top = 1 - 1.55 / h
    cw = (right - left - (cols - 1) * hgap) / cols
    ch = (top - bottom - (rows - 1) * vgap) / rows
    out = []
    for r in range(rows):
        for c in range(cols):
            out.append((left + c * (cw + hgap), top - (r + 1) * ch - r * vgap, cw, ch))
    for i in range(len(out) - 1):
        if (i + 1) % cols:
            x0, y0, w0, h0 = out[i]
            x1 = out[i + 1][0]
            ym = y0 + h0 * 0.55
            fig.patches.append(FancyArrowPatch((x0 + w0 + 0.002, ym), (x1 - 0.002, ym), transform=fig.transFigure,
                                               arrowstyle="-|>,head_length=6,head_width=3.5",
                                               color="#b5b0a6", lw=1.2, mutation_scale=1))
    return out


def panel(fig, cell, n, title, era="", domain="math", caption="", projection=None, pad=0.008, cap_fs=10, plot=False):
    x, y, w, h = cell
    W, H = fig.get_size_inches()
    col = DOMAIN[domain]
    fig.patches.append(Rectangle((x, y), w, h, transform=fig.transFigure, fc=PANEL, ec=GRID, lw=0.9, zorder=-2))
    fig.patches.append(Rectangle((x, y + h - 0.0045), w, 0.0045, transform=fig.transFigure, fc=col, ec="none",
                                 zorder=-1))
    hy = y + h - 0.27 / H
    fig.text(x + 0.010, hy, str(n), fontsize=10, weight="bold", color="white", va="center", ha="center",
             bbox=dict(boxstyle="circle,pad=0.28", fc=col, ec="none"))
    fig.text(x + 0.022, hy, title, fontsize=12.5, weight="bold", va="center", color=INK)
    if era:
        fig.text(x + w - 0.007, hy, era, fontsize=9.8, va="center", ha="right", color=MUTED, style="italic")
    cap_h = 0.0
    if caption:
        chars = max(20, int((w * W * 72 - 14) / (cap_fs * 0.49)))
        wrapped = "\n".join(textwrap.wrap(caption, chars))
        lines = wrapped.count("\n") + 1
        cap_h = (lines * cap_fs * 1.32 + 6) / 72 / H
        fig.text(x + 0.007, y + 0.05 / H, wrapped, fontsize=cap_fs, va="bottom", ha="left", color="#3c3c3c",
                 linespacing=1.32)
    head = 0.52 / H
    ml, mb, mr, mt = (0.62 / W, 0.48 / H, 0.12 / W, 0.06 / H) if plot else (0, 0, 0, 0)
    ax = fig.add_axes([x + pad + ml, y + cap_h + 0.08 / H + mb, w - 2 * pad - ml - mr,
                       h - head - cap_h - 0.1 / H - mb - mt], projection=projection)
    ax.set_facecolor("none")
    return ax


def split(fig, ax, n, direction="h", gap=0.01, ratios=None, projections=None):
    """Replace ax by n sub-axes laid out horizontally ('h') or vertically ('v')."""
    pos = ax.get_position()
    fig.delaxes(ax)
    ratios = np.array(ratios if ratios is not None else [1] * n, float)
    ratios = ratios / ratios.sum()
    projections = projections or [None] * n
    axes = []
    if direction == "h":
        total = pos.width - gap * (n - 1)
        x = pos.x0
        for r, p in zip(ratios, projections):
            a = fig.add_axes([x, pos.y0, total * r, pos.height], projection=p)
            a.set_facecolor("none")
            axes.append(a)
            x += total * r + gap
    else:
        total = pos.height - gap * (n - 1)
        y = pos.y1
        for r, p in zip(ratios, projections):
            a = fig.add_axes([pos.x0, y - total * r, pos.width, total * r], projection=p)
            a.set_facecolor("none")
            axes.append(a)
            y -= total * r + gap
    return axes


def clean(ax, equal=True, xlim=None, ylim=None):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect("equal", adjustable="box" if (xlim and ylim) else "datalim")


def plotstyle(ax, grid=True):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if grid:
        ax.grid(True, color="#ebe8e1", lw=0.7)
        ax.set_axisbelow(True)


def clean3d(ax, elev=22, azim=-60, box=True):
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off() if not box else None
    ax.xaxis.pane.fill = ax.yaxis.pane.fill = ax.zaxis.pane.fill = False
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_edgecolor("none")
        a.line.set_color((0, 0, 0, 0))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.grid(False)


def box(ax, x, y, text, fc="#ffffff", ec=INK, fs=9.5, color=INK, w=None, h=None, weight="normal",
        ha="center", pad=0.35, lw=1.0, style="round", zorder=3, ls="-", **kw):
    bb = dict(boxstyle=f"{style},pad={pad}", fc=fc, ec=ec, lw=lw, linestyle=ls)
    return ax.text(x, y, text, ha=ha, va="center", fontsize=fs, color=color, weight=weight, bbox=bb,
                   zorder=zorder, **kw)


def arrow(ax, p, q, color="#777", lw=1.2, style="-|>", rad=0.0, hl=7, hw=3.5, ls="-", zorder=2, shrink=0, **kw):
    a = FancyArrowPatch(p, q, arrowstyle=f"{style},head_length={hl},head_width={hw}" if style != "-" else "-",
                        connectionstyle=f"arc3,rad={rad}", color=color, lw=lw, linestyle=ls,
                        mutation_scale=1, zorder=zorder, shrinkA=shrink, shrinkB=shrink, **kw)
    ax.add_patch(a)
    return a


def note(ax, x, y, text, fs=8.8, color=MUTED, ha="center", va="center", **kw):
    return ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va=va, **kw)


def footer(fig, text="Schematic drawings; all plotted curves and numbers are computed from the formulas named in each panel."):
    fig.text(0.978, 0.008, text, fontsize=9, color=MUTED, ha="right", va="bottom", style="italic")


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig)
    print("saved", path)
    return path


def wavelength_rgb(wl):
    """Approximate visible colour for a wavelength in nm (Bruton's algorithm)."""
    if 380 <= wl < 440:
        r, g, b = -(wl - 440) / 60, 0.0, 1.0
    elif 440 <= wl < 490:
        r, g, b = 0.0, (wl - 440) / 50, 1.0
    elif 490 <= wl < 510:
        r, g, b = 0.0, 1.0, -(wl - 510) / 20
    elif 510 <= wl < 580:
        r, g, b = (wl - 510) / 70, 1.0, 0.0
    elif 580 <= wl < 645:
        r, g, b = 1.0, -(wl - 645) / 65, 0.0
    elif 645 <= wl <= 780:
        r, g, b = 1.0, 0.0, 0.0
    else:
        r = g = b = 0.0
    if 380 <= wl < 420:
        f = 0.3 + 0.7 * (wl - 380) / 40
    elif 700 < wl <= 780:
        f = 0.3 + 0.7 * (780 - wl) / 80
    else:
        f = 1.0
    return (r * f, g * f, b * f)


def rk4(f, y0, t):
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(len(t) - 1):
        h = t[i + 1] - t[i]
        k1 = f(t[i], y[i])
        k2 = f(t[i] + h / 2, y[i] + h / 2 * k1)
        k3 = f(t[i] + h / 2, y[i] + h / 2 * k2)
        k4 = f(t[i] + h, y[i] + h * k3)
        y[i + 1] = y[i] + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y
