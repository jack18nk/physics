"""Math ladder 01-05: the big map, two ways to learn, olympiad→university bridge, toolbox, one idea at every level."""
from math import comb

import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

from style import (C, GRID, INK, L, MUTED, OLY, STRAND, arrow, box, cells, clean, clean3d, figure, footer, panel,
                   plotstyle, save, split)


def _link(ax, ta, tb, color, lw=1.0, alpha=0.6, rad=0.0, z=2):
    ax.add_patch(FancyArrowPatch(ta.get_position(), tb.get_position(), patchA=ta.get_bbox_patch(),
                                 patchB=tb.get_bbox_patch(),
                                 arrowstyle="-|>,head_length=6,head_width=3", mutation_scale=1, color=color, lw=lw,
                                 alpha=alpha, connectionstyle=f"arc3,rad={rad}", zorder=z))


# ---------------------------------------------------------------------------------------------
# 01 The big ladder
# ---------------------------------------------------------------------------------------------
def fig01():
    W, H = 24, 17
    fig = figure("The ladder of mathematics: from primary school to the research frontier",
                 "Six strands climb together. Arrows mean 'is needed for'; coloured arrows cross between strands. "
                 "★ gold boxes are the core olympiad topics — notice they sit exactly where school maths turns into "
                 "university maths", w=W, h=H, flow=False)
    ax = fig.add_axes([0.005, 0.01, 0.99, 0.885])
    ax.set_xlim(-14, 120)
    ax.set_ylim(0, 106)
    ax.axis("off")
    strands = ["nt", "alg", "geo", "comb", "ana", "prob"]
    stages = ["Primary\nage 6–11", "Middle school\n11–14", "High school\n& olympiad\n14–18", "Undergraduate",
              "Graduate", "Research\nfrontier"]
    rowh = 16.5
    for s, lab in enumerate(stages):
        y0 = s * rowh
        ax.add_patch(Rectangle((-14, y0), 134, rowh, fc="#f3efe6" if s % 2 == 0 else "#faf8f3", ec="none", zorder=0))
        ax.text(-13, y0 + rowh / 2, lab, fontsize=12, weight="bold", va="center", color=INK)
    ax.add_patch(Rectangle((-14, 2 * rowh), 134, rowh, fc="none", ec=OLY, lw=2.5, ls="--", zorder=1))
    ax.text(119.5, 3 * rowh - 1.2, "olympiad zone", ha="right", va="top", fontsize=10.5, color=OLY, weight="bold")
    for j, k in enumerate(strands):
        ax.text(j * 20 + 10, 104, STRAND[k][0], ha="center", va="center", fontsize=13.5, weight="bold", color=C[k])
        ax.plot([j * 20 + 10, j * 20 + 10], [0.5, 101.5], color=L[k], lw=8, zorder=0.5, solid_capstyle="round")

    N = {
        "p_cnt": (0, "nt", "counting & place value"), "p_fac": (0, "nt", "factors & multiples"),
        "p_par": (0, "nt", "even and odd"),
        "p_pat": (0, "alg", "patterns & sequences"), "p_eq": (0, "alg", "missing-number puzzles  □ + 3 = 7"),
        "p_area": (0, "geo", "shapes, area, perimeter"), "p_sym": (0, "geo", "symmetry & tilings"),
        "p_list": (0, "comb", "listing all cases"), "p_logic": (0, "comb", "logic puzzles"),
        "p_frac": (0, "ana", "fractions & decimals"), "p_line": (0, "ana", "the number line"),
        "p_chance": (0, "prob", "chance & data tables"),
        "m_prime": (1, "nt", "primes, gcd, lcm"), "m_rem": (1, "nt", "★ remainders & divisibility"),
        "m_lin": (1, "alg", "variables, linear equations"), "m_ratio": (1, "alg", "ratio & proportion"),
        "m_pyth": (1, "geo", "angles, triangles, Pythagoras"), "m_sim": (1, "geo", "congruence & similarity"),
        "m_perm": (1, "comb", "permutations & combinations"), "m_pig": (1, "comb", "★ pigeonhole & parity"),
        "m_irr": (1, "ana", "negative & irrational numbers"), "m_fun": (1, "ana", "functions & graphs"),
        "m_prob": (1, "prob", "probability = favourable / total"), "m_stat": (1, "prob", "mean, median, spread"),
        "h_mod": (2, "nt", "★ modular arithmetic,\nFermat & Euler"), "h_dio": (2, "nt", "★ Diophantine equations"),
        "h_poly": (2, "alg", "★ polynomials & Vieta"), "h_ineq": (2, "alg", "★ inequalities\nAM-GM, Cauchy"),
        "h_fe": (2, "alg", "★ functional equations"),
        "h_circ": (2, "geo", "★ circles, power of a point"), "h_trig": (2, "geo", "trigonometry & vectors"),
        "h_inv": (2, "geo", "★ transformations, inversion"),
        "h_ind": (2, "comb", "★ induction & recursion"), "h_inv2": (2, "comb", "★ invariants & extremal"),
        "h_graph": (2, "comb", "★ graphs, double counting"),
        "h_lim": (2, "ana", "sequences & limits"), "h_calc": (2, "ana", "calculus"),
        "h_exp": (2, "prob", "★ expectation, binomial"), "h_cond": (2, "prob", "conditional probability"),
        "u_ant": (3, "nt", "algebraic NT basics\n(ℤ[i], quadratic forms)"), "u_crypt": (3, "nt", "cryptography"),
        "u_la": (3, "alg", "linear algebra"), "u_grp": (3, "alg", "groups, rings, fields"),
        "u_gal": (3, "alg", "Galois theory"),
        "u_proj": (3, "geo", "projective geometry"), "u_dg": (3, "geo", "curves & surfaces"),
        "u_top": (3, "geo", "topology"),
        "u_gt": (3, "comb", "graph theory"), "u_gf": (3, "comb", "generating functions"),
        "u_ra": (3, "ana", "real analysis"), "u_ca": (3, "ana", "complex analysis"),
        "u_ode": (3, "ana", "differential equations"),
        "u_pt": (3, "prob", "probability theory"), "u_st": (3, "prob", "statistics"),
        "g_ant": (4, "nt", "analytic number theory"), "g_alnt": (4, "nt", "algebraic number theory"),
        "g_rep": (4, "alg", "representation theory"), "g_comm": (4, "alg", "commutative algebra"),
        "g_riem": (4, "geo", "Riemannian geometry"), "g_at": (4, "geo", "algebraic topology"),
        "g_ag": (4, "geo", "algebraic geometry"),
        "g_ext": (4, "comb", "extremal & probabilistic\ncombinatorics"), "g_add": (4, "comb", "additive combinatorics"),
        "g_meas": (4, "ana", "measure theory"), "g_fa": (4, "ana", "functional analysis"), "g_pde": (4, "ana", "PDE"),
        "g_sto": (4, "prob", "stochastic processes"),
        "f_rh": (5, "nt", "Riemann hypothesis (open)"), "f_lang": (5, "nt", "Langlands program"),
        "f_glang": (5, "alg", "geometric Langlands\n(proved 2024)"),
        "f_poinc": (5, "geo", "Poincaré conjecture\n(Perelman 2003)"), "f_mirror": (5, "geo", "mirror symmetry"),
        "f_ramsey": (5, "comb", "Ramsey bounds (2023)"), "f_pnp": (5, "comb", "P vs NP (open)"),
        "f_gt": (5, "comb", "primes in progressions\n(Green–Tao 2004)"),
        "f_ns": (5, "ana", "Navier–Stokes (open)"), "f_kak": (5, "ana", "Kakeya in 3-D (2025)"),
        "f_rmt": (5, "prob", "random matrices ↔ zeta zeros"), "f_sle": (5, "prob", "SLE & critical phenomena"),
    }
    groups = {}
    for key, (s, k, lab) in N.items():
        groups.setdefault((s, k), []).append(key)
    T = {}
    for (s, k), keys in groups.items():
        n = len(keys)
        step = 5.0 if n == 3 else 6.4
        for i, key in enumerate(keys):
            x = strands.index(k) * 20 + 10
            y = s * rowh + rowh / 2 + (n - 1) * step / 2 - i * step
            lab = N[key][2]
            star = lab.startswith("★")
            T[key] = ax.text(x, y, lab, ha="center", va="center", fontsize=12.2, zorder=5, linespacing=1.05,
                             weight="bold" if star else "normal",
                             bbox=dict(boxstyle="round,pad=0.42", fc="#fff6d6" if star else "white",
                                       ec=OLY if star else C[k], lw=2.0 if star else 1.1))
    E = ("p_cnt-p_fac p_fac-m_prime p_par-m_rem p_fac-p_frac m_prime-h_mod m_rem-h_mod h_mod-h_dio h_mod-u_ant "
         "h_dio-u_ant h_mod-u_crypt u_ant-g_alnt u_ant-g_ant g_ant-f_rh g_alnt-f_lang u_ca-g_ant u_grp-u_ant "
         "u_gal-g_alnt "
         "p_pat-m_lin p_eq-m_lin m_ratio-m_lin m_lin-h_poly m_lin-h_fe h_poly-u_gal m_lin-u_la u_la-u_grp u_grp-u_gal "
         "u_la-g_rep u_grp-g_rep u_grp-g_comm g_rep-f_lang g_rep-f_glang g_comm-g_ag "
         "p_area-m_pyth p_sym-m_sim m_pyth-h_trig m_sim-h_circ h_circ-h_inv h_trig-u_dg h_inv-u_proj u_proj-g_ag "
         "u_dg-g_riem u_top-g_at g_riem-f_poinc g_at-f_poinc g_ag-f_mirror p_sym-u_grp "
         "p_list-m_perm p_logic-m_pig m_perm-h_graph m_pig-h_inv2 p_pat-h_ind h_graph-u_gt h_ind-u_gf m_perm-u_gf "
         "u_gt-g_ext g_ext-f_ramsey g_add-f_gt g_ant-f_gt u_gt-f_pnp h_inv2-u_top "
         "p_line-m_irr p_frac-m_irr m_irr-h_lim m_fun-h_calc h_lim-h_calc h_lim-u_ra h_calc-u_ode h_calc-u_ca "
         "u_ra-g_meas u_ra-g_fa u_ode-g_pde g_pde-f_ns g_meas-f_kak h_ineq-u_ra m_lin-m_fun "
         "p_chance-m_prob m_prob-h_exp h_exp-h_cond h_cond-u_pt m_stat-u_st m_perm-m_prob u_pt-g_sto g_meas-g_sto "
         "g_sto-f_sle g_sto-f_rmt g_ant-f_rmt h_exp-g_ext g_add-g_ext h_dio-g_ag").split()
    for e in E:
        a, b = e.split("-")
        ka, kb = N[a][1], N[b][1]
        cross = ka != kb
        _link(ax, T[a], T[b], C[ka] if cross else "#8f8a80", lw=1.5 if cross else 1.0,
              alpha=0.85 if cross else 0.55, rad=0.12 if cross else 0.0)
    save(fig, "01-ladder-of-mathematics.png")


