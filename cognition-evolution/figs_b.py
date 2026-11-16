"""Figures 06-10: algebra & structure, motion, space & time, light, matter."""
import itertools

import numpy as np
from matplotlib.patches import Arc, Circle, FancyBboxPatch, Polygon, Rectangle, Wedge

from common import (BOTH, GRID, INK, MATH, MUTED, PALETTE, PHYS, SOFT, arrow, box, cells, clean, clean3d,
                    figure, footer, note, panel, plotstyle, rk4, save, split, wavelength_rgb)


# ---------------------------------------------------------------------------------------------
# 06 Algebra to structure
# ---------------------------------------------------------------------------------------------
def fig06():
    fig = figure("From solving equations to studying structure: algebra",
                 "Algebra moved from recipes for particular numbers, to symbols for any number, to the symmetry "
                 "of the solutions themselves — the language later used for particles and forces")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Notation compresses thought", "820 → 1637", "math",
               "The same equation written three ways. Symbols made it possible to manipulate whole classes of "
               "problems at once and to see patterns no sentence could show.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    cards = [("Rhetorical", "al-Khwārizmī, c. 820", "“A square and ten of its roots\nare equal to thirty-nine dirhams.”",
              10),
             ("Syncopated", "abbreviations, Diophantus → Cardano 1545", "1 quad. p. 10 pos. aeq. 39", 11),
             ("Symbolic", "Viète 1591 · Descartes 1637", r"$x^2 + 10x = 39$", 17)]
    for k, (name, who, txt, fs) in enumerate(cards):
        y = 8.2 - k * 3.15
        ax.add_patch(FancyBboxPatch((0.3, y - 1.25), 9.4, 2.55, boxstyle="round,pad=0,rounding_size=0.3",
                                    fc=SOFT["math"] if k == 2 else "#f7f5f0", ec=MATH if k == 2 else GRID, lw=1.2))
        ax.text(0.6, y + 0.85, name, fontsize=10.5, weight="bold", color=MATH, va="center")
        ax.text(9.4, y + 0.85, who, fontsize=8.5, color=MUTED, va="center", ha="right", style="italic")
        ax.text(5, y - 0.25, txt, fontsize=fs, ha="center", va="center", color=INK,
                style="italic" if k == 0 else "normal")

    ax = panel(fig, cs[1], 2, "Completing the square", "al-Khwārizmī c. 820", "math",
               "x² + 10x = 39 solved with pictures: split 10x into two 5x strips, add the missing 5 × 5 corner. "
               "(x + 5)² = 39 + 25 = 64, so x + 5 = 8 and x = 3.")
    clean(ax, xlim=(-1.2, 10.2), ylim=(-1.2, 9.4))
    x = 3
    ax.add_patch(Rectangle((0, 0), x, x, fc="#7fa6d6", ec=INK))
    ax.add_patch(Rectangle((x, 0), 5, x, fc="#e59a7c", ec=INK))
    ax.add_patch(Rectangle((0, x), x, 5, fc="#e59a7c", ec=INK))
    ax.add_patch(Rectangle((x, x), 5, 5, fc="#fff3c4", ec=INK, ls="--", lw=1.4))
    for (cx, cy, t) in [(1.5, 1.5, "x²"), (5.5, 1.5, "5x"), (1.5, 5.5, "5x"), (5.5, 5.5, "25\n(added)")]:
        ax.text(cx, cy, t, ha="center", va="center", fontsize=12, weight="bold")
    ax.text(1.5, -0.6, "x", ha="center", fontsize=11)
    ax.text(5.5, -0.6, "5", ha="center", fontsize=11)
    ax.text(-0.6, 1.5, "x", ha="center", fontsize=11)
    ax.text(-0.6, 5.5, "5", ha="center", fontsize=11)
    ax.text(4, 8.8, "side x + 5 = 8", ha="center", fontsize=10.5, color=MATH)

    ax = panel(fig, cs[2], 3, "Every polynomial has roots", "Gauss 1799", "math",
               "Fundamental theorem of algebra: degree n ⇒ n complex roots. Shown: all roots of all 8,192 "
               "polynomials of degree 12 with coefficients ±1 (≈98,000 points, computed) — unexpected fractal "
               "structure.")
    pts = []
    for signs in itertools.product((-1, 1), repeat=12):
        pts.append(np.roots((1,) + signs))
    pts = np.concatenate(pts)
    ax.scatter(pts.real, pts.imag, s=0.05, color=MATH, alpha=0.5, lw=0)
    ax.add_patch(Circle((0, 0), 1, fc="none", ec=PHYS, lw=0.6, ls="--"))
    clean(ax, xlim=(-1.75, 1.75), ylim=(-1.6, 1.6))

    ax = panel(fig, cs[3], 4, "The limits of formulas", "Babylon → Galois 1832", "math",
               "Formulas in radicals exist up to degree 4. For degree 5 none can exist (Abel 1824). Galois showed "
               "why: solvability depends on the symmetry group of the roots — the birth of group theory.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    rows = [("1", "antiquity", r"$x=-\frac{b}{a}$", True),
            ("2", "Babylon", r"$x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$", True),
            ("3", "Cardano 1545",
             r"$t=\sqrt[3]{-\frac{q}{2}+\sqrt{\frac{q^2}{4}+\frac{p^3}{27}}}+\sqrt[3]{-\frac{q}{2}-\sqrt{\frac{q^2}{4}+\frac{p^3}{27}}}$",
             True),
            ("4", "Ferrari 1545", "reduce to a cubic 'resolvent'", True),
            ("5", "Abel 1824", "no general formula in radicals", False)]
    for k, (deg, who, form, ok) in enumerate(rows):
        y = 9.0 - k * 1.95
        ax.text(0.25, y, f"degree {deg}", fontsize=10, weight="bold", color=MATH, va="center")
        ax.text(0.25, y - 0.55, who, fontsize=8, color=MUTED, va="center")
        ax.text(2.35, y - 0.15, form, fontsize=10 if k != 2 else 7.8, va="center", color=INK)
        ax.text(9.75, y - 0.15, "✓" if ok else "✗", fontsize=16, color="#2e7d32" if ok else "#c62828", ha="right",
                va="center")
        if k < 4:
            ax.plot([0.2, 9.8], [y - 0.98, y - 0.98], color=GRID, lw=0.8)

    ax = panel(fig, cs[4], 5, "A group: symmetries of a triangle", "Cayley 1854", "math",
               "Six symmetries of an equilateral triangle: identity e, rotations r, r², reflections s₁, s₂, s₃. "
               "The table of compositions (row ∘ column) is the group D₃. Note r∘s ≠ s∘r: it is non-commutative.")
    names = ["e", "r", "r²", "s₁", "s₂", "s₃"]
    perms = [(0, 1, 2), (1, 2, 0), (2, 0, 1), (0, 2, 1), (2, 1, 0), (1, 0, 2)]
    idx = {p: i for i, p in enumerate(perms)}
    table = np.array([[idx[tuple(a[b[i]] for i in range(3))] for b in perms] for a in perms])
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(["#f2f2f2", "#9cc0e7", "#5b8fd1", "#f2b8a0", "#e58b6a", "#c95f3d"])
    ax.imshow(table, cmap=cmap, vmin=-0.5, vmax=5.5)
    for i in range(6):
        for j in range(6):
            ax.text(j, i, names[table[i, j]], ha="center", va="center", fontsize=11, weight="bold")
    ax.set_xticks(range(6))
    ax.set_xticklabels(names, fontsize=10)
    ax.set_yticks(range(6))
    ax.set_yticklabels(names, fontsize=10)
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)

    ax = panel(fig, cs[5], 6, "Symmetry as action", "Klein 1872 (Erlangen)", "math",
               "The 8 symmetries of a square (group D₄) acting on an asymmetric 'F'. Klein's Erlangen programme: "
               "a geometry is defined by its group of transformations.")
    clean(ax, xlim=(-0.2, 8.2), ylim=(-0.5, 4.6))
    F = np.array([[-0.25, -0.5], [-0.05, -0.5], [-0.05, -0.05], [0.2, -0.05], [0.2, 0.12], [-0.05, 0.12], [-0.05, 0.3],
                  [0.3, 0.3], [0.3, 0.5], [-0.25, 0.5]])
    mats = [("e", np.eye(2)), ("r", [[0, -1], [1, 0]]), ("r²", [[-1, 0], [0, -1]]), ("r³", [[0, 1], [-1, 0]]),
            ("mirror |", [[-1, 0], [0, 1]]), ("mirror —", [[1, 0], [0, -1]]), ("mirror /", [[0, 1], [1, 0]]),
            ("mirror \\", [[0, -1], [-1, 0]])]
    for k, (lab, M) in enumerate(mats):
        cx, cy = 1.0 + (k % 4) * 2.0, 3.3 - (k // 4) * 2.35
        ax.add_patch(Rectangle((cx - 0.75, cy - 0.75), 1.5, 1.5, fc="#f7f5f0", ec=GRID))
        G = F @ np.array(M, float).T
        ax.add_patch(Polygon(G + [cx, cy], fc=MATH if k < 4 else PHYS, ec="none"))
        ax.text(cx, cy - 1.0, lab, ha="center", fontsize=9)

    ax = panel(fig, cs[6], 7, "Linear algebra", "Grassmann 1844 · Cayley 1858", "math",
               "A matrix is a transformation of the whole plane. A = [[1.2, 0.6], [0.3, 1.0]] maps the grey grid to the "
               "blue one and the unit circle to an ellipse; eigenvectors (dashed) are only stretched, by λ = 1.54 and 0.66.")
    A = np.array([[1.2, 0.6], [0.3, 1.0]])
    for k in np.arange(-3, 4):
        t = np.linspace(-3, 3, 2)
        ax.plot([k, k], [-3, 3], color="#e3e0d8", lw=0.8)
        ax.plot([-3, 3], [k, k], color="#e3e0d8", lw=0.8)
        L1 = A @ np.vstack([np.full(2, k), t])
        L2 = A @ np.vstack([t, np.full(2, k)])
        ax.plot(*L1, color="#9bb6d8", lw=0.9)
        ax.plot(*L2, color="#9bb6d8", lw=0.9)
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(th), np.sin(th), color="#aaa", lw=1.2)
    E = A @ np.vstack([np.cos(th), np.sin(th)])
    ax.plot(*E, color=MATH, lw=2)
    for v, c, lab in [((1, 0), PHYS, "Ae₁"), ((0, 1), "#3d8b5a", "Ae₂")]:
        w = A @ np.array(v)
        ax.annotate("", xy=w, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=c, lw=2))
        ax.text(w[0] + 0.1, w[1] + 0.1, lab, color=c, fontsize=10)
    vals, vecs = np.linalg.eig(A)
    for lam, v in zip(vals, vecs.T):
        ax.plot([-3 * v[0], 3 * v[0]], [-3 * v[1], 3 * v[1]], color=INK, lw=1, ls="--")
        ax.text(2.2 * v[0] + 0.1, 2.2 * v[1] - 0.25, f"λ = {lam:.2f}", fontsize=9)
    clean(ax, xlim=(-2.6, 2.6), ylim=(-2.2, 2.2))

    ax = panel(fig, cs[7], 8, "Continuous groups", "Lie 1873 · Minkowski 1908", "both",
               "Lie groups: symmetries that vary smoothly. Rotations move points along circles (x² + y² fixed); "
               "Lorentz boosts move events along hyperbolas (x² − t² fixed). Same mathematics, new physics.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.01)
    for r in (0.5, 1.0, 1.5, 2.0):
        a1.add_patch(Circle((0, 0), r, fc="none", ec=MATH, lw=1.3))
        a1.annotate("", xy=(r * np.cos(0.9), r * np.sin(0.9)), xytext=(r * np.cos(0.75), r * np.sin(0.75)),
                    arrowprops=dict(arrowstyle="-|>", color=MATH, lw=1.3))
    a1.set_title("rotations SO(2)", fontsize=9.5, color=MATH)
    clean(a1, xlim=(-2.3, 2.3), ylim=(-2.3, 2.3))
    eta = np.linspace(-1.5, 1.5, 100)
    for s in (0.5, 1.0, 1.5):
        for sg in (1, -1):
            a2.plot(sg * s * np.cosh(eta), s * np.sinh(eta), color=PHYS, lw=1.3)
            a2.plot(s * np.sinh(eta), sg * s * np.cosh(eta), color="#e2a38a", lw=1.0)
    a2.plot([-2.3, 2.3], [-2.3, 2.3], color=INK, lw=0.8, ls="--")
    a2.plot([-2.3, 2.3], [2.3, -2.3], color=INK, lw=0.8, ls="--")
    a2.annotate("", xy=(np.cosh(0.6), np.sinh(0.6)), xytext=(np.cosh(0.4), np.sinh(0.4)),
                arrowprops=dict(arrowstyle="-|>", color=PHYS, lw=1.4))
    a2.set_title("boosts SO(1,1)", fontsize=9.5, color=PHYS)
    a2.text(2.0, -0.2, "x", fontsize=9)
    a2.text(0.1, 2.05, "t", fontsize=9)
    clean(a2, xlim=(-2.3, 2.3), ylim=(-2.3, 2.3))

    ax = panel(fig, cs[8], 9, "Categories: maps between structures", "Eilenberg & Mac Lane 1945", "math",
               "Focus moves from objects to arrows. A diagram 'commutes' if all paths agree (g∘f = k∘h); a functor F "
               "maps one whole category into another, preserving composition — used in topology and quantum theory.")
    clean(ax, equal=False, xlim=(0, 10.6), ylim=(0, 10))

    def square(ox, labels, col, fname=""):
        P = {"A": (ox, 7.5), "B": (ox + 3, 7.5), "C": (ox, 3.5), "D": (ox + 3, 3.5)}
        for k, (x, y) in P.items():
            ax.text(x, y, labels[k], ha="center", va="center", fontsize=11, weight="bold", color=col)
        for p, q, lab, off in [("A", "B", "f", (0, 0.45)), ("A", "C", "h", (-0.45, 0)), ("B", "D", "g", (0.45, 0)),
                               ("C", "D", "k", (0, -0.45))]:
            (x1, y1), (x2, y2) = P[p], P[q]
            dx, dy = np.sign(x2 - x1), np.sign(y2 - y1)
            arrow(ax, (x1 + 0.55 * dx, y1 + 0.5 * dy), (x2 - 0.55 * dx, y2 - 0.5 * dy), color=col, lw=1.3)
            ax.text((x1 + x2) / 2 + off[0], (y1 + y2) / 2 + off[1], fname + lab if not fname else f"F{lab}",
                    ha="center", va="center", fontsize=10, style="italic", color=col)
        ax.text(ox + 1.5, 5.5, "↻", ha="center", va="center", fontsize=16, color=MUTED)

    square(0.9, {"A": "A", "B": "B", "C": "C", "D": "D"}, MATH)
    square(6.7, {"A": "FA", "B": "FB", "C": "FC", "D": "FD"}, BOTH, fname="F")
    arrow(ax, (4.45, 5.5), (5.75, 5.5), color=INK, lw=1.8)
    ax.text(5.1, 6.0, "functor F", ha="center", fontsize=9.5)
    ax.text(5, 1.4, "g∘f = k∘h   ⇒   Fg∘Ff = Fk∘Fh", ha="center", fontsize=10.5, color=INK)
    footer(fig)
    save(fig, "06-from-equations-to-structure.png")


# ---------------------------------------------------------------------------------------------
# 07 Motion
# ---------------------------------------------------------------------------------------------
def fig07():
    fig = figure("How the concept of motion grew",
                 "From 'every motion needs a mover' to inertia, orbits, phase space, least action and chaos — "
                 "motion becomes a geometric object")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Natural and violent motion", "Aristotle c. 350 BC", "phys",
               "Heavy things seek the centre, light things rise; anything else needs a constant push. A thrown stone "
               "flies straight until its push runs out, then drops straight down. Wrong — but a theory.")
    clean(ax, xlim=(0, 10), ylim=(0, 7))
    ax.plot([0, 10], [0.5, 0.5], color="#8d6e63", lw=3)
    ax.add_patch(Polygon([[0.6, 0.5], [1.3, 0.5], [1.6, 1.2], [1.2, 1.4]], fc="#5d6d7e"))
    ax.plot([1.4, 6.0, 6.0], [1.3, 5.6, 0.6], color=PHYS, lw=2.4)
    ax.text(3.2, 4.0, "violent\n(forced)", fontsize=9.5, color=PHYS, ha="center")
    ax.text(6.25, 3.0, "natural\n(downward)", fontsize=9.5, color=PHYS)
    ax.annotate("", xy=(9.7, 4.8), xytext=(9.7, 6.4), arrowprops=dict(arrowstyle="-|>", color="#6d4c41", lw=2))
    ax.text(9.5, 5.6, "earth falls", fontsize=9, color="#6d4c41", ha="right")
    ax.annotate("", xy=(9.7, 3.5), xytext=(9.7, 1.8), arrowprops=dict(arrowstyle="-|>", color="#e67e22", lw=2))
    ax.text(9.5, 2.6, "fire rises", fontsize=9, color="#e67e22", ha="right")

    ax = panel(fig, cs[1], 2, "Impetus", "Philoponus c. 530 · Buridan c. 1350", "phys",
               "The thrower gives the stone an internal 'impetus' that slowly wears off — a step toward inertia. "
               "Sixteenth-century gunnery books drew trajectories as straight line, arc, then vertical fall.")
    clean(ax, xlim=(0, 10), ylim=(0, 7))
    ax.plot([0, 10], [0.5, 0.5], color="#8d6e63", lw=3)
    ax.add_patch(Polygon([[0.5, 0.5], [1.4, 0.5], [1.7, 1.3], [1.1, 1.4]], fc="#5d6d7e"))
    s = np.linspace(0, 1, 50)
    x1, y1 = 1.5 + 3.2 * s, 1.3 + 3.2 * s
    ang = np.linspace(np.pi * 0.75, 0.0, 60)
    cx, cy, r = 4.7 + 1.2 * np.cos(np.pi * 0.25), 4.5 - 1.2 * np.sin(np.pi * 0.25), 1.2
    cx, cy = x1[-1] + r * np.cos(-np.pi / 4), y1[-1] + r * np.sin(-np.pi / 4)
    ax2 = np.linspace(np.pi * 3 / 4, 0, 60)
    xa, ya = cx + r * np.cos(ax2), cy + r * np.sin(ax2)
    ax.plot(np.r_[x1, xa, [xa[-1], xa[-1]]], np.r_[y1, ya, [ya[-1], 0.6]], color=PHYS, lw=2.4)
    ax.text(2.0, 3.6, "impetus\ndominates", fontsize=9, color=PHYS)
    ax.text(cx + r + 0.2, 2.0, "impetus\nexhausted", fontsize=9, color=PHYS)

    ax = panel(fig, cs[2], 3, "Uniform acceleration", "Galileo 1604 / 1638", "phys",
               "Rolling balls down a ramp, Galileo found distances in successive equal times go as 1 : 3 : 5 : 7 : 9, "
               "so total distance ∝ t². First law of motion stated as a mathematical function.")
    clean(ax, xlim=(-0.3, 10.3), ylim=(-1.6, 6.2))
    L = 10
    angle = np.radians(25)
    ax.plot([0, L * np.cos(angle)], [L * np.sin(angle) * 1.0 + 0.0 - L * np.sin(angle) + 4.6,
                                     4.6 - L * np.sin(angle)], color="#8d6e63", lw=3)
    top = np.array([0, 4.6])
    d = np.array([np.cos(angle), -np.sin(angle)])
    for t in range(6):
        p = top + d * (t ** 2) * (L / 25) * 0.98
        ax.add_patch(Circle(p + np.array([np.sin(angle), np.cos(angle)]) * 0.22, 0.22, fc=PHYS, alpha=0.35 + 0.13 * t))
        if t > 0:
            q = top + d * ((t - 1) ** 2) * (L / 25) * 0.98
            m = (p + q) / 2 - np.array([np.sin(angle), np.cos(angle)]) * 0.45
            ax.text(*m, str(2 * t - 1), fontsize=10, color=MATH, weight="bold", ha="center", va="center")
    ax.text(5, -1.2, "distances per interval: 1, 3, 5, 7, 9   →   totals 1, 4, 9, 16, 25", ha="center",
            fontsize=9.3, color=MATH)
    ax.text(6.5, 4.6, "ball positions at equal\ntime steps t = 0, 1, …, 5", fontsize=9, color=PHYS, ha="center")

    ax = panel(fig, cs[3], 4, "Projectiles are parabolas", "Galileo 1638", "phys",
               "Horizontal motion is uniform, vertical motion is accelerated: combined, a parabola. Launch at "
               "20 m/s; range R = v² sin 2θ / g is largest at 45°, and complementary angles land together.", plot=True)
    g, v = 9.81, 20.0
    for k, th in enumerate([15, 30, 45, 60, 75]):
        t = np.linspace(0, 2 * v * np.sin(np.radians(th)) / g, 200)
        x = v * np.cos(np.radians(th)) * t
        y = v * np.sin(np.radians(th)) * t - 0.5 * g * t ** 2
        R = v ** 2 * np.sin(np.radians(2 * th)) / g
        ax.plot(x, y, lw=2.2 if th == 45 else 1.5, color=PHYS if th == 45 else PALETTE[[0, 2, 1, 3, 4][k]],
                label=f"{th}°: R = {R:.1f} m")
    ax.set_xlabel("distance (m)")
    ax.set_ylabel("height (m)")
    ax.set_aspect("equal")
    ax.set_ylim(0, 20.5)
    ax.legend(loc="upper right", fontsize=8)
    plotstyle(ax)

    ax = panel(fig, cs[4], 5, "Kepler's equal areas", "Kepler 1609", "phys",
               "Planets move on ellipses with the Sun at a focus, sweeping equal areas in equal times. Positions at "
               "12 equal time steps for e = 0.6, from Kepler's equation M = E − e sin E (solved numerically).")
    e, a = 0.6, 1.0
    b = a * np.sqrt(1 - e ** 2)
    Ms = np.linspace(0, 2 * np.pi, 13)
    Es = []
    for M in Ms:
        E = M
        for _ in range(50):
            E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
        Es.append(E)
    Es = np.array(Es)
    X, Y = a * (np.cos(Es) - e), b * np.sin(Es)
    for k in range(12):
        EE = np.linspace(Es[k], Es[k + 1], 30)
        poly = np.vstack([[0, 0], np.c_[a * (np.cos(EE) - e), b * np.sin(EE)]])
        ax.add_patch(Polygon(poly, fc=PHYS if k % 2 == 0 else "#f3c9b8", ec="white", lw=0.6, alpha=0.9))
    EE = np.linspace(0, 2 * np.pi, 300)
    ax.plot(a * (np.cos(EE) - e), b * np.sin(EE), color=INK, lw=1.2)
    ax.plot(X, Y, "o", color=INK, ms=4)
    ax.plot(0, 0, "o", color="#f1c40f", ms=14, mec="#b7950b")
    ax.text(0.02, -0.17, "Sun", fontsize=9, ha="center")
    clean(ax, xlim=(-1.75, 0.55), ylim=(-0.95, 0.95))

    ax = panel(fig, cs[5], 6, "Newton's cannon", "Newton 1687", "phys",
               "Fire faster and the ball falls around the Earth: the Moon's motion and an apple's fall are one "
               "law, F = GMm / r². Trajectories integrated numerically for launch speeds 0.55–1.12 × circular "
               "speed.")
    ax.add_patch(Circle((0, 0), 1, fc="#cfe3d4", ec="#3d8b5a", lw=1.5))
    ax.add_patch(Polygon([[-0.07, 0.99], [0.0, 1.15], [0.07, 0.99]], fc="#6d4c41"))
    r0 = 1.15
    vc = np.sqrt(1 / r0)
    f = lambda t, s: np.array([s[2], s[3], -s[0] / np.hypot(s[0], s[1]) ** 3, -s[1] / np.hypot(s[0], s[1]) ** 3])
    for k, fac in enumerate([0.55, 0.75, 0.9, 1.0, 1.12]):
        t = np.linspace(0, 14, 3500)
        sol = rk4(f, np.array([0, r0, fac * vc, 0]), t)
        rr = np.hypot(sol[:, 0], sol[:, 1])
        hit = np.argmax(rr < 1.0) if np.any(rr < 1.0) else len(rr)
        ax.plot(sol[:hit, 0], sol[:hit, 1], color=PALETTE[k], lw=1.8, label=f"{fac:.2f} v_c")
    ax.legend(loc="lower left", fontsize=7.8)
    clean(ax, xlim=(-2.5, 2.5), ylim=(-2.1, 1.6))

    ax = panel(fig, cs[6], 7, "Phase space", "Hamilton 1834 · Poincaré 1890", "both",
               "A state is a point (position q, momentum p); motion is a flow. Pendulum energy contours "
               "H = p²/2 − cos q: closed loops = swinging, open curves = spinning over the top; the separatrix "
               "(red) divides them.", plot=True)
    q, p = np.meshgrid(np.linspace(-2 * np.pi, 2 * np.pi, 400), np.linspace(-3, 3, 300))
    H = p ** 2 / 2 - np.cos(q)
    ax.contour(q, p, H, levels=np.linspace(-0.9, 3.5, 16), colors=MATH, linewidths=0.9)
    ax.contour(q, p, H, levels=[1.0], colors=PHYS, linewidths=2.2)
    ax.set_xlabel("angle q")
    ax.set_ylabel("momentum p")
    ax.set_xticks([-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi])
    ax.set_xticklabels(["−2π", "−π", "0", "π", "2π"])
    plotstyle(ax, grid=False)

    ax = panel(fig, cs[7], 8, "Principle of least action", "Maupertuis 1744 · Lagrange · Hamilton", "both",
               "Nature picks the path that makes the action S = ∫(½v² − g x) dt stationary. Ball thrown up and caught "
               "after 1 s: the true parabola has the smallest S among nearby paths (values computed).", plot=True)
    g = 9.81
    t = np.linspace(0, 1, 801)
    true = 0.5 * g * t * (1 - t)

    def S(x):
        v = np.gradient(x, t)
        return np.trapz(0.5 * v ** 2 - g * x, t)

    for k, (eps, mode) in enumerate([(0, 1), (0.35, 1), (-0.35, 1), (0.25, 2), (0.6, 1)]):
        x = true + eps * np.sin(mode * np.pi * t)
        c = PHYS if eps == 0 else PALETTE[[0, 0, 2, 3, 4][k]]
        ax.plot(t, x, color=c, lw=2.6 if eps == 0 else 1.3, ls="-" if eps == 0 else "--",
                label=("true path" if eps == 0 else f"trial {k}") + f": S = {S(x):.3f}")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("height (m)")
    ax.legend(loc="lower center", fontsize=7.6, ncol=2)
    ax.set_ylim(-1.5, 2.2)
    plotstyle(ax)

    ax = panel(fig, cs[8], 9, "Deterministic chaos", "Poincaré 1890 · Lorenz 1963", "both",
               "Fully deterministic equations can be unpredictable. Lorenz system (σ = 10, ρ = 28, β = 8/3): two runs "
               "starting 10⁻⁵ apart (blue, orange) separate completely; inset: separation grows exponentially.")
    def lor(t, s):
        x, y, z = s
        return np.array([10 * (y - x), x * (28 - z) - y, x * y - 8 / 3 * z])
    t = np.linspace(0, 30, 9000)
    s1 = rk4(lor, np.array([1.0, 1.0, 20.0]), t)
    s2 = rk4(lor, np.array([1.0 + 1e-5, 1.0, 20.0]), t)
    ax.plot(s1[:, 0], s1[:, 2], color=MATH, lw=0.45, alpha=0.8)
    ax.plot(s2[6000:, 0], s2[6000:, 2], color=PHYS, lw=0.45, alpha=0.8)
    clean(ax, equal=False)
    ia = ax.inset_axes([0.69, 0.02, 0.3, 0.32])
    sep = np.linalg.norm(s1 - s2, axis=1)
    ia.semilogy(t, sep, color=INK, lw=0.8)
    ia.set_xticks([0, 15, 30])
    ia.set_yticks([1e-5, 1e-2, 10])
    ia.tick_params(labelsize=7)
    ia.set_xlabel("t", fontsize=7, labelpad=0)
    ia.set_title("separation", fontsize=7.5, pad=2)
    footer(fig)
    save(fig, "07-evolution-of-motion.png")


