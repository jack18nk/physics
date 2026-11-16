"""Figures 16-20: symmetry, dimension, gravity, cognitive tools, learning pathway."""
from math import comb, gamma

import matplotlib.tri as mtri
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

from common import (BOTH, GRID, INK, MATH, MUTED, PALETTE, PHYS, SOFT, arrow, box, cells, clean, clean3d,
                    figure, footer, note, panel, plotstyle, rk4, save, split)

PHI = (1 + 5 ** 0.5) / 2


def _edges_by_distance(V, tol=1e-6):
    d = np.linalg.norm(V[:, None] - V[None], axis=2)
    m = d[d > tol].min()
    return [(i, j) for i in range(len(V)) for j in range(i + 1, len(V)) if abs(d[i, j] - m) < 1e-4]


def _cyc(v):
    a, b, c = v
    return [(a, b, c), (b, c, a), (c, a, b)]


def _platonic():
    tet = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float)
    cube = np.array([(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)], float)
    octa = np.array([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)], float)
    ico = np.array([p for s1 in (-1, 1) for s2 in (-1, 1) for p in _cyc((0, s1, s2 * PHI))], float)
    dod = np.array(list(cube) + [p for s1 in (-1, 1) for s2 in (-1, 1) for p in _cyc((0, s1 / PHI, s2 * PHI))],
                   float)
    return [("tetrahedron", tet), ("cube", cube), ("octahedron", octa), ("dodecahedron", dod),
            ("icosahedron", ico)]


