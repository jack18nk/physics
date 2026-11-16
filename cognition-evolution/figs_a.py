"""Figures 01-05: abstraction ladder, cognitive roots, numbers, geometry, calculus."""
from math import erf

import numpy as np
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Polygon, Rectangle, Wedge

from common import (BOTH, GRID, INK, MATH, MUTED, PALETTE, PHYS, SOFT, arrow, box, cells, clean, clean3d,
                    figure, footer, note, panel, plotstyle, save, split)


# ---------------------------------------------------------------------------------------------
# 01 Ladder of abstraction
# ---------------------------------------------------------------------------------------------
def fig01():
    fig = figure("The ladder of abstraction",
                 "Mathematics and physics climb the same rungs: at each level, the results of the level below "
                 "become the new objects of thought", h=13.5, flow=False)
    ax = fig.add_axes([0.015, 0.025, 0.97, 0.87])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 64)
    ax.axis("off")
    levels = [
        ("Perception & action", "prehistory · infancy",
         "See 'three' at a glance; tell 8 dots from 16 without counting.",
         "Expect unsupported things to fall and solid things to block motion.",
         "Innate expectations, shared with many animals."),
        ("Quantity & measurement", "c. 3000 BC",
         "Number words and tallies; adding, measuring fields and grain.",
         "Units of length, weight and time; calendars, water clocks.",
         "Numbers detach from the things they count."),
        ("Relations & proofs", "c. 600 BC – 1600",
         "Euclidean proof: a theorem holds for every right triangle.",
         "Lever law, buoyancy, Kepler's orbits, Snell's law.",
         "Claims about all cases, not just this case."),
        ("Symbols & functions", "1600 – 1850",
         "Algebraic notation, coordinates, calculus, differential equations.",
         "F = ma, universal gravitation, wave and heat equations.",
         "Symbols let reasoning run mechanically."),
        ("Structures & symmetries", "1830 – 1930",
         "Groups, vector spaces, non-Euclidean and Riemannian geometry.",
         "Conservation laws from symmetry; curved spacetime; Hilbert space.",
         "Transformations matter more than objects."),
        ("Structures of structures", "1940 – today",
         "Categories and functors; classification theorems; homotopy theory.",
         "Gauge theories, renormalization group, dualities between theories.",
         "Whole theories become objects to compare."),
    ]
    import textwrap
    shades = ["#f1eee7", "#ebe7de", "#e4dfd4", "#ddd7ca", "#d6cfc0", "#cfc7b6"]
    W = 27.5
    for i, (name, era, m, p, idea) in enumerate(levels):
        x0, y0 = 11 + i * 12.2, 1.2 + i * 10.4
        ax.add_patch(Rectangle((x0 - 1.2, 0), 101 - x0, y0 - 0.3, fc=shades[i], ec="none", zorder=0))
        card = FancyBboxPatch((x0, y0), W, 9.4, boxstyle="round,pad=0,rounding_size=0.8", fc="white",
                              ec="#9d968a", lw=1.1, zorder=2)
        ax.add_patch(card)
        ax.text(x0 + 0.8, y0 + 8.55, f"Level {i}  ·  {name}", fontsize=11.5, weight="bold", va="center", zorder=3)
        ax.text(x0 + W - 0.7, y0 + 8.55, era, fontsize=9, color=MUTED, style="italic", ha="right", va="center",
                zorder=3)
        ax.plot([x0 + 0.6, x0 + W - 0.6], [y0 + 7.75, y0 + 7.75], color=GRID, lw=0.8, zorder=3)
        for k, (lab, txt, col) in enumerate([("Mathematics", m, MATH), ("Physics", p, PHYS)]):
            cx = x0 + 0.8 + k * (W / 2)
            ax.text(cx, y0 + 7.1, lab, fontsize=9.5, weight="bold", color=col, va="center", zorder=3)
            ax.text(cx, y0 + 6.45, "\n".join(textwrap.wrap(txt, 34)), fontsize=9.1, va="top", zorder=3,
                    linespacing=1.25)
        ax.text(x0 + 0.8, y0 + 0.85, "New move: " + idea, fontsize=9.1, color=BOTH, style="italic", va="center",
                zorder=3)
        # icon
        ia = ax.inset_axes([x0 - 10.0, y0 + 0.4, 8.6, 8.6], transform=ax.transData)
        ia.set_xlim(0, 10)
        ia.set_ylim(0, 10)
        ia.axis("off")
        ia.set_facecolor("none")
        _ladder_icon(ia, i)
        if i < 5:
            arrow(ax, (x0 + W * 0.62, y0 + 9.5), (x0 + 12.2 + 3, y0 + 10.4 + 0.1), color="#a39c90", lw=1.4,
                  rad=-0.25)
    ax.annotate("", xy=(1.2, 63), xytext=(1.2, 2), arrowprops=dict(arrowstyle="-|>", color="#8f887c", lw=2))
    ax.text(0.2, 32, "increasing abstraction", rotation=90, va="center", ha="center", fontsize=11, color=MUTED)
    ax.text(99, 3.2, "Each rung keeps everything below it:\nan infant's object sense still runs\ninside a "
                     "string theorist's head.", ha="right", va="bottom", fontsize=10, color=MUTED, style="italic")
    save(fig, "01-ladder-of-abstraction.png")