# ---------------------------------------------------------------------------------------------
# 02 Two ways to learn from the same problems
# ---------------------------------------------------------------------------------------------
IDEAS = ["invariants &\ncolouring", "symmetry", "extremal\nprinciple", "induction &\nrecursion", "pigeonhole",
         "double\ncounting", "parity &\nmodular", "change of\nviewpoint", "convexity &\nsmoothing"]
PROBLEMS = [
    ("last digit of 7²⁰²⁶", "nt", [6]), ("x² + y² ≠ 4k + 3", "nt", [6]), ("gcd of Fibonacci numbers", "nt", [3, 0]),
    ("infinitely many primes", "nt", [2]), ("n² + n is even", "nt", [6]),
    ("AM-GM inequality", "alg", [8, 1]), ("f(x + y) = f(x) + f(y)", "alg", [3, 7]), ("roots of a cubic", "alg", [1]),
    ("1 + 2 + … + 100", "alg", [1, 5]), ("telescoping sums", "alg", [7]),
    ("angle chasing", "geo", [0]), ("shortest path via reflection", "geo", [7, 1]), ("area ratios", "geo", [0]),
    ("inversion problems", "geo", [7]), ("max area, fixed perimeter", "geo", [8, 2]),
    ("domino tilings", "comb", [0, 6]), ("handshake lemma", "comb", [5, 6]), ("socks in a drawer", "comb", [4]),
    ("who wins this game?", "comb", [0, 3]), ("6 people, 3 friends", "comb", [4, 2]),
]
CAT = [("nt", "Number theory"), ("alg", "Algebra"), ("geo", "Geometry"), ("comb", "Combinatorics")]