# ---------------------------------------------------------------------------------------------
# 16 Symmetry
# ---------------------------------------------------------------------------------------------
def fig16():
    fig = figure("How the concept of symmetry grew",
                 "From the visible regularity of shapes to invariance under transformations — and finally to the "
                 "principle that symmetries dictate the laws and forces of nature")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Symmetry you can see", "prehistory →", "both",
               "Bilateral symmetry (butterfly curve r = e^{sin θ} − 2cos 4θ + sin⁵((2θ − π)/24)) and six-fold "
               "symmetry of a snowflake — Kepler (1611) asked why snowflakes are hexagonal; the answer is the water "
               "molecule's crystal lattice.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.01)
    th = np.linspace(0, 12 * np.pi, 6000)
    r = np.exp(np.sin(th)) - 2 * np.cos(4 * th) + np.sin((2 * th - np.pi) / 24) ** 5
    a1.plot(r * np.sin(th), r * np.cos(th), color=PHYS, lw=0.7)
    a1.axvline(0, color=MUTED, ls="--", lw=0.8)
    clean(a1, xlim=(-3.4, 3.4), ylim=(-2.5, 3.6))
    for k in range(6):
        ang = np.pi / 2 + k * np.pi / 3
        R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        segs = [((0, 0), (1, 0))]
        for s in (0.35, 0.6, 0.8):
            ln = 0.32 * (1 - s) + 0.08
            segs += [((s, 0), (s + ln * 0.6, ln)), ((s, 0), (s + ln * 0.6, -ln))]
        for p, q in segs:
            P, Q = R @ np.array(p), R @ np.array(q)
            a2.plot([P[0], Q[0]], [P[1], Q[1]], color=MATH, lw=1.8, solid_capstyle="round")
    t6 = np.linspace(0, 2 * np.pi, 7) + np.pi / 6
    a2.plot(0.18 * np.cos(t6), 0.18 * np.sin(t6), color=MATH, lw=1.5)
    clean(a2, xlim=(-1.1, 1.1), ylim=(-1.1, 1.1))

    ax = panel(fig, cs[1], 2, "Only five regular solids", "Theaetetus · Euclid XIII c. 300 BC", "math",
               "Convex solids with identical regular faces and identical corners: exactly five exist, proved in the "
               "last book of Euclid. Plato assigned them to the elements; Kepler (1596) to planetary orbits.")
    axes = split(fig, ax, 5, "h", gap=0.0, projections=["3d"] * 5)
    for k, (a, (name, V)) in enumerate(zip(axes, _platonic())):
        for i, j in _edges_by_distance(V):
            a.plot(*V[[i, j]].T, color=PALETTE[k], lw=1.5)
        a.scatter(*V.T, s=6, color=INK)
        clean3d(a, elev=18, azim=30 + 10 * k)
        lim = np.abs(V).max()
        a.set_xlim(-lim, lim)
        a.set_ylim(-lim, lim)
        a.set_zlim(-lim, lim)
        a.set_box_aspect((1, 1, 1), zoom=1.25)
        a.set_title(name, fontsize=8, y=-0.16)

    ax = panel(fig, cs[2], 3, "Repeating patterns", "Alhambra 14th c. · Fedorov 1891", "math",
               "A motif repeated by translations and 90° rotations (wallpaper group p4). Fedorov and Schoenflies "
               "proved there are exactly 17 wallpaper groups and 230 three-dimensional crystal groups.")
    motif = np.array([[0.05, 0.05], [0.45, 0.08], [0.42, 0.2], [0.2, 0.22], [0.3, 0.42], [0.12, 0.45]])
    cols = ["#2a5d9f", "#c4512c", "#3d8b5a", "#b8860b"]
    for i in range(-1, 6):
        for j in range(-1, 4):
            for k in range(4):
                a = k * np.pi / 2
                R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
                ax.add_patch(Polygon(motif @ R.T + [i, j], fc=cols[k], ec="white", lw=0.6))
            ax.plot(i, j, "o", color=INK, ms=2)
    clean(ax, xlim=(-0.3, 5.3), ylim=(-0.3, 3.3))

    ax = panel(fig, cs[3], 4, "Crystal lattices", "Haüy 1784 · Bravais 1848 · Bragg 1913", "phys",
               "Symmetry inside matter: atoms sit on lattices. Simple, body-centred and face-centred cubic cells "
               "(iron, copper…). X-ray diffraction (1912–13) confirmed the hidden symmetry directly.")
    axes = split(fig, ax, 3, "h", gap=0.0, projections=["3d"] * 3)
    corners = np.array([(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)], float)
    for a, (name, extra) in zip(axes, [("simple cubic", []), ("body-centred", [(0.5, 0.5, 0.5)]),
                                       ("face-centred", [(0.5, 0.5, 0), (0.5, 0.5, 1), (0.5, 0, 0.5), (0.5, 1, 0.5),
                                                         (0, 0.5, 0.5), (1, 0.5, 0.5)])]):
        for i, j in _edges_by_distance(corners):
            a.plot(*corners[[i, j]].T, color=MUTED, lw=1)
        a.scatter(*corners.T, s=90, color=MATH, depthshade=False, edgecolor="white")
        if extra:
            E = np.array(extra, float)
            a.scatter(*E.T, s=90, color=PHYS, depthshade=False, edgecolor="white")
        clean3d(a, elev=18, azim=-55)
        a.set_box_aspect((1, 1, 1), zoom=1.15)
        a.set_title(name, fontsize=8.5, y=-0.05)

    ax = panel(fig, cs[4], 5, "Symmetry ⇔ conservation", "Noether 1918", "both",
               "Emmy Noether's theorem: every continuous symmetry of the laws implies a conserved quantity. "
               "Conservation laws stop being lucky facts and become consequences of symmetry.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    rows = [("laws same at all times", "time translation", "energy"),
            ("laws same at all places", "space translation", "momentum"),
            ("laws same in all directions", "rotation", "angular momentum"),
            ("quantum phase can be shifted", "U(1) phase", "electric charge")]
    for k, (desc, sym, cons) in enumerate(rows):
        y = 8.6 - k * 2.3
        box(ax, 2.3, y, f"{sym}\n{desc}", fc=SOFT["math"], ec=MATH, fs=8.6, pad=0.4, linespacing=1.2)
        arrow(ax, (4.75, y), (6.3, y), color=BOTH, lw=2)
        box(ax, 8.0, y, cons, fc=SOFT["phys"], ec=PHYS, fs=10, pad=0.45, weight="bold")
    ax.text(2.3, 9.85, "symmetry", ha="center", fontsize=9.5, color=MATH, weight="bold")
    ax.text(8.0, 9.85, "conserved", ha="center", fontsize=9.5, color=PHYS, weight="bold")

    ax = panel(fig, cs[5], 6, "Spacetime symmetry", "Lorentz 1904 · Poincaré 1905", "phys",
               "Lorentz boosts are 'rotations' of spacetime that preserve s² = c²t² − x². Boosting an event by "
               "rapidities −1.2 … +1.2 slides it along its hyperbola; light rays are mapped to themselves.")
    eta = np.linspace(-1.8, 1.8, 200)
    for s in (0.5, 1.0, 1.5, 2.0):
        ax.plot(s * np.sinh(eta), s * np.cosh(eta), color=GRID, lw=1)
        ax.plot(s * np.cosh(eta), s * np.sinh(eta), color=GRID, lw=1)
    ax.plot([-3, 3], [-3, 3], color="#d4a017", lw=1.4)
    ax.plot([-3, 3], [3, -3], color="#d4a017", lw=1.4)
    for k, b in enumerate(np.linspace(-1.2, 1.2, 9)):
        ax.plot(np.sinh(b) * 1.5, np.cosh(b) * 1.5, "o", color=PHYS, ms=6)
        ax.plot(np.cosh(b) * 1.0, np.sinh(b) * 1.0, "s", color=MATH, ms=5)
    ax.text(-2.9, 2.7, "● timelike event, boosted", fontsize=8.5, color=PHYS)
    ax.text(-2.9, 2.35, "■ spacelike event, boosted", fontsize=8.5, color=MATH)
    ax.text(2.2, 2.75, "light", fontsize=8.5, color="#b8860b")
    ax.axhline(0, color=INK, lw=0.6)
    ax.axvline(0, color=INK, lw=0.6)
    clean(ax, xlim=(-3, 3), ylim=(-1.6, 3))

    ax = panel(fig, cs[6], 7, "Spontaneous symmetry breaking", "Heisenberg 1928 · Landau 1937", "both",
               "The laws may be symmetric while the state is not. Above the Curie point magnetic spins point every "
               "which way; below it they align along one arbitrary direction, breaking rotational symmetry.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.03)
    rng = np.random.default_rng(9)
    X, Y = np.meshgrid(np.arange(8), np.arange(8))
    th1 = rng.uniform(0, 2 * np.pi, X.shape)
    th2 = 0.6 + rng.normal(0, 0.18, X.shape)
    for a, th, lab, c in [(a1, th1, "hot: symmetric", MUTED), (a2, th2, "cold: ordered", PHYS)]:
        a.quiver(X, Y, np.cos(th), np.sin(th), color=c, pivot="mid", scale=11, width=0.012)
        clean(a, xlim=(-0.8, 7.8), ylim=(-1.6, 7.8))
        a.text(3.5, -1.2, lab, ha="center", fontsize=9)

    ax = panel(fig, cs[7], 8, "Symmetry predicts particles", "Gell-Mann, Ne'eman 1961 · Ω⁻ found 1964", "both",
               "Hadrons fill patterns of the group SU(3). The baryon decuplet had one empty slot; Gell-Mann "
               "predicted its charge, strangeness and mass (≈1680 MeV). The Ω⁻ was found at 1672 MeV.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.02)
    octet = [("n", -0.5, 0), ("p", 0.5, 0), ("Σ⁻", -1, -1), ("Σ⁰ Λ", 0, -1), ("Σ⁺", 1, -1), ("Ξ⁻", -0.5, -2),
             ("Ξ⁰", 0.5, -2)]
    hexagon = np.array([(-0.5, 0), (0.5, 0), (1, -1), (0.5, -2), (-0.5, -2), (-1, -1), (-0.5, 0)])
    a1.plot(hexagon[:, 0], hexagon[:, 1], color=GRID, lw=1.2)
    for lab, x, y in octet:
        a1.add_patch(Circle((x, y), 0.22, fc=MATH, ec="white"))
        a1.text(x, y - 0.42, lab, ha="center", fontsize=8.5)
    a1.set_title("baryon octet", fontsize=9)
    clean(a1, xlim=(-1.7, 1.7), ylim=(-2.8, 0.6))
    dec = [("Δ⁻", -1.5, 0), ("Δ⁰", -0.5, 0), ("Δ⁺", 0.5, 0), ("Δ⁺⁺", 1.5, 0), ("Σ*⁻", -1, -1), ("Σ*⁰", 0, -1),
           ("Σ*⁺", 1, -1), ("Ξ*⁻", -0.5, -2), ("Ξ*⁰", 0.5, -2), ("Ω⁻", 0, -3)]
    tri = np.array([(-1.5, 0), (1.5, 0), (0, -3), (-1.5, 0)])
    a2.plot(tri[:, 0], tri[:, 1], color=GRID, lw=1.2)
    for lab, x, y in dec:
        omega = lab == "Ω⁻"
        a2.add_patch(Circle((x, y), 0.22, fc=PHYS if omega else "#e59a7c", ec="white"))
        a2.text(x + 0.3, y + 0.15, lab, fontsize=8, color=PHYS if omega else INK, weight="bold" if omega else "normal")
    for y, m in zip([0, -1, -2, -3], [1232, 1385, 1533, 1672]):
        a2.text(1.95, y, f"{m} MeV", fontsize=7.5, color=MUTED, va="center")
    a2.set_title("baryon decuplet", fontsize=9)
    clean(a2, xlim=(-1.9, 2.9), ylim=(-3.5, 0.6))

    ax = panel(fig, cs[8], 9, "Forces from symmetry groups", "Glashow, Weinberg, Salam 1967", "both",
               "The Standard Model is built from the group SU(3) × SU(2) × U(1): 8 gluons + 3 W's + 1 B. Electroweak "
               "symmetry breaking rotates (W³, B) by the Weinberg angle θ_W = 28.7° (sin²θ_W = 0.231) into the Z "
               "and the photon.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.02, ratios=[1.1, 1])
    clean(a1, equal=False, xlim=(0, 10), ylim=(0, 10))
    for k, (g, bos, col) in enumerate([("SU(3)", "8 gluons\nstrong", "#3d8b5a"), ("SU(2)", "W¹ W² W³\nweak", PHYS),
                                       ("U(1)", "B\nhypercharge", MATH)]):
        y = 8.2 - k * 3.1
        a1.add_patch(Circle((2.0, y), 1.25, fc=col, alpha=0.2, ec=col, lw=1.5))
        a1.text(2.0, y, g, ha="center", va="center", fontsize=11, weight="bold", color=col)
        a1.text(3.7, y, bos, va="center", fontsize=9)
        if k < 2:
            a1.text(2.0, y - 1.55, "×", ha="center", va="center", fontsize=14, color=MUTED)
    thw = np.arcsin(np.sqrt(0.231))
    for v, lab, c in [((1, 0), "B", MATH), ((0, 1), "W³", PHYS)]:
        a2.annotate("", xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=c, lw=1.6))
        a2.text(v[0] * 1.08, v[1] * 1.08, lab, fontsize=10, color=c)
    g = np.array([np.cos(thw), np.sin(thw)])
    z = np.array([-np.sin(thw), np.cos(thw)])
    for v, lab, c in [(g, "γ", "#d4a017"), (z, "Z", INK)]:
        a2.annotate("", xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=c, lw=2.4))
        a2.text(v[0] * 1.12, v[1] * 1.12, lab, fontsize=12, color=c, weight="bold")
    from matplotlib.patches import Arc
    a2.add_patch(Arc((0, 0), 0.8, 0.8, theta1=0, theta2=np.degrees(thw), color=MUTED))
    a2.text(0.45, 0.1, f"θ_W = {np.degrees(thw):.1f}°", fontsize=8.5)
    clean(a2, xlim=(-0.8, 1.3), ylim=(-0.3, 1.3))
    footer(fig)
    save(fig, "16-evolution-of-symmetry.png")


# ---------------------------------------------------------------------------------------------
# 17 Dimension
# ---------------------------------------------------------------------------------------------
def fig17():
    fig = figure("How the concept of dimension grew",
                 "From the three directions we can point in, to four-dimensional spacetime, n and infinitely many "
                 "dimensions, fractional dimensions, and hidden curled-up ones")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Building up dimensions", "Euclid → Schläfli 1852", "math",
               "Drag a point to get a segment, drag the segment to get a square, the square to get a cube, the cube "
               "to get a tesseract. Each step doubles the vertices: 1, 2, 4, 8, 16.")
    clean(ax, xlim=(-0.3, 12.4), ylim=(-1.4, 3.2))
    ax.plot(0.3, 1, "o", color=INK, ms=7)
    ax.plot([1.5, 3.0], [1, 1], "-o", color=INK, ms=5, lw=2)
    sq = np.array([[4.2, 0.25], [5.7, 0.25], [5.7, 1.75], [4.2, 1.75], [4.2, 0.25]])
    ax.plot(sq[:, 0], sq[:, 1], "-o", color=MATH, ms=4, lw=2)
    o = np.array([0.55, 0.45])
    f = np.array([[7.0, 0.0], [8.4, 0.0], [8.4, 1.4], [7.0, 1.4], [7.0, 0.0]])
    ax.plot(f[:, 0], f[:, 1], "-o", color=PHYS, ms=4, lw=1.8)
    ax.plot(f[:, 0] + o[0], f[:, 1] + o[1], "-o", color=PHYS, ms=4, lw=1.8)
    for p in f[:4]:
        ax.plot([p[0], p[0] + o[0]], [p[1], p[1] + o[1]], color=PHYS, lw=1.8)
    big = np.array([[9.8, -0.1], [11.9, -0.1], [11.9, 2.0], [9.8, 2.0], [9.8, -0.1]])
    sm = np.array([[10.4, 0.5], [11.3, 0.5], [11.3, 1.4], [10.4, 1.4], [10.4, 0.5]])
    ax.plot(big[:, 0], big[:, 1], color=BOTH, lw=1.6)
    ax.plot(sm[:, 0], sm[:, 1], color=BOTH, lw=1.6)
    for p, q in zip(big[:4], sm[:4]):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=BOTH, lw=1.6)
    for x, n, v in [(0.3, "0-D", 1), (2.25, "1-D", 2), (4.95, "2-D", 4), (7.95, "3-D", 8), (10.85, "4-D", 16)]:
        ax.text(x, -0.75, n, ha="center", fontsize=10, weight="bold")
        ax.text(x, -1.2, f"{v} vertices", ha="center", fontsize=8, color=MUTED)

    ax = panel(fig, cs[1], 2, "The tesseract", "Hinton 1880s · Schläfli 1852", "math",
               "A 4-D hypercube projected into 3-D and then onto the page after rotating it in the x–w and y–w "
               "planes (computed). Its 16 vertices and 32 edges are all equivalent; the 'inner cube' is an "
               "illusion of projection. Colour = 4th coordinate w.")
    V = np.array([(x, y, z, w) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1) for w in (-1, 1)], float)

    def rot(i, j, a):
        R = np.eye(4)
        R[i, i] = R[j, j] = np.cos(a)
        R[i, j], R[j, i] = -np.sin(a), np.sin(a)
        return R

    Vr = V @ (rot(0, 3, 0.55) @ rot(1, 3, 0.35) @ rot(0, 2, 0.4)).T
    d4 = 3.2
    P3 = Vr[:, :3] * (d4 / (d4 - Vr[:, 3]))[:, None]
    d3 = 6.0
    P2 = P3[:, :2] * (d3 / (d3 - P3[:, 2]))[:, None]
    import matplotlib.cm as cm
    for i in range(16):
        for j in range(i + 1, 16):
            if np.sum(V[i] != V[j]) == 1:
                wm = (Vr[i, 3] + Vr[j, 3]) / 2
                ax.plot(*P2[[i, j]].T, color=cm.coolwarm((wm + 1.8) / 3.6), lw=1.8)
    ax.scatter(*P2.T, c=Vr[:, 3], cmap="coolwarm", s=30, zorder=5, vmin=-1.8, vmax=1.8)
    clean(ax)

    ax = panel(fig, cs[2], 3, "Flatland", "Abbott 1884", "both",
               "How would 2-D beings see a 3-D sphere passing through their plane? A point appears, grows into a "
               "circle, shrinks, vanishes (radius √(R² − z²)). We would see a 4-D object as a changing 3-D shape.")
    clean(ax, xlim=(-0.5, 13.5), ylim=(-2.4, 3.4))
    zs = np.linspace(-0.98, 0.98, 7)
    for k, z in enumerate(zs):
        r = np.sqrt(1 - z ** 2)
        ax.add_patch(Circle((1 + k * 1.9, 0), r * 0.85, fc=SOFT["math"], ec=MATH, lw=1.5))
        ax.text(1 + k * 1.9, -1.35, f"z = {z:+.1f}", ha="center", fontsize=8)
    ax.plot([-0.3, 13.3], [-1.9, -1.9], color=GRID)
    ax.text(6.7, 2.6, "what Flatlanders see as the sphere passes through", ha="center", fontsize=9, color=MUTED)
    ax.annotate("", xy=(13.2, 1.8), xytext=(0.2, 1.8), arrowprops=dict(arrowstyle="-|>", color=MUTED))
    ax.text(6.7, 1.95, "time", ha="center", fontsize=8.5, color=MUTED)

    ax = panel(fig, cs[3], 4, "Counting faces in n dimensions", "Schläfli 1852 · Euler 1758", "math",
               "Number of k-dimensional faces of an n-cube: C(n, k)·2ⁿ⁻ᵏ. The alternating sum of each row is always "
               "1 — Euler's V − E + F = 2 generalised to every dimension.")
    N = 7
    T = np.full((N, N), np.nan)
    for n in range(N):
        for k in range(n + 1):
            T[n, k] = comb(n, k) * 2 ** (n - k)
    ax.imshow(np.log1p(T), cmap="Blues", vmin=0, vmax=7)
    for n in range(N):
        for k in range(n + 1):
            ax.text(k, n, f"{int(T[n, k])}", ha="center", va="center", fontsize=8.5,
                    color="white" if T[n, k] > 60 else INK)
    ax.xaxis.tick_top()
    ax.set_xticks(range(N))
    ax.set_xticklabels([f"k={k}" for k in range(N)], fontsize=8)
    ax.set_yticks(range(N))
    ax.set_yticklabels([f"{n}-cube" for n in range(N)], fontsize=8)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)

    ax = panel(fig, cs[4], 5, "Spheres in high dimensions", "Schläfli · Riemann", "math",
               "Volume of the unit ball V_n = π^{n/2} / Γ(n/2 + 1) peaks at n = 5 and then falls to zero; the surface "
               "area peaks at n = 7. High-dimensional geometry defies intuition.", plot=True)
    n = np.arange(0, 21)
    Vn = np.array([np.pi ** (k / 2) / gamma(k / 2 + 1) for k in n])
    Sn = np.array([2 * np.pi ** ((k + 1) / 2) / gamma((k + 1) / 2) for k in n])
    ax.plot(n, Vn, "-o", color=MATH, lw=2, ms=4, label="volume of unit n-ball")
    ax.plot(n + 1, Sn, "-s", color=PHYS, lw=2, ms=4, label="surface area (of the n-ball's boundary)")
    ax.annotate(f"max at n = 5: {Vn[5]:.2f}", xy=(5, Vn[5]), xytext=(7, 12), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", color=MATH))
    ax.annotate(f"max at n = 7: {Sn[6]:.2f}", xy=(7, Sn[6]), xytext=(-0.3, 31), fontsize=8.5,
                arrowprops=dict(arrowstyle="-", color=PHYS))
    ax.set_xlabel("dimension n")
    ax.set_xticks(range(0, 21, 2))
    ax.legend(loc="upper right", fontsize=8)
    plotstyle(ax)

    ax = panel(fig, cs[5], 6, "Almost everything is near the surface", "concentration of measure", "math",
               "In n dimensions, the fraction of a ball's volume within 10% of its surface is 1 − 0.9ⁿ; the fraction "
               "of a cube filled by its inscribed ball is V_n / 2ⁿ. Both explain why statistical physics works with "
               "10²³ particles.", plot=True)
    n = np.arange(1, 101)
    ax.plot(n, 1 - 0.9 ** n, color=PHYS, lw=2.4, label="ball volume in outer 10% shell")
    frac = np.array([np.pi ** (k / 2) / gamma(k / 2 + 1) / 2.0 ** k for k in n])
    ax.plot(n, frac, color=MATH, lw=2.4, label="cube volume inside inscribed ball")
    ax.set_xscale("log")
    ax.set_xlabel("dimension n")
    ax.set_ylabel("fraction")
    ax.legend(loc="lower right", fontsize=8, bbox_to_anchor=(1, 0.18))
    plotstyle(ax)

    ax = panel(fig, cs[6], 7, "Infinitely many dimensions", "Fourier 1807 · Hilbert 1906", "both",
               "A function is a vector whose coordinates are its Fourier coefficients. f(x) = x on (−π, π) has "
               "b_n = 2(−1)ⁿ⁺¹/n: infinitely many components (right). Ten of them already rebuild f closely (left).", plot=True)
    a1, a2 = split(fig, ax, 2, "h", gap=0.05, ratios=[1.3, 1])
    x = np.linspace(-np.pi, np.pi, 600)
    a1.plot(x, x, color=INK, lw=1.2, ls="--")
    s = sum(2 * (-1) ** (k + 1) / k * np.sin(k * x) for k in range(1, 11))
    a1.plot(x, s, color=BOTH, lw=2)
    for k in range(1, 4):
        a1.plot(x, 2 * (-1) ** (k + 1) / k * np.sin(k * x), lw=0.9, color=PALETTE[k - 1], alpha=0.8)
    a1.set_xticks([-np.pi, 0, np.pi])
    a1.set_xticklabels(["−π", "0", "π"])
    a1.set_yticks([])
    plotstyle(a1, grid=False)
    k = np.arange(1, 16)
    a2.bar(k, 2 * (-1) ** (k + 1) / k, color=[BOTH if v > 0 else "#b9a6d6" for v in (-1) ** (k + 1)])
    a2.axhline(0, color=INK, lw=0.8)
    a2.set_xlabel("n", fontsize=9)
    a2.set_title("coordinates b_n", fontsize=9)
    plotstyle(a2, grid=False)

    ax = panel(fig, cs[7], 8, "Curled-up extra dimensions", "Kaluza 1921 · Klein 1926 · strings 1984", "both",
               "A garden hose looks 1-D from afar, 2-D up close. Extra dimensions might be curled up too small to see. "
               "Dimensions of spacetime in various theories (speculative ones hatched):", plot=True)
    theories = [("Newtonian (space only)", 3, False), ("relativity", 4, False), ("Kaluza–Klein", 5, True),
                ("superstrings", 10, True), ("M-theory", 11, True), ("bosonic string", 26, True)]
    for k, (name, d, spec) in enumerate(theories):
        ax.barh(k, d, color=PHYS if not spec else "white", ec=PHYS, hatch="///" if spec else None, lw=1.2)
        ax.text(d + 0.4, k, str(d), va="center", fontsize=9)
    ax.set_yticks(range(len(theories)))
    ax.set_yticklabels([t[0] for t in theories], fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlabel("number of dimensions")
    ax.set_xlim(0, 29)
    plotstyle(ax)

    ax = panel(fig, cs[8], 9, "Fractional dimensions", "Hausdorff 1918 · Mandelbrot 1975", "math",
               "Self-similar shapes have non-integer dimension D = log N / log s. Koch snowflake (4 copies at 1/3 "
               "scale): D = log 4 / log 3 = 1.262. Sierpiński triangle (3 copies at 1/2): D = 1.585. Coastlines, "
               "clouds and turbulence are fractal.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.01)

    def koch(p, q, n):
        if n == 0:
            return [p]
        p, q = np.array(p), np.array(q)
        d = (q - p) / 3
        r = np.array([[0.5, -np.sqrt(3) / 2], [np.sqrt(3) / 2, 0.5]])
        a, b = p + d, p + 2 * d
        c = a + r @ d
        return koch(p, a, n - 1) + koch(a, c, n - 1) + koch(c, b, n - 1) + koch(b, q, n - 1)

    T = [np.array([0, 0]), np.array([1, 0]), np.array([0.5, np.sqrt(3) / 2])]
    pts = koch(T[0], T[2], 4) + koch(T[2], T[1], 4) + koch(T[1], T[0], 4) + [T[0]]
    pts = np.array(pts)
    a1.fill(pts[:, 0], pts[:, 1], color=SOFT["math"], ec=MATH, lw=0.6)
    a1.text(0.5, -0.42, "D = 1.262", ha="center", fontsize=9)
    clean(a1, xlim=(-0.15, 1.15), ylim=(-0.55, 1.1))
    rng = np.random.default_rng(0)
    V = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2]])
    p = np.array([0.3, 0.3])
    out = []
    for i in range(30000):
        p = (p + V[rng.integers(3)]) / 2
        out.append(p)
    out = np.array(out[20:])
    a2.scatter(out[:, 0], out[:, 1], s=0.1, color=PHYS, lw=0)
    a2.text(0.5, -0.12, "D = 1.585", ha="center", fontsize=9)
    clean(a2, xlim=(-0.05, 1.05), ylim=(-0.25, 0.92))
    footer(fig)
    save(fig, "17-evolution-of-dimension.png")