def _ladder_icon(a, i):
    if i == 0:
        for k, (x, y) in enumerate([(2, 6.5), (4, 7.6), (3.2, 5.0)]):
            a.add_patch(Circle((x, y), 0.9, fc="#c0392b", ec="none"))
            a.plot([x, x + 0.2], [y + 0.9, y + 1.4], color="#5d4037", lw=1.5)
        a.text(3, 2.6, "“three”", ha="center", fontsize=9, color=MATH)
        a.add_patch(Circle((7.8, 8.2), 0.7, fc="#7f8c8d", ec="none"))
        a.annotate("", xy=(7.8, 3.2), xytext=(7.8, 7.2), arrowprops=dict(arrowstyle="-|>", color=PHYS, lw=1.6))
        a.plot([6.3, 9.3], [2.6, 2.6], color="#6d4c41", lw=2)
    elif i == 1:
        a.add_patch(Rectangle((0.8, 4.2), 8.4, 1.6, fc="#f3d58c", ec="#8d6e2f", lw=1))
        for k in range(9):
            hgt = 0.9 if k % 2 == 0 else 0.5
            a.plot([1.2 + k * 0.95, 1.2 + k * 0.95], [5.8, 5.8 - hgt], color="#5b4a1f", lw=1)
            if k % 2 == 0:
                a.text(1.2 + k * 0.95, 4.55, str(k // 2), fontsize=6.5, ha="center")
        a.text(5, 2.4, "||||  ||||  |||", ha="center", fontsize=10, color=MATH, weight="bold")
        a.text(5, 7.8, "1 cubit · 1 mina · 1 day", ha="center", fontsize=7.2, color=PHYS)
    elif i == 2:
        a.add_patch(Polygon([[1, 1.5], [6.5, 1.5], [1, 6.0]], fc="#dbe7f5", ec=MATH, lw=1.4))
        a.text(3.7, 0.7, "a", ha="center", fontsize=9, color=MATH)
        a.text(0.4, 3.7, "b", ha="center", fontsize=9, color=MATH)
        a.text(4.2, 4.2, "c", ha="center", fontsize=9, color=MATH)
        a.text(5.3, 7.4, r"$a^2+b^2=c^2$", fontsize=8.5, ha="center", color=MATH)
        a.plot([5.5, 9.5], [3.4, 4.6], color=PHYS, lw=1.6)
        a.add_patch(Polygon([[7.2, 2.4], [6.8, 3.2], [7.6, 3.2]], fc=PHYS))
        a.add_patch(Rectangle((5.4, 3.4), 0.7, 0.7, fc="#7f8c8d"))
        a.add_patch(Rectangle((9.0, 4.5), 0.6, 0.45, fc="#7f8c8d"))
    elif i == 3:
        x = np.linspace(0.5, 9.5, 100)
        y = 1 + 0.08 * (x - 1) ** 2
        a.plot(x, y, color=MATH, lw=1.6)
        x0 = 6
        y0 = 1 + 0.08 * (x0 - 1) ** 2
        s = 0.16 * (x0 - 1)
        a.plot([x0 - 3, x0 + 3], [y0 - 3 * s, y0 + 3 * s], color=PHYS, lw=1.3)
        a.plot([x0], [y0], "o", color=PHYS, ms=4)
        a.text(2.6, 8.4, r"$F = m\,\ddot{x}$", fontsize=10, color=PHYS)
        a.text(2.6, 6.8, r"$\frac{dy}{dx}$", fontsize=11, color=MATH)
    elif i == 4:
        t = np.linspace(0, 2 * np.pi, 7)
        a.add_patch(Polygon(np.c_[5 + 3.4 * np.cos(t + np.pi / 6), 5 + 3.4 * np.sin(t + np.pi / 6)], fc="#e6eef8",
                            ec=MATH, lw=1.5))
        a.add_patch(Arc((5, 5), 4.0, 4.0, theta1=20, theta2=300, color=PHYS, lw=1.5))
        a.annotate("", xy=(5 + 2 * np.cos(np.radians(300)), 5 + 2 * np.sin(np.radians(300))),
                   xytext=(5 + 2 * np.cos(np.radians(292)), 5 + 2 * np.sin(np.radians(292))),
                   arrowprops=dict(arrowstyle="-|>", color=PHYS, lw=1.5))
        a.text(5, 5, r"$C_6$", ha="center", va="center", fontsize=10, color=MATH)
    else:
        pts = {"A": (2, 8), "B": (8, 8), "C": (2, 2), "D": (8, 2)}
        for k, (x, y) in pts.items():
            a.text(x, y, k, ha="center", va="center", fontsize=10, weight="bold", color=BOTH)
        for p, q, lab, off in [("A", "B", "f", (0, 0.6)), ("A", "C", "h", (-0.7, 0)), ("B", "D", "g", (0.7, 0)),
                               ("C", "D", "k", (0, -0.7))]:
            (x1, y1), (x2, y2) = pts[p], pts[q]
            a.annotate("", xy=(x2 - 0.6 * np.sign(x2 - x1), y2 - 0.7 * np.sign(y2 - y1)),
                       xytext=(x1 + 0.6 * np.sign(x2 - x1), y1 + 0.7 * np.sign(y2 - y1)),
                       arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1))
            a.text((x1 + x2) / 2 + off[0], (y1 + y2) / 2 + off[1], lab, ha="center", va="center", fontsize=9,
                   style="italic")
        a.text(5, 5, "↻", ha="center", va="center", fontsize=14, color=MUTED)


# ---------------------------------------------------------------------------------------------
# 02 Cognitive roots
# ---------------------------------------------------------------------------------------------
def fig02():
    fig = figure("Where it starts: innate number sense and intuitive physics",
                 "Human infants (and many animals) arrive with core systems for quantity, objects and motion. "
                 "Formal mathematics and physics are built on, and sometimes against, them")
    cs = cells(fig, 2, 3, vgap=0.045)

    ax = panel(fig, cs[0], 1, "Subitizing vs. counting", "infants · adults", "both",
               "Up to about 3–4 items are recognised at a glance (subitizing); beyond that each extra item costs "
               "~0.3 s of counting. Shape of curve after Trick & Pylyshyn (1994); values illustrative.", plot=True)
    n = np.arange(1, 9)
    rt = np.where(n <= 3, 500 + 50 * (n - 1), 600 + 300 * (n - 3))
    ax.axvspan(0.5, 3.5, color=SOFT["both"])
    ax.plot(n, rt, "-o", color=BOTH, lw=2, ms=6)
    ax.text(2, 2200, "subitizing\n≈50 ms / item", ha="center", fontsize=9.5, color=BOTH)
    ax.text(6.2, 1000, "counting\n≈300 ms / item", ha="center", fontsize=9.5, color=BOTH)
    for k in n:
        rng = np.random.default_rng(k)
        pts = rng.uniform(-0.28, 0.28, (k, 2))
        ax.scatter(k + pts[:, 0], 2650 + pts[:, 1] * 500, s=6, color=INK)
    ax.set_xlim(0.5, 8.5)
    ax.set_ylim(300, 3000)
    ax.set_xlabel("number of dots shown")
    ax.set_ylabel("response time (ms)")
    plotstyle(ax)

    ax = panel(fig, cs[1], 2, "Approximate number system", "Weber's law", "math",
               "Telling two quantities apart depends on their ratio, not their difference. The acuity "
               "(Weber fraction w) sharpens from infancy to adulthood. P = ½[1 + erf((r−1) / (√2·w·√(1+r²)))]; "
               "w values after Halberda & Feigenson (2008).", plot=True)
    r = np.linspace(1, 3, 300)
    verf = np.vectorize(erf)
    for w, lab, c in [(0.5, "6-month infants (w≈0.5)", "#9ab5d9"), (0.38, "age 3–4 (w≈0.38)", "#6b93c8"),
                      (0.2, "age 6 (w≈0.2)", "#3f6fae"), (0.11, "adults (w≈0.11)", "#1c3f73")]:
        ax.plot(r, 0.5 * (1 + verf((r - 1) / (np.sqrt(2) * w * np.sqrt(1 + r ** 2)))), color=c, lw=2, label=lab)
    ax.axhline(0.75, color=GRID, ls="--", lw=1)
    ax.set_xlabel("ratio of the two quantities (larger / smaller)")
    ax.set_ylabel("probability correct")
    ax.legend(loc="lower right", fontsize=8)
    ia = ax.inset_axes([0.27, 0.03, 0.3, 0.25])
    rng = np.random.default_rng(3)
    for k, (cnt, x0) in enumerate([(8, 0.0), (16, 1.15)]):
        p = rng.uniform(0, 1, (cnt, 2))
        ia.scatter(x0 + p[:, 0], p[:, 1], s=7, color=INK)
        ia.text(x0 + 0.5, -0.32, f"{cnt}", ha="center", fontsize=8)
    clean(ia, equal=False, xlim=(-0.1, 2.25), ylim=(-0.5, 1.1))
    ax.set_ylim(0.45, 1.02)
    plotstyle(ax)

    ax = panel(fig, cs[2], 3, "The mental number line", "age 7 → 12", "math",
               "Asked to place numbers on a 0–1000 line, young children compress large numbers (logarithmic "
               "placement); by about age 12 placement becomes linear. Pattern after Siegler & Opfer (2003); "
               "data points simulated.", plot=True)
    x = np.array([2, 5, 18, 34, 56, 78, 100, 122, 147, 150, 163, 179, 246, 366, 486, 606, 722, 725, 738, 754,
                  818, 938])
    rng = np.random.default_rng(1)
    child = 1000 * np.log(x) / np.log(1000) + rng.normal(0, 45, len(x))
    adult = x + rng.normal(0, 30, len(x))
    xx = np.linspace(1, 1000, 300)
    ax.plot(xx, xx, color=GRID, lw=1, ls="--")
    ax.plot(xx, 1000 * np.log(xx) / np.log(1000), color="#7fa6d6", lw=2, label="second graders: logarithmic")
    ax.scatter(x, child, s=16, color="#7fa6d6")
    ax.plot(xx, xx, color=MATH, lw=2, label="sixth graders: linear")
    ax.scatter(x, adult, s=16, color=MATH, marker="s")
    ax.set_xlabel("number to place")
    ax.set_ylabel("estimated position on 0–1000 line")
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1100)
    ax.legend(loc="lower right")
    plotstyle(ax)

    ax = panel(fig, cs[3], 4, "Infants' core physics", "2.5–12 months", "phys",
               "Violation-of-expectation studies: infants look longer at impossible events. Objects persist "
               "when hidden, cannot pass through solids, and fall without support (Spelke, Baillargeon et al.).")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 9.6))
    rows = [("Object permanence", "≈3.5–5 months"), ("Solidity", "≈2.5–4 months"), ("Support", "≈4.5–12 months")]
    for k, (lab, age) in enumerate(rows):
        y = 6.6 - k * 3.15
        ax.text(0.1, y + 2.35, lab, fontsize=10, weight="bold", color=PHYS)
        ax.text(9.9, y + 2.35, age, fontsize=9, color=MUTED, ha="right")
        for j, (ok, x0) in enumerate([(True, 1.0), (False, 5.6)]):
            ax.add_patch(Rectangle((x0 - 0.3, y), 3.9, 0.12, fc="#8d6e63", ec="none"))
            if k == 0:
                ax.add_patch(Rectangle((x0 + 1.9, y + 0.12), 0.7, 0.7, fc="#e67e22", ec="none", alpha=1 if ok else 0.18,
                                       ls="--"))
                ax.add_patch(Polygon([[x0 + 0.6, y + 0.12], [x0 + 0.75, y + 0.12], [x0 + 2.0, y + 1.5],
                                      [x0 + 1.85, y + 1.6]], fc="#5d6d7e"))
                if not ok:
                    ax.text(x0 + 2.25, y + 0.47, "?", ha="center", va="center", fontsize=11, color="#e67e22")
            elif k == 1:
                ax.add_patch(Rectangle((x0 + 1.8, y + 0.12), 0.25, 1.6, fc="#5d6d7e"))
                bx = x0 + 1.4 if ok else x0 + 2.6
                ax.add_patch(Circle((bx, y + 0.45), 0.33, fc="#e74c3c"))
                ax.annotate("", xy=(x0 + 1.0, y + 1.2), xytext=(x0 + 0.1, y + 1.2),
                            arrowprops=dict(arrowstyle="-|>", color=MUTED))
            else:
                ax.add_patch(Rectangle((x0 - 0.2, y + 0.12), 1.6, 0.9, fc="#95a5a6"))
                bx = x0 + 0.3 if ok else x0 + 1.25
                ax.add_patch(Rectangle((bx, y + 1.02), 0.85, 0.75, fc="#27ae60"))
            ax.text(x0 + 3.45, y + 1.5, "✓" if ok else "✗", fontsize=15, color="#2e7d32" if ok else "#c62828",
                    ha="center", va="center")
        ax.text(2.9, y - 0.35, "possible", fontsize=8.5, color=MUTED, ha="center")
        ax.text(7.5, y - 0.35, "impossible → longer looking", fontsize=8.5, color=MUTED, ha="center")

    ax = panel(fig, cs[4], 5, "Intuitive physics can be wrong", "naive impetus", "phys",
               "Many adults predict that a ball leaving a curved tube keeps curving, or that a dropped object falls "
               "straight down from a moving carrier — medieval 'impetus' thinking (McCloskey 1980–83). Newton: "
               "with no force, motion is straight.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.008)
    clean(a1, xlim=(-1.6, 3.0), ylim=(-1.9, 1.7))
    th = np.linspace(np.pi * 0.0, np.pi * 1.0, 100)
    for rr in (0.92, 1.08):
        a1.plot(rr * np.cos(th + np.pi / 2), rr * np.sin(th + np.pi / 2), color="#5d6d7e", lw=1.6)
    ex, ey = 0, -1
    a1.plot([0, 2.6], [-1, -1], color="#2e7d32", lw=2.2, label="Newton: straight")
    s = np.linspace(0, 1.45, 60)
    a1.plot(1.5 * np.sin(s), -1 + 0.9 * (1 - np.cos(s)), color="#c62828", lw=2, ls="--",
            label="naive: keeps curving")
    a1.add_patch(Circle((0, -1), 0.1, fc=INK))
    a1.text(0, 1.35, "tube seen from above", ha="center", fontsize=8.5, color=MUTED)
    a1.legend(loc="lower center", fontsize=7.8, bbox_to_anchor=(0.5, -0.07))
    clean(a2, xlim=(-0.4, 4.4), ylim=(-0.3, 4.2))
    a2.add_patch(Polygon([[0, 3.5], [1.2, 3.5], [1.0, 3.85], [0.15, 3.85]], fc="#5d6d7e"))
    a2.annotate("", xy=(2.2, 3.7), xytext=(1.35, 3.7), arrowprops=dict(arrowstyle="-|>", color=MUTED))
    t = np.linspace(0, 1, 50)
    a2.plot(0.6 + 3.2 * t, 3.45 - 3.3 * t ** 2, color="#2e7d32", lw=2.2)
    a2.plot([0.6, 0.6], [3.45, 0.15], color="#c62828", lw=2, ls="--")
    a2.plot([-0.3, 4.3], [0.1, 0.1], color="#8d6e63", lw=2)
    a2.text(2.7, 2.6, "real path:\nparabola", fontsize=8.5, color="#2e7d32")
    a2.text(0.75, 1.4, "naive:\nstraight\ndown", fontsize=8.5, color="#c62828")

    ax = panel(fig, cs[5], 6, "From core systems to formal theory", "bootstrapping", "both",
               "Language, symbols and schooling recombine the innate systems into new concepts — Carey's "
               "'Quinian bootstrapping' (2009); core knowledge after Spelke & Kinzler (2007).")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    stages = [("Core systems (innate)", "objects · approximate number · geometry & navigation · agents", "#efe9f6"),
              ("Language", "number words 'one, two, three…'; spatial words; counting routine", "#e7dff2"),
              ("Cultural tools", "tallies, numerals, maps, rulers, clocks, written proofs", "#ddd2ec"),
              ("Schooling & practice", "arithmetic, measurement, experiments, explicit rules", "#d2c4e5"),
              ("Formal theories", "axioms, equations, models that can contradict intuition", "#c6b5de")]
    for k, (t1, t2, c) in enumerate(stages):
        y = 9.0 - k * 1.95
        ax.add_patch(FancyBboxPatch((0.4, y - 0.7), 9.2, 1.4, boxstyle="round,pad=0,rounding_size=0.25", fc=c,
                                    ec=BOTH, lw=1))
        ax.text(0.75, y + 0.22, t1, fontsize=10.2, weight="bold", va="center", color=INK)
        ax.text(0.75, y - 0.3, t2, fontsize=8.8, va="center", color="#333")
        if k < 4:
            arrow(ax, (5, y - 0.72), (5, y - 1.23), color=BOTH, lw=1.4)
    footer(fig, "Curves in panels 1–3 are schematic models of published findings, not raw data.")
    save(fig, "02-cognitive-roots.png")


# ---------------------------------------------------------------------------------------------
# 03 Evolution of number
# ---------------------------------------------------------------------------------------------
def fig03():
    fig = figure("How the concept of number grew",
                 "Each extension was forced by a problem the old numbers could not solve — and each was first "
                 "resisted as 'absurd', 'negative', 'irrational' or 'imaginary'")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Tally marks", "c. 20,000 BC", "math",
               "Ishango bone (Congo): notches in groups of 11, 13, 17 and 19. One mark per thing: one-to-one "
               "correspondence long before abstract number words.")
    clean(ax, xlim=(0, 10), ylim=(0, 5))
    ax.add_patch(FancyBboxPatch((0.4, 1.4), 9.2, 2.2, boxstyle="round,pad=0,rounding_size=1.0", fc="#efe3c8",
                                ec="#a1887f", lw=1.2))
    x = 1.0
    for g in (11, 13, 17, 19):
        for k in range(g):
            ax.plot([x, x], [2.0, 3.0 + 0.05 * (k % 2)], color="#4e342e", lw=1.2)
            x += 0.105
        ax.text(x - g * 0.105 / 2 - 0.05, 0.95, str(g), ha="center", fontsize=10, color=MATH, weight="bold")
        x += 0.35
    ax.text(5, 4.25, "|||| ||||  →  “this many”", ha="center", fontsize=10, color=MUTED)

    ax = panel(fig, cs[1], 2, "Counting numbers ℕ", "c. 3000 BC → Peano 1889", "math",
               "Number becomes a property shared by all collections of the same size. Peano's axioms (1889): start "
               "at 0 and apply 'successor' forever — infinity in one rule.")
    clean(ax, xlim=(0, 10), ylim=(0, 5))
    for k in range(1, 7):
        x0 = 0.3 + (k - 1) * 1.6
        rng = np.random.default_rng(k + 10)
        for j in range(k):
            ax.add_patch(Circle((x0 + 0.35 + 0.42 * (j % 2), 3.4 - 0.42 * (j // 2)), 0.15, fc=MATH))
        ax.text(x0 + 0.55, 1.35, str(k), ha="center", fontsize=14, weight="bold")
        if k < 6:
            arrow(ax, (x0 + 0.85, 1.35), (x0 + 1.45, 1.35), color=MUTED, lw=1, hl=5, hw=2.5)
            ax.text(x0 + 1.15, 1.75, "+1", fontsize=7.5, color=MUTED, ha="center")
    ax.text(9.9, 1.35, "…", fontsize=14, ha="center")
    ax.text(5, 0.35, "S(n) = n + 1", ha="center", fontsize=10, color=MATH)

    ax = panel(fig, cs[2], 3, "Place value and zero", "Babylon c. 1800 BC · India 628", "math",
               "Position gives a digit its value; an empty column needs a symbol. Brahmagupta (628) treated zero "
               "as a number with rules (a − a = 0). The same quantity in three notations:")
    clean(ax, xlim=(0, 10), ylim=(0, 5))
    ax.add_patch(Rectangle((0.5, 0.9), 5.0, 3.6, fc="none", ec="#6d4c41", lw=3))
    for k, (val, lab) in enumerate([(2, "100s"), (0, "10s"), (5, "1s")]):
        x = 1.3 + k * 1.7
        ax.plot([x, x], [0.9, 4.5], color="#8d6e63", lw=1.5)
        for j in range(val):
            ax.add_patch(Rectangle((x - 0.45, 1.05 + j * 0.55), 0.9, 0.45, fc="#c0392b", ec="#7b241c"))
        ax.text(x, 0.45, lab, ha="center", fontsize=8.5, color=MUTED)
        if val == 0:
            ax.text(x, 2.2, "0", ha="center", fontsize=16, color=MATH, weight="bold")
    for k, (t, c) in enumerate([("205", MATH), ("CCV  (Roman)", INK), ("3 ; 25  (base 60)", INK)]):
        ax.text(6.1, 3.8 - k * 1.15, t, fontsize=12 if k == 0 else 10, weight="bold" if k == 0 else "normal",
                color=c, va="center")

    ax = panel(fig, cs[3], 4, "Negative numbers ℤ", "China c. 200 BC · India 628", "math",
               "Debts and directions: the Nine Chapters used red rods for gains and black for debts. Europe called "
               "negatives 'absurd' until the 1600s. Now subtraction always works: 3 + (−5) = −2.")
    ax.set_xlim(-6.6, 6.6)
    ax.set_ylim(-1.8, 2.6)
    clean(ax, equal=False)
    ax.plot([-6.3, 6.3], [0, 0], color=INK, lw=1.2)
    for k in range(-6, 7):
        ax.plot([k, k], [-0.12, 0.12], color=INK, lw=1)
        ax.text(k, -0.55, str(k), ha="center", fontsize=9, color=PHYS if k < 0 else INK)
    arrow(ax, (0, 0.5), (3, 0.5), color="#2e7d32", lw=2.2, rad=-0.35)
    ax.text(1.5, 1.45, "+3", ha="center", color="#2e7d32", fontsize=10)
    arrow(ax, (3, 0.5), (-2, 0.5), color="#c62828", lw=2.2, rad=-0.3)
    ax.text(0.5, 2.25, "−5", ha="center", color="#c62828", fontsize=10)
    ax.add_patch(Circle((-2, 0), 0.16, fc=MATH, zorder=5))
    ax.text(-4.5, -1.35, "debt", ha="center", fontsize=9, color=MUTED)
    ax.text(4.5, -1.35, "credit", ha="center", fontsize=9, color=MUTED)

    ax = panel(fig, cs[4], 5, "Fractions ℚ", "Egypt c. 1650 BC", "math",
               "Sharing and measuring need parts. Every fraction p/q in [0, 1] is drawn here with height 1/q: "
               "between any two fractions lies another, yet gaps remain.", plot=True)
    from math import gcd
    for q in range(1, 25):
        for p in range(0, q + 1):
            if gcd(p, q) == 1:
                ax.plot([p / q, p / q], [0, 1 / q], color=MATH, lw=0.9 if q > 6 else 1.6, alpha=0.9)
    for p, q in [(0, 1), (1, 1), (1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5)]:
        ax.text(p / q, 1 / q + 0.035, f"{p}/{q}" if q > 1 else str(p), ha="center", fontsize=8.5)
    ax.set_ylim(0, 1.12)
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylabel("1 / denominator")
    plotstyle(ax, grid=False)

    ax = panel(fig, cs[5], 6, "The irrational √2", "Pythagoreans c. 450 BC", "math",
               "The diagonal of a unit square is no ratio of whole numbers: if √2 = p/q in lowest terms, both p and "
               "q must be even — contradiction. Geometry outruns arithmetic.")
    clean(ax, xlim=(-0.3, 2.3), ylim=(-0.55, 1.35))
    ax.add_patch(Rectangle((0, 0), 1, 1, fc=SOFT["math"], ec=MATH, lw=1.5))
    ax.plot([0, 1], [0, 1], color=PHYS, lw=2.2)
    ax.add_patch(Arc((0, 0), 2 * np.sqrt(2), 2 * np.sqrt(2), theta1=0, theta2=45, color=PHYS, lw=1.3, ls="--"))
    ax.plot([-0.2, 2.2], [0, 0], color=INK, lw=1)
    for k in (0, 1, 2):
        ax.plot([k, k], [-0.04, 0.04], color=INK)
        ax.text(k, -0.15, str(k), ha="center", fontsize=9)
    ax.add_patch(Circle((np.sqrt(2), 0), 0.035, fc=PHYS, zorder=5))
    ax.text(np.sqrt(2), -0.34, "√2 = 1.41421356…", ha="center", fontsize=10, color=PHYS, weight="bold")
    ax.text(0.38, 0.62, "√2", fontsize=11, color=PHYS, rotation=45)
    ax.text(0.5, 1.12, "1", ha="center", fontsize=10)

    ax = panel(fig, cs[6], 7, "The real continuum ℝ", "Dedekind, Cantor 1872", "math",
               "A real number is pinned down by nested rational intervals (or a 'cut' in the rationals). Zooming "
               "into √2: each row magnifies the highlighted tenth of the row above.")
    clean(ax, equal=False, xlim=(-0.08, 1.08), ylim=(-0.3, 4.5))
    target = np.sqrt(2)
    lo, width = 1.0, 1.0
    for row in range(5):
        y = 4.0 - row * 0.95
        ax.plot([0, 1], [y, y], color=INK, lw=1.2)
        for k in range(11):
            ax.plot([k / 10, k / 10], [y - 0.06, y + 0.06], color=INK, lw=0.8)
        ax.text(-0.02, y + 0.22, f"{lo:.{row}f}", ha="left", fontsize=8.2, color=MUTED)
        ax.text(1.02, y + 0.22, f"{lo + width:.{row}f}", ha="right", fontsize=8.2, color=MUTED)
        k = int((target - lo) / width * 10)
        ax.add_patch(Rectangle((k / 10, y - 0.09), 0.1, 0.18, fc=PHYS, ec="none", alpha=0.8))
        if row < 4:
            ax.plot([k / 10, 0], [y - 0.1, y - 0.85], color=GRID, lw=0.9)
            ax.plot([(k + 1) / 10, 1], [y - 0.1, y - 0.85], color=GRID, lw=0.9)
        lo, width = lo + k * width / 10, width / 10
    ax.text(0.5, -0.22, "√2 = 1.4142…  (never terminates, never repeats)", ha="center", fontsize=9, color=PHYS)

    ax = panel(fig, cs[7], 8, "Complex numbers ℂ", "Cardano 1545 · Argand 1806", "math",
               "√−1 first appeared as a trick for solving cubics. Drawn as a plane, multiplying by i is a quarter "
               "turn, and Euler's formula e^{iθ} = cos θ + i sin θ ties rotation to growth.")
    clean(ax, xlim=(-2.5, 2.7), ylim=(-1.6, 2.6))
    ax.plot([-2.4, 2.6], [0, 0], color=INK, lw=1)
    ax.plot([0, 0], [-1.5, 2.5], color=INK, lw=1)
    ax.add_patch(Circle((0, 0), 1, fc="none", ec=GRID, lw=1.3))
    for z, lab, off in [(1, "1", (0.12, -0.18)), (1j, "i", (0.1, 0.1)), (-1, "−1", (-0.25, -0.2)),
                        (-1j, "−i", (0.1, -0.2))]:
        ax.add_patch(Circle((z.real, z.imag), 0.05, fc=MATH, zorder=5))
        ax.text(z.real + off[0], z.imag + off[1], lab, fontsize=10, color=MATH)
    z = 2 + 1j
    for w, lab, c in [(z, "z = 2 + i", MATH), (1j * z, "i·z = −1 + 2i", PHYS)]:
        ax.annotate("", xy=(w.real, w.imag), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=c, lw=1.8))
        ax.text(w.real + (0.08 if w.real > 0 else -0.1), w.imag + 0.12, lab, fontsize=9.5, color=c,
                ha="left" if w.real > 0 else "right")
    ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=np.degrees(np.angle(z)), theta2=np.degrees(np.angle(1j * z)),
                     color=PHYS, lw=1.2))
    ax.text(0.25, 0.95, "90°", fontsize=8.5, color=PHYS)
    ax.text(1.35, -1.25, r"$e^{i\pi} + 1 = 0$", fontsize=11, color=INK, ha="center")

    ax = panel(fig, cs[8], 9, "Nested number systems", "Hamilton 1843 · Cayley 1845", "math",
               "Each step gains a power and loses a property. The last two, quaternions (ij = −ji) and octonions, "
               "describe 3-D rotations and appear in exceptional symmetries.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    sets = [("ℕ", "naturals", "counting"), ("ℤ", "integers", "+ subtraction always works"),
            ("ℚ", "rationals", "+ division always works"), ("ℝ", "reals", "+ limits (no gaps)"),
            ("ℂ", "complex", "+ every polynomial has roots; − order"), ("ℍ", "quaternions", "4-D; − commutativity"),
            ("O", "octonions", "8-D; − associativity")]
    n = len(sets)
    for k in range(n - 1, -1, -1):
        right, top = 1.55 + k * 0.62, 0.3 + 1.0 + k * 1.27
        ax.add_patch(FancyBboxPatch((0.2, 0.3), right - 0.2, top - 0.3, boxstyle="round,pad=0,rounding_size=0.25",
                                    fc=(0.16, 0.36, 0.62, 0.05 + 0.025 * (n - k)), ec=MATH, lw=1))
    for k, (s, name, prop) in enumerate(sets):
        right, top = 1.55 + k * 0.62, 0.3 + 1.0 + k * 1.27
        ax.text(right - 0.12, top - 0.45, s, fontsize=13, weight="bold", color=MATH, va="center", ha="right")
        ax.plot([right + 0.05, 6.0], [top - 0.45, top - 0.45], color=GRID, lw=0.8)
        ax.text(6.1, top - 0.3, name, fontsize=9.5, weight="bold", va="center", color=INK)
        ax.text(6.1, top - 0.78, prop, fontsize=8.6, va="center", color="#444")
    footer(fig)
    save(fig, "03-evolution-of-number.png")


# ---------------------------------------------------------------------------------------------
# 04 Geometry
# ---------------------------------------------------------------------------------------------
def _geodesic(a, b, n=120):
    pa = np.array([np.cos(a), np.sin(a)])
    pb = np.array([np.cos(b), np.sin(b)])
    d = (b - a) % (2 * np.pi)
    if d > np.pi:
        a, b = b, a
        pa, pb = pb, pa
        d = 2 * np.pi - d
    if abs(d - np.pi) < 1e-6:
        t = np.linspace(0, 1, n)
        return np.outer(1 - t, pa) + np.outer(t, pb)
    mid = a + d / 2
    c = np.array([np.cos(mid), np.sin(mid)]) / np.cos(d / 2)
    r = np.tan(d / 2)
    t1 = np.arctan2(*(pa - c)[::-1])
    t2 = np.arctan2(*(pb - c)[::-1])
    dt = (t2 - t1 + np.pi) % (2 * np.pi) - np.pi
    t = t1 + np.linspace(0, dt, n)
    return np.c_[c[0] + r * np.cos(t), c[1] + r * np.sin(t)]


def fig04():
    fig = figure("How the concept of space grew: geometry",
                 "From stretching ropes over fields to curved spaces measured from the inside — the geometry that "
                 "physics later needed for gravity")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Rope stretching", "Egypt · Babylon c. 2000 BC", "math",
               "A loop with 12 equally spaced knots, pulled into sides 3, 4, 5, gives a right angle. "
               "Geometry begins as a practical recipe ('earth measurement').")
    clean(ax, xlim=(-0.8, 4.8), ylim=(-0.8, 3.6))
    P = np.array([[0, 0], [4, 0], [0, 3], [0, 0]])
    ax.plot(P[:, 0], P[:, 1], color="#8d6e63", lw=3.5, solid_capstyle="round")
    per = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    for s in range(12):
        k = np.searchsorted(per, s, side="right") - 1
        f = (s - per[k]) / (per[k + 1] - per[k])
        x, y = P[k] + f * (P[k + 1] - P[k])
        ax.add_patch(Circle((x, y), 0.11, fc="#4e342e", zorder=4))
    for x, y in P[:3]:
        ax.plot([x, x], [y - 0.35, y + 0.05], color="#5d4037", lw=4)
    ax.add_patch(Rectangle((0, 0), 0.4, 0.4, fc="none", ec=MATH, lw=1.4))
    ax.text(2, -0.5, "4", ha="center", fontsize=12, color=MATH)
    ax.text(-0.45, 1.5, "3", ha="center", fontsize=12, color=MATH)
    ax.text(2.25, 1.75, "5", ha="center", fontsize=12, color=MATH)

    ax = panel(fig, cs[1], 2, "Axioms and construction", "Euclid c. 300 BC", "math",
               "Elements, Book I, Proposition 1: with only a straightedge and compass, build an equilateral "
               "triangle. Five postulates generate hundreds of theorems by pure deduction.")
    clean(ax, xlim=(-1.6, 2.6), ylim=(-1.4, 1.9))
    A, B = np.array([0, 0]), np.array([1, 0])
    for c in (A, B):
        ax.add_patch(Circle(c, 1, fc="none", ec=MATH, lw=1.2, ls="--"))
    C = np.array([0.5, np.sqrt(3) / 2])
    ax.add_patch(Polygon([A, B, C], fc=SOFT["math"], ec=MATH, lw=2))
    for p, lab, off in [(A, "A", (-0.15, -0.15)), (B, "B", (0.08, -0.15)), (C, "C", (-0.04, 0.1))]:
        ax.add_patch(Circle(p, 0.04, fc=INK, zorder=5))
        ax.text(p[0] + off[0], p[1] + off[1], lab, fontsize=11, weight="bold")
    ax.text(0.5, -1.25, "AC = AB = BC", ha="center", fontsize=10, color=MATH)

    ax = panel(fig, cs[2], 3, "Theorem for all right triangles", "Pythagoras c. 530 BC", "math",
               "Squares on the legs (9 + 16 unit cells) exactly tile the square on the hypotenuse (25). Known as a "
               "rule in Babylon (Plimpton 322, c. 1800 BC); proved in general by the Greeks.")
    clean(ax, xlim=(-3.6, 8.6), ylim=(-4.6, 7.6))
    a, b = 3, 4
    T = np.array([[0, 0], [b, 0], [0, a]])
    ax.add_patch(Polygon(T, fc="#ffe9a8", ec=INK, lw=1.5))

    def sq(p, q, col, n):
        p, q = np.array(p, float), np.array(q, float)
        v = q - p
        nrm = np.array([v[1], -v[0]])
        ax.add_patch(Polygon([p, q, q + nrm, p + nrm], fc=col, ec=INK, lw=1.2, alpha=0.9))
        for k in range(1, n):
            ax.plot(*np.c_[p + v * k / n, p + v * k / n + nrm], color="white", lw=0.8)
            ax.plot(*np.c_[p + nrm * k / n, q + nrm * k / n], color="white", lw=0.8)
        return p + v / 2 + nrm / 2

    c1 = sq([0, 0], [b, 0], "#7fa6d6", 4)
    c2 = sq([0, a], [0, 0], "#e59a7c", 3)
    c3 = sq([b, 0], [0, a], "#9f86c0", 5)
    ax.text(*c1, "16", ha="center", va="center", fontsize=13, weight="bold", color="white")
    ax.text(*c2, "9", ha="center", va="center", fontsize=13, weight="bold", color="white")
    ax.text(*c3, "25", ha="center", va="center", fontsize=13, weight="bold", color="white")

    ax = panel(fig, cs[3], 4, "Conic sections", "Apollonius c. 200 BC", "math",
               "Slicing a cone gives one family: r = p / (1 + e cos θ). Studied for pure beauty, they became "
               "Kepler's planetary orbits 1800 years later.", plot=True)
    th = np.linspace(-np.pi, np.pi, 2000)
    for e, lab, c in [(0, "circle  e = 0", "#555"), (0.6, "ellipse  e = 0.6", MATH), (1.0, "parabola  e = 1", PHYS),
                      (1.6, "hyperbola  e = 1.6", "#3d8b5a")]:
        r = 1.0 / (1 + e * np.cos(th))
        ok = (r > 0) & (r < 8)
        x, y = r * np.cos(th), r * np.sin(th)
        x[~ok] = np.nan
        ax.plot(x, y, color=c, lw=2, label=lab)
    ax.plot(0, 0, "*", color=INK, ms=10)
    ax.text(0.08, -0.25, "focus", fontsize=9)
    ax.set_xlim(-3.2, 3.8)
    ax.set_ylim(-2.4, 2.4)
    ax.set_aspect("equal")
    ax.legend(loc="center right", fontsize=8)
    plotstyle(ax)

    ax = panel(fig, cs[4], 5, "Coordinates unite algebra and geometry", "Descartes, Fermat 1637", "math",
               "Every curve becomes an equation and every equation a curve. Solving x² − 2 = x is now finding where "
               "the parabola meets the line: x = −1 and x = 2.", plot=True)
    x = np.linspace(-2.6, 2.8, 300)
    ax.plot(x, x ** 2 - 2, color=MATH, lw=2.2, label="y = x² − 2")
    ax.plot(x, x, color=PHYS, lw=2.2, label="y = x")
    for xr in (-1, 2):
        ax.plot(xr, xr, "o", color=INK, ms=7, zorder=5)
        ax.text(xr + 0.15, xr - 0.45, f"({xr}, {xr})", fontsize=9.5)
    ax.axhline(0, color=INK, lw=0.8)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_xlim(-2.6, 2.8)
    ax.set_ylim(-2.6, 4.5)
    ax.legend(loc="lower right")
    plotstyle(ax)

    ax = panel(fig, cs[5], 6, "Projective geometry", "Brunelleschi c. 1415 · Desargues 1639", "math",
               "Painters' perspective: parallel lines meet at a vanishing point on the horizon. Desargues added "
               "'points at infinity', creating a geometry where any two lines meet.")
    clean(ax, xlim=(-5, 5), ylim=(-3.6, 2.3))
    hz = 1.4
    ax.plot([-5, 5], [hz, hz], color=MUTED, lw=1)
    ax.text(4.9, hz + 0.15, "horizon", ha="right", fontsize=8.5, color=MUTED)
    ax.plot(0, hz, "o", color=PHYS, ms=6)
    ax.text(0, hz + 0.3, "vanishing point", ha="center", fontsize=8.5, color=PHYS)
    f, h = 2.0, 1.4 + 3.4
    zs = 1 + np.arange(0, 12) * 0.9
    xs = np.arange(-4, 5)
    for i in range(len(zs) - 1):
        for j in range(len(xs) - 1):
            if (i + j) % 2 == 0:
                pts = []
                for zz, xx in [(zs[i], xs[j]), (zs[i], xs[j + 1]), (zs[i + 1], xs[j + 1]), (zs[i + 1], xs[j])]:
                    pts.append([f * xx / zz, hz - h * 1.0 / zz])
                ax.add_patch(Polygon(pts, fc="#7fa6d6", ec="none", alpha=0.85))
    for xx in xs:
        ax.plot([f * xx / zs[0], 0], [hz - h / zs[0], hz], color=MATH, lw=0.7, alpha=0.6)

    ax = panel(fig, cs[6], 7, "Geometry on a sphere", "Menelaus c. 100 · Girard 1625", "math",
               "On a sphere the 'straight lines' are great circles. This triangle has three right angles: "
               "90° + 90° + 90° = 270°. The excess over 180° is proportional to its area.", projection="3d")
    u, v = np.mgrid[0:2 * np.pi:40j, 0:np.pi:20j]
    ax.plot_wireframe(np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v), color=GRID, lw=0.5)
    t = np.linspace(0, np.pi / 2, 60)
    for arc in [(np.cos(t), np.sin(t), 0 * t), (0 * t, np.cos(t), np.sin(t)), (np.sin(t), 0 * t, np.cos(t))]:
        ax.plot(*arc, color=PHYS, lw=3)
    uu, vv = np.mgrid[0:np.pi / 2:20j, 0:np.pi / 2:20j]
    ax.plot_surface(np.cos(uu) * np.sin(vv), np.sin(uu) * np.sin(vv), np.cos(vv), color=PHYS, alpha=0.25,
                    linewidth=0)
    ax.text(0.75, 0.75, 0.75, "270°", fontsize=11, color=PHYS, weight="bold")
    clean3d(ax, elev=25, azim=35)
    ax.set_box_aspect((1, 1, 1), zoom=1.45)

    ax = panel(fig, cs[7], 8, "Hyperbolic geometry", "Lobachevsky 1829 · Bolyai 1832", "math",
               "Drop Euclid's parallel postulate and a consistent new geometry appears. In Poincaré's disk model "
               "(1882) lines are arcs meeting the rim at right angles; this ideal triangle's angles sum to 0°.")
    clean(ax, xlim=(-1.1, 1.1), ylim=(-1.1, 1.1))
    ax.add_patch(Circle((0, 0), 1, fc="#f6f2fb", ec=INK, lw=1.3))
    angs = np.radians([25, 90, 155])
    tri = np.vstack([_geodesic(angs[0], angs[1]), _geodesic(angs[1], angs[2]), _geodesic(angs[2], angs[0])[::-1]])
    for k in range(18):
        a = np.radians(k * 20 + 5)
        g = _geodesic(a, a + np.radians(55))
        ax.plot(g[:, 0], g[:, 1], color=MATH, lw=0.5, alpha=0.35)
    ax.add_patch(Polygon(tri, fc="#b9a6d6", ec=BOTH, lw=1.8, alpha=0.75, zorder=3))
    ax.text(0, 0.55, "angles\nsum 0°", ha="center", va="center", fontsize=8.5, color=BOTH, zorder=4)
    Lg = _geodesic(np.radians(235), np.radians(305))
    ax.plot(Lg[:, 0], Lg[:, 1], color=PHYS, lw=2.6, zorder=4)
    ax.text(0, -0.86, "L", ha="center", fontsize=11, weight="bold", color=PHYS)
    for a, ls in [(55, "--"), (125, "--"), (0, "-"), (20, "-"), (160, "-")]:
        r = np.radians(a)
        ax.plot([np.cos(r), -np.cos(r)], [np.sin(r), -np.sin(r)], color="#3d8b5a", lw=1.3, ls=ls, zorder=2)
    ax.plot(0, 0, "o", color=INK, ms=6, zorder=6)
    ax.text(0.06, -0.12, "P", fontsize=10, weight="bold")
    ax.text(0, -1.08, "all green lines through P miss L", ha="center", fontsize=8.5, color="#3d8b5a")

    ax = panel(fig, cs[8], 9, "Intrinsic curvature", "Gauss 1827 · Riemann 1854", "math",
               "Gauss's 'remarkable theorem': curvature can be measured from inside the surface. Colour = "
               "Gaussian curvature K (red > 0 like a sphere, blue < 0 like a saddle). Riemann extended it to any "
               "dimension — the language of general relativity.", projection="3d")
    x, y = np.mgrid[-2.2:2.2:90j, -2.2:2.2:90j]
    f = 1.1 * np.exp(-((x - 0.7) ** 2 + (y - 0.3) ** 2) / 0.9) - 0.8 * np.exp(-((x + 0.9) ** 2 + (y + 0.6) ** 2) / 0.6)
    fx, fy = np.gradient(f, x[:, 0], y[0, :])
    fxx, fxy = np.gradient(fx, x[:, 0], y[0, :])
    _, fyy = np.gradient(fy, x[:, 0], y[0, :])
    K = (fxx * fyy - fxy ** 2) / (1 + fx ** 2 + fy ** 2) ** 2
    import matplotlib.cm as cm
    from matplotlib.colors import TwoSlopeNorm
    norm = TwoSlopeNorm(vmin=K.min(), vcenter=0, vmax=K.max())
    ax.plot_surface(x, y, f, facecolors=cm.RdBu_r(norm(K)), rstride=1, cstride=1, linewidth=0, antialiased=True,
                    shade=False)
    clean3d(ax, elev=32, azim=-55)
    ax.set_box_aspect((1, 1, 0.45), zoom=1.6)
    footer(fig)
    save(fig, "04-evolution-of-geometry.png")


