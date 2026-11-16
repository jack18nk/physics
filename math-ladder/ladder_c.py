"""Math ladder 12-14: the map of modern mathematics, mathematics and the universe, a study path."""
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, Wedge

from style import C, GRID, INK, L, MUTED, OLY, STRAND, box, clean, figure, footer, lighten, panel, plotstyle, save

PHYS = "#c4512c"
MP = "#555555"


def _link(ax, ta, tb, color, lw=1.2, alpha=0.7, rad=0.0, style="-|>", ls="-", z=2):
    ax.add_patch(FancyArrowPatch(ta.get_position(), tb.get_position(), patchA=ta.get_bbox_patch(),
                                 patchB=tb.get_bbox_patch(),
                                 arrowstyle=f"{style},head_length=6,head_width=3" if style != "-" else "-",
                                 mutation_scale=1, color=color, lw=lw, alpha=alpha, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}", zorder=z))


# ---------------------------------------------------------------------------------------------
# 12 Map of modern mathematics
# ---------------------------------------------------------------------------------------------
def fig12():
    W, H = 24, 15.5
    fig = figure("The frontier: a map of modern mathematics",
                 "Major fields (bubbles) and their links. Green notes are recent breakthroughs; red notes are famous "
                 "open problems (★ = Millennium Prize, $1 000 000). Gold rings: fields that olympiad training enters "
                 "most directly", w=W, h=H, keys=("nt", "alg", "geo", "comb", "ana", "prob", "meta"), flow=False)
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.87])
    clean(ax, equal=False, xlim=(-6, 168), ylim=(0, 100))
    F = {
        "nt": (52, 66, "Number\ntheory", "nt", 7.5, True),
        "alg": (68, 52, "Algebra\n& groups", "alg", 6.5, True),
        "ag": (72, 78, "Algebraic\ngeometry", "alg", 6.8, False),
        "rep": (90, 64, "Representation\ntheory", "alg", 7.2, False),
        "top": (100, 84, "Topology", "geo", 6.3, False),
        "dg": (112, 62, "Differential\ngeometry", "geo", 7.0, True),
        "ana": (100, 38, "Analysis\n& PDE", "ana", 7.0, False),
        "dyn": (118, 22, "Dynamical\nsystems", "ana", 6.3, False),
        "prob": (80, 22, "Probability", "prob", 6.6, False),
        "comb": (52, 34, "Combinatorics", "comb", 7.0, True),
        "tcs": (34, 18, "Computer\nscience", "comb", 6.3, False),
        "logic": (32, 46, "Logic &\nfoundations", "meta", 6.0, False),
        "mp": (130, 44, "Mathematical\nphysics", None, 6.8, False),
    }
    E = [("nt", "ag"), ("nt", "rep"), ("ag", "rep"), ("ag", "top"), ("top", "dg"), ("dg", "ana"), ("ana", "prob"),
         ("prob", "comb"), ("comb", "nt"), ("comb", "tcs"), ("logic", "tcs"), ("ana", "nt"), ("rep", "mp"),
         ("dg", "mp"), ("ana", "dyn"), ("dyn", "nt"), ("prob", "mp"), ("alg", "nt"), ("alg", "ag"), ("alg", "rep"),
         ("alg", "top"), ("alg", "comb"), ("logic", "alg"), ("ana", "mp"), ("prob", "dyn"), ("top", "mp")]
    for a, b in E:
        xa, ya = F[a][:2]
        xb, yb = F[b][:2]
        ax.plot([xa, xb], [ya, yb], color="#cfc9bd", lw=2.2, zorder=1)
    for key, (x, y, lab, k, r, oly) in F.items():
        col = C[k] if k else MP
        ax.add_patch(Circle((x, y), r, fc=lighten(col, 0.7), ec=col, lw=2, zorder=3))
        if oly:
            ax.add_patch(Circle((x, y), r + 1.0, fc="none", ec=OLY, lw=3, zorder=3))
        ax.text(x, y, lab, ha="center", va="center", fontsize=13.5, weight="bold", color=INK, zorder=4,
                linespacing=1.05)
    notes = [
        ("nt", -4, 92, [("+", "Fermat's Last Theorem — Wiles 1995"), ("+", "bounded gaps between primes —"),
                        ("+", "   Zhang 2013, Maynard 2013"), ("−", "★ Riemann hypothesis"), ("−", "★ Birch–Swinnerton-Dyer"),
                        ("−", "twin primes, Goldbach")]),
        ("ag", 56, 99, [("−", "★ Hodge conjecture")]),
        ("rep", 76, 99, [("+", "geometric Langlands conjecture proved —"), ("+", "   Gaitsgory, Raskin et al. 2024"),
                         ("·", "Langlands program: bridges NT, rep. theory, geometry")]),
        ("top", 112, 99, [("+", "Poincaré conjecture — Perelman 2003"),
                          ("+", "Kervaire invariant problem — Hill, Hopkins, Ravenel 2009")]),
        ("mp", 138, 72, [("−", "★ Yang–Mills mass gap"), ("·", "mirror symmetry, string theory,"),
                         ("·", "quantum field theory made rigorous")]),
        ("ana", 104, 14, [("+", "sphere packing in 8 & 24 dimensions —"), ("+", "   Viazovska 2016 (Fields Medal 2022)"),
                          ("+", "Kakeya conjecture in 3-D — Wang & Zahl 2025"), ("−", "★ Navier–Stokes smoothness")]),
        ("comb", -4, 38, [("+", "primes contain arbitrarily long arithmetic"), ("+", "   progressions — Green–Tao 2004"),
                         ("+", "diagonal Ramsey bound improved — 2023"), ("+", "aperiodic 'hat' monotile — 2023"),
                         ("+", "sensitivity conjecture — Huang 2019")]),
        ("tcs", -4, 9, [("−", "★ P vs NP"), ("·", "proof assistants (Lean) verify modern proofs;"),
                       ("·", "AI systems reached IMO gold-medal level in 2025")]),
        ("dyn", 138, 16, [("−", "Collatz 3n + 1 problem"), ("·", "chaos, ergodic theory")]),
    ]
    colmap = {"+": "#2e7d32", "−": "#b71c1c", "·": MUTED}
    for key, x, y, items in notes:
        for i, (kind, txt) in enumerate(items):
            mark = {"+": "✔ ", "−": "? ", "·": "• "}[kind] if not txt.startswith("   ") else "   "
            ax.text(x, y - i * 2.7, mark + txt.strip() if not txt.startswith("   ") else "      " + txt.strip(),
                    fontsize=12, color=colmap[kind], va="top", zorder=5)
    ax.text(-4, 56, "Euclidean geometry, inequalities and\nfunctional equations from olympiads feed\n"
            "into algebra, analysis and geometry", fontsize=12, color=OLY, weight="bold", va="top")
    save(fig, "12-map-of-modern-mathematics.png")


