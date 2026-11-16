"""Math ladder 06-11: one 3×3 ladder for each strand, from primary school to the frontier."""
from itertools import permutations
from math import comb, factorial

import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Polygon, Rectangle, Wedge

from style import (C, GRID, INK, L, MUTED, OLY, arrow, box, cells, clean, clean3d, figure, footer, panel, plotstyle,
                   save, split)

PAL = ["#2a5d9f", "#c4512c", "#3d8b5a", "#b8860b", "#6a4c93", "#2b8a9e", "#a23b72", "#555555"]


def sieve(n):
    s = np.ones(n + 1, bool)
    s[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if s[p]:
            s[p * p::p] = False
    return s


def _stage(ax, text, color):
    ax.text(0.99, 0.99, text, transform=ax.transAxes, ha="right", va="top", fontsize=8.5, color=color,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, lw=0.8))


# ---------------------------------------------------------------------------------------------
# 06 Number theory
# ---------------------------------------------------------------------------------------------
def fig06():
    fig = figure("The number theory ladder",
                 "From even and odd to the Riemann hypothesis: the oldest questions about whole numbers keep leading to "
                 "the deepest mathematics", keys=("nt",))
    cs = cells(fig, 3, 3)
    k = "nt"

    ax = panel(fig, cs[0], 1, "Even and odd", "primary", k,
               "A number is even if its dots pair up perfectly, odd if one is left over. Pictures prove the rules: "
               "odd + odd = even (the two leftovers pair up), even × anything = even.")
    clean(ax, xlim=(-0.5, 19), ylim=(-2.6, 2.6))
    for n in range(1, 10):
        x0 = (n - 1) * 2.1
        for i in range(n):
            ax.add_patch(Circle((x0 + (i % 2) * 0.8, 1.6 - (i // 2) * 0.8), 0.3,
                                fc=C[k] if not (n % 2 and i == n - 1) else C["comb"], ec="none"))
        ax.text(x0 + 0.4, -2.4, str(n), ha="center", fontsize=11, weight="bold",
                color=C["comb"] if n % 2 else C[k])

    ax = panel(fig, cs[1], 2, "Primes: the sieve", "middle · Eratosthenes c. 240 BC", k,
               "Cross out multiples of 2, 3, 5, 7 (colour = smallest prime factor). What survives up to 100 are the 25 "
               "primes (gold) — the atoms from which every number is built by multiplication.")
    s = sieve(100)
    spf_col = {2: "#d6e4f5", 3: "#f4d5c8", 5: "#d4ead9", 7: "#ece0f5"}
    for n in range(1, 101):
        r, c = (n - 1) // 10, (n - 1) % 10
        if n == 1:
            fc = "#eeeeee"
        elif s[n]:
            fc = OLY
        else:
            fc = spf_col[next(p for p in (2, 3, 5, 7) if n % p == 0)]
        ax.add_patch(Rectangle((c, 9 - r), 0.94, 0.94, fc=fc, ec="white"))
        ax.text(c + 0.47, 9 - r + 0.47, str(n), ha="center", va="center", fontsize=7.5,
                weight="bold" if s[n] else "normal")
    for i, (p, col) in enumerate(spf_col.items()):
        ax.add_patch(Rectangle((10.6, 8.5 - i * 1.1), 0.7, 0.7, fc=col))
        ax.text(11.5, 8.85 - i * 1.1, f"×{p}", va="center", fontsize=8.5)
    ax.add_patch(Rectangle((10.6, 8.5 - 4 * 1.1), 0.7, 0.7, fc=OLY))
    ax.text(11.5, 8.85 - 4 * 1.1, "prime", va="center", fontsize=8.5)
    clean(ax, xlim=(-0.2, 13.5), ylim=(-0.2, 10.1))

    ax = panel(fig, cs[2], 3, "Greatest common divisor", "middle · Euclid c. 300 BC", k,
               "Euclid's algorithm as tiling: fill a 42 × 30 rectangle with the largest possible squares, then repeat "
               "on the leftover strip. The last square size, 6, is gcd(42, 30) — the oldest algorithm still in use.")
    a, b, x0, y0 = 42, 30, 0, 0
    w, h = a, b
    i = 0
    while w and h:
        if w >= h:
            for _ in range(w // h):
                ax.add_patch(Rectangle((x0, y0), h, h, fc=PAL[i % 6], alpha=0.35, ec=PAL[i % 6], lw=1.5))
                ax.text(x0 + h / 2, y0 + h / 2, f"{h}", ha="center", va="center", fontsize=9 + h / 4)
                x0 += h
            w = w % h
        else:
            for _ in range(h // w):
                ax.add_patch(Rectangle((x0, y0), w, w, fc=PAL[i % 6], alpha=0.35, ec=PAL[i % 6], lw=1.5))
                ax.text(x0 + w / 2, y0 + w / 2, f"{w}", ha="center", va="center", fontsize=9 + w / 4)
                y0 += w
            h = h % w
        i += 1
    ax.text(44, 22, "42 = 1·30 + 12\n30 = 2·12 + 6\n12 = 2·6 + 0\n\ngcd = 6", fontsize=10, va="top",
            family="monospace")
    clean(ax, xlim=(-1, 62), ylim=(-1, 31))

    ax = panel(fig, cs[3], 4, "Clock arithmetic", "high school · Gauss 1801", k,
               "Arithmetic mod 12 lives on a clock. Jumping by 5 visits all 12 hours (gcd(5, 12) = 1); jumping by 4 "
               "gets trapped in triangles (gcd = 4). Remainders turn number theory into geometry.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.02)
    for a_, step in [(a1, 5), (a2, 4)]:
        th = np.pi / 2 - np.arange(12) * 2 * np.pi / 12
        P = np.c_[np.cos(th), np.sin(th)]
        a_.add_patch(Circle((0, 0), 1, fc="none", ec=GRID))
        seen = set()
        ci = 0
        for st in range(12):
            if st in seen:
                continue
            cur = st
            while True:
                seen.add(cur)
                nxt = (cur + step) % 12
                a_.plot(*P[[cur, nxt]].T, color=PAL[ci], lw=1.6)
                cur = nxt
                if cur == st:
                    break
            ci += 1
        for i, p in enumerate(P):
            a_.text(*(p * 1.17), str(i if i else 12), ha="center", va="center", fontsize=8)
        a_.set_title(f"step {step}", fontsize=9.5)
        clean(a_, xlim=(-1.35, 1.35), ylim=(-1.35, 1.35))

    ax = panel(fig, cs[4], 5, "Fermat's little theorem", "olympiad · Fermat 1640, Euler 1736", k,
               "Powers aᵏ mod 13. Every row returns to 1 at k = 12 (gold column): a¹² ≡ 1. Rows 2, 6, 7, 11 hit all "
               "12 residues — 'primitive roots'. Behind it: Lagrange's theorem in group theory.")
    p = 13
    T = np.array([[pow(a_, kk, p) for kk in range(1, p)] for a_ in range(1, p)])
    ax.imshow(T, cmap="Blues", vmin=-3, vmax=14)
    for i in range(12):
        for j in range(12):
            ax.text(j, i, str(T[i, j]), ha="center", va="center", fontsize=7, color="white" if T[i, j] > 8 else INK)
    ax.add_patch(Rectangle((10.5, -0.5), 1, 12, fc="none", ec=OLY, lw=2.5))
    ax.set_xticks(range(12))
    ax.set_xticklabels(range(1, 13), fontsize=7)
    ax.set_yticks(range(12))
    ax.set_yticklabels([f"a={a_}" for a_ in range(1, 13)], fontsize=7)
    ax.set_xlabel("exponent k", fontsize=8)
    ax.tick_params(length=0)
    for s_ in ax.spines.values():
        s_.set_visible(False)

    ax = panel(fig, cs[5], 6, "Primes in the complex plane", "Fermat 1640 · Gauss 1832", k,
               "Primes p ≡ 1 (mod 4) split as p = a² + b² (5 = 2² + 1², 13 = 3² + 2²); primes ≡ 3 (mod 4) never do. "
               "In the Gaussian integers a + bi this becomes factorisation. Plotted: all Gaussian primes with |a|, |b| ≤ 40.")
    s = sieve(3300)
    R = 40
    xs, ys = [], []
    for a_ in range(-R, R + 1):
        for b_ in range(-R, R + 1):
            if a_ and b_:
                ok = s[a_ * a_ + b_ * b_]
            else:
                m = abs(a_ + b_)
                ok = s[m] and m % 4 == 3
            if ok:
                xs.append(a_)
                ys.append(b_)
    ax.scatter(xs, ys, s=7, marker="s", color=C[k], lw=0)
    ax.axhline(0, color=GRID, lw=0.6, zorder=0)
    ax.axvline(0, color=GRID, lw=0.6, zorder=0)
    clean(ax, xlim=(-R - 1, R + 1), ylim=(-R - 1, R + 1))

    ax = panel(fig, cs[6], 7, "How many primes?", "university · proved 1896",
               k, "Prime number theorem: π(x), the number of primes ≤ x, behaves like x / ln x and even more closely "
               "like Li(x) = ∫ dt / ln t. Computed up to 200,000.", plot=True)
    N = 200000
    s = sieve(N)
    x = np.arange(2, N + 1)
    pi = np.cumsum(s[2:])
    li = np.cumsum(1 / np.log(x)) - 1 / np.log(2)
    step = 200
    ax.plot(x[::step], pi[::step], color=C[k], lw=2.4, label=f"π(x)   π(200000) = {pi[-1]}")
    ax.plot(x[::step], (x / np.log(x))[::step], color=C["comb"], lw=1.6, ls="--",
            label=f"x / ln x   ≈ {N / np.log(N):.0f}")
    ax.plot(x[::step], li[::step], color=C["geo"], lw=1.6, ls=":", label=f"Li(x)   ≈ {li[-1]:.0f}")
    ax.set_xlabel("x")
    ax.legend(loc="upper left", fontsize=8.5)
    plotstyle(ax)

    ax = panel(fig, cs[7], 8, "The Riemann hypothesis", "frontier · Riemann 1859 · open", k,
               "The errors in the prime count are controlled by the zeros of the zeta function. Riemann–Siegel Z(t) "
               "(computed) crosses zero at t = 14.13, 21.02, 25.01, …; RH says all such zeros lie on one line. "
               "Verified for 10¹³ zeros; unproved. Prize: $1 000 000.", plot=True)
    t = np.linspace(8, 60, 4000)

    def Z(t):
        th = t / 2 * np.log(t / (2 * np.pi)) - t / 2 - np.pi / 8 + 1 / (48 * t) + 7 / (5760 * t ** 3)
        a_ = np.sqrt(t / (2 * np.pi))
        N_ = np.floor(a_).astype(int)
        out = np.zeros_like(t)
        for i in range(len(t)):
            n = np.arange(1, N_[i] + 1)
            out[i] = 2 * np.sum(np.cos(th[i] - t[i] * np.log(n)) / np.sqrt(n))
            pfrac = a_[i] - N_[i]
            C0 = np.cos(2 * np.pi * (pfrac ** 2 - pfrac - 1 / 16)) / np.cos(2 * np.pi * pfrac)
            out[i] += (-1) ** (N_[i] - 1) * (t[i] / (2 * np.pi)) ** -0.25 * C0
        return out

    z = Z(t)
    ax.plot(t, z, color=C[k], lw=1.4)
    ax.axhline(0, color=INK, lw=0.7)
    zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052, 49.7738, 52.9703,
             56.4462, 59.3470]
    ax.plot(zeros, np.zeros(len(zeros)), "o", color=OLY, ms=6, mec=INK, mew=0.6, zorder=5)
    ax.set_xlabel("height t on the critical line")
    ax.set_ylabel("Z(t)")
    ax.set_ylim(-4.5, 4.5)
    plotstyle(ax)

    ax = panel(fig, cs[8], 9, "Elliptic curves", "frontier · Mordell 1922 · Wiles 1995", k,
               "Rational points on y² = x³ + 17 form a group: the line through P = (−2, 3) and Q = (−1, 4) meets the "
               "curve again at (4, 9); reflecting gives P + Q = (4, −9). Elliptic curves proved Fermat's Last "
               "Theorem and secure today's internet.", plot=True)
    xx = np.linspace(-17 ** (1 / 3), 5.2, 800)
    yy = np.sqrt(np.clip(xx ** 3 + 17, 0, None))
    ax.plot(xx, yy, color=C[k], lw=2)
    ax.plot(xx, -yy, color=C[k], lw=2)
    xl = np.linspace(-3, 5.2, 10)
    ax.plot(xl, xl + 5, color=C["comb"], lw=1.2)
    ax.plot([4, 4], [9, -9], color=MUTED, ls="--", lw=1)
    for (px, py, lab) in [(-2, 3, "P"), (-1, 4, "Q"), (4, 9, "R"), (4, -9, "P + Q")]:
        ax.plot(px, py, "o", color=OLY if lab == "P + Q" else INK, ms=7, mec=INK)
        ax.text(px + 0.2, py - 1.4 if lab != "R" else py + 0.6, lab, fontsize=9.5, weight="bold")
    for (px, py) in [(2, 5), (8, 23)]:
        pass
    ax.set_xlim(-3, 5.4)
    ax.set_ylim(-12, 12)
    plotstyle(ax)
    footer(fig)
    save(fig, "06-number-theory-ladder.png")


# ---------------------------------------------------------------------------------------------
# 07 Algebra
# ---------------------------------------------------------------------------------------------
def fig07():
    fig = figure("The algebra ladder",
                 "From balancing a scale to the symmetries of equations: algebra grows from 'find the unknown' into "
                 "the study of structure itself", keys=("alg",))
    cs = cells(fig, 3, 3)
    k = "alg"

    ax = panel(fig, cs[0], 1, "The balance", "primary / middle", k,
               "An equation is a balance: do the same thing to both sides. 3x + 2 = 11 → remove 2 from each pan → "
               "3x = 9 → share into 3 → x = 3.")
    clean(ax, xlim=(0, 10), ylim=(0, 5.5))
    ax.add_patch(Polygon([(4.6, 0.3), (5.4, 0.3), (5.0, 2.0)], fc=MUTED))
    ax.plot([1.0, 9.0], [2.0, 2.0], color=INK, lw=3)
    for x in (2.2, 7.8):
        ax.plot([x - 1.2, x, x + 1.2], [2.0 - 0.0, 2.0, 2.0], color=INK)
        ax.plot([x - 1.3, x + 1.3], [2.15, 2.15], color=INK, lw=2)
    for i in range(3):
        box(ax, 1.4 + i * 0.8, 2.65, "x", fc=L[k], ec=C[k], fs=10, pad=0.25)
    for i in range(2):
        ax.add_patch(Circle((1.8 + i * 0.8, 3.5), 0.26, fc=OLY, ec=INK, lw=0.6))
    for i in range(11):
        ax.add_patch(Circle((6.7 + (i % 4) * 0.55, 2.5 + (i // 4) * 0.55), 0.24, fc=OLY, ec=INK, lw=0.6))
    ax.text(5, 4.7, "3x + 2 = 11   ⇒   3x = 9   ⇒   x = 3", ha="center", fontsize=11.5, weight="bold", color=C[k])

    ax = panel(fig, cs[1], 2, "Algebra as area", "middle · al-Khwārizmī 820, Euclid II", k,
               "(a + b)² = a² + 2ab + b², read off a picture: a square of side a + b cut into one a-square, one "
               "b-square and two a × b rectangles. Here a = 3, b = 1.6.")
    a_, b_ = 3.0, 1.6
    for (x, y, w, h, col, lab) in [(0, b_, a_, a_, C[k], "a²"), (a_, 0, b_, b_, C["comb"], "b²"),
                                   (0, 0, a_, b_, C["geo"], "ab"), (a_, b_, b_, a_, C["geo"], "ab")]:
        ax.add_patch(Rectangle((x, y), w, h, fc=col, alpha=0.3, ec=col, lw=1.5))
        ax.text(x + w / 2, y + h / 2, lab, ha="center", va="center", fontsize=14, weight="bold", color=col)
    ax.text(a_ / 2, -0.4, "a", ha="center", fontsize=11)
    ax.text(a_ + b_ / 2, -0.4, "b", ha="center", fontsize=11)
    ax.text(5.3, 2.3, "(a + b)²\n= a² + 2ab + b²", fontsize=12, va="center", weight="bold")
    clean(ax, xlim=(-0.3, 9.0), ylim=(-0.8, 4.9))

    ax = panel(fig, cs[2], 3, "Completing the square", "high school · al-Khwārizmī 820", k,
               "x² + 6x: put the 6x as two 3 × x strips around an x-square. One corner (3 × 3 = 9) is missing: "
               "x² + 6x + 9 = (x + 3)². This picture is the quadratic formula.")
    xg, bh = 3.2, 1.6
    ax.add_patch(Rectangle((0, 0), xg, xg, fc=L[k], ec=C[k], lw=1.5))
    ax.text(xg / 2, xg / 2, "x²", ha="center", va="center", fontsize=15, color=C[k], weight="bold")
    ax.add_patch(Rectangle((xg, 0), bh, xg, fc=lighten_(C["geo"]), ec=C["geo"], lw=1.5))
    ax.add_patch(Rectangle((0, xg), xg, bh, fc=lighten_(C["geo"]), ec=C["geo"], lw=1.5))
    ax.text(xg + bh / 2, xg / 2, "3x", ha="center", va="center", fontsize=12, color=C["geo"])
    ax.text(xg / 2, xg + bh / 2, "3x", ha="center", va="center", fontsize=12, color=C["geo"])
    ax.add_patch(Rectangle((xg, xg), bh, bh, fc="none", ec=C["comb"], lw=1.8, ls="--"))
    ax.text(xg + bh / 2, xg + bh / 2, "9", ha="center", va="center", fontsize=13, color=C["comb"], weight="bold")
    ax.text(5.6, 2.4, "x² + 6x + 9\n= (x + 3)²", fontsize=12, va="center", weight="bold")
    clean(ax, xlim=(-0.3, 9.3), ylim=(-0.3, 5.1))

    ax = panel(fig, cs[3], 4, "Roots and coefficients", "olympiad · Viète 1591", k,
               "y = x² − 2x − 3 = (x + 1)(x − 3). The roots −1 and 3 add to 2 and multiply to −3: the coefficients are "
               "symmetric functions of the roots (Vieta). This is the seed of Galois theory.", plot=True)
    x = np.linspace(-2.5, 4.5, 300)
    ax.plot(x, x ** 2 - 2 * x - 3, color=C[k], lw=2.4)
    ax.axhline(0, color=INK, lw=0.8)
    for r in (-1, 3):
        ax.plot(r, 0, "o", color=OLY, ms=9, mec=INK)
    ax.plot(1, -4, "s", color=C["comb"], ms=7)
    ax.text(1, -4.8, "vertex (1, −4)", ha="center", fontsize=9)
    ax.text(-2.4, -1.0, "sum of roots = 2 = −b/a\nproduct = −3 = c/a", fontsize=10, color=C[k], va="top")
    ax.set_ylim(-5.5, 9)
    plotstyle(ax)

    ax = panel(fig, cs[4], 5, "Roots of unity", "university · de Moivre 1707, Gauss 1796", k,
               "The solutions of zⁿ = 1 sit at the corners of a regular n-gon on the unit circle. Gauss used them to "
               "show the 17-gon can be constructed with ruler and compass — at age 19.")
    for n_, col, r in [(5, C[k], 1.0), (7, C["comb"], 1.0), (17, C["geo"], 1.0)]:
        th = 2 * np.pi * np.arange(n_ + 1) / n_
        ax.plot(r * np.cos(th), r * np.sin(th), "-o", color=col, ms=4, lw=1.2, alpha=0.85, label=f"z^{n_} = 1")
    ax.add_patch(Circle((0, 0), 1, fc="none", ec=GRID))
    ax.axhline(0, color=GRID, lw=0.6)
    ax.axvline(0, color=GRID, lw=0.6)
    ax.legend(loc="upper right", fontsize=8.5, bbox_to_anchor=(1.75, 1.0))
    clean(ax, xlim=(-1.2, 1.2), ylim=(-1.2, 1.2))

    ax = panel(fig, cs[5], 6, "The world of roots", "university · algebraic numbers", k,
               "All complex roots of all 16 384 polynomials of degree 13 with coefficients ±1 (computed). Simple rules, "
               "astonishing structure: fractal holes and a ring near |z| = 1 that are still being studied.")
    deg = 13
    roots = []
    for m in range(2 ** (deg + 1)):
        coeffs = [1 if (m >> i) & 1 else -1 for i in range(deg + 1)]
        roots.append(np.roots(coeffs))
    roots = np.concatenate(roots)
    ax.scatter(roots.real, roots.imag, s=0.05, color=C[k], alpha=0.5, lw=0)
    clean(ax, xlim=(-1.75, 1.75), ylim=(-1.3, 1.3))

    ax = panel(fig, cs[6], 7, "Groups: algebra of symmetry", "university · Galois 1832, Cayley 1854", k,
               "The 6 symmetries of a triangle (e, two rotations r, r², three flips) combine like numbers multiply. "
               "Cayley table computed from the permutations: each row is a rearrangement — a group.")
    els = {"e": (0, 1, 2), "r": (1, 2, 0), "r²": (2, 0, 1), "s": (0, 2, 1), "sr": (2, 1, 0), "sr²": (1, 0, 2)}
    names = list(els)
    perms = list(els.values())
    def mul(p, q):
        return tuple(p[q[i]] for i in range(3))
    T = np.array([[perms.index(mul(p, q)) for q in perms] for p in perms])
    cm = ListedColormap([lighten_(c) for c in PAL[:6]])
    ax.imshow(T, cmap=cm, vmin=-0.5, vmax=5.5)
    for i in range(6):
        for j in range(6):
            ax.text(j, i, names[T[i, j]], ha="center", va="center", fontsize=10)
    ax.set_xticks(range(6))
    ax.set_xticklabels(names, fontsize=9)
    ax.set_yticks(range(6))
    ax.set_yticklabels(names, fontsize=9)
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    for s_ in ax.spines.values():
        s_.set_visible(False)

    ax = panel(fig, cs[7], 8, "Linear algebra", "university · Grassmann 1844, Cayley 1858", k,
               "A matrix is a transformation of the whole plane. A = [[1.5, 0.5], [0.5, 1]] stretches the grid; its "
               "eigenvectors (gold) only get scaled, by λ = 1.81 and 0.69. The unit square's area becomes det A = 1.25.")
    A = np.array([[1.5, 0.5], [0.5, 1.0]])
    for v in np.arange(-2, 2.01, 0.5):
        for seg in [np.array([[v, -2], [v, 2]]), np.array([[-2, v], [2, v]])]:
            ax.plot(*seg.T, color=GRID, lw=0.7)
            ax.plot(*(seg @ A.T).T, color=C[k], lw=0.8, alpha=0.6)
    sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    ax.add_patch(Polygon(sq @ A.T, fc=C[k], alpha=0.3, ec=C[k], lw=1.5))
    ax.add_patch(Polygon(sq, fc="none", ec=INK, lw=1.2, ls="--"))
    w, V = np.linalg.eigh(A)
    for lam, vec in zip(w, V.T):
        for sgn in (1, -1):
            ax.annotate("", xy=sgn * lam * vec * 1.4, xytext=(0, 0),
                        arrowprops=dict(arrowstyle="-|>", color=OLY, lw=2.2))
    clean(ax, xlim=(-2.6, 2.6), ylim=(-2.2, 2.2))

    ax = panel(fig, cs[8], 9, "Galois correspondence", "→ Langlands 1967", k,
               "The fields between ℚ and ℚ(∛2, ω) match the subgroups of the symmetry group S₃ — upside down. Asking "
               "how such symmetry groups relate to analysis led to the Langlands program, today's grand unified "
               "theory of mathematics.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    F = {"top": (2.4, 9.0, "ℚ(∛2, ω)"), "a": (0.6, 5.6, "ℚ(∛2)"), "b": (1.85, 5.6, "ℚ(ω∛2)"),
         "c": (3.1, 5.6, "ℚ(ω²∛2)"), "d": (4.3, 3.6, "ℚ(ω)"), "bot": (2.4, 0.8, "ℚ")}
    G = {"top": (7.6, 0.8, "{e}"), "a": (5.9, 4.4, "⟨s₁⟩"), "b": (7.15, 4.4, "⟨s₂⟩"), "c": (8.4, 4.4, "⟨s₃⟩"),
         "d": (9.4, 6.4, "A₃"), "bot": (7.6, 9.0, "S₃")}
    for D, col in [(F, C[k]), (G, C["comb"])]:
        for u, v in [("top", "a"), ("top", "b"), ("top", "c"), ("top", "d"), ("a", "bot"), ("b", "bot"),
                     ("c", "bot"), ("d", "bot")]:
            ax.plot([D[u][0], D[v][0]], [D[u][1], D[v][1]], color=col, lw=1, alpha=0.6, zorder=1)
        for key, (x, y, lab) in D.items():
            box(ax, x, y, lab, fc="white", ec=col, fs=9.5, pad=0.25, zorder=3)
    ax.text(2.4, 9.9, "fields", ha="center", fontsize=9.5, color=C[k], weight="bold")
    ax.text(7.6, 9.9, "groups", ha="center", fontsize=9.5, color=C["comb"], weight="bold")
    ax.annotate("", xy=(5.6, 5.0), xytext=(4.4, 5.0), arrowprops=dict(arrowstyle="<|-|>", color=MUTED, lw=1.4))
    footer(fig)
    save(fig, "07-algebra-ladder.png")


def lighten_(c, f=0.75):
    from style import lighten
    return lighten(c, f)


# ---------------------------------------------------------------------------------------------
# 08 Geometry
# ---------------------------------------------------------------------------------------------
def _circumcenter(A, B, Cc):
    ax_, ay = A
    bx, by = B
    cx, cy = Cc
    d = 2 * (ax_ * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax_ ** 2 + ay ** 2) * (by - cy) + (bx ** 2 + by ** 2) * (cy - ay) + (cx ** 2 + cy ** 2) * (ay - by)) / d
    uy = ((ax_ ** 2 + ay ** 2) * (cx - bx) + (bx ** 2 + by ** 2) * (ax_ - cx) + (cx ** 2 + cy ** 2) * (bx - ax_)) / d
    return np.array([ux, uy])


def _foot(P, A, B):
    d = B - A
    return A + np.dot(P - A, d) / np.dot(d, d) * d


def _intersect(p1, p2, p3, p4):
    d1, d2 = p2 - p1, p4 - p3
    M = np.array([d1, -d2]).T
    t = np.linalg.solve(M, p3 - p1)
    return p1 + t[0] * d1


def fig08():
    fig = figure("The geometry ladder",
                 "From cutting paper to curved space: geometry moves from measuring shapes to studying what stays the "
                 "same when shapes are transformed", keys=("geo",))
    cs = cells(fig, 3, 3)
    k = "geo"

    ax = panel(fig, cs[0], 1, "Area by cut and paste", "primary", k,
               "Cut a triangle off a parallelogram and slide it across: a rectangle with the same base and height. "
               "Two copies of any triangle make a parallelogram, so triangle = ½ × base × height.")
    clean(ax, xlim=(-0.3, 14.5), ylim=(-1.4, 4.2))
    par = np.array([(0, 0), (4, 0), (5.5, 3), (1.5, 3)])
    ax.add_patch(Polygon(par, fc=L[k], ec=C[k], lw=1.5))
    ax.add_patch(Polygon([(0, 0), (1.5, 0), (1.5, 3)], fc=C["comb"], alpha=0.35, ec=C["comb"], lw=1.2))
    ax.plot([1.5, 1.5], [0, 3], color=C["comb"], ls="--")
    arrow(ax, (5.9, 1.5), (7.0, 1.5), color=MUTED, lw=1.6)
    ax.add_patch(Rectangle((7.5, 0), 4, 3, fc=L[k], ec=C[k], lw=1.5))
    ax.add_patch(Polygon([(11.5, 0), (13.0, 0), (13.0, 3)], fc=C["comb"], alpha=0.35, ec=C["comb"], lw=1.2))
    ax.add_patch(Rectangle((11.5, 0), 1.5, 3, fc="none", ec=C["comb"], lw=0.8, ls=":"))
    ax.text(2.75, -0.8, "parallelogram", ha="center", fontsize=9.5)
    ax.text(10.2, -0.8, "rectangle: base × height", ha="center", fontsize=9.5)

    ax = panel(fig, cs[1], 2, "Pythagoras by rearrangement", "middle · Babylon → Euclid", k,
               "Both big squares have side a + b and contain four identical right triangles. What is left over is c² "
               "on the left and a² + b² on the right — so a² + b² = c².")
    a_, b_ = 1.2, 2.2
    s_ = a_ + b_
    for ox in (0, s_ + 1.2):
        ax.add_patch(Rectangle((ox, 0), s_, s_, fc="white", ec=INK, lw=1.4))
    tri_l = [[(0, 0), (b_, 0), (0, a_)], [(b_, 0), (s_, 0), (s_, b_)], [(s_, b_), (s_, s_), (a_, s_)],
             [(a_, s_), (0, s_), (0, a_)]]
    for t in tri_l:
        ax.add_patch(Polygon(t, fc=C[k], alpha=0.45, ec=C[k]))
    ax.add_patch(Polygon([(b_, 0), (s_, b_), (a_, s_), (0, a_)], fc=OLY, alpha=0.35, ec=OLY))
    ax.text(s_ / 2, s_ / 2, "c²", ha="center", va="center", fontsize=15, weight="bold")
    ox = s_ + 1.2
    for t in [[(ox, 0), (ox + b_, 0), (ox, a_)], [(ox + b_, a_), (ox, a_), (ox + b_, 0)],
              [(ox + b_, a_), (ox + s_, a_), (ox + b_, s_)], [(ox + s_, s_), (ox + b_, s_), (ox + s_, a_)]]:
        ax.add_patch(Polygon(t, fc=C[k], alpha=0.45, ec=C[k]))
    ax.add_patch(Rectangle((ox + b_, 0), a_, a_, fc=OLY, alpha=0.35, ec=OLY))
    ax.add_patch(Rectangle((ox, a_), b_, b_, fc=OLY, alpha=0.35, ec=OLY))
    ax.text(ox + b_ + a_ / 2, a_ / 2, "a²", ha="center", va="center", fontsize=12, weight="bold")
    ax.text(ox + b_ / 2, a_ + b_ / 2, "b²", ha="center", va="center", fontsize=14, weight="bold")
    clean(ax, xlim=(-0.2, 2 * s_ + 1.4), ylim=(-0.2, s_ + 0.2))

    ax = panel(fig, cs[2], 3, "The inscribed angle theorem", "middle / olympiad · Euclid III.21", k,
               "Every angle that chord AB subtends from the major arc is the same (computed: all 50.0°), and the "
               "central angle is exactly double. Most olympiad 'angle chasing' rests on this one fact.")
    ax.add_patch(Circle((0, 0), 1, fc="none", ec=INK, lw=1.2))
    A, B = np.array([np.cos(-0.5 * np.pi + 0.873), np.sin(-0.5 * np.pi + 0.873)]), \
        np.array([np.cos(-0.5 * np.pi - 0.873), np.sin(-0.5 * np.pi - 0.873)])
    ax.plot(*np.c_[A, B], color=INK, lw=1.5)
    for i, t in enumerate([1.2, 1.9, 2.6, 0.5]):
        P = np.array([np.cos(t), np.sin(t)])
        ang = np.degrees(np.arccos(np.dot(A - P, B - P) / np.linalg.norm(A - P) / np.linalg.norm(B - P)))
        ax.plot(*np.c_[A, P, B], color=PAL[i], lw=1.2)
        ax.text(*(P * 1.12), f"{ang:.1f}°", ha="center", va="center", fontsize=8.5, color=PAL[i])
    ax.plot(*np.c_[A, (0, 0), B], color=C["comb"], lw=2)
    cang = np.degrees(np.arccos(np.dot(A, B)))
    ax.text(0.0, -0.32, f"{cang:.0f}°", ha="center", fontsize=10, color=C["comb"], weight="bold")
    ax.text(*(A * 1.12), "A", fontsize=10, ha="center")
    ax.text(*(B * 1.12), "B", fontsize=10, ha="center")
    clean(ax, xlim=(-1.4, 1.4), ylim=(-1.25, 1.3))

    ax = panel(fig, cs[3], 4, "Triangle centres & the Euler line", "olympiad · Euler 1765", k,
               "Circumcentre O, centroid G, orthocentre H always lie on one line, with HG = 2·GO. The nine-point "
               "circle (centre N, radius R/2) passes through the 3 side midpoints, 3 altitude feet and 3 midpoints "
               "of AH, BH, CH. Computed.")
    A, B, Cc = np.array([0.0, 0.0]), np.array([6.0, 0.0]), np.array([1.6, 4.2])
    O = _circumcenter(A, B, Cc)
    G = (A + B + Cc) / 3
    H = A + B + Cc - 2 * O
    N = (O + H) / 2
    R = np.linalg.norm(A - O)
    ax.add_patch(Polygon([A, B, Cc], fc="none", ec=INK, lw=1.6))
    ax.add_patch(Circle(O, R, fc="none", ec=GRID, lw=1.2))
    ax.add_patch(Circle(N, R / 2, fc="none", ec=C[k], lw=1.4))
    nine = [(A + B) / 2, (B + Cc) / 2, (A + Cc) / 2, _foot(A, B, Cc), _foot(B, A, Cc), _foot(Cc, A, B),
            (A + H) / 2, (B + H) / 2, (Cc + H) / 2]
    for P in nine:
        ax.plot(*P, "o", color=C[k], ms=4)
    for V, F_ in [(A, _foot(A, B, Cc)), (B, _foot(B, A, Cc)), (Cc, _foot(Cc, A, B))]:
        ax.plot(*np.c_[V, F_], color=MUTED, lw=0.7, ls=":")
    d = (H - O) / np.linalg.norm(H - O)
    ax.plot(*np.c_[O - 2.5 * d, H + 1.2 * d], color=C["comb"], lw=1.4)
    for P, lab in [(O, "O"), (G, "G"), (H, "H"), (N, "N")]:
        ax.plot(*P, "o", color=C["comb"], ms=6)
        ax.text(P[0] + 0.15, P[1] + 0.12, lab, fontsize=10, weight="bold", color=C["comb"])
    clean(ax, xlim=(O[0] - R - 0.2, O[0] + R + 0.2), ylim=(O[1] - R - 0.2, O[1] + R + 0.2))

    ax = panel(fig, cs[4], 5, "Power of a point", "olympiad · Euclid III.35", k,
               "Through any point P, every chord satisfies PA · PB = constant = R² − OP². Computed for three chords: "
               "the products agree. A workhorse of olympiad geometry, and a first example of an invariant.")
    ax.add_patch(Circle((0, 0), 1, fc="none", ec=INK, lw=1.2))
    P = np.array([0.35, 0.2])
    for i, th in enumerate([0.3, 1.4, 2.3]):
        d = np.array([np.cos(th), np.sin(th)])
        bq = np.dot(P, d)
        cq = np.dot(P, P) - 1
        t1, t2 = -bq + np.sqrt(bq ** 2 - cq), -bq - np.sqrt(bq ** 2 - cq)
        A_, B_ = P + t1 * d, P + t2 * d
        ax.plot(*np.c_[A_, B_], color=PAL[i], lw=1.6)
        ax.text(1.25, 0.75 - i * 0.32, f"{abs(t1):.3f} × {abs(t2):.3f} = {abs(t1 * t2):.3f}", fontsize=9,
                color=PAL[i])
    ax.plot(*P, "o", color=INK, ms=6)
    ax.text(P[0] + 0.06, P[1] - 0.15, "P", fontsize=10, weight="bold")
    ax.text(1.25, -0.4, f"R² − OP² = {1 - P @ P:.3f}", fontsize=9.5, weight="bold")
    clean(ax, xlim=(-1.1, 3.1), ylim=(-1.1, 1.1))

    ax = panel(fig, cs[5], 6, "Inversion", "olympiad / university · Steiner 1824, Möbius", k,
               "Inversion in the unit circle sends each point to the point on the same ray at distance 1/r. Straight "
               "lines (left, grey) become circles through the centre (colour). A powerful olympiad trick and the door "
               "to Möbius transformations.")
    th = np.linspace(0, 2 * np.pi, 400)
    ax.add_patch(Circle((0, 0), 1, fc="none", ec=INK, lw=1.8))
    tt = np.linspace(-30, 30, 4000)
    for i, c in enumerate([0.5, 0.8, 1.3, 2.0]):
        for pts, col in [(np.c_[np.full_like(tt, c), tt], PAL[i]), (np.c_[tt, np.full_like(tt, -c)], PAL[i + 4 if i < 3 else 0])]:
            r2 = (pts ** 2).sum(1)
            inv = pts / r2[:, None]
            ax.plot(*inv.T, color=col, lw=1.4)
            ax.plot(*pts.T, color=GRID, lw=0.8, zorder=0)
    clean(ax, xlim=(-2.2, 2.2), ylim=(-2.2, 1.6))

    ax = panel(fig, cs[6], 7, "Projective geometry: Pascal's theorem", "Pascal 1640, age 16", k,
               "Take any six points on a conic (here an ellipse). The three intersection points of opposite sides of "
               "the hexagon always lie on one line (gold). No lengths or angles — only incidence: projective "
               "geometry.")
    ang = np.array([0.91, 4.37, 1.5, 0.29, 3.43, 5.21])
    E = np.c_[2.0 * np.cos(ang), 1.0 * np.sin(ang)]
    tt = np.linspace(0, 2 * np.pi, 300)
    ax.plot(2 * np.cos(tt), np.sin(tt), color=C[k], lw=1.6)
    hexa = np.vstack([E, E[:1]])
    ax.plot(*hexa.T, color=INK, lw=1)
    X = [_intersect(E[0], E[1], E[3], E[4]), _intersect(E[1], E[2], E[4], E[5]), _intersect(E[2], E[3], E[5], E[0])]
    X = np.array(X)
    for i, (i0, i1, j0, j1) in enumerate([(0, 1, 3, 4), (1, 2, 4, 5), (2, 3, 5, 0)]):
        for p, q in [(i0, i1), (j0, j1)]:
            ax.plot(*np.c_[E[p], X[i]], color=MUTED, lw=0.6, ls=":")
            ax.plot(*np.c_[E[q], X[i]], color=MUTED, lw=0.6, ls=":")
    o = np.argsort(X[:, 0])
    dirv = X[o[-1]] - X[o[0]]
    ax.plot(*np.c_[X[o[0]] - 0.15 * dirv, X[o[-1]] + 0.15 * dirv], color=OLY, lw=2.2)
    ax.plot(*X.T, "o", color=C["comb"], ms=7, mec=INK, zorder=5)
    ax.plot(*E.T, "o", color=C[k], ms=5)
    lo = np.minimum(X.min(0), E.min(0)) - 0.4
    hi = np.maximum(X.max(0), E.max(0)) + 0.4
    clean(ax, xlim=(lo[0], hi[0]), ylim=(lo[1], hi[1]))

    ax = panel(fig, cs[7], 8, "Curved space", "university · Gauss 1827, Riemann 1854", k,
               "On a sphere a triangle with three right angles exists: angle sum 270°. The excess over 180° equals the "
               "area divided by R² (Gauss–Bonnet): here π/2 = one-eighth of 4π. The geometry of general relativity.",
               projection="3d")
    u, v = np.mgrid[0:2 * np.pi:40j, 0:np.pi:20j]
    ax.plot_wireframe(np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v), color=GRID, lw=0.4)
    t = np.linspace(0, np.pi / 2, 50)
    for arc in [np.c_[np.cos(t), np.sin(t), 0 * t], np.c_[0 * t, np.cos(t), np.sin(t)],
                np.c_[np.sin(t), 0 * t, np.cos(t)]]:
        ax.plot(*arc.T, color=C["comb"], lw=3)
    uu, vv = np.mgrid[0:np.pi / 2:15j, 0:np.pi / 2:15j]
    ax.plot_surface(np.cos(uu) * np.sin(vv), np.sin(uu) * np.sin(vv), np.cos(vv), color=C["comb"], alpha=0.25,
                    lw=0)
    clean3d(ax, elev=25, azim=35)
    ax.set_box_aspect((1, 1, 1), zoom=1.25)
    ax.text2D(0.02, 0.9, "90° + 90° + 90° = 270°", transform=ax.transAxes, fontsize=10, color=C["comb"])

    ax = panel(fig, cs[8], 9, "Topology: V − E + F", "→ Perelman 2003", k,
               "Vertices − edges + faces = 2 for every convex polyhedron, but 0 for a torus: a number that cannot change "
               "under stretching. Classifying shapes by such invariants led to the Poincaré conjecture, solved by "
               "Perelman.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.0, ratios=[1, 1.15], projections=["3d", None])
    u, v = np.mgrid[0:2 * np.pi:40j, 0:2 * np.pi:20j]
    a1.plot_surface((2 + 0.8 * np.cos(v)) * np.cos(u), (2 + 0.8 * np.cos(v)) * np.sin(u), 0.8 * np.sin(v),
                    color=lighten_(C[k], 0.4), edgecolor=C[k], lw=0.2, alpha=0.9)
    clean3d(a1, elev=35, azim=30)
    a1.set_box_aspect((1, 1, 0.45), zoom=1.3)
    clean(a2, equal=False, xlim=(0, 10), ylim=(0, 10))
    rows = [("shape", "V", "E", "F", "V−E+F"), ("tetrahedron", 4, 6, 4, 2), ("cube", 8, 12, 6, 2),
            ("octahedron", 6, 12, 8, 2), ("dodecahedron", 20, 30, 12, 2), ("icosahedron", 12, 30, 20, 2),
            ("torus (4×4 grid)", 16, 32, 16, 0)]
    for i, r in enumerate(rows):
        y = 9.3 - i * 1.35
        for j, (x, val) in enumerate(zip([0.0, 4.8, 6.0, 7.2, 8.4], r)):
            a2.text(x, y, str(val), fontsize=9, weight="bold" if i == 0 or j == 4 else "normal",
                    color=C["comb"] if (j == 4 and i == 6) else INK)
    footer(fig)
    save(fig, "08-geometry-ladder.png")


# ---------------------------------------------------------------------------------------------
# 09 Combinatorics
# ---------------------------------------------------------------------------------------------
def fig09():
    fig = figure("The combinatorics ladder",
                 "From listing outfits to the hidden order in large structures — the strand where olympiad training "
                 "connects most directly to modern research", keys=("comb",))
    cs = cells(fig, 3, 3)
    k = "comb"

    ax = panel(fig, cs[0], 1, "Tree diagrams", "primary", k,
               "3 shirts and 2 pairs of trousers: each shirt branches into 2 choices, so 3 × 2 = 6 outfits. The "
               "multiplication principle — the first theorem of counting.")
    clean(ax, xlim=(-0.5, 10.5), ylim=(-0.5, 7))
    shirts = [C["nt"], C["comb"], C["geo"]]
    ax.add_patch(Circle((0.5, 3.25), 0.3, fc=INK))
    for i, sc in enumerate(shirts):
        y = 5.5 - i * 2.25
        ax.plot([0.5, 3.5], [3.25, y], color=MUTED)
        ax.add_patch(Rectangle((3.1, y - 0.4), 0.8, 0.8, fc=sc))
        for j, pc in enumerate(["#555555", "#c8b98f"]):
            y2 = y + 0.55 - j * 1.1
            ax.plot([3.9, 6.5], [y, y2], color=MUTED)
            ax.add_patch(Rectangle((6.6, y2 - 0.35), 0.35, 0.7, fc=pc))
            ax.add_patch(Rectangle((7.2, y2 - 0.3), 0.6, 0.6, fc=sc))
            ax.add_patch(Rectangle((7.85, y2 - 0.3), 0.3, 0.6, fc=pc))
            ax.text(8.6, y2, f"{2 * i + j + 1}", va="center", fontsize=9)

    ax = panel(fig, cs[1], 2, "Counting paths", "middle · Pascal 1654", k,
               "How many shortest routes from bottom-left to top-right on a 4 × 3 street grid? Each corner's count is "
               "the sum of the counts from the left and from below — Pascal's rule — giving C(7, 3) = 35.")
    m, n = 4, 3
    for i in range(m + 1):
        ax.plot([i, i], [0, n], color=GRID, lw=2)
    for j in range(n + 1):
        ax.plot([0, m], [j, j], color=GRID, lw=2)
    path = [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (4, 3)]
    ax.plot(*np.array(path).T, color=k and C[k], lw=3)
    for i in range(m + 1):
        for j in range(n + 1):
            ax.add_patch(Circle((i, j), 0.22, fc="white", ec=C[k], zorder=3))
            ax.text(i, j, str(comb(i + j, i)), ha="center", va="center", fontsize=9, zorder=4,
                    weight="bold" if (i, j) == (m, n) else "normal")
    clean(ax, xlim=(-0.4, 4.4), ylim=(-0.4, 3.4))

    ax = panel(fig, cs[2], 3, "Pascal's triangle mod 2", "high school · Lucas 1878", k,
               "Colour the odd entries of the first 128 rows of Pascal's triangle: the Sierpiński triangle appears. "
               "Lucas' theorem explains it with binary digits — counting, number theory and fractals in one picture.")
    Nr = 128
    img = np.zeros((Nr, 2 * Nr))
    row = np.array([1])
    for r in range(Nr):
        for kk, v in enumerate(row):
            img[r, Nr - r + 2 * kk - 1:Nr - r + 2 * kk + 1] = 1 if v % 2 else 0.12
        row = np.r_[row, 0] + np.r_[0, row]
        row %= 2
    ax.imshow(img, cmap=ListedColormap(["white", lighten_(C[k], 0.8), C[k]]), interpolation="nearest",
              vmin=0, vmax=1, aspect="auto")
    clean(ax, equal=False)

    ax = panel(fig, cs[3], 4, "Graphs: the bridges of Königsberg", "olympiad · Euler 1736", k,
               "Can you cross all 7 bridges exactly once? Euler turned land into dots and bridges into lines. A walk "
               "needs at most 2 dots of odd degree; here all 4 are odd (5, 3, 3, 3). Impossible — graph theory is born.")
    Pn = {"A": (0, 0), "B": (0, 2), "C": (0, -2), "D": (2.6, 0)}
    deg = {key: 0 for key in Pn}
    for u, v, rad in [("A", "B", 0.3), ("A", "B", -0.3), ("A", "C", 0.3), ("A", "C", -0.3), ("A", "D", 0),
                      ("B", "D", 0.15), ("C", "D", -0.15)]:
        ax.add_patch(FancyArrowPatch(Pn[u], Pn[v], connectionstyle=f"arc3,rad={rad}", arrowstyle="-", lw=2.2,
                                     color=C[k], shrinkA=0, shrinkB=0))
        deg[u] += 1
        deg[v] += 1
    for key, p in Pn.items():
        ax.add_patch(Circle(p, 0.28, fc=OLY, ec=INK, zorder=3))
        ax.text(*p, key, ha="center", va="center", fontsize=10, weight="bold", zorder=4)
        ax.text(p[0] + 0.35, p[1] + 0.3, f"deg {deg[key]}", fontsize=8.5, color=MUTED)
    clean(ax, xlim=(-1.6, 3.8), ylim=(-2.6, 2.6))

    ax = panel(fig, cs[4], 5, "Colouring invariants", "olympiad classic", k,
               "Can a 10 × 10 board be tiled by 1 × 4 strips? Colour square (i, j) by (i + j) mod 4. Every strip covers "
               "one of each colour, but the board has 25, 26, 25, 24 squares of the four colours (computed). No!")
    cols4 = [C["nt"], C["comb"], C["geo"], OLY]
    cnt = [0] * 4
    for i in range(10):
        for j in range(10):
            c = (i + j) % 4
            cnt[c] += 1
            ax.add_patch(Rectangle((i, j), 1, 1, fc=cols4[c], alpha=0.6, ec="white", lw=0.6))
    ax.add_patch(Rectangle((1.1, 7.1), 3.8, 0.8, fc="none", ec=INK, lw=2))
    for c in range(4):
        ax.add_patch(Rectangle((10.8, 8 - c * 1.3), 0.8, 0.8, fc=cols4[c], alpha=0.6))
        ax.text(11.9, 8.4 - c * 1.3, f"{cnt[c]}", va="center", fontsize=11, weight="bold")
    clean(ax, xlim=(-0.2, 13.2), ylim=(-0.2, 10.2))

    ax = panel(fig, cs[5], 6, "Catalan numbers", "olympiad / university · Euler 1751, Catalan 1838", k,
               "Paths of 4 up-steps and 4 down-steps that never dip below the start: all 14 drawn (computed). The same "
               "numbers 1, 1, 2, 5, 14, 42, 132 count bracketings, triangulations and binary trees.")
    n = 4
    paths = []
    for perm in set(permutations([1] * n + [-1] * n)):
        if min(np.cumsum(perm)) >= 0:
            paths.append(perm)
    paths.sort(reverse=True)
    for idx, pth in enumerate(paths):
        r, c = idx // 5, idx % 5
        ox, oy = c * 9.5, -r * 5.6
        y = np.r_[0, np.cumsum(pth)]
        ax.plot(ox + np.arange(2 * n + 1), oy + y, color=C[k], lw=1.6)
        ax.plot([ox, ox + 2 * n], [oy, oy], color=GRID, lw=0.8)
    ax.text(29, -12.5, f"{len(paths)} paths  =  C(8,4)/5", fontsize=10.5, weight="bold", color=C[k])
    clean(ax, xlim=(-0.5, 47), ylim=(-13.5, 4.5))

    ax = panel(fig, cs[6], 7, "Ramsey: complete disorder is impossible", "Ramsey 1930", k,
               "Among any 6 people, 3 are mutual friends or 3 mutual strangers: R(3, 3) = 6. With 5 people it can fail "
               "— the pentagon/pentagram colouring (left) has no single-colour triangle. Every large structure "
               "contains order.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.02)
    th = np.pi / 2 + 2 * np.pi * np.arange(5) / 5
    P5 = np.c_[np.cos(th), np.sin(th)]
    for i in range(5):
        for j in range(i + 1, 5):
            col = C["nt"] if (j - i) in (1, 4) else C["comb"]
            a1.plot(*P5[[i, j]].T, color=col, lw=2)
    a1.scatter(*P5.T, s=60, color=INK, zorder=3)
    a1.set_title("5 people: no triangle", fontsize=9)
    clean(a1, xlim=(-1.2, 1.2), ylim=(-1.2, 1.3))
    th6 = np.pi / 2 + 2 * np.pi * np.arange(6) / 6
    P6 = np.c_[np.cos(th6), np.sin(th6)]
    for j in range(1, 6):
        a2.plot(*P6[[0, j]].T, color=C["comb"] if j <= 3 else C["nt"], lw=2.2 if j <= 3 else 1)
    for i, j in [(1, 2), (2, 3), (1, 3)]:
        a2.plot(*P6[[i, j]].T, color=MUTED, lw=1.2, ls="--")
    a2.scatter(*P6.T, s=60, color=INK, zorder=3)
    a2.set_title("6 people: 3 of 5 edges agree", fontsize=9)
    clean(a2, xlim=(-1.2, 1.2), ylim=(-1.2, 1.3))

    ax = panel(fig, cs[7], 8, "Random graphs & phase transitions", "university · Erdős & Rényi 1960", k,
               "Add random links among 3000 dots. When the average number of links per dot passes 1, a giant connected "
               "cluster suddenly appears — simulated (dots) vs theory S = 1 − e^{−cS} (line). Combinatorics meets "
               "physics.", plot=True)
    rng = np.random.default_rng(1)
    nN = 3000

    def giant(c):
        parent = np.arange(nN)

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        m_ = int(c * nN / 2)
        e = rng.integers(0, nN, (m_, 2))
        for a_, b_ in e:
            ra, rb = find(a_), find(b_)
            if ra != rb:
                parent[ra] = rb
        roots = np.array([find(i) for i in range(nN)])
        return np.bincount(roots).max() / nN

    cs_ = np.linspace(0.1, 4, 26)
    ax.plot(cs_, [giant(c) for c in cs_], "o", color=C[k], ms=5, label="simulation, n = 3000")
    cc = np.linspace(0.01, 4, 400)
    S = []
    for c in cc:
        s_ = 0.9
        for _ in range(200):
            s_ = 1 - np.exp(-c * s_)
        S.append(s_ if c > 1 else 0)
    ax.plot(cc, S, color=INK, lw=1.6, label="theory")
    ax.axvline(1, color=MUTED, ls=":")
    ax.set_xlabel("average degree c")
    ax.set_ylabel("fraction in largest cluster")
    ax.legend(loc="lower right", fontsize=8.5)
    plotstyle(ax)

    ax = panel(fig, cs[8], 9, "Frontier: how big are Ramsey numbers?", "Erdős 1947 → 2023", k,
               "R(k, k) is known only for k ≤ 4 (6 and 18); R(5, 5) lies between 43 and 46. Bounds: Erdős' random "
               "colourings give 2^{k/2}; the upper bound 4ᵏ stood for 88 years until 2023 (Campos–Griffiths–Morris–"
               "Sahasrabudhe), since improved to about 3.8ᵏ.", plot=True)
    kk = np.arange(3, 21)
    ax.fill_between(kk, kk / 2, kk * np.log2(3.8), color=lighten_(C[k], 0.8), label="unknown territory")
    ax.plot(kk, kk / 2, color=C["nt"], lw=2, label="lower 2^{k/2} (Erdős 1947)")
    ax.plot(kk, 2 * kk, color=MUTED, lw=1.5, ls="--", label="upper 4ᵏ (Erdős–Szekeres 1935)")
    ax.plot(kk, kk * np.log2(3.8), color=C[k], lw=2, label="upper ≈ 3.8ᵏ (2023–24)")
    ax.plot([3, 4], np.log2([6, 18]), "o", color=OLY, ms=8, mec=INK, label="known: R(3,3)=6, R(4,4)=18")
    ax.errorbar([5], [np.log2(44.5)], yerr=[[np.log2(44.5) - np.log2(43)], [np.log2(46) - np.log2(44.5)]],
                fmt="s", color=OLY, mec=INK, capsize=3)
    ax.set_xlabel("k")
    ax.set_ylabel("log₂ R(k, k)")
    ax.set_ylim(0, 62)
    ax.legend(loc="upper left", fontsize=7.6)
    plotstyle(ax)
    footer(fig)
    save(fig, "09-combinatorics-ladder.png")


# ---------------------------------------------------------------------------------------------
# 10 Inequalities → analysis
# ---------------------------------------------------------------------------------------------
def fig10():
    fig = figure("The analysis ladder: from comparing numbers to the infinite",
                 "Olympiad inequalities are the training ground of analysis — the mathematics of approximation, limits "
                 "and change that describes the physical universe", keys=("ana",))
    cs = cells(fig, 3, 3)
    k = "ana"

    ax = panel(fig, cs[0], 1, "Approaching without arriving", "primary / middle · Fibonacci 1202", k,
               "Ratios of Fibonacci numbers 2/1, 3/2, 5/3, 8/5, 13/8 … jump from side to side, closing in on the golden "
               "ratio φ = 1.618…: the first picture of a limit.")
    clean(ax, equal=False, xlim=(0.95, 2.1), ylim=(-1.2, 1.5))
    ax.plot([1, 2.05], [0, 0], color=INK, lw=1.2)
    for v in np.arange(1, 2.01, 0.1):
        ax.plot([v, v], [-0.05, 0.05], color=INK, lw=0.8)
        ax.text(v, -0.25, f"{v:.1f}", ha="center", fontsize=8)
    F = [1, 1]
    for _ in range(10):
        F.append(F[-1] + F[-2])
    phi = (1 + 5 ** 0.5) / 2
    for i in range(1, 9):
        r = F[i + 1] / F[i]
        y = 0.35 + (i % 2) * 0.45
        ax.plot([r, r], [0, y - 0.08], color=PAL[i % 6], lw=1)
        if i <= 5:
            ax.text(r, y, f"{F[i + 1]}/{F[i]}", ha="center", fontsize=9, color=PAL[i % 6])
    ax.plot(phi, 0, "o", color=OLY, ms=9, mec=INK)
    ax.text(phi, -0.7, "φ = 1.6180…", ha="center", fontsize=10, weight="bold", color=C[k])

    ax = panel(fig, cs[1], 2, "AM ≥ GM, seen in a circle", "middle / olympiad · Euclid VI.13", k,
               "On a diameter of length a + b, the half-chord at the split point has length √(ab) (geometric mean); "
               "the radius is (a + b)/2 (arithmetic mean). A half-chord can never exceed the radius. Here a = 4, b = 1.")
    a_, b_ = 4.0, 1.0
    R = (a_ + b_) / 2
    t = np.linspace(0, np.pi, 200)
    ax.plot(R * np.cos(t), R * np.sin(t), color=INK, lw=1.4)
    ax.plot([-R, R], [0, 0], color=INK)
    x0 = -R + a_
    g = np.sqrt(a_ * b_)
    ax.plot([x0, x0], [0, g], color=C[k], lw=3)
    ax.plot([0, 0], [0, R], color=C["nt"], lw=3)
    ax.text(x0 + 0.1, g / 2, f"√(ab) = {g:.1f}", fontsize=10, color=C[k], weight="bold")
    ax.text(-0.1, R * 0.55, f"(a+b)/2 = {R:.1f}", fontsize=10, color=C["nt"], weight="bold", ha="right")
    ax.text(-R + a_ / 2, -0.35, "a", ha="center", fontsize=11)
    ax.text(x0 + b_ / 2, -0.35, "b", ha="center", fontsize=11)
    clean(ax, xlim=(-R - 0.3, R + 0.3), ylim=(-0.6, R + 0.3))

    ax = panel(fig, cs[2], 3, "Optimisation", "olympiad · Heron, Dido's problem", k,
               "Among rectangles with perimeter 20, the area x(10 − x) is largest for the square x = 5 — AM-GM in "
               "disguise, and the first step towards calculus of variations.", plot=True)
    x = np.linspace(0, 10, 200)
    ax.plot(x, x * (10 - x), color=C[k], lw=2.5)
    for xv in (1.5, 3, 5, 7.5):
        ax.add_patch(Rectangle((xv - 0.05, 0), 0.1, xv * (10 - xv), fc=MUTED, alpha=0.5))
        ax.text(xv, xv * (10 - xv) + 1, f"{xv:g} × {10 - xv:g}", ha="center", fontsize=8)
    ax.plot(5, 25, "o", color=OLY, ms=9, mec=INK)
    ax.set_xlabel("width x")
    ax.set_ylabel("area")
    ax.set_ylim(0, 30)
    plotstyle(ax)

    ax = panel(fig, cs[3], 4, "Cauchy–Schwarz", "olympiad / university · Cauchy 1821, Schwarz 1888", k,
               "(a₁b₁ + a₂b₂)² ≤ (a₁² + a₂²)(b₁² + b₂²) says |u · v| ≤ |u||v|: a shadow is never longer than the stick. "
               "The same inequality holds in infinite-dimensional spaces — it underlies quantum uncertainty.")
    u = np.array([3.0, 1.0])
    v = np.array([1.5, 2.6])
    proj = np.dot(u, v) / np.dot(u, u) * u
    for vec, col, lab in [(u, C["nt"], "u"), (v, C[k], "v")]:
        ax.annotate("", xy=vec, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=col, lw=2.4))
        ax.text(*(vec * 1.06), lab, fontsize=12, weight="bold", color=col)
    ax.plot(*np.c_[v, proj], color=MUTED, ls="--")
    ax.plot(*np.c_[(0, 0), proj], color=C["comb"], lw=4, alpha=0.6)
    ax.text(proj[0] * 0.5, proj[1] * 0.5 - 0.35, "shadow of v", fontsize=9, color=C["comb"])
    ax.text(0.1, 2.9, f"u·v = {u @ v:.1f} ≤ |u||v| = {np.linalg.norm(u) * np.linalg.norm(v):.2f}", fontsize=10)
    clean(ax, xlim=(-0.3, 4.0), ylim=(-0.6, 3.3))

    ax = panel(fig, cs[4], 5, "Convexity & Jensen", "olympiad / university · Jensen 1906", k,
               "For a convex function the chord lies above the curve: f((x+y)/2) ≤ (f(x) + f(y))/2. One picture "
               "contains AM-GM, power-mean and many olympiad inequalities; in physics it gives entropy bounds.",
               plot=True)
    x = np.linspace(-0.5, 2.6, 200)
    f = np.exp
    ax.plot(x, f(x), color=C[k], lw=2.5, label="f(x) = eˣ")
    x1, x2 = 0.0, 2.2
    ax.plot([x1, x2], [f(x1), f(x2)], color=C["nt"], lw=1.8, label="chord")
    xm = (x1 + x2) / 2
    ax.plot([xm, xm], [f(xm), (f(x1) + f(x2)) / 2], color=C["comb"], lw=2.5, label="gap ≥ 0")
    ax.plot([x1, x2, xm, xm], [f(x1), f(x2), f(xm), (f(x1) + f(x2)) / 2], "o", color=INK, ms=4)
    ax.legend(loc="upper left", fontsize=8.5)
    plotstyle(ax)

    ax = panel(fig, cs[5], 6, "Infinite sums", "university · Oresme 1350, Euler 1734", k,
               "1 + 1/2 + 1/3 + … grows without bound (like ln n + 0.577), but 1 + 1/4 + 1/9 + … converges to π²/6 — "
               "Euler's Basel problem. Partial sums computed to n = 10⁵.", plot=True)
    n = np.arange(1, 100001)
    ax.semilogx(n, np.cumsum(1 / n), color=C["comb"], lw=2, label="Σ 1/k  (diverges)")
    ax.semilogx(n, np.cumsum(1 / n ** 2), color=C[k], lw=2.5, label="Σ 1/k²  → π²/6")
    ax.semilogx(n, np.log(n) + 0.5772, color=C["comb"], lw=1, ls=":", label="ln n + γ")
    ax.axhline(np.pi ** 2 / 6, color=C[k], ls="--", lw=1)
    ax.set_xlabel("number of terms n")
    ax.legend(loc="upper left", fontsize=8.5)
    plotstyle(ax)

    ax = panel(fig, cs[6], 7, "Taylor series", "university · Newton 1669, Taylor 1715", k,
               "Polynomials can imitate any smooth function: sin x ≈ x − x³/3! + x⁵/5! − … Each extra term hugs the "
               "curve over a wider range. Calculators and physics approximations work this way.", plot=True)
    x = np.linspace(-2 * np.pi, 2 * np.pi, 600)
    ax.plot(x, np.sin(x), color=INK, lw=3, label="sin x")
    for i, deg in enumerate([1, 3, 5, 7, 9, 11]):
        p = sum((-1) ** m * x ** (2 * m + 1) / factorial(2 * m + 1) for m in range((deg + 1) // 2))
        ax.plot(x, p, color=PAL[i], lw=1.4, label=f"degree {deg}")
    ax.set_ylim(-3.4, 2)
    ax.legend(loc="lower center", fontsize=7.5, ncol=4)
    plotstyle(ax)

    ax = panel(fig, cs[7], 8, "Fourier series", "university · Fourier 1807", k,
               "Any periodic signal is a sum of sine waves: square wave = (4/π)(sin x + sin 3x/3 + sin 5x/5 + …), "
               "shown with 1, 3, 10 and 50 terms. The 9% overshoot at jumps (Gibbs) never disappears.", plot=True)
    x = np.linspace(-np.pi, np.pi, 2000)
    ax.plot(x, np.sign(x), color=INK, lw=1.2, ls="--")
    for i, N_ in enumerate([1, 3, 10, 50]):
        s_ = sum(4 / np.pi * np.sin((2 * m + 1) * x) / (2 * m + 1) for m in range(N_))
        ax.plot(x, s_, color=PAL[i], lw=1.3, label=f"{N_} terms")
    ax.set_xticks([-np.pi, 0, np.pi])
    ax.set_xticklabels(["−π", "0", "π"])
    ax.legend(loc="upper left", fontsize=8, ncol=2)
    ax.set_ylim(-1.5, 1.6)
    plotstyle(ax)

    ax = panel(fig, cs[8], 9, "Partial differential equations", "Navier–Stokes: open",
               k, "The heat equation ∂u/∂t = ∂²u/∂x² smooths a jagged temperature profile (finite differences, "
               "computed). Whether the Navier–Stokes equations of fluids always stay smooth is a $1 000 000 "
               "Millennium problem.", plot=True)
    nx = 300
    x = np.linspace(0, 1, nx)
    u = ((x > 0.15) & (x < 0.35)).astype(float) + 0.6 * ((x > 0.55) & (x < 0.6)) + 0.4 * np.sin(18 * x) ** 8
    dx = x[1] - x[0]
    dt = 0.4 * dx ** 2
    times = [0, 0.0005, 0.002, 0.008, 0.03]
    t = 0.0
    for i, T_ in enumerate(times):
        while t < T_:
            u[1:-1] += dt / dx ** 2 * (u[2:] - 2 * u[1:-1] + u[:-2])
            t += dt
        ax.plot(x, u.copy(), color=PAL[i], lw=1.8, label=f"t = {T_}")
    ax.set_xlabel("position x")
    ax.set_ylabel("temperature u")
    ax.legend(loc="upper right", fontsize=8)
    plotstyle(ax)
    footer(fig)
    save(fig, "10-analysis-ladder.png")


# ---------------------------------------------------------------------------------------------
# 11 Probability
# ---------------------------------------------------------------------------------------------
def fig11():
    fig = figure("The probability ladder",
                 "From dice games to the laws of the universe: probability starts as careful counting and grows into "
                 "the language of statistical physics, quantum theory and data", keys=("prob",))
    cs = cells(fig, 3, 3)
    k = "prob"
    rng = np.random.default_rng(2026)

    ax = panel(fig, cs[0], 1, "Two dice", "primary / middle · Cardano 1564", k,
               "36 equally likely outcomes, coloured by their sum. Seven appears 6 times — the most likely total, "
               "probability 6/36 = 1/6. Probability starts as careful counting.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.03, ratios=[1, 1.1])
    from matplotlib import cm as cmm
    for i in range(6):
        for j in range(6):
            s_ = i + j + 2
            a1.add_patch(Rectangle((i, j), 0.94, 0.94, fc=cmm.viridis((s_ - 2) / 10), alpha=0.85))
            a1.text(i + 0.47, j + 0.47, str(s_), ha="center", va="center", fontsize=8.5,
                    color="white" if s_ < 9 else INK)
    clean(a1, xlim=(-0.1, 6), ylim=(-0.1, 6))
    sums = np.arange(2, 13)
    cnt = 6 - np.abs(sums - 7)
    a2.bar(sums, cnt, color=[cmm.viridis((s_ - 2) / 10) for s_ in sums])
    a2.set_xticks(sums)
    a2.tick_params(labelsize=7)
    a2.set_ylabel("ways", fontsize=8)
    plotstyle(a2)

    ax = panel(fig, cs[1], 2, "The Galton board", "high school · Galton 1889", k,
               "Each ball bounces left or right at 12 pegs. 4000 simulated balls pile up in the binomial shape C(12, k)/2¹² "
               "(line) — already close to the bell curve.", plot=True)
    rows = 12
    balls = rng.integers(0, 2, (4000, rows)).sum(1)
    ax.hist(balls, bins=np.arange(-0.5, rows + 1.5), color=lighten_(C[k], 0.5), ec=C[k])
    kk = np.arange(rows + 1)
    ax.plot(kk, [4000 * comb(rows, x) / 2 ** rows for x in kk], "o-", color=INK, ms=4, lw=1.2)
    ax.set_xlabel("number of 'right' bounces")
    ax.set_ylabel("balls")
    plotstyle(ax)

    ax = panel(fig, cs[2], 3, "Expected value & linearity", "olympiad · Montmort 1708", k,
               "n letters put into n envelopes at random: on average exactly 1 is in the right envelope, for every n — "
               "linearity of expectation. 20 000 random shuffles of 10 (bars) vs Poisson(1) (dots).", plot=True)
    n = 10
    fixed = np.array([np.sum(rng.permutation(n) == np.arange(n)) for _ in range(20000)])
    ax.hist(fixed, bins=np.arange(-0.5, 7.5), density=True, color=lighten_(C[k], 0.5), ec=C[k],
            label=f"simulation, mean {fixed.mean():.3f}")
    kk = np.arange(0, 7)
    ax.plot(kk, np.exp(-1) / np.array([factorial(x) for x in kk]), "o", color=INK, label="Poisson(1)")
    ax.set_xlabel("letters in the right envelope")
    ax.legend(loc="upper right", fontsize=8.5)
    plotstyle(ax)

    ax = panel(fig, cs[3], 4, "Conditional probability", "high school · Bayes 1763", k,
               "A disease affects 1% of people; the test catches 90% of cases but also flags 9% of healthy people. "
               "If you test positive, the chance you are ill is only 9 / (9 + 89) ≈ 9%. Intuition fails; trees don't.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    box(ax, 1.0, 5, "1000\npeople", fc=L[k], ec=C[k], fs=10)
    box(ax, 4.0, 8, "10 ill", fc="#f8e2db", ec=C["comb"], fs=10)
    box(ax, 4.0, 2, "990 healthy", fc="#e3f0e6", ec=C["geo"], fs=10)
    for (x, y, lab, col) in [(7.6, 9.0, "9 test +", C["comb"]), (7.6, 7.0, "1 test −", MUTED),
                             (7.6, 3.0, "89 test +", C["comb"]), (7.6, 1.0, "901 test −", MUTED)]:
        box(ax, x, y, lab, fc="white", ec=col, fs=9.5)
    for (p, q, lab) in [((1.8, 5.3), (3.3, 7.8), "1%"), ((1.8, 4.7), (3.0, 2.2), "99%"), ((4.7, 8.1), (6.8, 9.0), "90%"),
                        ((4.7, 7.9), (6.8, 7.0), "10%"), ((5.1, 2.1), (6.7, 3.0), "9%"), ((5.1, 1.9), (6.7, 1.0), "91%")]:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=MUTED, lw=1)
        ax.text((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 0.25, lab, fontsize=8.5, color=C[k], ha="center")
    ax.text(5.0, 5.0, "P(ill | +) = 9/98 ≈ 9%", fontsize=11.5, weight="bold", color=C["comb"], ha="center")

    ax = panel(fig, cs[4], 5, "Law of large numbers", "university · Bernoulli 1713", k,
               "Running fraction of heads in 6 simulated sequences of 10 000 coin flips. Early on anything happens; in "
               "the long run every sequence settles at 1/2, with fluctuations shrinking like 1/√n (dashed).",
               plot=True)
    nn = np.arange(1, 10001)
    for i in range(6):
        flips = rng.integers(0, 2, 10000)
        ax.semilogx(nn, np.cumsum(flips) / nn, color=PAL[i], lw=1)
    ax.semilogx(nn, 0.5 + 1 / np.sqrt(nn), color=INK, ls="--", lw=1)
    ax.semilogx(nn, 0.5 - 1 / np.sqrt(nn), color=INK, ls="--", lw=1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("number of flips")
    ax.set_ylabel("fraction of heads")
    plotstyle(ax)

    ax = panel(fig, cs[5], 6, "Random walks", "university · Pearson 1905, Einstein 1905", k,
               "Ten simulated walkers take ±1 steps. Their typical distance grows like √n (shaded: ±√n and ±2√n) — the "
               "law of diffusion, Brownian motion and the proof that atoms exist.", plot=True)
    steps = 1000
    for i in range(10):
        w_ = np.cumsum(rng.choice([-1, 1], steps))
        ax.plot(w_, color=PAL[i % 8], lw=0.9)
    t = np.arange(steps)
    ax.fill_between(t, -2 * np.sqrt(t), 2 * np.sqrt(t), color=lighten_(C[k], 0.85))
    ax.fill_between(t, -np.sqrt(t), np.sqrt(t), color=lighten_(C[k], 0.7))
    ax.set_xlabel("step n")
    ax.set_ylabel("position")
    plotstyle(ax)

    ax = panel(fig, cs[6], 7, "The central limit theorem", "university · de Moivre 1733, Laplace 1810", k,
               "Add n random numbers drawn uniformly from [0, 1]: n = 1 is flat, n = 2 a triangle, and by n = 12 the bell "
               "curve (line) appears. This is why measurement errors, heights and noise are normally distributed.", plot=True)
    axes = split(fig, ax, 4, "h", gap=0.012)
    for a_, n_ in zip(axes, [1, 2, 3, 12]):
        sm = rng.uniform(0, 1, (40000, n_)).sum(1)
        a_.hist(sm, bins=40, density=True, color=lighten_(C[k], 0.5), ec="none")
        xg = np.linspace(sm.min(), sm.max(), 200)
        mu, sd = n_ / 2, np.sqrt(n_ / 12)
        a_.plot(xg, np.exp(-(xg - mu) ** 2 / (2 * sd ** 2)) / (sd * np.sqrt(2 * np.pi)), color=INK, lw=1.3)
        a_.set_title(f"n = {n_}", fontsize=9)
        a_.set_yticks([])
        a_.tick_params(labelsize=7)
        plotstyle(a_, grid=False)

    ax = panel(fig, cs[7], 8, "Markov chains", "university · Markov 1906 · PageRank 1998", k,
               "A random surfer follows links (and with probability 15% jumps anywhere). The long-run share of time on "
               "each page — computed by power iteration — is its PageRank (circle size and number).")
    Pn = {0: (0, 1), 1: (1.2, 1.4), 2: (2.2, 0.6), 3: (1.2, -0.4), 4: (0.1, -0.3), 5: (2.4, -0.8)}
    links = {0: [1, 3], 1: [2], 2: [0, 3], 3: [0, 1, 2], 4: [0, 3], 5: [2, 3]}
    nP = len(Pn)
    M = np.zeros((nP, nP))
    for i, outs in links.items():
        for j in outs:
            M[j, i] = 1 / len(outs)
    r = np.ones(nP) / nP
    for _ in range(200):
        r = 0.85 * M @ r + 0.15 / nP
    for i, outs in links.items():
        for j in outs:
            ax.add_patch(FancyArrowPatch(Pn[i], Pn[j], arrowstyle="-|>", mutation_scale=11, color=MUTED, lw=1,
                                         connectionstyle="arc3,rad=0.15", shrinkA=16, shrinkB=16))
    for i, p in Pn.items():
        ax.add_patch(Circle(p, 0.14 + 0.9 * r[i], fc=C[k], alpha=0.75, ec="white"))
        ax.text(*p, f"{r[i]:.2f}", ha="center", va="center", fontsize=8.5, color="white", weight="bold")
    clean(ax, xlim=(-0.6, 3.0), ylim=(-1.2, 1.9))

    ax = panel(fig, cs[8], 9, "Random matrices", "frontier · Wigner 1955, Montgomery–Dyson 1972", k,
               "Eigenvalues of a large random symmetric matrix (GUE, n = 400, computed) fill a semicircle (left) and "
               "repel each other (right: spacing histogram vs Wigner's s²-law; Poisson dashed). Mysteriously, the zeros "
               "of the Riemann zeta function show the same statistics.", plot=True)
    a1, a2 = split(fig, ax, 2, "h", gap=0.04)
    n = 400
    X = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / np.sqrt(2)
    Hm = (X + X.conj().T) / np.sqrt(4 * n)
    ev = np.linalg.eigvalsh(Hm)
    a1.hist(ev, bins=40, density=True, color=lighten_(C[k], 0.5), ec="none")
    xg = np.linspace(-1, 1, 200)
    a1.plot(xg, 2 / np.pi * np.sqrt(1 - xg ** 2), color=INK, lw=1.4)
    a1.set_yticks([])
    a1.tick_params(labelsize=7)
    plotstyle(a1, grid=False)
    bulk = ev[(ev > -0.5) & (ev < 0.5)]
    dens = 2 / np.pi * np.sqrt(1 - bulk ** 2) * n
    sp = np.diff(bulk) * dens[:-1]
    a2.hist(sp, bins=25, range=(0, 3), density=True, color=lighten_(C[k], 0.5), ec="none")
    s_ = np.linspace(0, 3, 200)
    a2.plot(s_, 32 / np.pi ** 2 * s_ ** 2 * np.exp(-4 * s_ ** 2 / np.pi), color=INK, lw=1.4)
    a2.plot(s_, np.exp(-s_), color=C["comb"], lw=1.2, ls="--")
    a2.set_yticks([])
    a2.tick_params(labelsize=7)
    plotstyle(a2, grid=False)
    footer(fig)
    save(fig, "11-probability-ladder.png")


if __name__ == "__main__":
    for f in (fig06, fig07, fig08, fig09, fig10, fig11):
        f()