# ---------------------------------------------------------------------------------------------
# 05 Calculus
# ---------------------------------------------------------------------------------------------
def fig05():
    fig = figure("From measuring areas to calculus",
                 "Two millennia of approximating curved things by straight things, until limits made the "
                 "approximation exact and change itself became computable")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Method of exhaustion", "Eudoxus · Archimedes c. 250 BC", "math",
               "Squeeze a circle between polygons. Archimedes reached 96 sides: 3 10/71 < π < 3 1/7. Inscribed "
               "perimeters below are computed as n·sin(π/n).")
    clean(ax, xlim=(-1.3, 2.9), ylim=(-1.2, 1.2))
    ax.add_patch(Circle((0, 0), 1, fc="none", ec=INK, lw=1.5))
    for n, c in [(6, "#c4512c"), (12, "#3d8b5a"), (24, MATH)]:
        t = np.linspace(0, 2 * np.pi, n + 1)
        ax.plot(np.cos(t), np.sin(t), color=c, lw=1.4)
        ax.text(1.35, 0.75 - [6, 12, 24].index(n) * 0.45, f"n = {n:>2}:  π ≈ {n * np.sin(np.pi / n):.4f}",
                fontsize=10, color=c, family="DejaVu Sans Mono")
    ax.text(1.35, -0.62, f"n = 96:  π ≈ {96 * np.sin(np.pi / 96):.4f}", fontsize=10, color=INK, family="DejaVu Sans Mono")
    ax.text(1.35, -0.98, f"true:    π = {np.pi:.4f}", fontsize=10, color=MUTED, family="DejaVu Sans Mono")

    ax = panel(fig, cs[1], 2, "Quadrature of the parabola", "Archimedes c. 250 BC", "math",
               "Fill a parabolic segment with triangles: each generation adds 1/4 of the previous area. "
               "1 + 1/4 + 1/16 + … = 4/3 — the first summed infinite series.")
    x = np.linspace(-1, 1, 200)
    ax.fill_between(x, x ** 2, 1, color="#f4f1ea")
    ax.plot(x, x ** 2, color=INK, lw=1.6)
    ax.plot([-1, 1], [1, 1], color=INK, lw=1.2)
    cols = [MATH, PHYS, "#3d8b5a", "#b8860b", BOTH]
    segs = [(-1.0, 1.0)]
    for g in range(5):
        new = []
        for a, b in segs:
            m = (a + b) / 2
            ax.add_patch(Polygon([[a, a * a], [b, b * b], [m, m * m]], fc=cols[g], ec="white", lw=0.5, alpha=0.85))
            new += [(a, m), (m, b)]
        segs = new
    for g in range(4):
        ax.text(1.1, 0.95 - g * 0.18, f"gen {g}: area {0.25 ** g:.4f}".replace("area 1.0000", "area 1"),
                fontsize=8.8, color=cols[g])
    ax.text(1.1, 0.95 - 4 * 0.18, "sum → 4/3", fontsize=9.5, color=INK, weight="bold")
    ax.set_xlim(-1.1, 2.0)
    ax.set_ylim(-0.05, 1.08)
    clean(ax, equal=False)

    ax = panel(fig, cs[2], 3, "Indivisibles", "Cavalieri 1635", "math",
               "Think of solids as stacks of infinitely thin slices. If two stacks have equal slices at every "
               "height, their volumes are equal — even if one is sheared.")
    clean(ax, xlim=(0, 10), ylim=(0, 6))
    for k in range(18):
        y = 0.4 + k * 0.28
        ax.add_patch(Rectangle((1.0, y), 2.6, 0.24, fc="#7fa6d6", ec="white", lw=0.5))
        ax.add_patch(Rectangle((5.6 + 1.6 * np.sin(k / 17 * np.pi) , y), 2.6, 0.24, fc="#e59a7c", ec="white",
                               lw=0.5))
    ax.text(2.3, 5.75, "straight stack", ha="center", fontsize=9)
    ax.text(7.7, 5.75, "sheared stack", ha="center", fontsize=9)
    ax.text(5.0, 0.1, "same slices → same volume", ha="center", fontsize=9.5, color=MATH)

    ax = panel(fig, cs[3], 4, "Tangent as a limit of secants", "Fermat 1636 · Leibniz 1684", "math",
               "The slope of a curve at P is the limit of slopes of lines through P and a nearby point Q as Q → P. "
               "For y = x³/3 at x = 1, secant slopes approach 1.", plot=True)
    f = lambda x: x ** 3 / 3
    xx = np.linspace(-0.3, 2.3, 200)
    ax.plot(xx, f(xx), color=INK, lw=2)
    p = 1.0
    for h, c in [(1.0, "#e0a58f"), (0.5, "#d0785a"), (0.2, "#c4512c")]:
        s = (f(p + h) - f(p)) / h
        ax.plot([-0.3, 2.3], [f(p) + s * (-0.3 - p), f(p) + s * (2.3 - p)], color=c, lw=1.4,
                label=f"h = {h}: slope {s:.3f}")
        ax.plot(p + h, f(p + h), "o", color=c, ms=5)
    ax.plot([-0.3, 2.3], [f(p) - 1.3, f(p) + 1.3], color=MATH, lw=2.2, label="tangent: slope 1")
    ax.plot(p, f(p), "o", color=MATH, ms=7, zorder=5)
    ax.text(p - 0.1, f(p) + 0.25, "P", fontsize=11, weight="bold", color=MATH)
    ax.set_xlim(-0.3, 2.3)
    ax.set_ylim(-0.6, 3.2)
    ax.legend(loc="lower right", fontsize=8)
    plotstyle(ax)

    ax = panel(fig, cs[4], 5, "The integral as a limit of sums", "Leibniz 1675 · Riemann 1854", "math",
               "Area under f(x) = 1 + sin x on [0, π] by n rectangles (midpoints). The error shrinks like 1/n²; "
               "Leibniz's ∫ is an elongated S for 'summa'.", plot=True)
    f = lambda x: 1 + np.sin(x)
    exact = np.pi + 2
    n = 8
    xs = np.linspace(0, np.pi, n + 1)
    mids = (xs[:-1] + xs[1:]) / 2
    ax.bar(mids, f(mids), width=np.pi / n, color="#cfe0f3", ec=MATH, lw=1)
    xx = np.linspace(0, np.pi, 200)
    ax.plot(xx, f(xx), color=INK, lw=2)
    for k, nn in enumerate([4, 8, 16, 64]):
        xs2 = np.linspace(0, np.pi, nn + 1)
        m2 = (xs2[:-1] + xs2[1:]) / 2
        approx = np.sum(f(m2)) * np.pi / nn
        ax.text(3.35, 2.05 - k * 0.2, f"n = {nn:>2}: {approx:.5f}", fontsize=8.8, family="DejaVu Sans Mono",
                color=MATH)
    ax.text(3.35, 2.05 - 4 * 0.2, f"exact:  {exact:.5f}", fontsize=8.8, family="DejaVu Sans Mono", color=INK)
    ax.set_xlim(-0.1, 5.1)
    ax.set_ylim(0, 2.25)
    ax.set_xticks([0, np.pi / 2, np.pi])
    ax.set_xticklabels(["0", "π/2", "π"])
    plotstyle(ax, grid=False)

    ax = panel(fig, cs[5], 6, "Fundamental theorem of calculus", "Newton 1666 · Leibniz 1675", "math",
               "Accumulated area A(x) = ∫₀ˣ f(t) dt grows at exactly the rate f(x): A′(x) = f(x). Rates and "
               "totals are inverse operations — the key that unlocked mechanics.", plot=True)
    a1, a2 = split(fig, ax, 2, "v", gap=0.012)
    f = lambda x: 0.6 + 0.5 * np.sin(1.5 * x) + 0.1 * x
    xx = np.linspace(0, 4, 400)
    A = np.concatenate([[0], np.cumsum((f(xx[1:]) + f(xx[:-1])) / 2 * np.diff(xx))])
    x0 = 2.6
    a1.plot(xx, f(xx), color=PHYS, lw=2)
    a1.fill_between(xx, 0, f(xx), where=xx <= x0, color="#f3c9b8")
    a1.axvline(x0, color=MUTED, lw=0.8, ls="--")
    a1.text(1.2, 0.35, "area A(x)", fontsize=9.5, color=PHYS)
    a1.text(0.05, 1.32, "f(x)", fontsize=10, color=PHYS)
    a1.set_xlim(0, 4)
    a1.set_ylim(0, 1.6)
    a1.set_xticks([])
    plotstyle(a1, grid=False)
    a2.plot(xx, A, color=MATH, lw=2)
    i0 = np.searchsorted(xx, x0)
    a2.plot([x0 - 0.7, x0 + 0.7], [A[i0] - 0.7 * f(x0), A[i0] + 0.7 * f(x0)], color=PHYS, lw=1.8)
    a2.plot(x0, A[i0], "o", color=PHYS)
    a2.axvline(x0, color=MUTED, lw=0.8, ls="--")
    a2.text(0.1, A.max() * 0.82, "A(x); slope of tangent = f(x)", fontsize=9.5, color=MATH)
    a2.set_xlim(0, 4)
    plotstyle(a2, grid=False)

    ax = panel(fig, cs[6], 7, "Differential equations", "Newton 1671 · Euler 1768", "math",
               "Laws of change instead of formulas for quantities. Slope field of the logistic equation "
               "dy/dt = y(1 − y) (Verhulst 1838) with solution curves computed by Runge–Kutta integration.", plot=True)
    T, Y = np.meshgrid(np.linspace(0, 8, 22), np.linspace(-0.2, 1.5, 16))
    S = Y * (1 - Y)
    L = np.sqrt(1 + S ** 2)
    ax.quiver(T, Y, 1 / L, S / L, color="#9bb6d8", angles="xy", scale=32, width=0.003, headwidth=0, headlength=0,
              headaxislength=0, pivot="mid")
    from common import rk4
    t = np.linspace(0, 8, 200)
    for y0, c in zip([0.02, 0.1, 0.3, 1.4, -0.02], [MATH, MATH, MATH, PHYS, "#3d8b5a"]):
        sol = rk4(lambda t, y: y * (1 - y), np.array([y0]), t)[:, 0]
        sol[np.abs(sol) > 2] = np.nan
        ax.plot(t, sol, color=c, lw=2)
    ax.set_xlim(0, 8)
    ax.set_ylim(-0.2, 1.5)
    ax.set_xlabel("t")
    ax.set_ylabel("y")
    plotstyle(ax, grid=False)

    ax = panel(fig, cs[7], 8, "Fourier series", "Fourier 1807 (heat flow)", "math",
               "Any periodic function as a sum of sines: square wave = (4/π) Σ sin(kx)/k over odd k. "
               "The 9% overshoot near jumps never disappears (Gibbs phenomenon, 1899).", plot=True)
    x = np.linspace(-np.pi, np.pi, 2000)
    sq = np.sign(np.sin(x))
    ax.plot(x, sq, color=INK, lw=1.2, ls="--")
    for N, c in [(1, "#9bb6d8"), (3, "#6b93c8"), (9, MATH), (49, PHYS)]:
        s = sum(4 / np.pi * np.sin(k * x) / k for k in range(1, 2 * N, 2))
        ax.plot(x, s, color=c, lw=1.5, label=f"{N} term{'s' if N > 1 else ''}")
    ax.legend(loc="lower right", ncol=2)
    ax.set_xlim(-np.pi, np.pi)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xticks([-np.pi, 0, np.pi])
    ax.set_xticklabels(["−π", "0", "π"])
    plotstyle(ax)

    ax = panel(fig, cs[8], 9, "Calculus of variations", "Bernoulli 1696 · Euler 1744", "math",
               "Optimise a whole curve: which slide gets a bead from A to B fastest under gravity? Answer: the "
               "cycloid. Descent times (g = 9.81 m/s², drop 2 m, run π m) computed numerically:", plot=True)
    g = 9.81
    th = np.linspace(0, np.pi, 400)
    cx, cy = th - np.sin(th), -(1 - np.cos(th))
    T_cyc = np.pi * np.sqrt(1 / g)
    L = np.hypot(np.pi, 2)
    T_line = L / np.sqrt(g)
    u = np.linspace(0, 1, 4001)
    integrand = 2 * np.sqrt(4 * np.pi ** 2 * u ** 4 + 4) / np.sqrt(4 * g)
    T_root = np.trapz(integrand, u)
    xr = np.pi * u ** 4
    yr = -2 * u ** 2
    ax.plot([0, np.pi], [0, -2], color="#888", lw=2, label=f"straight line: {T_line:.3f} s")
    ax.plot(xr, yr, color="#3d8b5a", lw=2, label=f"y ∝ −√x curve: {T_root:.3f} s")
    ax.plot(cx, cy, color=PHYS, lw=2.6, label=f"cycloid: {T_cyc:.3f} s (fastest)")
    ax.plot([0, np.pi], [0, -2], "o", color=INK)
    ax.text(-0.05, 0.12, "A", fontsize=11, weight="bold")
    ax.text(np.pi + 0.06, -2.05, "B", fontsize=11, weight="bold")
    ax.set_xlim(-0.2, 3.6)
    ax.set_ylim(-2.4, 0.4)
    ax.set_aspect("equal")
    ax.legend(loc="upper right", fontsize=8.2)
    plotstyle(ax)
    footer(fig)
    save(fig, "05-from-areas-to-calculus.png")


if __name__ == "__main__":
    for f in (fig01, fig02, fig03, fig04, fig05):
        f()