# ---------------------------------------------------------------------------------------------
# 13 Mathematics and the universe
# ---------------------------------------------------------------------------------------------
def fig13():
    W, H = 22, 15
    fig = figure("Mathematics and the universe",
                 "\"The book of nature is written in the language of mathematics\" (Galileo, 1623). Each row: a branch of "
                 "mathematics, what it does, and the part of the universe or technology it describes",
                 w=W, h=H, keys=("nt", "alg", "geo", "comb", "ana", "prob", "meta"), flow=False)
    ax = fig.add_axes([0.01, 0.03, 0.98, 0.85])
    clean(ax, equal=False, xlim=(0, 100), ylim=(0, 100))
    for x, hd, col in [(14, "mathematics", INK), (50, "what it lets us do", MUTED), (84, "the universe & technology", PHYS)]:
        ax.text(x, 98.5, hd, ha="center", fontsize=14, weight="bold", color=col)
    rows = [
        ("ana", "calculus & differential\nequations", "predict change from local rules", "planets, rockets, bridges\n(Newton 1687)"),
        ("ana", "Fourier analysis", "split signals into waves", "sound, light, MRI scans,\nJPEG, mobile networks"),
        ("alg", "linear algebra &\nHilbert spaces", "superpose states, find eigenvalues",
         "quantum mechanics (1925),\nsearch engines"),
        ("alg", "group theory &\nrepresentations", "classify symmetries", "quarks and the Standard Model,\ncrystals"),
        ("geo", "Riemannian geometry", "measure curved spaces", "gravity, black holes, GPS,\nthe expanding universe"),
        ("geo", "topology", "find what survives deformation", "topological matter (Nobel 2016),\nknotted DNA"),
        ("prob", "probability &\nstatistics", "reason under uncertainty",
         "thermodynamics, quantum\nmeasurement, data science"),
        ("prob", "random processes", "model noise and diffusion", "Brownian motion → atoms exist (1905),\nfinance"),
        ("nt", "number theory", "build one-way functions", "RSA (1977) & elliptic-curve\ncryptography: secure internet"),
        ("comb", "graphs & combinatorics", "count and connect discrete things",
         "networks, logistics, chip\ndesign, algorithms"),
        ("ana", "dynamical systems\n& chaos", "understand long-term behaviour", "weather (Lorenz 1963),\nturbulence, orbits"),
        ("meta", "logic & computation", "mechanise reasoning", "computers (Turing 1936),\nartificial intelligence"),
        ("ana", "optimisation &\nconvex analysis", "find the best among infinitely many", "machine learning, economics,\nengineering design"),
    ]
    n = len(rows)
    T = {}
    for i, (k, m, how, uni) in enumerate(rows):
        y = 93 - i * (90 / n) - 2
        ax.add_patch(Rectangle((0.5, y - 3.1), 99, 6.2, fc=lighten(C[k], 0.9) if i % 2 == 0 else "white", ec="none"))
        t1 = box(ax, 14, y, m, fc=lighten(C[k], 0.8), ec=C[k], fs=13.5, pad=0.45, lw=1.5, linespacing=1.1, zorder=4,
                 weight="bold")
        ax.text(50, y, how, ha="center", va="center", fontsize=13.5, color="#3c3c3c", style="italic", zorder=4)
        t3 = box(ax, 84, y, uni, fc="#fbeee8", ec=PHYS, fs=13, pad=0.45, lw=1.3, linespacing=1.1, zorder=4)
        T[i] = (t1, t3)
        ax.annotate("", xy=(36, y), xytext=(28, y), arrowprops=dict(arrowstyle="-", color=C[k], lw=1.6))
        ax.annotate("", xy=(70, y), xytext=(64, y), arrowprops=dict(arrowstyle="-|>", color=C[k], lw=1.6))
    footer(fig, "\"The unreasonable effectiveness of mathematics in the natural sciences\" — Eugene Wigner, 1960.")
    save(fig, "13-mathematics-and-the-universe.png")