def fig02():
    W, H = 22, 15
    fig = figure("Same problems, two ways of learning",
                 "Collecting problem types (left) is how most contest training starts. Understanding comes when the "
                 "types are reorganised around a small number of reusable ideas (right)",
                 w=W, h=H, keys=("nt", "alg", "geo", "comb", "meta"), flow=False)
    top, mid = 1 - 1.4 / H, 0.43
    cA = (0.02, mid + 0.02, 0.37, top - mid - 0.02)
    cB = (0.40, mid + 0.02, 0.58, top - mid - 0.02)
    cC = (0.02, 0.03, 0.96, mid - 0.04)
    ax = panel(fig, cA, "A", "A catalogue of problem types", "how drilling looks", "comb",
               "Each category is a list of templates. Fast on familiar problems; brittle on new ones, because the "
               "links between categories stay invisible.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    for j, (k, name) in enumerate(CAT):
        x0, y0 = (0.2 + (j % 2) * 5.0, 5.2 - (j // 2) * 5.0)
        ax.add_patch(Rectangle((x0, y0), 4.6, 4.6, fc=L[k], ec=C[k], lw=1.4))
        ax.text(x0 + 2.3, y0 + 4.2, name, ha="center", fontsize=11, weight="bold", color=C[k])
        probs = [p for p in PROBLEMS if p[1] == k]
        for i, (lab, _, _) in enumerate(probs):
            ax.text(x0 + 0.25, y0 + 3.45 - i * 0.74, "▪ " + lab, fontsize=10.5, va="center")

    ax = panel(fig, cB, "B", "The same problems, organised by ideas", "how understanding looks", "meta",
               "Nine ideas power all twenty problems. A child who owns 'invariant' or 'double counting' can attack a "
               "problem type he has never seen — and he will meet these same ideas again in university mathematics.")
    clean(ax, xlim=(-1.55, 1.55), ylim=(-1.12, 1.12))
    ia = np.linspace(np.pi / 2, np.pi / 2 - 2 * np.pi, len(IDEAS), endpoint=False)
    ipos = [(0.68 * np.cos(a), 0.52 * np.sin(a)) for a in ia]
    pa = np.linspace(np.pi / 2 + 0.12, np.pi / 2 + 0.12 - 2 * np.pi, len(PROBLEMS), endpoint=False)
    order = sorted(range(len(PROBLEMS)), key=lambda i: np.mean(PROBLEMS[i][2]) * 10 + i * 0.01)
    ppos = {}
    for slot, i in enumerate(order):
        a = pa[slot]
        ppos[i] = (1.38 * np.cos(a), 1.0 * np.sin(a))
    for i, (lab, k, ids) in enumerate(PROBLEMS):
        for idx in ids:
            ax.plot([ppos[i][0], ipos[idx][0]], [ppos[i][1], ipos[idx][1]], color=C[k], lw=1.1, alpha=0.55,
                    zorder=1)
    for i, (lab, k, ids) in enumerate(PROBLEMS):
        x, y = ppos[i]
        ax.text(x, y, lab, ha="center", va="center", fontsize=8.6, zorder=3,
                bbox=dict(boxstyle="round,pad=0.25", fc=L[k], ec=C[k], lw=1))
    for idx, (x, y) in enumerate(ipos):
        ax.text(x, y, IDEAS[idx], ha="center", va="center", fontsize=9.2, weight="bold", color="white", zorder=4,
                linespacing=1.0, bbox=dict(boxstyle="circle,pad=0.25", fc=C["meta"], ec="white", lw=1.5))

    ax = panel(fig, cC, "C", "Which big ideas power which olympiad categories — and where they live on",
               "typical frequency, author's estimate", "meta",
               "Read a row to see one idea travel through every category; read the last column to see the "
               "university mathematics it grows into. Training by idea (rows) as well as by category (columns) gives "
               "both exam coverage and real understanding.")
    M = np.array([[2, 2, 3, 3], [1, 3, 3, 2], [2, 2, 1, 3], [2, 3, 1, 3], [2, 1, 1, 3], [1, 2, 1, 3],
                  [3, 1, 0, 2], [2, 2, 3, 2], [0, 3, 1, 1]])
    grown = ["conserved quantities, homology, topological invariants", "group theory, Galois theory, Noether's theorem",
             "variational methods, compactness, optimisation", "recursion theory, dynamic programming, generating functions",
             "Ramsey theory, Dirichlet approximation, compactness", "Fubini's theorem, linear algebra (trace), Burnside",
             "ring theory, finite fields, cryptography", "inversion → Möbius maps; coordinates → algebraic geometry",
             "convex analysis, Jensen, machine-learning optimisation"]
    clean(ax, equal=False, xlim=(-0.5, 12.5), ylim=(9.4, -0.9))
    for j, (k, name) in enumerate(CAT):
        ax.text(2.6 + j * 1.25, -0.5, name, ha="center", fontsize=10, weight="bold", color=C[k])
    ax.text(8.0, -0.5, "grows into (university and beyond)", fontsize=10, weight="bold", color=C["meta"])
    for i, idea in enumerate(IDEAS):
        ax.add_patch(Rectangle((-0.45, i - 0.45), 12.9, 0.9, fc="#f7f4ee" if i % 2 == 0 else "white", ec="none"))
        ax.text(-0.3, i, idea.replace("\n", " "), va="center", fontsize=10, weight="bold", color=INK)
        for j, (k, _) in enumerate(CAT):
            v = M[i, j]
            if v:
                ax.scatter(2.6 + j * 1.25, i, s=60 + 110 * v, color=C[k], alpha=0.3 + 0.23 * v, lw=0)
        ax.text(8.0, i, grown[i], va="center", fontsize=9.6, color="#3c3c3c")
    save(fig, "02-two-ways-of-learning.png")


# ---------------------------------------------------------------------------------------------
# 03 Olympiad → university bridge
# ---------------------------------------------------------------------------------------------
def fig03():
    W, H = 22, 15.5
    fig = figure("Every olympiad trick is a small window onto a big theory",
                 "Read each row left to right: a contest technique, the general fact behind it, the university subject "
                 "where it is fully developed, and where it leads today", w=W, h=H,
                 keys=("nt", "alg", "geo", "comb"), flow=True, flow_labels=("olympiad", "frontier"))
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.86])
    clean(ax, equal=False, xlim=(0, 100), ylim=(0, 100))
    heads = ["olympiad technique", "the general idea behind it", "university subject", "where it leads"]
    xs = [12, 37, 62, 87]
    for x, hd in zip(xs, heads):
        ax.text(x, 98.5, hd, ha="center", fontsize=13, weight="bold", color=INK)
    rows = [
        ("nt", "Fermat's little theorem\naᵖ ≡ a (mod p)", "Lagrange: the order of an element\ndivides the size of a group",
         "group theory", "RSA & elliptic-curve\ncryptography"),
        ("nt", "p = x² + y²  ⇔  p = 2 or\np ≡ 1 (mod 4)", "unique factorisation in the\nGaussian integers ℤ[i]",
         "algebraic number theory", "Fermat's Last Theorem\n(Wiles 1995)"),
        ("nt", "Pell equation x² − 2y² = 1", "units of ℤ[√2], continued\nfractions", "Diophantine geometry",
         "Langlands program"),
        ("alg", "Vieta's formulas", "symmetric polynomials", "Galois theory",
         "why no formula for the quintic;\nfield theory"),
        ("alg", "AM-GM, Jensen, smoothing", "convexity", "convex analysis,\noptimisation",
         "machine learning, economics"),
        ("alg", "Cauchy's equation\nf(x + y) = f(x) + f(y)", "linear maps", "linear algebra,\nfunctional analysis",
         "quantum mechanics\n(Hilbert space)"),
        ("geo", "angle chasing, cyclic\nquadrilaterals", "what stays unchanged under\nmotions",
         "Klein: geometry = invariants\nof a transformation group", "gauge symmetry in physics"),
        ("geo", "inversion, Pascal's theorem", "Möbius & projective maps", "projective & algebraic\ngeometry",
         "mirror symmetry,\nstring theory"),
        ("geo", "complex numbers & vectors\nin geometry", "shapes become equations", "differential geometry",
         "general relativity"),
        ("comb", "colouring & invariant\narguments", "conserved quantities",
         "algebraic topology\n(Euler characteristic, homology)", "topological phases of matter\n(Nobel 2016)"),
        ("comb", "pigeonhole, the 6-people\nparty problem", "large structures must contain\norder",
         "Ramsey theory,\nextremal graph theory", "Ramsey bounds (2023);\nnetwork science"),
        ("comb", "recursions & generating\nfunctions", "power series encode sequences", "analytic combinatorics",
         "statistical physics,\nanalysis of algorithms"),
        ("comb", "double counting, averaging", "expected value proves existence", "probabilistic method",
         "random graphs, computer\nscience"),
    ]
    n = len(rows)
    for i, (k, *cols) in enumerate(rows):
        y = 94 - i * (91 / n) - 3
        ax.add_patch(Rectangle((0.5, y - 3.2), 99, 6.4, fc=L[k] if i % 2 == 0 else "white", ec="none", alpha=0.6))
        prev = None
        for j, (x, txt) in enumerate(zip(xs, cols)):
            t = box(ax, x, y, txt, fc="#fff6d6" if j == 0 else "white", ec=OLY if j == 0 else C[k], fs=12,
                    pad=0.45, lw=1.8 if j == 0 else 1.1, linespacing=1.1, zorder=4)
            if prev is not None:
                _link(ax, prev, t, C[k], lw=1.6, alpha=0.9, z=3)
            prev = t
    footer(fig, "Arrows mean 'is a special case of' / 'leads to'. Topics chosen to match common olympiad categories.")
    save(fig, "03-olympiad-to-university-bridge.png")


# ---------------------------------------------------------------------------------------------
# 04 Problem-solving toolbox
# ---------------------------------------------------------------------------------------------
def fig04():
    fig = figure("The problem-solver's toolbox",
                 "Heuristics that work across every category. Each panel shows one move on a classic problem — try "
                 "them together, then ask 'which move did I use?' after every problem",
                 keys=("meta", "nt", "alg", "geo", "comb"), flow=True, flow_labels=("first moves", "deeper moves"))
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Pólya's four steps", "Pólya, How to Solve It, 1945", "meta",
               "Understand → plan → carry out → look back. Most children skip the first and the last step; the last "
               "step ('what did I learn? can I use it elsewhere?') is where understanding is built.")
    clean(ax, xlim=(-1.6, 1.6), ylim=(-1.25, 1.25))
    steps = ["1 understand\nwhat is given?\nwhat is asked?", "2 plan\nseen something\nsimilar?",
             "3 carry out\ncheck each step", "4 look back\nother method?\ngeneralise?"]
    angs = [np.pi / 2, 0, -np.pi / 2, np.pi]
    pos = [(1.0 * np.cos(a), 0.82 * np.sin(a)) for a in angs]
    for a in angs:
        a0, a1 = a - 0.5, a - np.pi / 2 + 0.5
        arrow(ax, (1.0 * np.cos(a0), 0.82 * np.sin(a0)), (1.0 * np.cos(a1), 0.82 * np.sin(a1)), color=C["meta"],
              lw=2.2, rad=-0.25, hl=10, hw=5)
    for (x, y), s in zip(pos, steps):
        box(ax, x, y, s, fc=L["meta"], ec=C["meta"], fs=9, pad=0.35, linespacing=1.1, zorder=4)

    ax = panel(fig, cs[1], 2, "Try small cases", "find the pattern, then prove it", "comb",
               "How many regions do n lines in general position make? Draw n = 0 … 4: 1, 2, 4, 7, 11. The jumps are "
               "1, 2, 3, 4 — the n-th line crosses n − 1 lines and adds n regions, so R(n) = 1 + n(n + 1)/2.")
    axes = split(fig, ax, 5, "h", gap=0.006)
    rng = np.random.default_rng(3)
    lines = [(0.3, 0.5), (-0.8, 0.2), (2.0, -0.3), (-0.15, -0.35)]
    for n, a in enumerate(axes):
        a.add_patch(Rectangle((-1, -1), 2, 2, fc=L["comb"], ec=C["comb"], lw=1))
        x = np.linspace(-1, 1, 10)
        for m, c in lines[:n]:
            a.plot(x, m * x + c, color=C["comb"], lw=1.6)
        a.text(0, -1.35, f"n = {n}\n{1 + n * (n + 1) // 2} regions", ha="center", va="top", fontsize=9)
        clean(a, xlim=(-1.05, 1.05), ylim=(-2.2, 1.05))

    ax = panel(fig, cs[2], 3, "Draw a picture", "turn words into a graph", "comb",
               "'Six people each shake hands once with everyone else — how many handshakes?' Drawn as a graph: 6 dots, "
               "each with 5 lines, every line counted twice: 6 × 5 / 2 = 15.")
    th = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, 7)[:-1]
    P = np.c_[np.cos(th), np.sin(th)]
    for i in range(6):
        for j in range(i + 1, 6):
            ax.plot(*P[[i, j]].T, color=C["comb"], lw=1.4, alpha=0.75)
    for i, p in enumerate(P):
        ax.add_patch(Circle(p, 0.12, fc="white", ec=INK, lw=1.4, zorder=3))
        ax.text(*p, "ABCDEF"[i], ha="center", va="center", fontsize=9, zorder=4)
    ax.text(1.6, 0, "15\nlines", fontsize=13, weight="bold", color=C["comb"], va="center")
    clean(ax, xlim=(-1.3, 2.3), ylim=(-1.2, 1.2))

    ax = panel(fig, cs[3], 4, "Use symmetry (pairing)", "Gauss at age 8 (legend)", "alg",
               "1 + 2 + … + 100: pair the first with the last. Every pair sums to 101 and there are 50 pairs, so the "
               "total is 5050. Symmetry turns a long computation into one multiplication.")
    clean(ax, equal=False, xlim=(0, 10.6), ylim=(0, 4))
    nums = [1, 2, 3, 4, 5, "…", 96, 97, 98, 99, 100]
    for i, v in enumerate(nums):
        ax.text(0.5 + i * 0.95, 2.0, str(v), ha="center", va="center", fontsize=11, weight="bold")
    for i in range(5):
        x1, x2 = 0.5 + i * 0.95, 0.5 + (10 - i) * 0.95
        ax.add_patch(FancyArrowPatch((x1, 2.35), (x2, 2.35), connectionstyle=f"arc3,rad=-{0.35 - i * 0.02}",
                                     arrowstyle="-", color=PALETTE_I[i], lw=1.5))
        ax.text((x1 + x2) / 2, 2.6 + (5 - i) * 0.25, "101", ha="center", fontsize=8, color=PALETTE_I[i])
    ax.text(5.25, 0.8, "50 pairs × 101 = 5050", ha="center", fontsize=13, color=C["alg"], weight="bold")

    ax = panel(fig, cs[4], 5, "Work backwards", "start from the end", "comb",
               "21 counters; players alternately take 1, 2 or 3; whoever takes the last one wins. From the end: 0 left "
               "is a loss for the player to move, so 4, 8, 12, 16, 20 are losing too. Take 1 and keep the opponent "
               "on multiples of 4.")
    clean(ax, xlim=(-0.8, 21.8), ylim=(-2.4, 2.6))
    lose = [n % 4 == 0 for n in range(22)]
    for n in range(22):
        ax.add_patch(Circle((n, 0), 0.44, fc=C["comb"] if lose[n] else "white", ec=C["comb"], lw=1.2))
        ax.text(n, 0, str(n), ha="center", va="center", fontsize=8, color="white" if lose[n] else INK)
    for n in (1, 2, 3):
        ax.add_patch(FancyArrowPatch((8, 0.5), (8 - n, 0.5), connectionstyle="arc3,rad=-1.2", arrowstyle="-|>",
                                     mutation_scale=8, color=MUTED, lw=0.9, shrinkA=2, shrinkB=2))
    ax.text(7.0, 1.9, "every move from 8 hands the\nopponent a winning position", ha="center", fontsize=8.5,
            color=MUTED)
    ax.text(21, -1.1, "start: take 1 → 20", ha="right", fontsize=9, color=C["comb"])
    ax.text(0, -1.1, "■ losing for the player to move", fontsize=9, color=C["comb"])

    ax = panel(fig, cs[5], 6, "Find an invariant", "colouring argument", "comb",
               "Remove two opposite corners of a chessboard. Can 31 dominoes cover the rest? Every domino covers one "
               "black and one white square, but 32 white and only 30 black squares remain. Impossible — no trial and "
               "error needed.")
    for i in range(8):
        for j in range(8):
            if (i, j) in [(0, 0), (7, 7)]:
                ax.add_patch(Rectangle((i, j), 1, 1, fc="none", ec=GRID, ls=":", lw=1))
                ax.text(i + 0.5, j + 0.5, "×", ha="center", va="center", fontsize=12, color=C["comb"])
                continue
            ax.add_patch(Rectangle((i, j), 1, 1, fc="#3a3a3a" if (i + j) % 2 == 0 else "#f4efe5", ec="none"))
    for (i, j, horiz) in [(1, 0, True), (3, 0, True), (0, 1, False), (5, 2, True)]:
        ax.add_patch(Rectangle((i + 0.1, j + 0.1), (1.8 if horiz else 0.8), (0.8 if horiz else 1.8),
                               fc=C["comb"], alpha=0.85, ec="white", lw=1.2))
    ax.text(8.5, 5, "black: 30\nwhite: 32", fontsize=11, va="center", weight="bold")
    clean(ax, xlim=(-0.2, 11.5), ylim=(-0.2, 8.2))

    ax = panel(fig, cs[6], 7, "Use the extremal principle", "look at the largest / smallest", "geo",
               "An odd number of children stand at different distances; each throws a water balloon at the nearest "
               "child. Someone stays dry! Look at the closest pair: they throw at each other (thick line). Computed "
               "for 9 random children; the dry one is circled.")
    rng = np.random.default_rng(4)
    Pt = (np.array([(i, j) for i in range(3) for j in range(3)]) + rng.uniform(0.1, 0.9, (9, 2))) / 3
    D = np.linalg.norm(Pt[:, None] - Pt[None], axis=2) + np.eye(9) * 9
    tgt = D.argmin(1)
    hit = np.zeros(9, int)
    for i, t in enumerate(tgt):
        hit[t] += 1
        lw = 3 if tgt[t] == i else 1.2
        ax.add_patch(FancyArrowPatch(Pt[i], Pt[t], arrowstyle="-|>", mutation_scale=10, color=C["geo"], lw=lw,
                                     shrinkA=7, shrinkB=7))
    for i, p in enumerate(Pt):
        ax.add_patch(Circle(p, 0.022, fc=INK, zorder=4))
        if hit[i] == 0:
            ax.add_patch(Circle(p, 0.06, fc="none", ec=C["comb"], lw=2.2))
    clean(ax, xlim=(-0.08, 1.08), ylim=(-0.08, 1.08))

    ax = panel(fig, cs[7], 8, "Pigeonhole principle", "Dirichlet 1834", "nt",
               "Place 5 points in a unit square. Two of them are at most √2/2 ≈ 0.707 apart: cut the square into 4 "
               "small squares (boxes) — 5 points (pigeons) force two into one box.")
    rng = np.random.default_rng(5)
    Q = rng.uniform(0.04, 0.96, (5, 2))
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec=INK, lw=1.5))
    ax.plot([0.5, 0.5], [0, 1], color=C["nt"], ls="--")
    ax.plot([0, 1], [0.5, 0.5], color=C["nt"], ls="--")
    cellid = (Q[:, 0] > 0.5).astype(int) + 2 * (Q[:, 1] > 0.5)
    for c in range(4):
        idx = np.where(cellid == c)[0]
        if len(idx) >= 2:
            ax.add_patch(Rectangle(((c % 2) * 0.5, (c // 2) * 0.5), 0.5, 0.5, fc=L["nt"], ec="none", zorder=0.5))
            a, b = Q[idx[0]], Q[idx[1]]
            ax.plot([a[0], b[0]], [a[1], b[1]], color=C["comb"], lw=2)
            ax.text(1.08, 0.5, f"distance\n{np.linalg.norm(a - b):.3f} ≤ 0.707", fontsize=10, va="center")
            break
    ax.scatter(Q[:, 0], Q[:, 1], s=55, color=INK, zorder=4)
    clean(ax, xlim=(-0.05, 1.75), ylim=(-0.05, 1.05))

    ax = panel(fig, cs[8], 9, "Generalise & look back", "from a line of numbers to a pyramid", "alg",
               "After 1 + … + n = n(n + 1)/2, ask the next question: what about 1² + 2² + … + n²? Stack squares into "
               "a pyramid; three pyramids fit into an n × (n + 1) × (2n + 1)/2 box, giving n(n + 1)(2n + 1)/6.",
               projection="3d")
    n = 5
    for k in range(1, n + 1):
        z = n - k
        for i in range(k):
            for j in range(k):
                ax.bar3d(i, j, z, 0.95, 0.95, 0.95, color=PALETTE_I[k - 1], alpha=0.9, shade=True, edgecolor="white",
                         linewidth=0.3)
    clean3d(ax, elev=24, azim=-55)
    ax.set_box_aspect((1, 1, 1), zoom=1.1)
    ax.text2D(0.02, 0.92, "1 + 4 + 9 + 16 + 25 = 55", transform=ax.transAxes, fontsize=10, color=C["alg"])
    footer(fig)
    save(fig, "04-problem-solving-toolbox.png")


PALETTE_I = ["#2a5d9f", "#c4512c", "#3d8b5a", "#b8860b", "#6a4c93", "#2b8a9e"]


# ---------------------------------------------------------------------------------------------
# 05 One idea at every level
# ---------------------------------------------------------------------------------------------
def fig05():
    fig = figure("One idea, climbed all the way up: 1 + 2 + 3 + … + n",
                 "Depth beats breadth: a single 'simple' sum connects counting, algebra, geometry, combinatorics, "
                 "calculus, number theory — and a surprising piece of modern physics")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Triangular numbers", "primary · Pythagoreans c. 500 BC", "nt",
               "Stack dots in rows of 1, 2, 3, …: the totals 1, 3, 6, 10, 15, 21 are called triangular numbers — "
               "numbers with a shape.")
    clean(ax, xlim=(-0.5, 26), ylim=(-2.2, 6.6))
    x0 = 0
    for n in range(1, 7):
        for r in range(n):
            for c in range(r + 1):
                ax.add_patch(Circle((x0 + c - r / 2 + n / 2, 6 - r), 0.33, fc=C["nt"], ec="none"))
        ax.text(x0 + n / 2, -1.2, str(n * (n + 1) // 2), ha="center", fontsize=11, weight="bold")
        x0 += n + 0.8

    ax = panel(fig, cs[1], 2, "Two copies make a rectangle", "primary / middle school", "alg",
               "Put an upside-down copy next to the staircase: together they make an n × (n + 1) rectangle. Half of it "
               "is the sum: 1 + … + n = n(n + 1)/2. Shown for n = 7: 7 × 8 / 2 = 28.")
    n = 7
    for r in range(n):
        for c in range(n + 1):
            mine = c <= r
            ax.add_patch(Rectangle((c, n - 1 - r), 0.92, 0.92, fc=C["alg"] if mine else L["alg"],
                                   ec=C["alg"], lw=0.6))
    ax.text(n + 1.6, n / 2, "n(n + 1)/2\n= 28", fontsize=12, va="center", weight="bold", color=C["alg"])
    clean(ax, xlim=(-0.3, 12.5), ylim=(-0.4, 7.3))

    ax = panel(fig, cs[2], 3, "Proof by induction", "high school · Pascal 1654, Maurolico 1575", "meta",
               "If the formula holds for n, add n + 1: n(n+1)/2 + (n+1) = (n+1)(n+2)/2, so it holds for n + 1. Like "
               "dominoes: the first falls, and each one knocks over the next — so all of them fall.")
    clean(ax, xlim=(0, 10.5), ylim=(0, 5.6))
    ax.plot([0.3, 10.2], [1.0, 1.0], color=INK, lw=1)
    for i, ang in enumerate([68, 52, 36, 18, 0, 0, 0, 0, 0]):
        x = 0.9 + i * 1.05
        ax.add_patch(Rectangle((x, 1.0), 0.3, 2.4, fc=C["meta"] if ang else L["meta"], ec=C["meta"],
                               angle=-ang, rotation_point=(x + 0.3, 1.0)))
    ax.text(0.8, 4.6, "P(1) true", fontsize=10, color=C["meta"], weight="bold")
    ax.text(4.6, 4.6, "P(n) ⇒ P(n + 1)", fontsize=10, color=C["meta"], weight="bold")
    ax.text(5, 0.35, "n(n+1)/2 + (n+1) = (n+1)(n+2)/2", ha="center", fontsize=10.5)

    ax = panel(fig, cs[3], 4, "It counts handshakes", "combinatorics · C(n+1, 2)", "comb",
               "Seven people arrive one at a time; each greets everyone already there: 0 + 1 + 2 + 3 + 4 + 5 + 6 = 21. "
               "But that is just the number of pairs: C(7, 2) = 21. So 1 + … + n = C(n + 1, 2).")
    th = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, 8)[:-1]
    P = np.c_[np.cos(th), np.sin(th)]
    for j in range(7):
        for i in range(j):
            ax.plot(*P[[i, j]].T, color=PALETTE_I[(j - 1) % 6], lw=1.3, alpha=0.85)
    for i, p in enumerate(P):
        ax.add_patch(Circle(p, 0.11, fc="white", ec=INK, zorder=3))
        ax.text(*p, str(i + 1), ha="center", va="center", fontsize=8.5, zorder=4)
    ax.text(1.5, 0.2, f"C(7,2) = {comb(7, 2)}", fontsize=12, weight="bold", color=C["comb"])
    ax.text(1.5, -0.25, "colour = who arrived", fontsize=8.5, color=MUTED)
    clean(ax, xlim=(-1.2, 3.2), ylim=(-1.2, 1.2))

    ax = panel(fig, cs[4], 5, "Pascal's triangle: the hockey stick", "Yang Hui 1261 · Pascal 1654", "comb",
               "The triangular numbers run down a diagonal of Pascal's triangle, and 1 + 2 + 3 + 4 + 5 + 6 (a "
               "'hockey stick' along the diagonal above) equals the entry at the bend, 21.")
    rows = 9
    for r in range(rows):
        for k in range(r + 1):
            x, y = k - r / 2, -r
            hl = (k == 1 and 1 <= r <= 6)
            end = (r == 7 and k == 2)
            tri = (k == 2 and r >= 2)
            fc = C["comb"] if hl else (C["nt"] if end else (L["nt"] if tri else "white"))
            ax.add_patch(Circle((x, y), 0.42, fc=fc, ec=GRID, lw=0.8))
            ax.text(x, y, str(comb(r, k)), ha="center", va="center", fontsize=8 if comb(r, k) < 100 else 6.5,
                    color="white" if (hl or end) else INK)
    ax.text(3.6, -1.5, "▬ 1+2+…+6\n● = 21\n○ triangular\n   numbers", fontsize=8.5, color=MUTED, va="top")
    clean(ax, xlim=(-4.8, 6.2), ylim=(-8.6, 0.6))

    ax = panel(fig, cs[5], 6, "Area under a line → calculus", "Archimedes · Fermat 1636 · Newton", "ana",
               "The staircase 1 + … + n is the triangle n²/2 plus n half-squares. Dividing by n² and letting n → ∞ "
               "gives ∫₀¹ x dx = 1/2 — the same reasoning with kᵖ gives ∫₀¹ xᵖ dx = 1/(p + 1).", plot=True)
    for n_, col in [(5, C["ana"]), (20, C["nt"])]:
        k = np.arange(1, n_ + 1)
        ax.bar((k - 0.5) / n_, k / n_, width=1 / n_, color=col, alpha=0.35 if n_ == 20 else 0.25, ec=col, lw=0.6,
               label=f"n = {n_}: sum/n² = {k.sum() / n_ ** 2:.3f}")
    ax.plot([0, 1], [0, 1], color=INK, lw=2, label="y = x, area 1/2")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper left", fontsize=8.5)
    plotstyle(ax)

    ax = panel(fig, cs[6], 7, "Sums of higher powers", "Faulhaber 1631 · Bernoulli 1713", "alg",
               "1ᵖ + … + nᵖ is a polynomial in n of degree p + 1 with leading term n^{p+1}/(p + 1); its coefficients "
               "involve the Bernoulli numbers. Plotted: the ratio (1ᵖ + … + nᵖ) / n^{p+1} approaching 1/(p + 1).",
               plot=True)
    nn = np.arange(1, 61)
    for p in range(1, 5):
        S = np.cumsum(nn.astype(float) ** p)
        ax.plot(nn, S / nn ** (p + 1), color=PALETTE_I[p - 1], lw=2, label=f"p = {p} → 1/{p + 1}")
        ax.axhline(1 / (p + 1), color=PALETTE_I[p - 1], ls=":", lw=1)
    ax.set_xlabel("n")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper right", fontsize=8.5, ncol=2)
    plotstyle(ax)

    ax = panel(fig, cs[7], 8, "Square triangular numbers", "Euler 1730 · Pell equation", "nt",
               "Which triangular numbers are perfect squares? 1, 36, 1225, 41616, 1413721, … They correspond to "
               "integer points on the hyperbola x² − 2y² = 1 — a Pell equation, gateway to algebraic number theory.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.03, ratios=[1, 1.1])
    sq = []
    m = 1
    while len(sq) < 6:
        t = m * (m + 1) // 2
        r = int(round(t ** 0.5))
        if r * r == t:
            sq.append((m, t, r))
        m += 1
    clean(a1, equal=False, xlim=(0, 10), ylim=(0, 10))
    a1.text(0.2, 9.2, "n        n(n+1)/2      = k²", fontsize=9.5, weight="bold", family="monospace")
    for i, (m_, t, r) in enumerate(sq):
        a1.text(0.2, 7.9 - i * 1.35, f"{m_:<8d} {t:<12d} {r}²", fontsize=9.5, family="monospace")
    x = np.linspace(1, 120, 400)
    a2.plot(x, np.sqrt((x ** 2 - 1) / 2), color=C["nt"], lw=1.6)
    pts = [(3, 2), (17, 12), (99, 70)]
    for (px, py) in pts:
        a2.plot(px, py, "o", color=C["comb"], ms=7)
        a2.text(px + 3, py - 4, f"({px}, {py})", fontsize=8.5)
    a2.set_title("x² − 2y² = 1", fontsize=9.5)
    a2.set_xlim(0, 125)
    a2.set_ylim(0, 90)
    plotstyle(a2)
    a2.tick_params(labelsize=7.5)

    ax = panel(fig, cs[8], 9, "Frontier: '1 + 2 + 3 + … = −1/12'", "Euler 1749 · Riemann 1859",
               "ana",
               "The sum diverges, but smoothing it reveals a hidden constant: Σ n·e^{−n/N} = N² − 1/12 + O(1/N²) "
               "(computed below). This −1/12 = ζ(−1) appears in the Casimir force and fixes the 26 dimensions of "
               "bosonic string theory.", plot=True)
    Ns = np.geomspace(1, 200, 60)
    vals = []
    for N_ in Ns:
        k = np.arange(1, int(60 * N_) + 1)
        vals.append(np.sum(k * np.exp(-k / N_)) - N_ ** 2)
    ax.semilogx(Ns, vals, "o-", color=C["ana"], ms=3, lw=1.5, label="Σ n e^{−n/N} − N²")
    ax.axhline(-1 / 12, color=C["comb"], ls="--", lw=1.4, label="−1/12 = ζ(−1)")
    ax.set_xlabel("smoothing scale N")
    ax.set_ylim(-0.12, 0.02)
    ax.legend(loc="upper right", fontsize=8.5)
    plotstyle(ax)
    footer(fig)
    save(fig, "05-one-idea-every-level.png")


if __name__ == "__main__":
    for f in (fig01, fig02, fig03, fig04, fig05):
        f()