# ---------------------------------------------------------------------------------------------
# 08 Space and time
# ---------------------------------------------------------------------------------------------
def fig08():
    fig = figure("How the concepts of space and time grew",
                 "From an absolute stage with a universal clock, to spacetime, to a dynamical geometry that bends, "
                 "traps light and expands")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Absolute space and time", "Newton 1687", "phys",
               "'Absolute, true and mathematical time flows equably without relation to anything external.' One "
               "fixed grid, and every clock everywhere shows the same time.")
    clean(ax, xlim=(-0.5, 6.5), ylim=(-0.5, 4.5))
    for i in range(7):
        ax.plot([i, i], [0, 4], color=GRID, lw=1)
    for j in range(5):
        ax.plot([0, 6], [j, j], color=GRID, lw=1)
    for i in range(0, 7, 2):
        for j in range(0, 5, 2):
            ax.add_patch(Circle((i, j), 0.33, fc="white", ec=INK, lw=1.2, zorder=3))
            ax.plot([i, i], [j, j + 0.24], color=INK, lw=1.2, zorder=4)
            ax.plot([i, i + 0.17], [j, j + 0.1], color=PHYS, lw=1.2, zorder=4)
    ax.text(3, 4.35, "same 'now' everywhere", ha="center", fontsize=9.5, color=PHYS)

    ax = panel(fig, cs[1], 2, "Galilean spacetime", "Galileo 1632", "phys",
               "Uniform motion is relative: a ship's worldlines (blue) are tilted, but everyone shares the same "
               "horizontal slices of simultaneity. Velocities simply add.")
    clean(ax, xlim=(-0.3, 6.3), ylim=(-0.3, 5.4))
    for x0 in range(0, 7):
        ax.plot([x0, x0], [0, 5], color="#cfcac0", lw=1)
    for x0 in np.arange(-4, 7):
        ax.plot([x0, x0 + 0.6 * 5], [0, 5], color="#7fa6d6", lw=1.1)
    for tt in range(6):
        ax.plot([0, 6], [tt, tt], color=PHYS, lw=0.9, alpha=0.6)
    ax.annotate("", xy=(6.2, 0), xytext=(-0.2, 0), arrowprops=dict(arrowstyle="-|>", color=INK))
    ax.annotate("", xy=(0, 5.3), xytext=(0, -0.2), arrowprops=dict(arrowstyle="-|>", color=INK))
    ax.text(6.15, -0.28, "x", fontsize=10)
    ax.text(0.1, 5.15, "t", fontsize=10)
    ax.text(4.9, 4.4, "ship\nworldlines", fontsize=8.5, color=MATH, ha="center")
    ax.text(5.9, 2.15, "shared 'now'", fontsize=8.5, color=PHYS, ha="right")
    ax.set_xlim(-0.3, 6.3)

    ax = panel(fig, cs[2], 3, "Minkowski spacetime", "Einstein 1905 · Minkowski 1908", "phys",
               "With c invariant, a moving frame (β = 0.5) tilts both its time and space axes toward the light cone. "
               "Its 'now' differs from ours. Hyperbolas c²t² − x² = ±1 mark equal intervals in every frame.")
    clean(ax, xlim=(-2.6, 2.6), ylim=(-2.6, 2.6))
    ax.fill_between([-2.6, 0, 2.6], [2.6, 0, 2.6], [2.6, 2.6, 2.6], color="#fff3c4", alpha=0.8)
    ax.fill_between([-2.6, 0, 2.6], [-2.6, 0, -2.6], [-2.6, -2.6, -2.6], color="#fff3c4", alpha=0.8)
    ax.plot([-2.6, 2.6], [-2.6, 2.6], color="#d4a017", lw=1.4)
    ax.plot([-2.6, 2.6], [2.6, -2.6], color="#d4a017", lw=1.4)
    ax.plot([-2.6, 2.6], [0, 0], color=INK, lw=1)
    ax.plot([0, 0], [-2.6, 2.6], color=INK, lw=1)
    b = 0.5
    ax.plot([-2.6 * b, 2.6 * b], [-2.6, 2.6], color=MATH, lw=2)
    ax.plot([-2.6, 2.6], [-2.6 * b, 2.6 * b], color=MATH, lw=2)
    eta = np.linspace(-1.6, 1.6, 200)
    for sg in (1, -1):
        ax.plot(np.sinh(eta), sg * np.cosh(eta), color=PHYS, lw=1, ls="--")
        ax.plot(sg * np.cosh(eta), np.sinh(eta), color=PHYS, lw=1, ls="--")
    g = 1 / np.sqrt(1 - b ** 2)
    ax.plot([g * b], [g], "o", color=MATH, ms=5)
    ax.plot([g], [g * b], "o", color=MATH, ms=5)
    ax.text(0.05, 2.35, "ct", fontsize=10)
    ax.text(2.35, 0.1, "x", fontsize=10)
    ax.text(1.35, 2.3, "ct′", fontsize=10, color=MATH)
    ax.text(2.25, 1.25, "x′", fontsize=10, color=MATH)
    ax.text(-2.4, 2.25, "future\nlight cone", fontsize=8, color="#b7950b")

    ax = panel(fig, cs[3], 4, "Time dilation", "Einstein 1905", "phys",
               "Moving clocks run slow by γ = 1/√(1 − v²/c²). Negligible in daily life (GPS satellites: γ − 1 = "
               "8.3 × 10⁻¹¹, still 7 μs/day), huge for particles: LHC protons γ ≈ 7,000.", plot=True)
    beta = np.linspace(0, 0.995, 500)
    gam = 1 / np.sqrt(1 - beta ** 2)
    ax.plot(beta, gam, color=PHYS, lw=2.4)
    for bb, lab in [(0.5, "β = 0.5\nγ = 1.15"), (0.8, "β = 0.8\nγ = 1.67"), (0.95, "β = 0.95\nγ = 3.20"),
                    (0.99, "β = 0.99\nγ = 7.09")]:
        gg = 1 / np.sqrt(1 - bb ** 2)
        ax.plot(bb, gg, "o", color=INK, ms=5)
        ax.text(bb - 0.03, gg + 0.35, lab, fontsize=8, ha="right")
    vg = 3874.0
    ax.text(0.03, 8.6, f"GPS satellite v = 3.87 km/s:\nγ − 1 = {vg ** 2 / 2 / 299792458.0 ** 2:.2e}"
                       f"  →  {vg ** 2 / 2 / 299792458.0 ** 2 * 86400e6:.1f} μs/day",
            fontsize=8.5, color=MATH, va="top")
    ax.set_xlabel("speed β = v / c")
    ax.set_ylabel("Lorentz factor γ")
    ax.set_ylim(0.8, 10)
    ax.set_xlim(0, 1.0)
    plotstyle(ax)

    ax = panel(fig, cs[4], 5, "The twin 'paradox'", "Langevin 1911", "phys",
               "One twin stays home 10 years; the other flies to a star 4 light-years away at 0.8c and back. Ticks "
               "mark each year of proper time: the traveller ages only 6 years. Time is path-dependent.")
    clean(ax, xlim=(-1.0, 6.2), ylim=(-0.6, 10.8))
    ax.plot([0, 0], [0, 10], color=MATH, lw=2.2)
    ax.plot([0, 4, 0], [0, 5, 10], color=PHYS, lw=2.2)
    for yr in range(11):
        ax.plot([-0.12, 0.12], [yr, yr], color=MATH, lw=1.2)
        if yr % 2 == 0:
            ax.text(-0.25, yr, str(yr), fontsize=8, color=MATH, ha="right", va="center")
    gam = 1 / 0.6
    for yr in range(1, 7):
        tc = yr * gam
        x = 0.8 * tc if tc <= 5 else 4 - 0.8 * (tc - 5)
        ax.plot(x, tc, "o", color=PHYS, ms=5)
        ax.text(x + 0.18, tc, str(yr), fontsize=8, color=PHYS, va="center")
    ax.plot([0, 5.5], [0, 5.5], color="#d4a017", lw=0.8, ls=":")
    ax.text(0.15, 10.3, "home twin: 10 yr", fontsize=9, color=MATH)
    ax.text(3.1, 7.4, "traveller: 6 yr", fontsize=9, color=PHYS)
    ax.text(5.0, -0.4, "x (light-years)", fontsize=8.5, color=MUTED, ha="center")

    ax = panel(fig, cs[5], 6, "Equivalence principle", "Einstein 1907", "phys",
               "'The happiest thought of my life': inside a closed box, uniform acceleration and gravity are "
               "indistinguishable. Light must bend in an accelerating box, so it must bend in gravity too.")
    clean(ax, xlim=(0, 10), ylim=(-0.6, 7))
    for ox, lab in [(0.6, "rocket accelerating at g\n(far from any star)"), (5.6, "box at rest on Earth")]:
        ax.add_patch(Rectangle((ox, 1.4), 3.8, 4.4, fc="#f7f5f0", ec=INK, lw=1.5))
        xs = np.linspace(ox, ox + 3.8, 50)
        ax.plot(xs, 4.6 - 0.11 * (xs - ox) ** 2, color="#d4a017", lw=2)
        ax.add_patch(Circle((ox + 2.6, 2.3), 0.22, fc=PHYS))
        ax.annotate("", xy=(ox + 2.6, 1.7), xytext=(ox + 2.6, 2.05), arrowprops=dict(arrowstyle="-|>", color=PHYS))
        ax.text(ox + 1.9, 6.35, lab, fontsize=8.5, ha="center")
    ax.add_patch(Polygon([[1.5, 1.4], [3.5, 1.4], [2.5, 0.2]], fc="#f39c12", ec="none"))
    ax.add_patch(Rectangle((5.0, 0.8), 5.0, 0.6, fc="#3d8b5a", ec="none"))
    ax.text(5, -0.3, "light beam (yellow) bends the same way in both", ha="center", fontsize=8.8, color="#b7950b")

    ax = panel(fig, cs[6], 7, "Space curved by mass", "Schwarzschild 1916 · Flamm 1916", "phys",
               "Embedding diagram of the spatial geometry outside a black hole: z = 2√(r_s (r − r_s)). Radial "
               "distances are stretched near the horizon r_s — space itself is curved.", projection="3d")
    rs = 1.0
    r = np.linspace(rs, 7 * rs, 60)
    ph = np.linspace(0, 2 * np.pi, 72)
    R, P = np.meshgrid(r, ph)
    Z = 2 * np.sqrt(rs * (R - rs))
    ax.plot_surface(R * np.cos(P), R * np.sin(P), -(Z.max() - Z), cmap="Blues_r", alpha=0.9, linewidth=0.2,
                    edgecolor="#2a5d9f", rstride=3, cstride=3)
    clean3d(ax, elev=28, azim=-60)
    ax.set_box_aspect((1, 1, 0.55), zoom=1.5)

    ax = panel(fig, cs[7], 8, "Light cones tip over", "Eddington 1924 · Finkelstein 1958", "phys",
               "Light-cone directions computed in Eddington–Finkelstein coordinates around a black hole. Far away "
               "they are symmetric; at the horizon r_s the outgoing edge becomes vertical; inside, every future "
               "path leads to r = 0.")
    ax.axvline(1, color=PHYS, lw=1.6, ls="--")
    ax.text(1.04, 1.68, "horizon r = r_s", color=PHYS, fontsize=9)
    ax.plot([0, 0], [0, 6], color=INK, lw=3)
    ax.text(0.05, 1.68, "r = 0", fontsize=9)
    for rr in [0.3, 0.55, 0.8, 1.0, 1.3, 1.75, 2.3, 3.0, 3.7]:
        tt = 0.95
        vin = np.array([-1.0, 1.0]) / np.sqrt(2)
        if abs(rr - 1) < 1e-9:
            vout = np.array([0.0, 1.0])
        else:
            slope = (1 + 1 / rr) / (1 - 1 / rr)
            vout = np.array([1 / slope, 1.0])
            vout /= np.linalg.norm(vout)
        s = 0.5
        ax.add_patch(Polygon([[rr, tt], [rr + s * vin[0], tt + s * vin[1]], [rr + s * vout[0], tt + s * vout[1]]],
                             fc="#fff3c4", ec="#d4a017", lw=1.2))
        ax.plot(rr, tt, "o", color=INK, ms=2.5)
    ax.set_xlim(-0.1, 4.2)
    ax.set_ylim(0.75, 1.85)
    ax.set_aspect("equal")
    ax.set_xlabel("r / r_s")
    ax.set_yticks([])
    ax.text(-0.05, 0.8, "future ↑", rotation=90, fontsize=8, color=MUTED, ha="right")
    plotstyle(ax, grid=False)

    ax = panel(fig, cs[8], 9, "Expanding space", "Friedmann 1922 · Lemaître 1927 · Hubble 1929", "phys",
               "Scale factor a(t) from the Friedmann equations with H₀ = 67.7 km/s/Mpc. Our universe (ΛCDM: "
               "Ωm = 0.31, ΩΛ = 0.69) is 13.8 Gyr old and now accelerating.", plot=True)
    H0 = 67.7 / 977.8
    Om, OL = 0.31, 0.69
    tH = 1 / H0
    t0 = 2 / (3 * np.sqrt(OL)) * np.arcsinh(np.sqrt(OL / Om)) * tH
    tt = np.linspace(0.0, 40, 800)
    a_lcdm = (Om / OL) ** (1 / 3) * np.sinh(1.5 * np.sqrt(OL) * tt / tH) ** (2 / 3)
    ax.plot(tt - t0, a_lcdm, color=PHYS, lw=2.6, label=f"ΛCDM (age {t0:.1f} Gyr)")
    t0e = 2 / 3 * tH
    ax.plot(tt - t0e, (tt / t0e) ** (2 / 3), color=MATH, lw=1.8, label=f"matter only (age {t0e:.1f} Gyr)")
    ax.plot(tt - tH, tt / tH, color="#3d8b5a", lw=1.5, ls="--", label=f"empty (age {tH:.1f} Gyr)")
    Omc = 2.0
    eta = np.linspace(0, 2 * np.pi, 400)
    A = Omc / (2 * (Omc - 1))
    B = Omc / (2 * (Omc - 1) ** 1.5) * tH
    ac = A * (1 - np.cos(eta))
    tc = B * (eta - np.sin(eta))
    et0 = np.arccos(1 - 1 / A)
    ax.plot(tc - B * (et0 - np.sin(et0)), ac, color="#888", lw=1.5, label="closed, Ωm = 2 (recollapses)")
    ax.axvline(0, color=INK, lw=0.8, ls=":")
    ax.text(0.4, 2.8, "today", fontsize=8.5)
    ax.set_xlim(-16, 20)
    ax.set_ylim(0, 3.0)
    ax.set_xlabel("time from today (Gyr)")
    ax.set_ylabel("scale factor a")
    ax.legend(loc="upper left", fontsize=7.8)
    plotstyle(ax)
    footer(fig)
    save(fig, "08-space-and-time.png")