# ---------------------------------------------------------------------------------------------
# 14 A study path for parent and child
# ---------------------------------------------------------------------------------------------
def fig14():
    W, H = 22, 15.5
    fig = figure("A study path to climb together",
                 "Olympiad problems are excellent training — the aim is to use them to build ideas, not only to "
                 "collect problem types. A suggested route, balance and habit loop (rules of thumb, not rules)",
                 w=W, h=H, keys=("meta", "nt", "comb", "ana"), flow=False)
    top = 1 - 1.4 / H
    c1 = (0.02, 0.45, 0.96, top - 0.45)
    ax = panel(fig, c1, 1, "The route", "age →", "meta")
    clean(ax, equal=False, xlim=(4.5, 25.5), ylim=(0, 10))
    stages = [(6, 11, "primary"), (11, 14, "middle school"), (14, 18, "high school"), (18, 22, "university"),
              (22, 25.3, "graduate → research")]
    for i, (a, b, lab) in enumerate(stages):
        ax.add_patch(Rectangle((a, 0), b - a, 9.2, fc="#f3efe6" if i % 2 == 0 else "white", ec="none", zorder=0))
        ax.text((a + b) / 2, 9.55, lab, ha="center", fontsize=11.5, weight="bold")
    for age in range(6, 26, 2):
        ax.text(age, -0.35, str(age), ha="center", fontsize=9, color=MUTED)
    tracks = [
        ("school\nmathematics", 7.6, "ana", [
            (6, 11, "arithmetic, fractions, shapes, measurement"), (11, 14, "algebra, geometry proofs, primes"),
            (14, 18, "functions, trigonometry, calculus, probability"),
            (18, 22, "analysis, linear & abstract algebra, topology"), (22, 25.3, "specialise; first research")]),
        ("contests", 5.4, "comb", [
            (8, 12, "school & regional contests\n(e.g. Kangaroo, MATHCOUNTS, AMC 8)"),
            (12, 15, "junior olympiad\n(e.g. AMC 10/12, AIME)"),
            (15, 19, "national olympiad → IMO\n(e.g. 全国高中数学联赛 → CMO, USAMO)"),
            (19, 22.5, "Putnam, university contests,\nsummer research (REU)")]),
        ("reading &\nexploring", 3.0, "nt", [
            (6.5, 11, "The Number Devil (Enzensberger);\nBeast Academy"),
            (11, 14.5, "AoPS Introduction series;\nPólya: How to Solve It"),
            (14.5, 18.5, "Engel: Problem-Solving Strategies;\nZeitz: The Art and Craft of Problem Solving;\n"
                         "Courant & Robbins: What Is Mathematics?"),
            (18.5, 22.3, "Spivak: Calculus; Axler: Linear Algebra\nDone Right; Needham: Visual Complex\nAnalysis; "
                         "Aigner & Ziegler: Proofs from THE BOOK"),
            (22.3, 25.3, "Princeton Companion\nto Mathematics;\nQuanta Magazine")]),
        ("habit", 0.9, "meta", [(6, 25.3, "after every problem: name the idea, find a second solution, generalise, "
                                          "invent a variant — and keep an 'idea journal' together")]),
    ]
    for name, y, k, items in tracks:
        ax.text(4.6, y, name, fontsize=12, weight="bold", color=C[k], va="center")
        for a, b, txt in items:
            ax.add_patch(Rectangle((a + 0.06, y - 1.05), b - a - 0.12, 2.1, fc=lighten(C[k], 0.85), ec=C[k], lw=1.2,
                                   zorder=2))
            ax.text((a + b) / 2, y, txt, ha="center", va="center", fontsize=11.5 if len(txt) < 80 else 10.3, zorder=3,
                    linespacing=1.1)

    w3 = 0.96 / 3
    cB = (0.02, 0.03, w3 - 0.01, 0.39)
    cC = (0.02 + w3 + 0.005, 0.03, w3 - 0.01, 0.39)
    cD = (0.02 + 2 * w3 + 0.01, 0.03, w3 - 0.01, 0.39)
    ax = panel(fig, cB, 2, "How the balance shifts", "suggested share of study time", "meta",
               "Early on: concepts and play. In the olympiad years: more mixed problems and written proofs. At university "
               "the balance tilts back to theory — now built on the ideas the problems trained.", plot=True)
    ages = np.array([6, 8, 10, 12, 14, 16, 18, 20, 22])
    parts = [("understanding concepts", np.array([50, 45, 40, 35, 30, 28, 32, 40, 42]), C["ana"]),
             ("mixed problem solving", np.array([25, 30, 30, 33, 35, 35, 30, 22, 15]), C["comb"]),
             ("proof writing & reflection", np.array([5, 5, 10, 15, 20, 22, 23, 23, 23]), C["meta"]),
             ("exploring & reading for fun", np.array([20, 20, 20, 17, 15, 15, 15, 15, 20]), C["nt"])]
    ax.stackplot(ages, *[p[1] for p in parts], colors=[lighten(p[2], 0.35) for p in parts],
                 labels=[p[0] for p in parts], edgecolor="white")
    ax.set_xlim(6, 22)
    ax.set_ylim(0, 100)
    ax.set_xlabel("age")
    ax.set_ylabel("% of time")
    ax.legend(loc="upper center", fontsize=8.3, ncol=2, bbox_to_anchor=(0.5, 1.0), frameon=True, framealpha=0.85)
    plotstyle(ax, grid=False)

    ax = panel(fig, cD, 4, "A weekly rhythm", "example for the olympiad years", "meta",
               "Category drills alone hide the ideas. Mix in sessions organised by idea, unlabeled mixed sets (no hint "
               "which tool to use) and a weekly review of the idea journal — the step that turns practice into "
               "understanding.")
    sessions = [("topic study\nby category", 2, C["ana"]), ("practice\nby idea", 1.5, C["meta"]),
                ("mixed set,\nno labels", 1.5, C["comb"]), ("review\nidea journal", 1, OLY),
                ("explore\ntogether", 1, C["nt"])]
    tot = sum(s[1] for s in sessions)
    a0 = 90
    for lab, v, col in sessions:
        a1 = a0 - 360 * v / tot
        ax.add_patch(Wedge((0, 0), 1, a1, a0, width=0.42, fc=lighten(col, 0.25), ec="white", lw=2))
        mid = np.radians((a0 + a1) / 2)
        ax.text(1.32 * np.cos(mid), 1.22 * np.sin(mid), f"{lab}\n{v:g}×", ha="center", va="center", fontsize=9.3)
        a0 = a1
    ax.text(0, 0, f"{tot:g} sessions\nper week", ha="center", va="center", fontsize=10.5, weight="bold")
    clean(ax, xlim=(-1.9, 1.9), ylim=(-1.6, 1.6))

    ax = panel(fig, cC, 3, "After every problem: six questions", "the habit loop", "meta",
               "Asked together, these questions convert a solved problem into a reusable idea. They also make the "
               "parent a fellow learner rather than an examiner.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    qs = ["Which big idea cracked it?", "Where was I stuck, and what got me unstuck?", "Can I solve it a second way?",
          "What is the simplest case? The most general?", "Which earlier problem is secretly the same?",
          "Can I invent a new problem with this idea?"]
    for i, q in enumerate(qs):
        y = 9.2 - i * 1.6
        ax.add_patch(Circle((0.6, y), 0.42, fc=C["meta"], ec="none"))
        ax.text(0.6, y, str(i + 1), ha="center", va="center", fontsize=11, color="white", weight="bold")
        ax.text(1.35, y, q, va="center", fontsize=12.5)
    footer(fig, "Book and contest names are examples; choose those available in your country and language.")
    save(fig, "14-study-path-together.png")


if __name__ == "__main__":
    for f in (fig12, fig13, fig14):
        f()