# ---------------------------------------------------------------------------------------------
# 18 Gravity
# ---------------------------------------------------------------------------------------------
def fig18():
    fig = figure("How the concept of gravity grew",
                 "Heaviness, then a universal force, then a potential landscape, then the curvature of spacetime "
                 "itself — each step confirmed by ever finer measurements")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Heavier falls faster?", "Aristotle · Galileo's thought experiment 1638", "phys",
               "If heavy stones fell faster, tie a light stone to a heavy one: the light one should slow the pair, yet "
               "the pair is heavier and should be faster. Contradiction — all bodies must fall alike.")
    clean(ax, xlim=(0, 10), ylim=(0, 7))
    ax.add_patch(Circle((1.6, 5.4), 0.7, fc="#566573"))
    ax.add_patch(Circle((3.5, 5.6), 0.35, fc="#aab7b8"))
    arrow(ax, (1.6, 4.5), (1.6, 2.2), color=PHYS, lw=3)
    arrow(ax, (3.5, 5.1), (3.5, 3.8), color=PHYS, lw=2)
    ax.text(1.6, 1.6, "fast?", ha="center", fontsize=9)
    ax.text(3.5, 3.2, "slow?", ha="center", fontsize=9)
    ax.add_patch(Circle((7.0, 5.4), 0.7, fc="#566573"))
    ax.add_patch(Circle((7.0, 3.9), 0.35, fc="#aab7b8"))
    ax.plot([7.0, 7.0], [4.7, 4.25], color=INK, lw=2)
    ax.text(8.0, 5.0, "slower (dragged)?\nor faster (heavier)?", fontsize=9, color=PHYS, va="center")
    ax.text(5, 0.6, "⇒ all bodies fall at the same rate", ha="center", fontsize=10, color=MATH, weight="bold")

    ax = panel(fig, cs[1], 2, "Universal free fall", "Galileo 1604 · Apollo 15 1971 · MICROSCOPE 2022", "phys",
               "Stroboscopic positions every 0.05 s from y = ½gt² for a heavy and a light ball: identical. On the Moon "
               "a hammer and a feather landed together; satellite tests confirm equality to 1 part in 10¹⁵.")
    t = np.arange(0, 0.55, 0.05)
    y = 0.5 * 9.81 * t ** 2
    for x, r, c in [(1, 0.06, "#566573"), (2, 0.03, "#aab7b8")]:
        for yy in y:
            ax.add_patch(Circle((x, -yy), r * 1.4, fc=c, ec="none"))
    for k, (tt, yy) in enumerate(zip(t, y)):
        if k % 2 == 0 and k >= 2:
            ax.plot([2.3, 2.5], [-yy, -yy], color=GRID)
            ax.text(2.6, -yy, f"{tt:.1f} s  {yy:.2f} m", fontsize=7.8, va="center")
    clean(ax, xlim=(0.3, 4.2), ylim=(-1.5, 0.15))

    ax = panel(fig, cs[2], 3, "The Moon test", "Newton 1666 / 1687", "phys",
               "Is the Moon falling like an apple? If gravity weakens as 1/r², at 60 Earth radii it should be "
               "g/60². Computed from the Moon's orbit:")
    clean(ax, xlim=(0, 10), ylim=(0, 4.6))
    ax.add_patch(Circle((1.4, 3.3), 0.8, fc="#5dade2", ec="#2471a3"))
    ax.add_patch(Circle((8.8, 3.3), 0.22, fc="#bfc9ca", ec="#7f8c8d"))
    ax.plot([2.2, 8.58], [3.3, 3.3], color=MUTED, ls=":", lw=1)
    ax.text(5.4, 3.5, "r = 60 R_E = 384,400 km", ha="center", fontsize=8.5, color=MUTED)
    ax.add_patch(Circle((1.4, 4.3), 0.12, fc="#c0392b"))
    r, T = 3.844e8, 27.32 * 86400
    am = 4 * np.pi ** 2 * r / T ** 2
    ax.text(5, 2.0, f"Moon: a = 4π²r / T² = {am:.5f} m/s²", ha="center", fontsize=10, color=PHYS)
    ax.text(5, 1.3, f"apple: g / 60² = 9.81 / 3600 = {9.81 / 3600:.5f} m/s²", ha="center", fontsize=10,
            color=MATH)
    ax.text(5, 0.5, "the same force reaches the Moon", ha="center", fontsize=9.5, weight="bold")

    ax = panel(fig, cs[3], 4, "Potential landscapes", "Euler 1767 · Lagrange 1772", "both",
               "Effective potential of the Earth–Moon system in the rotating frame (mass ratio μ = 0.0121). Five "
               "equilibrium points L1–L5, located numerically; JWST orbits near Sun–Earth L2.", plot=True)
    mu = 0.01215
    X, Y = np.meshgrid(np.linspace(-1.5, 1.5, 600), np.linspace(-1.3, 1.3, 520))
    r1 = np.hypot(X + mu, Y)
    r2 = np.hypot(X - 1 + mu, Y)
    Phi = -(1 - mu) / r1 - mu / r2 - 0.5 * (X ** 2 + Y ** 2)

    def dphi(x):
        return x - (1 - mu) * (x + mu) / abs(x + mu) ** 3 - mu * (x - 1 + mu) / abs(x - 1 + mu) ** 3

    def bisect(a, b):
        for _ in range(80):
            m = (a + b) / 2
            if np.sign(dphi(m)) == np.sign(dphi(a)):
                a = m
            else:
                b = m
        return (a + b) / 2

    L1 = bisect(0.5, 1 - mu - 1e-3)
    L2 = bisect(1 - mu + 1e-3, 1.5)
    L3 = bisect(-1.5, -mu - 1e-3)
    Ls = [(L1, 0), (L2, 0), (L3, 0), (0.5 - mu, np.sqrt(3) / 2), (0.5 - mu, -np.sqrt(3) / 2)]
    phiL = lambda x, y: -(1 - mu) / np.hypot(x + mu, y) - mu / np.hypot(x - 1 + mu, y) - 0.5 * (x * x + y * y)
    lev = sorted({round(phiL(*p), 5) for p in Ls})
    ax.contourf(X, Y, np.clip(Phi, -2.2, -1.4), levels=40, cmap="cividis")
    ax.contour(X, Y, Phi, levels=lev, colors="white", linewidths=0.9)
    for k, (x, y) in enumerate(Ls):
        ax.plot(x, y, "x", color=PHYS, ms=8, mew=2)
        ax.text(x + 0.05, y + 0.07, f"L{k + 1}", color="white", fontsize=9, weight="bold")
    ax.plot(-mu, 0, "o", color="#5dade2", ms=9)
    ax.plot(1 - mu, 0, "o", color="#d5d8dc", ms=5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

    ax = panel(fig, cs[4], 5, "Mercury's extra precession", "Le Verrier 1859 · Einstein 1915", "phys",
               "Mercury's orbit turns 574″ per century; planets explain 531″. General relativity adds exactly the "
               "missing 43″. Orbit integrated with the relativistic correction (exaggerated ~10⁶× to be visible).")
    alpha = 0.012
    f = lambda t, s: (lambda r: np.array([s[2], s[3], -s[0] / r ** 3 * (1 + 3 * alpha / r ** 2),
                                          -s[1] / r ** 3 * (1 + 3 * alpha / r ** 2)]))(np.hypot(s[0], s[1]))
    e = 0.45
    rp = 1 - e
    vp = np.sqrt((1 + e) / (1 - e))
    t = np.linspace(0, 70, 14000)
    sol = rk4(f, np.array([rp, 0, 0, vp]), t)
    ax.plot(sol[:, 0], sol[:, 1], color=PHYS, lw=0.6)
    rr = np.hypot(sol[:, 0], sol[:, 1])
    peri = [i for i in range(1, len(rr) - 1) if rr[i] < rr[i - 1] and rr[i] < rr[i + 1]]
    for i in peri:
        ax.plot([0, sol[i, 0]], [0, sol[i, 1]], color=MATH, lw=0.8)
        ax.plot(*sol[i, :2], "o", color=MATH, ms=3)
    ax.plot(0, 0, "o", color="#f1c40f", ms=11, mec="#b7950b")
    clean(ax)

    ax = panel(fig, cs[5], 6, "Light bends", "Soldner 1801 · Einstein 1915 · Eddington 1919", "phys",
               "Starlight grazing the Sun is deflected. Newtonian reasoning gives 0.87″, general relativity 1.75″. "
               "The 1919 eclipse expeditions measured 1.98″ ± 0.16 (Sobral) and 1.61″ ± 0.40 (Príncipe).", plot=True)
    a1, a2 = split(fig, ax, 2, "h", gap=0.05, ratios=[1.2, 1])
    clean(a1, xlim=(0, 10), ylim=(-1, 5.5))
    a1.add_patch(Circle((5, 1.2), 1.0, fc="#f9e79f", ec="#d4ac0d"))
    a1.plot([0.3, 5, 9.6], [1.9, 2.3, 1.2], color="#d4a017", lw=1.8)
    a1.plot([5, 0.3], [2.3, 3.42], color="#d4a017", lw=1, ls="--")
    a1.plot(9.6, 1.2, "o", color="#2471a3", ms=6)
    a1.plot(0.3, 1.9, "*", color=INK, ms=11)
    a1.plot(0.3, 3.42, "*", color=MUTED, ms=11, alpha=0.6)
    a1.text(0.6, 3.75, "apparent", fontsize=8, color=MUTED)
    a1.text(0.6, 1.4, "true", fontsize=8)
    a1.text(9.6, 0.6, "Earth", fontsize=8.5, ha="center")
    a1.text(5, -0.4, "Sun", fontsize=8.5, ha="center")
    vals = [("Newtonian", 0.87, 0, MATH), ("Einstein", 1.75, 0, PHYS), ("Sobral 1919", 1.98, 0.16, INK),
            ("Príncipe 1919", 1.61, 0.40, INK)]
    for k, (lab, v, err, c) in enumerate(vals):
        if err:
            a2.errorbar(v, k, xerr=err, fmt="o", color=c, capsize=3)
        else:
            a2.barh(k, v, color=c, alpha=0.8, height=0.55)
    a2.set_yticks(range(4))
    a2.set_yticklabels([v[0] for v in vals], fontsize=8)
    a2.invert_yaxis()
    a2.set_xlabel("deflection (″)", fontsize=8.5)
    a2.set_xlim(0, 2.6)
    a2.axvline(1.75, color=PHYS, lw=0.8, ls=":")
    plotstyle(a2)

    ax = panel(fig, cs[6], 7, "Gravity slows time", "Einstein 1907 · Pound–Rebka 1959 · GPS", "phys",
               "Clocks run faster higher in a gravitational field. For GPS satellites (computed): relativity of "
               "motion −7.2 μs/day, gravitational blueshift +45.7 μs/day, net +38.5 μs/day — uncorrected, positions "
               "would drift ~11 km per day.", plot=True)
    GM, c, RE, rs = 3.986004e14, 299792458.0, 6.371e6, 2.6561e7
    v = np.sqrt(GM / rs)
    sr = -v ** 2 / (2 * c ** 2) * 86400e6
    gr = GM / c ** 2 * (1 / RE - 1 / rs) * 86400e6
    labels = ["speed (special rel.)", "gravity (general rel.)", "net"]
    vals = [sr, gr, sr + gr]
    ax.bar(labels, vals, color=[MATH, PHYS, BOTH])
    for k, v_ in enumerate(vals):
        ax.text(k, v_ + (2 if v_ > 0 else -6), f"{v_:+.1f} μs/day", ha="center", fontsize=9)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_ylabel("satellite clock gain per day (μs)")
    ax.set_ylim(-15, 55)
    ax.tick_params(axis="x", labelsize=8)
    plotstyle(ax)

    ax = panel(fig, cs[7], 8, "Gravitational waves", "Einstein 1916 · Hulse–Taylor 1974 · LIGO 2015", "phys",
               "Merging black holes shake spacetime. Leading-order 'chirp' for chirp mass 30 M☉ (computed: frequency "
               "f ∝ τ^{−3/8} sweeps up to ~150 Hz before merger) plus ring-down; below, a ring of free masses "
               "stretched and squeezed by a passing wave.")
    a1, a2 = split(fig, ax, 2, "v", gap=0.035, ratios=[1.6, 1])
    Tm = 30 * 4.925491e-6
    tau = np.geomspace(0.35, 0.0035, 6000)
    fgw = (1 / np.pi) * (5 / (256 * tau)) ** 0.375 * Tm ** -0.625
    Ph = -2 * (tau / (5 * Tm)) ** 0.625
    h = (fgw / fgw[-1]) ** (2 / 3) * np.cos(Ph)
    tt = -tau
    tr = np.linspace(0, 0.03, 600)
    hr = np.cos(Ph[-1] + 2 * np.pi * 250 * tr) * np.exp(-tr / 0.004)
    a1.plot(tt, h, color=PHYS, lw=0.8)
    a1.plot(tr, hr, color=PHYS, lw=0.8)
    a1.set_xlim(-0.3, 0.03)
    a1.set_yticks([])
    a1.text(-0.295, 1.05, "time relative to merger (s)", fontsize=8, color=MUTED)
    a1.tick_params(labelsize=7.5)
    plotstyle(a1, grid=False)
    th = np.linspace(0, 2 * np.pi, 16, endpoint=False)
    for k, ph in enumerate(np.linspace(0, 1.5 * np.pi, 4)):
        hh = 0.35 * np.cos(ph)
        cx = k * 3.0
        a2.scatter(cx + np.cos(th) * (1 + hh), np.sin(th) * (1 - hh), s=8, color=MATH)
        a2.add_patch(Circle((cx, 0), 1, fc="none", ec=GRID, lw=0.6))
    clean(a2, xlim=(-1.6, 10.6), ylim=(-1.5, 1.5))

    ax = panel(fig, cs[8], 9, "Black holes trap light", "Schwarzschild 1916 · EHT image 2019", "phys",
               "Light rays from the left with different impact parameters b, integrated with the exact Schwarzschild "
               "orbit equation u″ = −u + 3Mu². Rays with b < 3√3 M ≈ 5.2 M are captured; the photon sphere at "
               "r = 3M (dashed) shapes the black-hole 'shadow'.")
    M = 1.0
    for b in np.r_[np.linspace(1.0, 5.1, 9), [5.196], np.linspace(5.3, 9, 8)]:
        phi = np.linspace(1e-4, 3.5 * np.pi, 8000)
        u = np.zeros_like(phi)
        du = np.zeros_like(phi)
        u[0], du[0] = phi[0] / b, 1 / b
        end = len(phi)
        for i in range(len(phi) - 1):
            h_ = phi[i + 1] - phi[i]
            def F(y):
                return np.array([y[1], -y[0] + 3 * M * y[0] ** 2])
            y = np.array([u[i], du[i]])
            k1 = F(y); k2 = F(y + h_ / 2 * k1); k3 = F(y + h_ / 2 * k2); k4 = F(y + h_ * k3)
            y = y + h_ / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            u[i + 1], du[i + 1] = y
            if y[0] > 0.5 or y[0] < 0:
                end = i + 1
                break
        r = 1 / np.clip(u[:end], 1e-6, None)
        x, yv = -r * np.cos(phi[:end]), r * np.sin(phi[:end])
        captured = u[end - 1] > 0.45
        ax.plot(x, yv, color=PHYS if captured else MATH, lw=1.0)
    ax.add_patch(Circle((0, 0), 2 * M, fc=INK))
    ax.add_patch(Circle((0, 0), 3 * M, fc="none", ec="#d4a017", ls="--", lw=1.2))
    clean(ax, xlim=(-14, 12), ylim=(-6, 10))
    footer(fig)
    save(fig, "18-evolution-of-gravity.png")


# ---------------------------------------------------------------------------------------------
# 19 Tools that extend cognition
# ---------------------------------------------------------------------------------------------
def _four_colour(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    col = [-1] * n
    order = sorted(range(n), key=lambda v: -len(adj[v]))

    def solve(i):
        if i == n:
            return True
        v = order[i]
        used = {col[u] for u in adj[v]}
        for c in range(4):
            if c not in used:
                col[v] = c
                if solve(i + 1):
                    return True
        col[v] = -1
        return False

    solve(0)
    return col


def fig19():
    fig = figure("Tools that extend thinking",
                 "Mathematical and physical cognition are not only in the head: notations, instruments and machines "
                 "let us think thoughts no unaided brain could hold")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Notation shapes number", "c. 3000 BC → today", "math",
               "The year 2026 in six systems. Positional notation with zero (Babylonian, Maya, Hindu-Arabic, binary) "
               "makes arithmetic mechanical; Roman numerals make it hard.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    rows = [("Roman", "MMXXVI"), ("Chinese", "二千零二十六"), ("Babylonian (base 60)", "33 ; 46"),
            ("Hindu-Arabic (base 10)", "2026"), ("binary (base 2)", "11111101010")]
    for k, (name, val) in enumerate(rows):
        y = 9.0 - k * 1.85
        ax.text(0.3, y, name, fontsize=9, color=MUTED, va="center")
        ax.text(3.9, y, val, fontsize=13, va="center", weight="bold", color=MATH if k >= 3 else INK)
    ax.text(8.4, 9.5, "Maya (base 20)", fontsize=8.5, ha="center", color=MUTED)
    for j, d in enumerate([5, 1, 6]):
        y = 7.6 - j * 2.2
        bars, dots = d // 5, d % 5
        for b in range(bars):
            ax.add_patch(Rectangle((7.7, y - 0.55 - b * 0.4), 1.4, 0.26, fc="#8d6e63"))
        for dd in range(dots):
            ax.add_patch(Circle((8.4 - (dots - 1) * 0.2 + dd * 0.4, y + 0.05), 0.13, fc="#8d6e63"))
        ax.text(9.5, y - 0.3, ["×400", "×20", "×1"][j], fontsize=7.5, color=MUTED, va="center")

    ax = panel(fig, cs[1], 2, "The abacus", "Salamis tablet c. 300 BC · suanpan c. 1200", "math",
               "Beads make place value physical: each upper bead is 5, each lower bead 1. Shown: 3 1 4 1 5 9. "
               "Skilled users visualise a 'mental abacus' and calculate faster than with a calculator.")
    clean(ax, xlim=(-0.5, 7.5), ylim=(-1.1, 7.4))
    ax.add_patch(Rectangle((-0.2, 0), 7.4, 7, fc="none", ec="#6d4c41", lw=4))
    ax.plot([-0.2, 7.2], [5.0, 5.0], color="#6d4c41", lw=3)
    for k, dgt in enumerate([3, 1, 4, 1, 5, 9]):
        x = 0.6 + k * 1.2
        ax.plot([x, x], [0, 7], color="#a1887f", lw=1.5)
        up = dgt // 5
        lo = dgt % 5
        for j in range(2):
            y = 5.12 + j * 0.55 if j < up else 6.45 - (1 - j) * 0.55
            ax.add_patch(Rectangle((x - 0.42, y), 0.84, 0.45, fc="#c0392b", ec="#7b241c"))
        for j in range(5):
            y = 4.43 - j * 0.5 if j < lo else 0.1 + (4 - j) * 0.5
            ax.add_patch(Rectangle((x - 0.42, y), 0.84, 0.45, fc="#e59866", ec="#a04000"))
        ax.text(x, -0.6, str(dgt), ha="center", fontsize=11, weight="bold", color=MATH)

    ax = panel(fig, cs[2], 3, "Logarithms and the slide rule", "Napier 1614 · Oughtred 1622", "both",
               "log(ab) = log a + log b turns multiplication into adding lengths. Slide the C scale so its 1 sits "
               "over 2 on D; under 3 on C read 6 on D. Engineers computed with slide rules until the 1970s.")
    clean(ax, equal=False, xlim=(-0.5, 10.5), ylim=(-0.5, 5))
    L = 9.0
    ax.add_patch(Rectangle((0, 0.4), L + 0.4, 1.4, fc="#fdf2e9", ec=INK))
    off = np.log10(2) * L
    ax.add_patch(Rectangle((off, 1.8), L, 1.4, fc="#eaf2f8", ec=INK))
    for v in np.arange(1, 10.01, 0.5):
        x = np.log10(v) * L
        big = abs(v - round(v)) < 1e-9
        ax.plot([x + 0.2, x + 0.2], [1.8, 1.8 - (0.35 if big else 0.18)], color=INK, lw=0.9)
        if big:
            ax.text(x + 0.2, 1.25, f"{int(v)}", ha="center", fontsize=8)
        xc = off + np.log10(v) * L
        if xc < 10.4:
            ax.plot([xc + 0.2, xc + 0.2], [1.8, 1.8 + (0.35 if big else 0.18)], color=INK, lw=0.9)
            if big:
                ax.text(xc + 0.2, 2.35, f"{int(v)}", ha="center", fontsize=8)
    for x0, col in [(off + 0.2, PHYS), (off + np.log10(3) * L + 0.2, PHYS)]:
        ax.plot([x0, x0], [0.4, 3.2], color=col, lw=1.4)
    ax.text(-0.45, 1.1, "D", fontsize=10, weight="bold", va="center")
    ax.text(off - 0.3, 2.5, "C", fontsize=10, weight="bold", va="center")
    ax.text(5, 4.2, "2 × 3: read 6 under the C-scale 3", ha="center", fontsize=9.5, color=PHYS)

    ax = panel(fig, cs[3], 4, "Calculating machines", "Pascal 1642 · Leibniz 1673 · Babbage 1822", "math",
               "Babbage's Difference Engine tabulates polynomials using only addition: for f(n) = n² + n + 41 "
               "(Euler's prime-generating polynomial) the second difference is always 2.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    n = np.arange(0, 8)
    fn = n ** 2 + n + 41
    d1 = np.diff(fn)
    d2 = np.diff(d1)
    heads = ["n", "f(n)", "Δ¹", "Δ²"]
    for j, hd in enumerate(heads):
        ax.text(1.2 + j * 2.4, 9.3, hd, ha="center", fontsize=10, weight="bold", color=MATH)
    for i in range(8):
        y = 8.3 - i * 1.0
        ax.text(1.2, y, str(n[i]), ha="center", fontsize=9.5)
        ax.text(3.6, y, str(fn[i]), ha="center", fontsize=9.5)
        if i < 7:
            ax.text(6.0, y - 0.5, str(d1[i]), ha="center", fontsize=9.5, color=PHYS)
        if i < 6:
            ax.text(8.4, y - 1.0, str(d2[i]), ha="center", fontsize=9.5, color="#3d8b5a", weight="bold")
    ax.plot([0.3, 9.7], [8.85, 8.85], color=GRID)

    ax = panel(fig, cs[4], 5, "Graphs make laws visible", "Oresme c. 1350 · Merton College 1330s", "both",
               "Oresme drew speed against time: for uniform acceleration the distance is the triangle's area, equal "
               "to the rectangle at the mean speed — the mean-speed theorem, 250 years before Galileo.", plot=True)
    t = np.array([0, 1])
    ax.fill_between(t, [0, 0], [0, 2], color="#f5b7a5", alpha=0.8, label="uniformly accelerated")
    ax.fill_between(t, [0, 0], [1, 1], color="none", ec=MATH, hatch="///", lw=1.2, label="uniform at mean speed")
    ax.plot([0, 1], [0, 2], color=PHYS, lw=2)
    ax.plot([0, 1], [1, 1], color=MATH, lw=2, ls="--")
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 2.3)
    ax.set_xlabel("time")
    ax.set_ylabel("speed")
    ax.set_xticks([])
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(["0", "v/2", "v"])
    ax.legend(loc="upper left", fontsize=8)
    plotstyle(ax, grid=False)

    ax = panel(fig, cs[5], 6, "Numerical methods", "Euler 1768 · Runge 1895 · Kutta 1901", "both",
               "Computers solve equations step by step. A circular orbit integrated for 5 periods with the same "
               "time step (0.05): Euler's method spirals outward, gaining energy; 4th-order Runge–Kutta stays on the "
               "circle.")
    f = lambda t, s: np.array([s[2], s[3], -s[0] / np.hypot(s[0], s[1]) ** 3, -s[1] / np.hypot(s[0], s[1]) ** 3])
    dt = 0.05
    T = np.arange(0, 10 * np.pi, dt)
    s = np.array([1.0, 0, 0, 1.0])
    eu = [s]
    for _ in T[1:]:
        s = s + dt * f(0, s)
        eu.append(s)
    eu = np.array(eu)
    rk = rk4(f, np.array([1.0, 0, 0, 1.0]), T)
    ax.plot(eu[:, 0], eu[:, 1], color=PHYS, lw=1, label="Euler")
    ax.plot(rk[:, 0], rk[:, 1], color=MATH, lw=2.2, label="Runge–Kutta 4")
    ax.plot(0, 0, "o", color="#f1c40f", ms=9)
    ax.legend(loc="upper right", fontsize=8)
    clean(ax)

    ax = panel(fig, cs[6], 7, "Monte Carlo", "Buffon 1777 · Ulam & von Neumann 1946", "both",
               "Use randomness to compute: the fraction of random points inside a quarter circle estimates π/4. "
               "Born at Los Alamos for neutron diffusion; now used from finance to lattice QCD.")
    rng = np.random.default_rng(42)
    N = 3000
    P = rng.uniform(0, 1, (N, 2))
    inside = (P ** 2).sum(1) <= 1
    ax.scatter(P[inside, 0], P[inside, 1], s=2, color=MATH)
    ax.scatter(P[~inside, 0], P[~inside, 1], s=2, color=PHYS)
    th = np.linspace(0, np.pi / 2, 100)
    ax.plot(np.cos(th), np.sin(th), color=INK, lw=1.2)
    ax.text(0.02, -0.1, f"N = {N}:  π ≈ 4 × {inside.sum()}/{N} = {4 * inside.mean():.4f}", fontsize=9.5)
    clean(ax, xlim=(-0.02, 1.02), ylim=(-0.16, 1.02))

    ax = panel(fig, cs[7], 8, "Simple rules, complex behaviour", "von Neumann 1948 · Wolfram 1983", "math",
               "Cellular automata: each cell's next state depends only on itself and two neighbours. Rule 30 "
               "(left) produces apparent randomness; Rule 110 (right) is capable of universal computation.")
    axes = split(fig, ax, 2, "h", gap=0.01)
    for a, rule in zip(axes, [30, 110]):
        W_, Hh = 241, 120
        g = np.zeros((Hh, W_), int)
        g[0, W_ // 2 if rule == 30 else W_ - 2] = 1
        bits = [(rule >> i) & 1 for i in range(8)]
        for i in range(1, Hh):
            l, c, r = np.roll(g[i - 1], 1), g[i - 1], np.roll(g[i - 1], -1)
            g[i] = np.array(bits)[4 * l + 2 * c + r]
        a.imshow(g, cmap=ListedColormap(["white", MATH if rule == 30 else BOTH]), interpolation="nearest",
                 aspect="auto")
        a.set_title(f"rule {rule}", fontsize=9)
        clean(a, equal=False)

    ax = panel(fig, cs[8], 9, "Computer-assisted proof", "Appel & Haken 1976 · Hales 2014 (Kepler)", "math",
               "The four-colour theorem — any map needs at most four colours so that neighbours differ — was the first "
               "major theorem proved by computer. A random map (Voronoi cells) coloured with four colours by "
               "backtracking search.")
    rng = np.random.default_rng(12)
    pts = rng.uniform(0, 1, (46, 2))
    tri = mtri.Triangulation(pts[:, 0], pts[:, 1])
    cols = _four_colour(len(pts), tri.edges)
    gx, gy = np.meshgrid(np.linspace(0, 1, 420), np.linspace(0, 1, 420))
    d = (gx[..., None] - pts[:, 0]) ** 2 + (gy[..., None] - pts[:, 1]) ** 2
    lab = d.argmin(-1)
    img = np.array(cols)[lab]
    four = ListedColormap(["#f5b7a5", "#aed6f1", "#abebc6", "#f9e79f"])
    ax.imshow(img, cmap=four, origin="lower", extent=(0, 1, 0, 1), vmin=-0.5, vmax=3.5, interpolation="nearest")
    edge = (np.diff(lab, axis=0, prepend=lab[:1]) != 0) | (np.diff(lab, axis=1, prepend=lab[:, :1]) != 0)
    ax.imshow(np.ma.masked_where(~edge, edge), cmap=ListedColormap([INK]), origin="lower", extent=(0, 1, 0, 1),
              interpolation="nearest")
    clean(ax, xlim=(0, 1), ylim=(0, 1))
    footer(fig)
    save(fig, "19-tools-that-extend-thinking.png")


# ---------------------------------------------------------------------------------------------
# 20 Learning pathway
# ---------------------------------------------------------------------------------------------
def fig20():
    W, H = 22, 13.5
    fig = figure("One mind's journey: how a person's mathematical and physical understanding builds up",
                 "A typical prerequisite map from infancy to research. Arrows mean 'is needed for'; purple arrows "
                 "cross between mathematics and physics", w=W, h=H, flow=False)
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.86])
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 100)
    ax.axis("off")
    stages = ["Infancy\n0–3", "Early childhood\n3–6", "Primary school\n6–11", "Secondary school\n11–18",
              "Undergraduate", "Graduate & research"]
    colw = 20
    for k, s in enumerate(stages):
        ax.add_patch(Rectangle((k * colw, 0), colw, 95, fc="#f4f1ea" if k % 2 == 0 else BG_COL, ec="none", zorder=0))
        ax.text(k * colw + colw / 2, 97.5, s, ha="center", va="center", fontsize=11.5, weight="bold", color=INK)
    ax.plot([0, 120], [50, 50], color=GRID, lw=1, ls="--", zorder=0)
    ax.text(0.8, 93.5, "MATHEMATICS", fontsize=11, weight="bold", color=MATH)
    ax.text(0.8, 47.5, "PHYSICS", fontsize=11, weight="bold", color=PHYS)
    nodes = {
        "ns": (0, "m", "approximate number sense"), "more": (0, "m", "more vs. less"), "sub": (0, "m", "subitizing 1–3"),
        "op": (0, "p", "object permanence"), "caus": (0, "p", "contact causality"), "gs": (0, "p", "gravity & support"),
        "cnt": (1, "m", "counting words,\none-to-one"), "pat": (1, "m", "patterns & sorting"), "shp": (1, "m", "shapes & spatial words"),
        "push": (1, "p", "pushes & pulls"), "ramp": (1, "p", "balls, ramps & balance"), "flt": (1, "p", "floating & sinking"),
        "ari": (2, "m", "arithmetic"), "frac": (2, "m", "fractions & decimals"), "meas": (2, "m", "measurement & units"),
        "geo": (2, "m", "basic geometry"),
        "mach": (2, "p", "simple machines"), "lgt": (2, "p", "light & shadows"), "som": (2, "p", "states of matter"),
        "mag": (2, "p", "magnets & circuits"),
        "alg": (3, "m", "algebra"), "euc": (3, "m", "Euclidean proof"), "fun": (3, "m", "functions & graphs"),
        "trig": (3, "m", "trigonometry"), "prob": (3, "m", "probability & statistics"), "calc": (3, "m", "intro calculus"),
        "kin": (3, "p", "kinematics"), "newt": (3, "p", "Newton's laws"), "en": (3, "p", "energy & momentum"),
        "wav": (3, "p", "waves & optics"), "elec": (3, "p", "electricity"), "atom": (3, "p", "atoms & nuclei"),
        "mvc": (4, "m", "multivariable calculus"), "la": (4, "m", "linear algebra"), "ode": (4, "m", "differential equations"),
        "cx": (4, "m", "complex analysis"), "ra": (4, "m", "real analysis"), "aa": (4, "m", "abstract algebra"),
        "cm": (4, "p", "analytical mechanics"), "em": (4, "p", "electromagnetism"), "sm": (4, "p", "thermo & stat. mech."),
        "sr": (4, "p", "special relativity"), "qm": (4, "p", "quantum mechanics"),
        "dg": (5, "m", "differential geometry"), "fa": (5, "m", "functional analysis"), "lie": (5, "m", "Lie groups &\nrepresentations"),
        "top": (5, "m", "topology"),
        "gr": (5, "p", "general relativity"), "qft": (5, "p", "quantum field theory"), "cmp": (5, "p", "condensed matter"),
        "pp": (5, "p", "particle physics"), "cos": (5, "p", "cosmology"),
    }
    order = {}
    for key, (st, dom, lab) in nodes.items():
        order.setdefault((st, dom), []).append(key)
    pos = {}
    texts = {}
    for (st, dom), keys in order.items():
        n = len(keys)
        top = 90 if dom == "m" else 44
        span = 40
        step = min(9.0, span / max(n, 1))
        y0 = top - (span - step * (n - 1)) / 2 - 1
        for i, key in enumerate(keys):
            x, y = st * colw + colw / 2, y0 - i * step
            pos[key] = (x, y)
            col = MATH if dom == "m" else PHYS
            texts[key] = ax.text(x, y, nodes[key][2], ha="center", va="center", fontsize=11, zorder=5,
                                 bbox=dict(boxstyle="round,pad=0.42", fc="white", ec=col, lw=1.3), linespacing=1.1)
    edges = ("ns-cnt sub-cnt cnt-ari shp-geo ari-frac ari-meas frac-alg geo-euc alg-fun geo-trig fun-trig fun-calc "
             "alg-prob calc-mvc alg-la calc-ode mvc-cx calc-ra euc-ra alg-aa mvc-dg la-dg ra-fa la-fa aa-lie la-lie "
             "ra-top "
             "op-push gs-flt push-mach flt-som mach-newt lgt-wav mag-elec som-atom kin-newt newt-en en-cm elec-em "
             "wav-em en-sm atom-qm newt-sr em-sr cm-qm sr-gr sr-qft qm-qft qm-cmp sm-cmp qft-pp gr-cos pp-cos "
             "meas-kin fun-kin calc-newt trig-wav la-qm ode-cm mvc-em prob-sm cx-qm dg-gr lie-pp fa-qft top-cmp "
             "ari-mach geo-lgt more-cnt pat-ari pat-alg caus-push ramp-mach gs-ramp").split()
    for e in edges:
        a, b = e.split("-")
        cross = nodes[a][1] != nodes[b][1]
        col = BOTH if cross else (MATH if nodes[a][1] == "m" else PHYS)
        same_col = nodes[a][0] == nodes[b][0]
        arr = FancyArrowPatch(pos[a], pos[b], patchA=texts[a].get_bbox_patch(), patchB=texts[b].get_bbox_patch(),
                              arrowstyle="-|>,head_length=6,head_width=3", mutation_scale=1,
                              connectionstyle=f"arc3,rad={0.35 if same_col else 0.08}", color=col,
                              lw=1.7 if cross else 1.3, alpha=0.75 if cross else 0.6, zorder=3)
        ax.add_patch(arr)
    save(fig, "20-learning-pathway.png")


BG_COL = "#faf8f3"


if __name__ == "__main__":
    for f in (fig16, fig17, fig18, fig19, fig20):
        f()