# ---------------------------------------------------------------------------------------------
# 09 Light
# ---------------------------------------------------------------------------------------------
def _refract(d, n, n1, n2):
    d = d / np.linalg.norm(d)
    n = n / np.linalg.norm(n)
    if np.dot(d, n) > 0:
        n = -n
    cosi = -np.dot(d, n)
    eta = n1 / n2
    k = 1 - eta ** 2 * (1 - cosi ** 2)
    if k < 0:
        return None
    return eta * d + (eta * cosi - np.sqrt(k)) * n


def _seg_hit(p, d, a, b):
    M = np.array([d, a - b]).T
    try:
        t, s = np.linalg.solve(M, a - p)
    except np.linalg.LinAlgError:
        return None
    if t > 1e-9 and 0 <= s <= 1:
        return t
    return None


def fig09():
    fig = figure("How the concept of light grew",
                 "Rays, then waves, then electromagnetic fields, then quanta — and finally all of these at once in "
                 "quantum electrodynamics")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Light travels in rays", "Euclid c. 300 BC · Ibn al-Haytham 1021", "phys",
               "Straight rays and the law of reflection (angle in = angle out) explain mirrors and shadows. Ibn "
               "al-Haytham showed by experiment that light enters the eye from objects, not the reverse.")
    clean(ax, xlim=(0, 10), ylim=(-3.2, 5))
    ax.add_patch(Rectangle((0.5, -0.25), 9, 0.25, fc="#b0bec5", ec="none"))
    for k in range(20):
        ax.plot([0.6 + k * 0.45, 0.4 + k * 0.45], [-0.25, -0.55], color="#90a4ae", lw=0.8)
    O, E = np.array([2.0, 3.0]), np.array([8.0, 2.0])
    xr = O[0] + (E[0] - O[0]) * O[1] / (O[1] + E[1])
    ax.plot([O[0], xr, E[0]], [O[1], 0, E[1]], color="#d4a017", lw=2.2)
    ax.plot([xr, E[0]], [0, E[1]], color="#d4a017", lw=2.2)
    ax.plot([O[0], xr], [-O[1], 0], color="#d4a017", lw=1.2, ls="--")
    ax.add_patch(Circle(O, 0.25, fc=PHYS))
    ax.add_patch(Circle((O[0], -O[1]), 0.25, fc=PHYS, alpha=0.3))
    ax.text(O[0] - 0.45, -O[1], "image", fontsize=8.5, ha="right", va="center", color=MUTED)
    ax.text(E[0] + 0.3, E[1], "eye", fontsize=9, va="center")
    ax.plot([xr, xr], [0, 3.2], color=GRID, ls=":")
    ax.add_patch(Arc((xr, 0), 2.2, 2.2, theta1=90, theta2=90 + np.degrees(np.arctan2(xr - O[0], O[1])), color=INK))
    ax.add_patch(Arc((xr, 0), 2.6, 2.6, theta1=90 - np.degrees(np.arctan2(E[0] - xr, E[1])), theta2=90, color=INK))
    ax.text(xr, 4.3, "θ_in = θ_out", ha="center", fontsize=9.5)

    ax = panel(fig, cs[1], 2, "Refraction", "Ptolemy · Snell 1621 · Descartes 1637", "phys",
               "Snell's law n₁ sin θ₁ = n₂ sin θ₂ (computed for water, n = 1.333). Beyond the critical angle "
               "θc = 48.6° light cannot escape: total internal reflection.")
    clean(ax, xlim=(-4.2, 4.2), ylim=(-2.8, 3.4))
    ax.add_patch(Rectangle((-4.2, -2.8), 8.4, 2.8, fc="#d6eaf8", ec="none"))
    ax.plot([-4.2, 4.2], [0, 0], color=MATH, lw=1)
    S = np.array([0.0, -2.0])
    n1, n2 = 1.333, 1.0
    thc = np.degrees(np.arcsin(n2 / n1))
    for th in np.arange(-70, 71, 10):
        d = np.array([np.sin(np.radians(th)), np.cos(np.radians(th))])
        t = -S[1] / d[1]
        P = S + t * d
        out = _refract(d, np.array([0, 1.0]), n1, n2)
        col = wavelength_rgb(450 + abs(th) * 3)
        ax.plot([S[0], P[0]], [S[1], P[1]], color=col, lw=1.4)
        if out is not None:
            ax.plot([P[0], P[0] + out[0] * 3], [P[1], P[1] + out[1] * 3], color=col, lw=1.4)
        else:
            rfl = np.array([d[0], -d[1]])
            ax.plot([P[0], P[0] + rfl[0] * 2], [P[1], P[1] + rfl[1] * 2], color=col, lw=1.4, ls="--")
    ax.add_patch(Circle(S, 0.12, fc=INK, zorder=5))
    ax.text(3.2, -0.5, "water", color=MATH, fontsize=9)
    ax.text(3.2, 0.3, "air", color=MUTED, fontsize=9)
    ax.text(0, -2.6, f"critical angle θc = {thc:.1f}°", ha="center", fontsize=9)

    ax = panel(fig, cs[2], 3, "White light is a mixture", "Newton 1666 / 1704", "phys",
               "A prism separates sunlight into colours, and a second prism cannot split them further. Ray-traced "
               "through a 60° glass prism, n(λ) = 1.5046 + 0.0042/λ² (BK7); dispersion exaggerated 6× for visibility.")
    clean(ax, xlim=(-3.4, 5.2), ylim=(-1.6, 2.6))
    A, B, C = np.array([0, 1.9]), np.array([-1.1, 0]), np.array([1.1, 0])
    ax.add_patch(Polygon([A, B, C], fc="#eef4f8", ec="#78909c", lw=1.5))
    p0 = np.array([-3.4, 0.25])
    d0 = np.array([1.0, 0.33])
    t = _seg_hit(p0, d0, B, A)
    p1 = p0 + t * d0
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="#999", lw=3)
    for wl in np.linspace(400, 700, 25):
        n = 1.5046 + 6 * 0.0042 / (wl / 1000) ** 2 - 5 * 0.0042 / 0.55 ** 2
        nrm1 = np.array([-(A - B)[1], (A - B)[0]])
        d1 = _refract(d0, nrm1, 1.0, n)
        t2 = _seg_hit(p1, d1, A, C)
        p2 = p1 + t2 * d1
        nrm2 = np.array([(C - A)[1], -(C - A)[0]])
        d2 = _refract(d1, nrm2, n, 1.0)
        col = wavelength_rgb(wl)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=col, lw=0.8, alpha=0.7)
        if d2 is not None:
            ax.plot([p2[0], p2[0] + 4 * d2[0]], [p2[1], p2[1] + 4 * d2[1]], color=col, lw=1.6)
    ax.text(-3.2, 0.62, "sunlight", fontsize=9, color=MUTED)

    ax = panel(fig, cs[3], 4, "Light as a wave", "Huygens 1678", "phys",
               "Every point of a wavefront emits secondary wavelets; their envelope is the next wavefront. Passing "
               "through a narrow gap, the wave spreads out (diffraction) — impossible for simple rays.")
    clean(ax, xlim=(0, 10), ylim=(-3.5, 3.5))
    for x in np.arange(0.4, 4.0, 0.7):
        ax.plot([x, x], [-3.3, 3.3], color=MATH, lw=1.2)
    for y in np.linspace(-3, 3, 7):
        ax.add_patch(Arc((3.9, y), 1.4, 1.4, theta1=-90, theta2=90, color="#7fa6d6", lw=0.9))
        ax.plot(3.9, y, "o", color=MATH, ms=3)
    ax.plot([4.6, 4.6], [-3.3, 3.3], color=MATH, lw=1.6, ls="--")
    ax.add_patch(Rectangle((5.6, 0.35), 0.25, 3.15, fc=INK))
    ax.add_patch(Rectangle((5.6, -3.5), 0.25, 3.15, fc=INK))
    for k, r in enumerate(np.arange(0.6, 4.4, 0.7)):
        ax.add_patch(Arc((5.85, 0), 2 * r, 2 * r, theta1=-75, theta2=75, color=MATH, lw=1.2))

    ax = panel(fig, cs[4], 5, "Interference", "Young 1801", "phys",
               "Two slits as coherent sources: the computed wave field (left) adds and cancels, producing bright "
               "and dark fringes on a screen (right: intensity). Waves were decisively back.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.006, ratios=[3.2, 1])
    lam, dsl = 1.0, 5.0
    k = 2 * np.pi / lam
    X, Y = np.meshgrid(np.linspace(0.5, 40, 520), np.linspace(-20, 20, 520))
    r1 = np.hypot(X, Y - dsl / 2)
    r2 = np.hypot(X, Y + dsl / 2)
    field = np.exp(1j * k * r1) / np.sqrt(r1) + np.exp(1j * k * r2) / np.sqrt(r2)
    a1.imshow(field.real, extent=(0.5, 40, -20, 20), origin="lower", cmap="RdBu", vmin=-0.9, vmax=0.9,
              aspect="auto")
    a1.plot([0.5, 0.5], [-20, 20], color=INK, lw=3)
    clean(a1, equal=False)
    yy = np.linspace(-20, 20, 800)
    I = np.abs(np.exp(1j * k * np.hypot(40, yy - dsl / 2)) / np.hypot(40, yy - dsl / 2) ** 0.5 +
               np.exp(1j * k * np.hypot(40, yy + dsl / 2)) / np.hypot(40, yy + dsl / 2) ** 0.5) ** 2
    a2.fill_betweenx(yy, 0, I, color="#f1c40f")
    a2.plot(I, yy, color="#b7950b", lw=0.8)
    a2.set_ylim(-20, 20)
    a2.set_xticks([])
    a2.set_yticks([])
    a2.set_title("screen", fontsize=8.5)

    ax = panel(fig, cs[5], 6, "Light is an electromagnetic wave", "Maxwell 1865 · Hertz 1887", "phys",
               "Maxwell's equations predict self-sustaining waves of electric (E) and magnetic (B) field moving at "
               "c = 1/√(μ₀ε₀) ≈ 3.0 × 10⁸ m/s — exactly the measured speed of light.", projection="3d")
    x = np.linspace(0, 4 * np.pi, 200)
    ax.plot(x, np.sin(x), 0 * x, color=PHYS, lw=2)
    ax.plot(x, 0 * x, np.sin(x), color=MATH, lw=2)
    for xi in x[::8]:
        ax.plot([xi, xi], [0, np.sin(xi)], [0, 0], color=PHYS, lw=0.7, alpha=0.6)
        ax.plot([xi, xi], [0, 0], [0, np.sin(xi)], color=MATH, lw=0.7, alpha=0.6)
    ax.plot([0, 4 * np.pi + 1], [0, 0], [0, 0], color=INK, lw=1)
    ax.text(4 * np.pi + 1.2, 0, 0, "c", fontsize=11)
    ax.text(1.6, 1.2, 0, "E", color=PHYS, fontsize=12, weight="bold")
    ax.text(1.6, 0, 1.3, "B", color=MATH, fontsize=12, weight="bold")
    clean3d(ax, elev=20, azim=-62)
    ax.set_box_aspect((3, 1, 1), zoom=1.3)

    ax = panel(fig, cs[6], 7, "Blackbody radiation and quanta", "Planck 1900", "phys",
               "Classical theory (Rayleigh–Jeans, dashed) predicts infinite ultraviolet energy. Planck's law "
               "B = (2hc²/λ⁵) / (e^{hc/λkT} − 1) fits perfectly if energy comes in packets E = hν.", plot=True)
    h, c, kB = 6.62607e-34, 2.99792458e8, 1.380649e-23
    lam = np.linspace(100, 3000, 600) * 1e-9
    for T, col in [(3000, "#c0392b"), (4000, "#e67e22"), (5000, "#d4a017"), (6000, "#2a5d9f")]:
        B = 2 * h * c ** 2 / lam ** 5 / (np.exp(h * c / (lam * kB * T)) - 1) / 1e12
        ax.plot(lam * 1e9, B, color=col, lw=2, label=f"{T} K")
        lm = 2.8978e-3 / T
        ax.plot(lm * 1e9, (2 * h * c ** 2 / lm ** 5 / (np.exp(h * c / (lm * kB * T)) - 1)) / 1e12, "o", color=col, ms=4)
    RJ = 2 * c * kB * 5000 / lam ** 4 / 1e12
    ax.plot(lam * 1e9, RJ, color="#d4a017", ls="--", lw=1.5, label="classical, 5000 K")
    spec = np.array([[wavelength_rgb(w) for w in np.linspace(380, 750, 200)]])
    ax.imshow(spec, extent=(380, 750, 0, 3), aspect="auto", zorder=0)
    ax.set_xlim(100, 3000)
    ax.set_ylim(0, 90)
    ax.set_xlabel("wavelength (nm)")
    ax.set_ylabel("radiance (kW/sr/m²/nm)")
    ax.legend(loc="upper right", fontsize=8)
    plotstyle(ax)

    ax = panel(fig, cs[7], 8, "Light comes in photons", "Einstein 1905 · Millikan 1916", "phys",
               "Electrons ejected by light have maximum energy K = hν − φ: the slope is Planck's constant for every "
               "metal; below a threshold frequency, no electrons at any brightness. Values computed for three metals.",
               plot=True)
    hev = 4.135667e-15
    nu = np.linspace(0, 16, 300)
    for (metal, phi), col in zip([("caesium", 2.14), ("sodium", 2.28), ("zinc", 4.33)], [PHYS, MATH, "#3d8b5a"]):
        K = hev * nu * 1e14 - phi
        ax.plot(nu[K >= 0], K[K >= 0], color=col, lw=2.2, label=f"{metal}: φ = {phi} eV, ν₀ = {phi / hev / 1e14:.2f}")
    ax.axvspan(4.0, 7.9, color="#fff3c4", zorder=0)
    ax.text(5.95, 4.1, "visible", ha="center", fontsize=8.5, color="#b7950b")
    ax.set_xlabel("frequency ν (10¹⁴ Hz)")
    ax.set_ylabel("max electron energy K (eV)")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 4.5)
    ax.legend(loc="upper left", fontsize=7.8)
    plotstyle(ax)

    ax = panel(fig, cs[8], 9, "Waves made of particles", "Taylor 1909 · QED 1948", "both",
               "Fire photons through two slits one at a time: each lands as a single dot, yet the fringes emerge "
               "statistically. Simulated by sampling the computed intensity for 10 to 20,000 photons.")
    axes = split(fig, ax, 4, "v", gap=0.006)
    rng = np.random.default_rng(7)
    def intensity(y):
        return np.cos(np.pi * 3.0 * y) ** 2 * np.sinc(0.6 * y) ** 2
    for a, N in zip(axes, [10, 200, 2000, 20000]):
        ys = []
        while len(ys) < N:
            y = rng.uniform(-3, 3, 4 * N)
            u = rng.uniform(0, 1, 4 * N)
            ys.extend(y[u < intensity(y)])
        ys = np.array(ys[:N])
        a.set_facecolor("#111")
        a.scatter(ys, rng.uniform(0, 1, N), s=2.5 if N < 1000 else 0.5, color="#f9e79f", lw=0)
        a.set_xlim(-3, 3)
        a.set_ylim(0, 1)
        a.set_xticks([])
        a.set_yticks([])
        a.text(-2.9, 0.5, f"N = {N:,}", color="white", fontsize=8.5, va="center")
    footer(fig)
    save(fig, "09-evolution-of-light.png")


# ---------------------------------------------------------------------------------------------
# 10 Matter
# ---------------------------------------------------------------------------------------------
SYMBOLS = ("H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr "
           "Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W "
           "Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt "
           "Ds Rg Cn Nh Fl Mc Lv Ts Og").split()


def _pt_position(z):
    if z == 1:
        return 1, 1
    if z == 2:
        return 1, 18
    for start, period in [(3, 2), (11, 3)]:
        if start <= z < start + 8:
            i = z - start
            return period, (i + 1 if i < 2 else i + 11)
    if 19 <= z <= 36:
        return 4, z - 18
    if 37 <= z <= 54:
        return 5, z - 36
    for start, period, frow in [(55, 6, 9), (87, 7, 10)]:
        if start <= z < start + 32:
            i = z - start
            if i < 2:
                return period, i + 1
            if i < 17:
                return frow, i + 1
            return period, i - 13
    raise ValueError(z)


def fig10():
    fig = figure("How the concept of matter grew",
                 "From four elements and philosophical atoms to a periodic system, a nuclear atom, quantum orbitals "
                 "and a table of 17 fundamental particles")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Four elements", "Empedocles c. 450 BC · Aristotle", "phys",
               "Everything is a mixture of earth, water, air and fire, each defined by a pair of qualities. "
               "Changing qualities transmutes elements — the basis of alchemy for 2,000 years.")
    clean(ax, xlim=(-2.4, 2.4), ylim=(-2.2, 2.2))
    ax.add_patch(Polygon([[-1.4, -1.4], [1.4, -1.4], [1.4, 1.4], [-1.4, 1.4]], fc="#fbf6ec", ec=MUTED, lw=1))
    ax.add_patch(Polygon([[0, 1.95], [1.95, 0], [0, -1.95], [-1.95, 0]], fc="none", ec=INK, lw=1.2))
    for (x, y, name, col) in [(0, 1.95, "Fire", "#e74c3c"), (1.95, 0, "Air", "#5dade2"), (0, -1.95, "Water", "#2a5d9f"),
                              (-1.95, 0, "Earth", "#8d6e63")]:
        ax.add_patch(Circle((x, y), 0.42, fc=col, ec="white", lw=1.5, zorder=3))
        ax.text(x, y, name, ha="center", va="center", fontsize=9, color="white", weight="bold", zorder=4)
    for (x, y, q) in [(1.4, 1.4, "hot"), (1.4, -1.4, "wet"), (-1.4, -1.4, "cold"), (-1.4, 1.4, "dry")]:
        ax.text(x * 1.12, y * 1.12, q, ha="center", va="center", fontsize=10, style="italic", color=MUTED)

    ax = panel(fig, cs[1], 2, "Atoms and the void", "Leucippus · Democritus c. 420 BC", "phys",
               "Matter is made of indivisible atoms of different shapes moving in empty space; hooked atoms "
               "cling into solids, smooth ones slide as liquids. A purely philosophical idea for 2,200 years.")
    clean(ax, xlim=(0, 10), ylim=(0, 7))
    rng = np.random.default_rng(4)
    for k in range(22):
        cx, cy = rng.uniform(0.6, 9.4), rng.uniform(0.6, 6.4)
        nv = rng.integers(3, 7)
        rr = rng.uniform(0.35, 0.6)
        ang = np.sort(rng.uniform(0, 2 * np.pi, nv))
        pts = np.c_[cx + rr * np.cos(ang), cy + rr * np.sin(ang)]
        ax.add_patch(Polygon(pts, fc=PALETTE[k % 6], ec="none", alpha=0.85))
        if k % 4 == 0:
            ax.plot([cx + rr * 0.8, cx + rr * 1.5, cx + rr * 1.5], [cy, cy, cy + rr * 0.5], color=PALETTE[k % 6], lw=1.5)
        d = rng.normal(0, 1, 2)
        d = d / np.linalg.norm(d) * 0.55
        ax.annotate("", xy=(cx + d[0], cy + d[1]), xytext=(cx + d[0] * 0.55, cy + d[1] * 0.55),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.7))

    ax = panel(fig, cs[2], 3, "Chemical atoms", "Lavoisier 1789 · Dalton 1808", "phys",
               "Elements combine in fixed whole-number ratios: 12 g of carbon takes 16 g or 32 g of oxygen (ratio "
               "1 : 2). Dalton's atoms explain it — though he guessed water was HO, not H₂O.")
    clean(ax, xlim=(0, 18), ylim=(0.4, 6.9))

    def dalton(x, y, kind, r=0.42):
        if kind == "H":
            ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.3))
            ax.add_patch(Circle((x, y), 0.07, fc=INK))
        elif kind == "O":
            ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.3))
        elif kind == "C":
            ax.add_patch(Circle((x, y), r, fc=INK, ec=INK, lw=1.3))
        elif kind == "N":
            ax.add_patch(Circle((x, y), r, fc="white", ec=INK, lw=1.3))
            ax.plot([x, x], [y - r, y + r], color=INK, lw=1.3)

    for k, (sym, name) in enumerate([("H", "hydrogen"), ("O", "oxygen"), ("C", "carbon"), ("N", "nitrogen")]):
        dalton(2.5 + k * 4.3, 6.1, sym)
        ax.text(2.5 + k * 4.3, 5.3, name, ha="center", fontsize=8.5)
    ax.text(0.3, 4.1, "water", fontsize=9.5, va="center")
    dalton(3.6, 4.1, "H"); dalton(4.5, 4.1, "O")
    ax.text(5.2, 4.1, "Dalton: HO ✗", fontsize=8.8, color="#c62828", va="center")
    dalton(11.0, 4.1, "H"); dalton(11.9, 4.1, "O"); dalton(12.8, 4.1, "H")
    ax.text(13.5, 4.1, "H₂O ✓", fontsize=9.5, color="#2e7d32", va="center")
    ax.text(0.3, 2.5, "CO", fontsize=9.5, va="center")
    dalton(3.6, 2.5, "C"); dalton(4.5, 2.5, "O")
    ax.text(5.2, 2.5, "C : O = 12 : 16", fontsize=9.2, va="center", color=MATH)
    ax.text(9.4, 2.5, "CO₂", fontsize=9.5, va="center")
    dalton(11.0, 2.5, "O"); dalton(11.9, 2.5, "C"); dalton(12.8, 2.5, "O")
    ax.text(13.5, 2.5, "12 : 32", fontsize=9.2, va="center", color=MATH)
    ax.text(9, 1.0, "law of multiple proportions: oxygen per 12 g carbon is 16 : 32 = 1 : 2", ha="center",
            fontsize=9.2, color=MATH)

    ax = panel(fig, cs[3], 4, "The periodic system", "Mendeleev 1869", "both",
               "Ordering elements by weight reveals repeating chemical families. Mendeleev left gaps and predicted "
               "the missing elements (★: gallium 1875, scandium 1879, germanium 1886). Blocks = s, p, d, f orbitals.")
    blk_col = {"s": "#e59a7c", "p": "#9bc59d", "d": "#9bb6d8", "f": "#d7bde2"}
    for z, sym in enumerate(SYMBOLS, start=1):
        row, col = _pt_position(z)
        if row >= 9:
            blk = "f"
        elif col <= 2 or z == 2:
            blk = "s"
        elif col >= 13:
            blk = "p"
        else:
            blk = "d"
        y = -row if row < 9 else -row - 0.4
        ax.add_patch(Rectangle((col - 0.47, y - 0.47), 0.94, 0.94, fc=blk_col[blk], ec="white", lw=0.5))
        ax.text(col, y + 0.02, sym, ha="center", va="center", fontsize=5.6)
        if sym in ("Ga", "Sc", "Ge"):
            ax.text(col + 0.33, y + 0.3, "★", fontsize=6, color="#c62828", ha="center", va="center")
    for blk, x in zip("spdf", [2, 5, 8, 11]):
        ax.add_patch(Rectangle((x + 4.2, -0.4), 0.6, 0.6, fc=blk_col[blk]))
        ax.text(x + 5.0, -0.1, blk, fontsize=8.5, va="center")
    clean(ax, xlim=(0.4, 18.6), ylim=(-11.0, 0.5))

    ax = panel(fig, cs[4], 5, "Atoms have parts", "Thomson 1897 / 1904", "phys",
               "Cathode rays are particles 1,800× lighter than hydrogen: electrons, e/m = 1.76 × 10¹¹ C/kg. The atom "
               "becomes a 'plum pudding' — electrons embedded in a diffuse positive sphere.")
    clean(ax, xlim=(-2.2, 2.2), ylim=(-1.8, 1.8))
    ax.add_patch(Circle((0, 0), 1.6, fc="#fadbd8", ec="#e6b0aa", lw=1.5))
    rng = np.random.default_rng(11)
    for k in range(14):
        r, t = 1.35 * np.sqrt(rng.uniform()), rng.uniform(0, 2 * np.pi)
        ax.add_patch(Circle((r * np.cos(t), r * np.sin(t)), 0.13, fc=MATH, ec="white", lw=0.8))
        ax.text(r * np.cos(t), r * np.sin(t), "−", color="white", ha="center", va="center", fontsize=9, weight="bold")
    for k in range(9):
        r, t = 1.4 * np.sqrt(rng.uniform()), rng.uniform(0, 2 * np.pi)
        ax.text(r * np.cos(t), r * np.sin(t), "+", color="#c0392b", ha="center", va="center", fontsize=10)

    ax = panel(fig, cs[5], 6, "The nuclear atom", "Geiger–Marsden 1909 · Rutherford 1911", "phys",
               "Alpha particles fired at gold foil occasionally bounce straight back: 'as if you fired a 15-inch shell "
               "at tissue paper and it came back'. Hyperbolic paths computed for Coulomb repulsion from a tiny nucleus.")
    kq = 0.5
    f = lambda t, s: np.array([s[2], s[3], kq * s[0] / np.hypot(s[0], s[1]) ** 3, kq * s[1] / np.hypot(s[0], s[1]) ** 3])
    t = np.linspace(0, 24, 2400)
    for b in np.r_[-np.arange(0.2, 3.2, 0.32), np.arange(0.2, 3.2, 0.32), [0.02]]:
        sol = rk4(f, np.array([-10.0, b, 1.0, 0.0]), t)
        defl = np.degrees(np.arctan2(sol[-1, 3], sol[-1, 2]))
        col = PHYS if abs(defl) > 60 else MATH
        ax.plot(sol[:, 0], sol[:, 1], color=col, lw=1.0, alpha=0.9)
    ax.add_patch(Circle((0, 0), 0.12, fc="#f1c40f", ec="#b7950b", zorder=5))
    ax.text(0.25, -0.35, "nucleus", fontsize=8.5)
    clean(ax, xlim=(-6, 6), ylim=(-3.6, 3.6))

    ax = panel(fig, cs[6], 7, "Quantized orbits", "Bohr 1913", "both",
               "Electrons occupy only orbits with E_n = −13.6 eV / n². Jumps down emit light of definite colour. "
               "Balmer lines computed from the Rydberg formula: 656, 486, 434, 410 nm — exactly hydrogen's spectrum.",
               plot=True)
    Rh = 1.09678e7
    for n in range(1, 7):
        E = -13.6057 / n ** 2
        ax.plot([0, 10], [E, E], color=INK, lw=1.2)
        if n <= 3:
            ax.text(10.2, E, f"n = {n}", fontsize=8.2, va="center")
    ax.text(10.2, -0.45, "n = 4, 5, 6…", fontsize=7.8, va="center")
    for k, n in enumerate(range(2, 6)):
        ax.annotate("", xy=(0.7 + k * 0.4, -13.6057), xytext=(0.7 + k * 0.4, -13.6057 / n ** 2),
                    arrowprops=dict(arrowstyle="-|>", color="#8e44ad", lw=1.2))
    for k, n in enumerate(range(3, 7)):
        wl = 1e9 / (Rh * (1 / 4 - 1 / n ** 2))
        ax.annotate("", xy=(3.8 + k * 0.9, -13.6057 / 4), xytext=(3.8 + k * 0.9, -13.6057 / n ** 2),
                    arrowprops=dict(arrowstyle="-|>", color=wavelength_rgb(wl), lw=2.2))
        ax.text(3.8 + k * 0.9, -4.1 - (k % 2) * 0.8, f"{wl:.0f}", fontsize=7.8, ha="center", color=INK)
    for k, n in enumerate(range(4, 7)):
        ax.annotate("", xy=(8.0 + k * 0.5, -13.6057 / 9), xytext=(8.0 + k * 0.5, -13.6057 / n ** 2),
                    arrowprops=dict(arrowstyle="-|>", color="#922b21", lw=1.2))
    ax.text(1.3, -12.5, "Lyman\n(UV)", fontsize=8, color="#8e44ad")
    ax.text(5.15, -6.3, "Balmer (visible, nm)", fontsize=8, ha="center")
    ax.text(8.5, -2.2, "Paschen (IR)", fontsize=8, color="#922b21", ha="center")
    ax.set_xlim(0, 11.3)
    ax.set_ylim(-14.5, 0.8)
    ax.set_xticks([])
    ax.set_ylabel("energy (eV)")
    plotstyle(ax, grid=False)

    ax = panel(fig, cs[7], 8, "Quantum orbitals", "Schrödinger 1926 · Born 1926", "both",
               "Electrons are standing waves; |ψ|² gives the probability of finding them. Exact hydrogen densities "
               "in a plane through the nucleus for the 1s, 2p and 3d states (computed from the analytic solutions).")
    axes = split(fig, ax, 3, "h", gap=0.005)
    for a, (name, L, fn) in zip(axes, [
        ("1s", 4.0, lambda r, c: np.exp(-2 * r)),
        ("2p", 13.0, lambda r, c: r ** 2 * np.exp(-r) * c ** 2),
        ("3d", 26.0, lambda r, c: r ** 4 * np.exp(-2 * r / 3) * (3 * c ** 2 - 1) ** 2)]):
        x, z = np.meshgrid(np.linspace(-L, L, 300), np.linspace(-L, L, 300))
        r = np.hypot(x, z) + 1e-9
        d = fn(r, z / r)
        a.imshow(d / d.max(), extent=(-L, L, -L, L), cmap="magma", origin="lower")
        a.text(-0.9 * L, 0.85 * L, name, color="white", fontsize=11, weight="bold", va="center")
        clean(a)

    ax = panel(fig, cs[8], 9, "The Standard Model", "1961 – 1975 · Higgs found 2012", "both",
               "All known matter is built from 6 quarks and 6 leptons in three generations; forces are carried by "
               "gauge bosons, and the Higgs field gives mass. Masses are measured values (PDG).")
    clean(ax, equal=False, xlim=(0, 10.4), ylim=(0, 8.4))
    grid = [
        [("u", "up", "2.2 MeV", "+2/3"), ("c", "charm", "1.27 GeV", "+2/3"), ("t", "top", "173 GeV", "+2/3"),
         ("g", "gluon", "0", "0")],
        [("d", "down", "4.7 MeV", "−1/3"), ("s", "strange", "93 MeV", "−1/3"), ("b", "bottom", "4.18 GeV", "−1/3"),
         ("γ", "photon", "0", "0")],
        [("e", "electron", "0.511 MeV", "−1"), ("μ", "muon", "106 MeV", "−1"), ("τ", "tau", "1.78 GeV", "−1"),
         ("Z", "Z boson", "91.2 GeV", "0")],
        [("νe", "e-neutrino", "< 0.8 eV", "0"), ("νμ", "μ-neutrino", "< 0.8 eV", "0"), ("ντ", "τ-neutrino", "< 0.8 eV", "0"),
         ("W", "W boson", "80.4 GeV", "±1")]]
    for i, row in enumerate(grid):
        for j, (sym, name, m, q) in enumerate(row):
            x0, y0 = 0.15 + j * 2.1, 6.3 - i * 2.0
            fc = "#e8daef" if i < 2 and j < 3 else ("#d5f5e3" if j < 3 else "#fdebd0")
            ax.add_patch(FancyBboxPatch((x0, y0), 1.95, 1.85, boxstyle="round,pad=0,rounding_size=0.15", fc=fc,
                                        ec="#aaa", lw=0.7))
            ax.text(x0 + 0.97, y0 + 1.0, sym, ha="center", va="center", fontsize=15, weight="bold")
            ax.text(x0 + 0.97, y0 + 0.35, name, ha="center", va="center", fontsize=7.3)
            ax.text(x0 + 0.1, y0 + 1.62, m, fontsize=6.6, va="center")
            ax.text(x0 + 1.85, y0 + 1.62, q, fontsize=6.6, va="center", ha="right", color=MUTED)
    ax.add_patch(FancyBboxPatch((8.55, 4.3), 1.75, 1.85, boxstyle="round,pad=0,rounding_size=0.15", fc="#fcf3cf",
                                ec="#aaa", lw=0.7))
    ax.text(9.42, 5.3, "H", ha="center", va="center", fontsize=15, weight="bold")
    ax.text(9.42, 4.65, "Higgs", ha="center", fontsize=7.3)
    ax.text(8.62, 5.93, "125 GeV", fontsize=6.6, va="center")
    for j, lab in enumerate(["I", "II", "III"]):
        ax.text(1.12 + j * 2.1, 8.25, lab, ha="center", fontsize=9, color=MUTED)
    ax.text(9.42, 3.3, "quarks", ha="center", fontsize=8, color="#8e44ad")
    ax.text(9.42, 2.8, "leptons", ha="center", fontsize=8, color="#27ae60")
    ax.text(9.42, 2.3, "gauge bosons", ha="center", fontsize=8, color="#d35400")
    footer(fig)
    save(fig, "10-evolution-of-matter.png")


if __name__ == "__main__":
    for f in (fig06, fig07, fig08, fig09, fig10):
        f()
