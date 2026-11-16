"""Figures 11-15: heat & entropy, probability & quantum, fields & unification, co-evolution timeline, state space."""
from math import lgamma, log

import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle, Wedge

from common import (BOTH, GRID, INK, MATH, MUTED, PALETTE, PHYS, SOFT, arrow, box, cells, clean, clean3d,
                    figure, footer, note, panel, plotstyle, rk4, save, split)


# ---------------------------------------------------------------------------------------------
# 11 Heat, energy, entropy
# ---------------------------------------------------------------------------------------------
def fig11():
    fig = figure("How the concepts of heat, energy and entropy grew",
                 "Heat went from a substance, to a form of energy, to a statistical count of microscopic "
                 "arrangements — and finally to information")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Heat as a fluid: caloric", "Black 1760s · Lavoisier 1787", "phys",
               "Heat was an invisible, conserved fluid flowing from hot to cold. It explained conduction and "
               "latent heat well — but Rumford (1798) boiled water endlessly by boring cannon: friction "
               "creates heat without limit.")
    clean(ax, xlim=(0, 10), ylim=(0, 6))
    ax.add_patch(FancyBboxPatch((0.6, 1.2), 3.2, 3.2, boxstyle="round,pad=0,rounding_size=0.3", fc="#f5b7a5",
                                ec="#c0392b", lw=1.5))
    ax.add_patch(FancyBboxPatch((6.2, 1.2), 3.2, 3.2, boxstyle="round,pad=0,rounding_size=0.3", fc="#aed6f1",
                                ec="#2471a3", lw=1.5))
    ax.text(2.2, 4.8, "hot body", ha="center", fontsize=9.5)
    ax.text(7.8, 4.8, "cold body", ha="center", fontsize=9.5)
    rng = np.random.default_rng(2)
    for k in range(24):
        x, y = rng.uniform(0.9, 3.5), rng.uniform(1.5, 4.1)
        ax.add_patch(Ellipse((x, y), 0.18, 0.26, fc="#e67e22", ec="none", alpha=0.8))
    for k in range(7):
        x, y = rng.uniform(6.5, 9.1), rng.uniform(1.5, 4.1)
        ax.add_patch(Ellipse((x, y), 0.18, 0.26, fc="#e67e22", ec="none", alpha=0.8))
    for k in range(5):
        ax.add_patch(Ellipse((4.3 + k * 0.38, 2.8 + 0.12 * np.sin(k)), 0.18, 0.26, fc="#e67e22", ec="none"))
    arrow(ax, (4.0, 2.2), (6.0, 2.2), color="#e67e22", lw=2)
    ax.text(5.0, 1.65, "caloric flows", ha="center", fontsize=9, color="#e67e22")

    ax = panel(fig, cs[1], 2, "Temperature scales", "Fahrenheit 1724 · Celsius 1742 · Kelvin 1848", "phys",
               "Fixed points made temperature reproducible. Kelvin's absolute scale starts at the coldest possible "
               "state, where classical molecular motion would stop: 0 K = −273.15 °C.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(-30, 420))
    pts = [(0, -273.15, -459.67, "absolute zero"), (273.15, 0, 32, "water freezes"), (310.15, 37, 98.6, "body"),
           (373.15, 100, 212, "water boils")]
    for x, lab in [(1.6, "K"), (3.4, "°C"), (5.2, "°F")]:
        ax.plot([x, x], [0, 400], color=INK, lw=1.4)
        ax.text(x, 412, lab, ha="center", fontsize=11, weight="bold")
    ax.add_patch(Rectangle((0.35, 0), 0.4, 400, fc="#fdedec", ec="#c0392b"))
    ax.add_patch(Rectangle((0.35, 0), 0.4, 300, fc="#e74c3c", ec="none"))
    ax.add_patch(Circle((0.55, -10), 0.5, fc="#e74c3c", ec="#c0392b"))
    for K, C, F, lab in pts:
        for x, v in [(1.6, K), (3.4, C), (5.2, F)]:
            ax.plot([x - 0.15, x + 0.15], [K, K], color=INK, lw=1.2)
            ax.text(x + 0.22, K, f"{v:g}", fontsize=8.2, va="center")
        ax.plot([6.3, 6.6], [K, K], color=GRID)
        ax.text(6.7, K, lab, fontsize=9, va="center", color=PHYS)

    ax = panel(fig, cs[2], 3, "Heat is energy", "Mayer 1842 · Joule 1845 · Helmholtz 1847", "phys",
               "A falling weight turns paddles that warm water. Joule measured the exchange rate: 4.18 J of work = "
               "1 calorie of heat. Energy is conserved but changes form — the first law of thermodynamics.")
    clean(ax, xlim=(0, 10), ylim=(0, 7))
    ax.add_patch(Rectangle((1.0, 0.6), 4.2, 3.6, fc="#d6eaf8", ec=INK, lw=1.5))
    ax.plot([3.1, 3.1], [1.0, 6.0], color=INK, lw=2)
    for k in range(4):
        y = 1.2 + k * 0.75
        ax.add_patch(Rectangle((2.1, y), 2.0, 0.18, fc="#7f8c8d"))
    ax.add_patch(Circle((3.1, 6.0), 0.45, fc="white", ec=INK, lw=1.5))
    ax.plot([3.55, 7.3], [6.0, 6.0], color=INK, lw=1.2)
    ax.add_patch(Circle((7.3, 5.6), 0.4, fc="white", ec=INK, lw=1.5))
    ax.plot([7.7, 7.7], [5.6, 3.2], color=INK, lw=1.2)
    ax.add_patch(Rectangle((7.2, 2.2), 1.0, 1.0, fc="#566573"))
    arrow(ax, (8.6, 3.4), (8.6, 1.6), color=PHYS, lw=2)
    ax.text(8.85, 2.5, "mgh", fontsize=10, color=PHYS)
    ax.text(3.1, 0.25, "water warms by ΔT", ha="center", fontsize=9, color=MATH)
    ax.text(6.2, 4.6, "W = J·Q\nJ ≈ 4.18 J/cal", fontsize=10, ha="center", color=INK)

    ax = panel(fig, cs[3], 4, "The Carnot cycle", "Carnot 1824 · Clapeyron 1834", "both",
               "1 mol of ideal gas between 500 K and 300 K (γ = 1.4). Two isotherms and two adiabats enclose the "
               "work. No engine between these temperatures can beat η = 1 − Tc/Th = 40% (computed: W = 1152 J).",
               plot=True)
    R, Th, Tc, g = 8.314, 500.0, 300.0, 1.4
    V1, V2 = 10.0, 20.0
    V3 = V2 * (Th / Tc) ** (1 / (g - 1))
    V4 = V1 * (Th / Tc) ** (1 / (g - 1))
    P = lambda V, T: R * T / V
    seg = [(np.linspace(V1, V2, 100), lambda V: P(V, Th), PHYS, "isothermal 500 K"),
           (np.linspace(V2, V3, 100), lambda V: P(V2, Th) * (V2 / V) ** g, "#888", "adiabatic"),
           (np.linspace(V3, V4, 100), lambda V: P(V, Tc), MATH, "isothermal 300 K"),
           (np.linspace(V4, V1, 100), lambda V: P(V4, Tc) * (V4 / V) ** g, "#888", None)]
    Vs, Ps = [], []
    for V, f, c, lab in seg:
        ax.plot(V, f(V), color=c, lw=2.2, label=lab)
        Vs.append(V)
        Ps.append(f(V))
    ax.fill(np.concatenate(Vs), np.concatenate(Ps), color="#f9e79f", alpha=0.6)
    W = R * (Th - Tc) * np.log(V2 / V1)
    ax.text(32, 160, f"W = {W:.0f} J\nη = {W / (R * Th * np.log(V2 / V1)):.0%}", fontsize=10, ha="center")
    ax.set_xlabel("volume (L)")
    ax.set_ylabel("pressure (kPa)")
    ax.legend(loc="upper right", fontsize=8)
    plotstyle(ax)

    ax = panel(fig, cs[4], 5, "Entropy and the arrow of time", "Clausius 1865", "phys",
               "Remove the wall and two gases mix; they never spontaneously unmix. Entropy rises by ΔS = 2Nk ln 2. "
               "For only 120 molecules, the chance of finding them sorted again is 2⁻¹²⁰ ≈ 7.5 × 10⁻³⁷.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.03)
    rng = np.random.default_rng(5)
    for a, mixed in [(a1, False), (a2, True)]:
        a.add_patch(Rectangle((0, 0), 2, 1, fc="white", ec=INK, lw=1.4))
        if not mixed:
            a.plot([1, 1], [0, 1], color=INK, lw=2)
            xb, xr = rng.uniform(0.03, 0.97, 60), rng.uniform(1.03, 1.97, 60)
        else:
            xb, xr = rng.uniform(0.03, 1.97, 60), rng.uniform(0.03, 1.97, 60)
        a.scatter(xb, rng.uniform(0.04, 0.96, 60), s=9, color=MATH)
        a.scatter(xr, rng.uniform(0.04, 0.96, 60), s=9, color=PHYS)
        clean(a, xlim=(-0.05, 2.05), ylim=(-0.25, 1.25))
        a.text(1, -0.17, "low entropy" if not mixed else "high entropy", ha="center", fontsize=9)
    fig.text((a1.get_position().x1 + a2.get_position().x0) / 2, a1.get_position().y0 + a1.get_position().height / 2,
             "→", fontsize=18, ha="center", va="center", color=MUTED)

    ax = panel(fig, cs[5], 6, "Heat is molecular motion", "Maxwell 1860 · Boltzmann 1872", "phys",
               "Temperature measures the average kinetic energy of molecules, which have a spread of speeds. "
               "Computed Maxwell–Boltzmann distributions for nitrogen (N₂); dots mark the most probable speed.",
               plot=True)
    kB, m = 1.380649e-23, 28 * 1.66054e-27
    v = np.linspace(0, 2000, 500)
    for T, c in [(77, MATH), (300, "#3d8b5a"), (1000, PHYS)]:
        f = 4 * np.pi * (m / (2 * np.pi * kB * T)) ** 1.5 * v ** 2 * np.exp(-m * v ** 2 / (2 * kB * T))
        vp = np.sqrt(2 * kB * T / m)
        ax.plot(v, f * 1000, color=c, lw=2.2, label=f"{T} K: most probable {vp:.0f} m/s")
        fp = 4 * np.pi * (m / (2 * np.pi * kB * T)) ** 1.5 * vp ** 2 * np.exp(-1)
        ax.plot(vp, fp * 1000, "o", color=c)
    ax.set_xlabel("molecular speed (m/s)")
    ax.set_ylabel("probability density (per km/s)")
    ax.legend(loc="upper right", fontsize=8)
    plotstyle(ax)

    ax = panel(fig, cs[6], 7, "Entropy counts arrangements: S = k ln W", "Boltzmann 1877", "both",
               "Toss N coins: almost all arrangements have nearly half heads. As N grows the distribution of the "
               "heads fraction sharpens (width ∝ 1/√N) — why macroscopic thermodynamics looks deterministic.",
               plot=True)
    for N, c in [(10, "#b7c9e2"), (100, "#7fa6d6"), (1000, MATH), (10000, PHYS)]:
        k = np.arange(0, N + 1)
        lp = np.array([lgamma(N + 1) - lgamma(i + 1) - lgamma(N - i + 1) - N * log(2) for i in k])
        ax.plot(k / N, np.exp(lp) * N, color=c, lw=1.8, label=f"N = {N:,}")
    ax.set_xlabel("fraction of heads")
    ax.set_ylabel("probability density")
    ax.set_xlim(0.2, 0.8)
    ax.legend(loc="upper right", fontsize=8)
    ax.text(0.22, 70, "W(N/2) for N = 100:\n1.01 × 10²⁹ arrangements", fontsize=8.5, color=MUTED, va="top")
    plotstyle(ax)

    ax = panel(fig, cs[7], 8, "Phase transitions", "Ising 1925 · Onsager 1944", "both",
               "A grid of up/down spins (Ising model), simulated by the Metropolis algorithm. Below the critical "
               "temperature Tc = 2.269 order wins, above it disorder wins; at Tc clusters of all sizes appear.")
    axes = split(fig, ax, 3, "h", gap=0.006)
    rng = np.random.default_rng(0)
    n = 128
    ii, jj = np.indices((n, n))
    checker = (ii + jj) % 2
    for a, T in zip(axes, [1.8, 2.269, 3.2]):
        s = rng.choice([-1, 1], size=(n, n))
        for sweep in range(600):
            for par in (0, 1):
                nb = np.roll(s, 1, 0) + np.roll(s, -1, 0) + np.roll(s, 1, 1) + np.roll(s, -1, 1)
                dE = 2 * s * nb
                flip = (checker == par) & (rng.random((n, n)) < np.exp(-dE / T))
                s[flip] *= -1
        a.imshow(s, cmap="RdBu", vmin=-1.5, vmax=1.5, interpolation="nearest")
        a.text(4, 10, f"T = {T}", fontsize=9, va="top", bbox=dict(fc="white", ec="none", pad=1.5))
        clean(a)

    ax = panel(fig, cs[8], 9, "Entropy is information", "Shannon 1948 · Landauer 1961", "both",
               "Shannon's entropy H = −Σ p log₂ p measures missing information. Landauer: erasing one bit "
               "must release at least kT ln 2 of heat (measured 2012) — which also exorcises Maxwell's demon.",
               plot=True)
    p = np.linspace(1e-4, 1 - 1e-4, 400)
    H = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
    ax.plot(p, H, color=BOTH, lw=2.4)
    ax.fill_between(p, 0, H, color=SOFT["both"])
    ax.text(0.5, 0.45, f"kT ln 2 at 300 K\n= {1.380649e-23 * 300 * np.log(2):.2e} J per bit", ha="center",
            fontsize=9.5, color=INK)
    ax.set_xlabel("probability p of '1'")
    ax.set_ylabel("entropy H (bits)")
    ax.set_ylim(0, 1.08)
    plotstyle(ax)
    footer(fig)
    save(fig, "11-heat-energy-entropy.png")


# ---------------------------------------------------------------------------------------------
# 12 Probability and quantum states
# ---------------------------------------------------------------------------------------------
def fig12():
    fig = figure("From games of chance to quantum states",
                 "Probability began as the mathematics of gambling, became the foundation of statistical physics, "
                 "and in quantum theory turned into a property of nature itself")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Counting chances", "Cardano c. 1564 · Pascal & Fermat 1654", "math",
               "Probability = favourable cases / all equally likely cases. Two dice: 36 outcomes; a sum of 7 can "
               "happen 6 ways, so P(7) = 6/36. Exact distribution of the sum:", plot=True)
    s = np.arange(2, 13)
    w = 6 - np.abs(s - 7)
    ax.bar(s, w / 36, color=MATH, ec="white")
    for x, ww in zip(s, w):
        ax.text(x, ww / 36 + 0.004, f"{ww}/36", ha="center", fontsize=7.5)
    ax.set_xticks(s)
    ax.set_xlabel("sum of two dice")
    ax.set_ylabel("probability")
    ax.set_ylim(0, 0.2)
    plotstyle(ax)

    ax = panel(fig, cs[1], 2, "Law of large numbers", "Jacob Bernoulli 1713", "math",
               "Individual outcomes are unpredictable, averages are not. Five simulated runs of 10,000 coin tosses: "
               "the running fraction of heads converges to 1/2, within ±1/(2√n) (dashed).", plot=True)
    rng = np.random.default_rng(3)
    n = np.arange(1, 10001)
    for k in range(5):
        f = np.cumsum(rng.integers(0, 2, 10000)) / n
        ax.plot(n, f, lw=1.1, color=PALETTE[k])
    ax.plot(n, 0.5 + 0.5 / np.sqrt(n), color=INK, ls="--", lw=1)
    ax.plot(n, 0.5 - 0.5 / np.sqrt(n), color=INK, ls="--", lw=1)
    ax.set_xscale("log")
    ax.set_ylim(0, 1)
    ax.set_xlabel("number of tosses n")
    ax.set_ylabel("fraction of heads")
    plotstyle(ax)

    ax = panel(fig, cs[2], 3, "Central limit theorem", "de Moivre 1733 · Laplace 1812", "math",
               "Add up independent random effects and the bell curve appears, whatever the ingredients. "
               "Histograms of sums of n uniform random numbers (200,000 samples, standardised) vs. the normal curve.")
    axes = split(fig, ax, 4, "h", gap=0.006)
    rng = np.random.default_rng(1)
    xx = np.linspace(-4, 4, 200)
    for a, k in zip(axes, [1, 2, 4, 16]):
        x = rng.uniform(0, 1, (200000, k)).sum(1)
        x = (x - k / 2) / np.sqrt(k / 12)
        a.hist(x, bins=60, range=(-4, 4), density=True, color="#9bb6d8")
        a.plot(xx, np.exp(-xx ** 2 / 2) / np.sqrt(2 * np.pi), color=PHYS, lw=1.6)
        a.text(-3.8, 0.5, f"n = {k}", fontsize=9, va="top")
        a.set_yticks([])
        a.set_xticks([-3, 0, 3])
        a.tick_params(labelsize=7)
        a.set_ylim(0, 0.52)
        for sp in ("top", "right", "left"):
            a.spines[sp].set_visible(False)

    ax = panel(fig, cs[3], 4, "Random walks and diffusion", "Brown 1827 · Einstein 1905 · Perrin 1908", "both",
               "Pollen jiggles because invisible molecules hit it. Einstein showed the mean squared distance grows "
               "linearly in time, ⟨r²⟩ ∝ t; Perrin's measurements of it proved atoms exist. Three simulated walks "
               "of 3,000 steps; circle radius √N.")
    rng = np.random.default_rng(8)
    for k in range(3):
        steps = rng.normal(0, 1, (3000, 2)) / np.sqrt(2)
        path = np.cumsum(steps, axis=0)
        ax.plot(path[:, 0], path[:, 1], lw=0.6, color=PALETTE[k])
        ax.plot(*path[-1], "o", color=PALETTE[k], ms=4)
    ax.add_patch(Circle((0, 0), np.sqrt(3000), fc="none", ec=INK, ls="--", lw=1))
    ax.plot(0, 0, "k+", ms=10)
    clean(ax, xlim=(-90, 90), ylim=(-70, 70))

    ax = panel(fig, cs[4], 5, "Uncertainty in phase space", "Heisenberg 1927 · Kennard 1927", "both",
               "A classical state is a point (x, p). A quantum state is a blob of area at least ħ/2: Δx·Δp ≥ ħ/2. "
               "A coherent state is round; a squeezed state trades position spread for momentum spread.")
    ax.plot(-2.2, 1.6, "o", color=INK, ms=6)
    ax.text(-2.05, 1.85, "classical point", fontsize=8.5)
    for (cx, cy, w, h, ang, col, lab) in [(0.5, 0.0, 1.2, 1.2, 0, MATH, "coherent"),
                                         (2.4, -1.4, 2.6, 0.55, 25, PHYS, "squeezed")]:
        for s, al in [(1.0, 0.5), (0.6, 0.7)]:
            ax.add_patch(Ellipse((cx, cy), w * s * 1.5, h * s * 1.5, angle=ang, fc=col, alpha=al * 0.5, ec="none"))
        ax.text(cx, cy + h * 0.9 + 0.2, lab, ha="center", fontsize=9, color=col)
    ax.annotate("", xy=(3.8, 0), xytext=(-3.5, 0), arrowprops=dict(arrowstyle="-|>", color=INK))
    ax.annotate("", xy=(0, 3.0), xytext=(0, -2.6), arrowprops=dict(arrowstyle="-|>", color=INK))
    ax.text(3.7, -0.35, "x", fontsize=10)
    ax.text(0.15, 2.75, "p", fontsize=10)
    ax.text(-3.3, -2.3, "area ≥ ħ/2", fontsize=9.5, color=MUTED)
    clean(ax, xlim=(-3.6, 4.0), ylim=(-2.7, 3.1))

    ax = panel(fig, cs[5], 6, "Quantized standing waves", "Schrödinger 1926", "both",
               "A particle in a box can only have energies E_n = n²h²/(8mL²): standing waves with n half-wavelengths. "
               "Solid: wavefunction ψ_n; dashed: probability density |ψ_n|².", plot=True)
    x = np.linspace(0, 1, 300)
    for n in range(1, 5):
        E = n ** 2
        psi = np.sqrt(2) * np.sin(n * np.pi * x)
        ax.axhline(E, color=GRID, lw=0.8)
        ax.plot(x, E + 0.9 * psi, color=PALETTE[n - 1], lw=1.8)
        ax.plot(x, E + 0.45 * psi ** 2, color=PALETTE[n - 1], lw=1, ls="--")
        ax.text(1.03, E, f"n = {n}", fontsize=8.5, va="center")
    ax.axvline(0, color=INK, lw=3)
    ax.axvline(1, color=INK, lw=3)
    ax.set_xlim(-0.02, 1.15)
    ax.set_ylim(-0.5, 17.8)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["0", "L"])
    ax.set_ylabel("energy (units of h²/8mL²)")
    plotstyle(ax, grid=False)

    ax = panel(fig, cs[6], 7, "Tunnelling", "Gamow 1928 · Gurney & Condon 1928", "both",
               "A wave packet with less energy than a barrier still leaks through — explaining alpha decay, "
               "fusion in the Sun and the scanning tunnelling microscope. Computed with the split-step Fourier "
               "method (ħ = m = 1).", plot=True)
    N = 4096
    x = np.linspace(-160, 160, N, endpoint=False)
    dx = x[1] - x[0]
    kgrid = 2 * np.pi * np.fft.fftfreq(N, dx)
    V0, wb = 0.85, 2.0
    V = np.where((x > 0) & (x < wb), V0, 0.0)
    k0, x0, sig = 1.2, -40.0, 6.0
    psi = np.exp(-(x - x0) ** 2 / (4 * sig ** 2) + 1j * k0 * x)
    psi /= np.sqrt(np.sum(np.abs(psi) ** 2) * dx)
    dt = 0.05
    snaps = {0: psi.copy()}
    for step in range(1, 1601):
        psi *= np.exp(-1j * V * dt / 2)
        psi = np.fft.ifft(np.exp(-1j * kgrid ** 2 / 2 * dt) * np.fft.fft(psi))
        psi *= np.exp(-1j * V * dt / 2)
        if step in (700, 1600):
            snaps[step] = psi.copy()
    Ttrans = np.sum(np.abs(psi[x > wb]) ** 2) * dx
    for k, (step, ps) in enumerate(sorted(snaps.items())):
        off = (2 - k) * 0.075
        ax.plot(x, off + np.abs(ps) ** 2, color=PALETTE[k], lw=1.5, label=f"t = {step * dt:.0f}")
        ax.axhline(off, color=GRID, lw=0.6)
    ax.add_patch(Rectangle((0, 0), wb, 0.23, fc="#bbb", ec="none", alpha=0.6))
    ax.text(wb + 2, 0.215, f"barrier V₀ = {V0}, energy ≈ {k0 ** 2 / 2:.2f}", fontsize=8)
    ax.text(60, 0.03, f"transmitted: {Ttrans:.0%}", fontsize=9, color=PALETTE[2], ha="center")
    ax.set_xlim(-90, 110)
    ax.set_ylim(0, 0.24)
    ax.set_yticks([])
    ax.set_xlabel("position x")
    ax.legend(loc="upper left", fontsize=7.8)
    plotstyle(ax, grid=False)

    ax = panel(fig, cs[7], 8, "The qubit and the Bloch sphere", "Bloch 1946 · Feynman 1982", "both",
               "Any pure state of a two-level system is a point on a sphere: |ψ⟩ = cos(θ/2)|0⟩ + e^{iφ} sin(θ/2)|1⟩. "
               "Here θ = 60°, φ = 45°. Quantum computing manipulates many such states coherently.", projection="3d")
    u, v = np.mgrid[0:2 * np.pi:40j, 0:np.pi:20j]
    ax.plot_wireframe(np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v), color=GRID, lw=0.4)
    for d in ([1.3, 0, 0], [0, 1.3, 0], [0, 0, 1.3]):
        ax.plot([-d[0], d[0]], [-d[1], d[1]], [-d[2], d[2]], color=MUTED, lw=0.8)
    th, ph = np.radians(60), np.radians(45)
    vec = [np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)]
    ax.quiver(0, 0, 0, *vec, color=PHYS, lw=2.5, arrow_length_ratio=0.12)
    ax.text(0, 0, 1.45, "|0⟩", fontsize=10, ha="center")
    ax.text(0, 0, -1.55, "|1⟩", fontsize=10, ha="center")
    ax.text(1.45, 0, 0, "|+⟩", fontsize=9)
    ax.text(0, 1.45, 0, "|+i⟩", fontsize=9)
    ax.text(vec[0] * 1.15, vec[1] * 1.15, vec[2] * 1.15, "|ψ⟩", fontsize=11, color=PHYS, weight="bold")
    clean3d(ax, elev=20, azim=30)
    ax.set_box_aspect((1, 1, 1), zoom=1.35)

    ax = panel(fig, cs[8], 9, "Entanglement beats classical limits", "Bell 1964 · Aspect 1982",
               "both",
               "Spin correlation of an entangled pair vs. detector angle: quantum E(θ) = −cos θ (red) vs. the best "
               "local hidden-variable model (blue). In the CHSH test classical theories give S ≤ 2; quantum gives "
               "2√2 ≈ 2.83; Aspect measured S = 2.70 ± 0.02.", plot=True)
    th = np.linspace(0, np.pi, 300)
    ax.plot(np.degrees(th), -np.cos(th), color=PHYS, lw=2.4, label="quantum: −cos θ")
    ax.plot(np.degrees(th), -1 + 2 * th / np.pi, color=MATH, lw=2, ls="--", label="local realism (linear)")
    ax.fill_between(np.degrees(th), -np.cos(th), -1 + 2 * th / np.pi, color=SOFT["phys"])
    ax.set_xlabel("angle between detectors (°)")
    ax.set_ylabel("correlation E(θ)")
    ax.set_xticks([0, 45, 90, 135, 180])
    ax.legend(loc="upper left", fontsize=8)
    plotstyle(ax)
    footer(fig)
    save(fig, "12-probability-to-quantum.png")


# ---------------------------------------------------------------------------------------------
# 13 Fields and unification
# ---------------------------------------------------------------------------------------------
def _wavy(ax, p, q, color, amp=0.12, waves=6, lw=1.6):
    p, q = np.array(p, float), np.array(q, float)
    t = np.linspace(0, 1, 300)
    d = q - p
    nrm = np.array([-d[1], d[0]]) / np.linalg.norm(d)
    pts = p + np.outer(t, d) + np.outer(amp * np.sin(2 * np.pi * waves * t), nrm)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw)


def _curly(ax, p, q, color, r=0.12, loops=7, lw=1.5):
    p, q = np.array(p, float), np.array(q, float)
    t = np.linspace(0, 1, 600)
    d = q - p
    L = np.linalg.norm(d)
    dh = d / L
    nrm = np.array([-dh[1], dh[0]])
    w = 2 * np.pi * loops
    pts = p + np.outer(t * L - r * np.sin(w * t), dh) + np.outer(r * (1 - np.cos(w * t)), nrm)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw)


def _fermion(ax, p, q, color=INK, lw=1.6):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw)
    m = (np.array(p) + np.array(q)) / 2
    d = (np.array(q) - np.array(p)) * 0.08
    ax.annotate("", xy=m + d, xytext=m - d, arrowprops=dict(arrowstyle="-|>", color=color, lw=lw))


def fig13():
    fig = figure("Fields and unification",
                 "From mysterious action at a distance to fields filling space, to symmetry principles that "
                 "generate forces — and the long road of merging forces into one")
    cs = cells(fig, 3, 3)

    ax = panel(fig, cs[0], 1, "Action at a distance", "Newton 1687", "phys",
               "Newton's gravity acts instantly across empty space. Newton himself called that 'so great an "
               "absurdity' (letter to Bentley, 1693), but the mathematics worked, so the question was shelved.")
    clean(ax, xlim=(0, 10), ylim=(0, 6))
    ax.add_patch(Circle((2.2, 3), 1.25, fc="#5dade2", ec="#2471a3"))
    ax.add_patch(Circle((8.2, 3), 0.42, fc="#bfc9ca", ec="#7f8c8d"))
    arrow(ax, (3.5, 3), (5.0, 3), color=PHYS, lw=2.2)
    arrow(ax, (7.7, 3), (6.2, 3), color=PHYS, lw=2.2)
    ax.text(5.6, 3.0, "?", fontsize=20, ha="center", va="center", color=MUTED)
    ax.text(5.2, 1.2, r"$F = G\,\frac{Mm}{r^2}$", fontsize=14, ha="center")
    ax.text(2.2, 4.6, "Earth", ha="center", fontsize=9)
    ax.text(8.2, 3.8, "Moon", ha="center", fontsize=9)

    ax = panel(fig, cs[1], 2, "Lines of force", "Faraday 1831 – 1852", "phys",
               "Faraday imagined space filled with physical 'lines of force' — like iron filings around a magnet. "
               "The field becomes real, carrying energy and taking time to change. Field computed for a bar magnet.")
    Y, X = np.mgrid[-3:3:200j, -4:4:260j]
    Bx = np.zeros_like(X)
    By = np.zeros_like(X)
    for q, xq in [(1, 0.9), (-1, -0.9)]:
        for yq in np.linspace(-0.25, 0.25, 5):
            rx, ry = X - xq, Y - yq
            r3 = (rx ** 2 + ry ** 2) ** 1.5 + 1e-3
            Bx += q * rx / r3
            By += q * ry / r3
    ax.streamplot(X, Y, Bx, By, color="#7f8c8d", density=1.4, linewidth=0.7, arrowsize=0.6)
    ax.add_patch(Rectangle((-1.2, -0.38), 1.2, 0.76, fc="#2a5d9f", ec=INK, zorder=3))
    ax.add_patch(Rectangle((0, -0.38), 1.2, 0.76, fc="#c4512c", ec=INK, zorder=3))
    ax.text(-0.6, 0, "S", color="white", ha="center", va="center", weight="bold", zorder=4)
    ax.text(0.6, 0, "N", color="white", ha="center", va="center", weight="bold", zorder=4)
    clean(ax, xlim=(-4, 4), ylim=(-3, 3))

    ax = panel(fig, cs[2], 3, "Potential theory", "Laplace 1782 · Poisson 1813 · Green 1828", "both",
               "Fields as gradients of a potential satisfying ∇²φ = −ρ/ε₀. Two equal positive charges: field lines "
               "(grey) are always perpendicular to equipotentials (colour). Mathematics built for gravity reused "
               "for electricity.")
    Y, X = np.mgrid[-3:3:240j, -4:4:320j]
    phi = np.zeros_like(X)
    Ex = np.zeros_like(X)
    Ey = np.zeros_like(X)
    for xq in (-1.2, 1.2):
        rx, ry = X - xq, Y
        r = np.sqrt(rx ** 2 + ry ** 2) + 1e-3
        phi += 1 / r
        Ex += rx / r ** 3
        Ey += ry / r ** 3
    ax.contourf(X, Y, np.log(phi), levels=20, cmap="YlOrRd", alpha=0.7)
    ax.contour(X, Y, np.log(phi), levels=20, colors="white", linewidths=0.5)
    ax.streamplot(X, Y, Ex, Ey, color="#555", density=1.1, linewidth=0.6, arrowsize=0.6)
    for xq in (-1.2, 1.2):
        ax.add_patch(Circle((xq, 0), 0.18, fc=PHYS, ec="white", zorder=4))
        ax.text(xq, 0, "+", color="white", ha="center", va="center", weight="bold", zorder=5)
    clean(ax, xlim=(-4, 4), ylim=(-3, 3))

    ax = panel(fig, cs[3], 4, "Maxwell's synthesis", "Maxwell 1865", "phys",
               "Four separate subjects merge into four equations. Their wave solutions travel at "
               "c = 1/√(μ₀ε₀): light is electromagnetism. The first great unification after Newton's.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    srcs = [("Electrostatics", "Coulomb 1785", 8.9), ("Magnetism", "Ørsted, Ampère 1820", 6.9),
            ("Induction", "Faraday 1831", 4.9), ("Optics", "Huygens, Young, Fresnel", 2.9)]
    for name, who, y in srcs:
        ax.add_patch(FancyBboxPatch((0.2, y - 0.75), 3.2, 1.5, boxstyle="round,pad=0,rounding_size=0.2",
                                    fc="#fbf6ec", ec=PHYS, lw=1))
        ax.text(1.8, y + 0.2, name, ha="center", fontsize=9.5, weight="bold")
        ax.text(1.8, y - 0.35, who, ha="center", fontsize=7.8, color=MUTED)
        arrow(ax, (3.45, y), (4.55, 5.9), color=PHYS, lw=1.1)
    ax.add_patch(FancyBboxPatch((4.6, 2.0), 5.25, 7.8, boxstyle="round,pad=0,rounding_size=0.3", fc=SOFT["phys"],
                                ec=PHYS, lw=1.5))
    eqs = [r"$\nabla\cdot\mathbf{E} = \rho/\varepsilon_0$", r"$\nabla\cdot\mathbf{B} = 0$",
           r"$\nabla\times\mathbf{E} = -\partial_t\mathbf{B}$",
           r"$\nabla\times\mathbf{B} = \mu_0\mathbf{J} + \mu_0\varepsilon_0\,\partial_t\mathbf{E}$"]
    for k, e in enumerate(eqs):
        ax.text(7.2, 8.7 - k * 1.45, e, ha="center", fontsize=10.5)
    ax.text(7.2, 2.9, r"$c = 1/\sqrt{\mu_0\varepsilon_0}$", ha="center", fontsize=12, color=PHYS)
    ax.text(5.0, 0.8, "≈ 3.0 × 10⁸ m/s = measured speed of light", ha="center", fontsize=8.8, color=MUTED)

    ax = panel(fig, cs[4], 5, "Gauge principle", "Weyl 1929 · Yang & Mills 1954", "both",
               "Demand that physics is unchanged when the quantum phase (arrows) is rotated differently at every "
               "point. Comparing neighbours then needs a connecting field on the links — that field is the photon "
               "(or gluons, W and Z).")
    a1, a2 = split(fig, ax, 2, "h", gap=0.02)
    rng = np.random.default_rng(6)
    for a, local in [(a1, False), (a2, True)]:
        angs = rng.uniform(0, 2 * np.pi, (5, 5)) if local else np.full((5, 5), 0.6)
        for i in range(5):
            for j in range(5):
                if local:
                    if i < 4:
                        a.add_patch(Rectangle((i + 0.38, j - 0.06), 0.24, 0.12,
                                              fc=PALETTE[int((angs[i + 1, j] - angs[i, j]) % (2 * np.pi) / (2 * np.pi) * 6) % 6],
                                              ec="none"))
                    if j < 4:
                        a.add_patch(Rectangle((i - 0.06, j + 0.38), 0.12, 0.24,
                                              fc=PALETTE[int((angs[i, j + 1] - angs[i, j]) % (2 * np.pi) / (2 * np.pi) * 6) % 6],
                                              ec="none"))
                a.add_patch(Circle((i, j), 0.08, fc=INK))
                a.annotate("", xy=(i + 0.42 * np.cos(angs[i, j]), j + 0.42 * np.sin(angs[i, j])), xytext=(i, j),
                           arrowprops=dict(arrowstyle="-|>,head_length=0.5,head_width=0.25", color=MATH if not local else PHYS, lw=1.6))
        a.set_title("global rotation" if not local else "local rotation + link field", fontsize=8.8)
        clean(a, xlim=(-0.6, 4.6), ylim=(-0.6, 4.6))

    ax = panel(fig, cs[5], 6, "The road of unification", "1687 → ?", "phys",
               "Each merger revealed that apparently different phenomena were one. Solid: established; dashed: "
               "hypothetical. Gravity has resisted every attempt so far.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(0, 10))
    nodes = {
        "celestial": (0.9, 1.0, "celestial\nmotion"), "terrestrial": (2.6, 1.0, "falling\nbodies"),
        "elec": (4.3, 1.0, "electricity"), "mag": (6.0, 1.0, "magnetism"), "light": (7.6, 1.0, "light"),
        "weak": (9.2, 1.0, "weak\nforce"),
        "gravity": (1.75, 3.6, "gravity\nNewton 1687"), "em": (5.9, 3.6, "electromagnetism\nMaxwell 1865"),
        "strong": (9.2, 5.2, "strong force\nQCD 1973"), "ew": (7.0, 5.2, "electroweak\n1967"),
        "gr": (1.75, 6.0, "general relativity\n1915"), "sm": (8.0, 7.3, "Standard Model\n1970s"),
        "gut": (8.0, 8.9, "grand unification?"), "toe": (3.4, 9.3, "quantum gravity /\ntheory of everything?")}
    edges = [("celestial", "gravity"), ("terrestrial", "gravity"), ("elec", "em"), ("mag", "em"), ("light", "em"),
             ("em", "ew"), ("weak", "ew"), ("ew", "sm"), ("strong", "sm"), ("gravity", "gr"),
             ("sm", "gut", True), ("gut", "toe", True), ("gr", "toe", True)]
    for e in edges:
        a, b = nodes[e[0]], nodes[e[1]]
        ax.plot([a[0], b[0]], [a[1] + 0.35, b[1] - 0.45], color=MUTED if len(e) == 2 else "#bbb", lw=1.4,
                ls="-" if len(e) == 2 else "--")
    for k, (x, y, t) in nodes.items():
        fc = "#fbeee6" if k not in ("gut", "toe") else "#f4f4f4"
        box(ax, x, y, t, fc=fc, ec=PHYS if k not in ("gut", "toe") else "#aaa", fs=7.8, pad=0.28,
            ls="-" if k not in ("gut", "toe") else "--")

    ax = panel(fig, cs[6], 7, "Running couplings", "1973 – 1974", "both",
               "Force strengths change with energy. One-loop renormalization-group running of the three Standard "
               "Model couplings from measured values at 91 GeV: they nearly, but not exactly, meet. With "
               "supersymmetry (dashed, hypothetical) they would meet near 2 × 10¹⁶ GeV.", plot=True)
    mz = 91.19
    inv0 = np.array([59.0, 29.6, 8.47])
    bsm = np.array([41 / 10, -19 / 6, -7])
    bms = np.array([33 / 5, 1, -3])
    mu = np.logspace(np.log10(mz), 19, 400)
    t = np.log(mu / mz)
    labels = ["U(1) hypercharge", "SU(2) weak", "SU(3) strong"]
    for i, c in enumerate([MATH, "#3d8b5a", PHYS]):
        ax.plot(mu, inv0[i] - bsm[i] / (2 * np.pi) * t, color=c, lw=2.2, label=labels[i])
        msusy = 1000.0
        inv_s = inv0[i] - bsm[i] / (2 * np.pi) * np.log(msusy / mz)
        mu2 = mu[mu > msusy]
        ax.plot(mu2, inv_s - bms[i] / (2 * np.pi) * np.log(mu2 / msusy), color=c, lw=1.2, ls="--")
    ax.set_xscale("log")
    ax.set_xlim(mz, 1e19)
    ax.set_ylim(0, 72)
    ax.set_xlabel("energy (GeV)")
    ax.set_ylabel("1 / coupling strength")
    ax.legend(loc="upper center", fontsize=7.5, ncol=3)
    plotstyle(ax)

    ax = panel(fig, cs[7], 8, "Spontaneous symmetry breaking", "Higgs et al. 1964", "both",
               "The Higgs potential V = −μ²|φ|² + λ|φ|⁴ is symmetric, but its lowest state is not: the field settles "
               "somewhere on the rim. That choice gives W, Z bosons and fermions their mass.", projection="3d")
    r = np.linspace(0, 1.45, 60)
    t = np.linspace(0, 2 * np.pi, 80)
    Rg, Tg = np.meshgrid(r, t)
    Vh = -2 * Rg ** 2 + Rg ** 4
    ax.plot_surface(Rg * np.cos(Tg), Rg * np.sin(Tg), Vh, cmap="viridis", alpha=0.85, linewidth=0, rstride=2,
                    cstride=2)
    ax.scatter([1.0], [0.0], [-1.0 + 0.12], color=PHYS, s=60, depthshade=False)
    ax.scatter([0.0], [0.0], [0.12], color="white", edgecolor=INK, s=40, depthshade=False)
    clean3d(ax, elev=28, azim=-50)
    ax.set_box_aspect((1, 1, 0.6), zoom=1.35)

    ax = panel(fig, cs[8], 9, "Forces as particle exchange", "Feynman 1948", "both",
               "Feynman diagrams: every force is the exchange of a gauge boson. Electrons trade photons (QED), "
               "quarks trade gluons (QCD), and in beta decay a down quark turns into an up quark by emitting a W⁻.")
    axes = split(fig, ax, 3, "h", gap=0.008)
    for a in axes:
        clean(a, xlim=(-1.2, 1.2), ylim=(-1.4, 1.4))
    a = axes[0]
    _fermion(a, (-1, -1.1), (-0.0, -0.45)); _fermion(a, (0.0, -0.45), (1, -1.1))
    _fermion(a, (-1, 1.1), (0.0, 0.45)); _fermion(a, (0.0, 0.45), (1, 1.1))
    _wavy(a, (0, -0.45), (0, 0.45), "#d4a017", amp=0.1, waves=4)
    a.text(0.18, 0, "γ", fontsize=12, color="#b7950b")
    a.text(-1.1, -1.25, "e⁻", fontsize=9); a.text(-1.1, 1.2, "e⁻", fontsize=9)
    a.set_title("QED", fontsize=9.5)
    a = axes[1]
    _fermion(a, (-1, -1.1), (0.0, -0.45), PHYS); _fermion(a, (0.0, -0.45), (1, -1.1), PHYS)
    _fermion(a, (-1, 1.1), (0.0, 0.45), MATH); _fermion(a, (0.0, 0.45), (1, 1.1), MATH)
    _curly(a, (0, -0.45), (0, 0.45), "#3d8b5a", r=0.07, loops=6)
    a.text(0.2, 0, "g", fontsize=12, color="#3d8b5a")
    a.text(-1.1, -1.25, "q", fontsize=9); a.text(-1.1, 1.2, "q", fontsize=9)
    a.set_title("QCD", fontsize=9.5)
    a = axes[2]
    _fermion(a, (-0.3, -1.2), (-0.3, 0.0), INK); _fermion(a, (-0.3, 0.0), (-0.3, 1.2), INK)
    _wavy(a, (-0.3, 0.0), (0.45, 0.45), PHYS, amp=0.07, waves=4)
    _fermion(a, (0.45, 0.45), (1.0, 1.15), INK); _fermion(a, (1.0, -0.2), (0.45, 0.45), INK)
    a.text(-0.6, -1.15, "d", fontsize=10); a.text(-0.6, 1.05, "u", fontsize=10)
    a.text(0.0, 0.42, "W⁻", fontsize=9, color=PHYS)
    a.text(1.02, 1.15, "e⁻", fontsize=9); a.text(1.02, -0.3, "ν̄", fontsize=9)
    a.set_title("weak (β decay)", fontsize=9.5)
    footer(fig)
    save(fig, "13-fields-and-unification.png")


# ---------------------------------------------------------------------------------------------
# 14 Co-evolution timeline
# ---------------------------------------------------------------------------------------------
def fig14():
    W, H = 22, 12.5
    fig = figure("Co-evolution: how mathematics and physics fed each other",
                 "Upper track: mathematical ideas. Lower track: physical theories. Arrows show where a tool or "
                 "question crossed over — blue: mathematics enabled physics; orange: physics created mathematics",
                 w=W, h=H, flow=False)
    ax = fig.add_axes([0.015, 0.04, 0.97, 0.84])
    breaks = [(-350, 0.0), (1500, 12.0), (1900, 62.0), (2000, 96.0)]

    def X(y):
        for (y0, x0), (y1, x1) in zip(breaks[:-1], breaks[1:]):
            if y <= y1:
                return x0 + (y - y0) / (y1 - y0) * (x1 - x0)
        return breaks[-1][1]

    ax.set_xlim(-2, 100)
    ax.set_ylim(-3.2, 24)
    ax.axis("off")
    math_ev = [("euclid", -300, "Euclid's Elements"), ("conics", -200, "Apollonius: conics"),
               ("zero", 628, "zero & place value"), ("algebra", 820, "al-Khwārizmī: algebra"),
               ("analytic", 1637, "analytic geometry"), ("calculus", 1675, "calculus"),
               ("variational", 1744, "calculus of variations"), ("fourier", 1822, "Fourier analysis"),
               ("gauss", 1827, "Gauss: curved surfaces"), ("galois", 1832, "Galois: groups"),
               ("quaternion", 1843, "quaternions → vectors"), ("riemann", 1854, "Riemannian geometry"),
               ("matrix", 1858, "matrices"), ("lie", 1873, "Lie groups"), ("probab", 1933, "Kolmogorov probability"),
               ("hilbert", 1906, "Hilbert spaces"), ("noether", 1918, "Noether's theorem"),
               ("distrib", 1945, "distributions"), ("stoch", 1944, "Itô stochastic calculus"),
               ("bundle", 1950, "fibre bundles"), ("dynsys", 1963, "chaos / dynamical systems"),
               ("knots", 1984, "knot invariants (Jones)"), ("mirror", 1991, "mirror symmetry")]
    phys_ev = [("archimedes", -250, "Archimedes: statics"), ("ptolemy", 150, "Ptolemy: epicycles"),
               ("kepler", 1609, "Kepler's ellipses"), ("galileo", 1638, "Galileo: motion"),
               ("newton", 1687, "Newton: Principia"), ("lagrangeM", 1788, "Lagrangian mechanics"),
               ("heat", 1807, "heat conduction"), ("hamiltonM", 1834, "Hamiltonian mechanics"),
               ("maxwell", 1865, "Maxwell's equations"), ("boltz", 1877, "statistical mechanics"),
               ("threebody", 1890, "three-body problem"), ("brown", 1905, "Brownian motion"),
               ("sr", 1905, "special relativity"), ("gr", 1915, "general relativity"),
               ("qm", 1925, "matrix & wave mechanics"), ("dirac", 1930, "Dirac delta"),
               ("su3", 1961, "SU(3) quark model"), ("ym", 1954, "Yang–Mills gauge theory"),
               ("lorenz", 1963, "Lorenz weather model"), ("tqft", 1989, "Witten: QFT & knots"),
               ("strings", 1990, "string theory dualities")]

    def place(events, ybase, direction):
        events = sorted(events, key=lambda e: X(e[1]))
        rows = []
        pos = {}
        for key, yr, lab in events:
            x = X(yr)
            w = len(lab) * 0.42 + 1.4
            for r, end in enumerate(rows):
                if end + 0.4 < x - w / 2:
                    rows[r] = x + w / 2
                    break
            else:
                r = len(rows)
                rows.append(x + w / 2)
            y = ybase + direction * r * 1.55
            pos[key] = (x, y, yr, lab)
        return pos

    mp = place(math_ev, 12.6, 1)
    pp = place(phys_ev, 7.6, -1)
    ax.add_patch(Rectangle((-2, 11.7), 102, 12.3, fc="#eef3fa", ec="none", zorder=0))
    ax.add_patch(Rectangle((-2, -3.2), 102, 11.6, fc="#fbefe9", ec="none", zorder=0))
    ax.text(-1.5, 23.3, "MATHEMATICS", fontsize=13, weight="bold", color=MATH)
    ax.text(-1.5, -2.7, "PHYSICS", fontsize=13, weight="bold", color=PHYS)
    for yr in [-300, 0, 500, 1000, 1500, 1600, 1700, 1800, 1850, 1900, 1925, 1950, 1975, 2000]:
        x = X(yr)
        ax.plot([x, x], [8.6, 11.4], color="#c9c4b8", lw=0.8)
        ax.text(x, 10.0, f"{-yr} BC" if yr < 0 else str(yr), ha="center", va="center", fontsize=9, color=MUTED,
                bbox=dict(fc=BG_SAFE, ec="none", pad=1))
    ax.plot([-1, 99], [10.0, 10.0], color="#c9c4b8", lw=1, zorder=0)
    ax.text(X(1500) + 0.3, 11.05, "scale changes", fontsize=7.5, color=MUTED)
    ax.text(X(1900) + 0.3, 11.05, "scale changes", fontsize=7.5, color=MUTED)
    for pos, col, fc in [(mp, MATH, "white"), (pp, PHYS, "white")]:
        for key, (x, y, yr, lab) in pos.items():
            box(ax, x, y, f"{lab}\n{yr if yr > 0 else str(-yr) + ' BC'}", fc=fc, ec=col, fs=9.6, pad=0.32, lw=1.2,
                linespacing=1.15, zorder=5)
    links = [("conics", "kepler", "m"), ("euclid", "ptolemy", "m"), ("analytic", "newton", "m"),
             ("calculus", "newton", "b"), ("variational", "lagrangeM", "m"), ("heat", "fourier", "p"),
             ("riemann", "gr", "m"), ("quaternion", "maxwell", "m"), ("matrix", "qm", "m"), ("hilbert", "qm", "b"),
             ("lie", "su3", "m"), ("noether", "ym", "m"), ("dirac", "distrib", "p"), ("bundle", "ym", "b"),
             ("tqft", "knots", "p"), ("strings", "mirror", "p"), ("brown", "stoch", "p"), ("boltz", "probab", "p"),
             ("threebody", "dynsys", "p"), ("lorenz", "dynsys", "p"), ("hamiltonM", "qm", "m")]
    for a, b, kind in links:
        src = mp.get(a) or pp.get(a)
        dst = mp.get(b) or pp.get(b)
        col = {"m": MATH, "p": PHYS, "b": BOTH}[kind]
        sy = src[1] - 0.55 if src[1] > 10 else src[1] + 0.55
        dy = dst[1] - 0.55 if dst[1] > 10 else dst[1] + 0.55
        arrow(ax, (src[0], sy), (dst[0], dy), color=col, lw=1.5, rad=0.0, hl=9, hw=4.5, zorder=3, alpha=0.85,
              style="-|>" if kind != "b" else "<|-|>")
    for k, (col, lab) in enumerate([(MATH, "mathematics → physics"), (PHYS, "physics → mathematics"),
                                     (BOTH, "developed together")]):
        ax.plot([66 + k * 11, 68 + k * 11], [-2.6, -2.6], color=col, lw=2.5)
        ax.text(68.5 + k * 11, -2.6, lab, fontsize=10, va="center")
    save(fig, "14-co-evolution-timeline.png")


BG_SAFE = "#faf8f3"


# ---------------------------------------------------------------------------------------------
# 15 State space
# ---------------------------------------------------------------------------------------------
def fig15():
    fig = figure("What is a 'state'? The growing space of descriptions",
                 "Physics describes a system by a point in some space. That space grew from a line, to phase space, "
                 "to configuration spaces of huge dimension, to function spaces, Hilbert space and Fock space", h=10.5)
    cs = cells(fig, 2, 3, vgap=0.05)

    ax = panel(fig, cs[0], 1, "A position", "Aristotle · Galileo", "phys",
               "The state of a body is where it is. Motion is change of place: x(t). One number per body per "
               "direction.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(-1.5, 3))
    ax.plot([0.5, 9.5], [0, 0], color=INK, lw=1.5)
    for k in range(10):
        ax.plot([0.5 + k, 0.5 + k], [-0.15, 0.15], color=INK)
        ax.text(0.5 + k, -0.55, str(k), ha="center", fontsize=9)
    for k, t in enumerate([0, 1, 2, 3]):
        ax.add_patch(Circle((1.5 + 0.6 * t ** 1.6, 0.45), 0.28, fc=PHYS, alpha=0.3 + 0.23 * k))
        ax.text(1.5 + 0.6 * t ** 1.6, 1.0, f"t={t}", ha="center", fontsize=8.5)
    ax.text(5, 2.3, "state = x", fontsize=14, ha="center", color=PHYS)

    ax = panel(fig, cs[1], 2, "Phase space", "Hamilton 1834 · Liouville 1838 · Gibbs 1902", "both",
               "Position alone does not determine the future; position and momentum do. A blob of initial states "
               "flows under the pendulum dynamics: it stretches and folds but keeps its area (Liouville's theorem). "
               "Computed.", plot=True)
    q, p = np.meshgrid(np.linspace(-np.pi, np.pi, 300), np.linspace(-2.6, 2.6, 200))
    ax.contour(q, p, p ** 2 / 2 - np.cos(q), levels=12, colors=GRID, linewidths=0.7)
    th = np.linspace(0, 2 * np.pi, 400)
    blob = np.c_[-1.6 + 0.3 * np.cos(th), 0.6 + 0.3 * np.sin(th)]
    f = lambda t, s: np.concatenate([s[len(s) // 2:], -np.sin(s[:len(s) // 2])])
    times = np.linspace(0, 6, 601)
    sol = rk4(f, np.concatenate([blob[:, 0], blob[:, 1]]), times)
    for k, ti in enumerate([0, 150, 300, 600]):
        qq, pp = sol[ti, :400], sol[ti, 400:]
        area = 0.5 * np.abs(np.dot(qq, np.roll(pp, 1)) - np.dot(pp, np.roll(qq, 1)))
        ax.fill(qq, pp, color=PALETTE[k], alpha=0.75, label=f"t = {times[ti]:.1f}: area {area:.3f}")
    ax.set_xlabel("position q")
    ax.set_ylabel("momentum p")
    ax.legend(loc="lower right", fontsize=7.8)
    plotstyle(ax, grid=False)

    ax = panel(fig, cs[2], 3, "Configuration space", "Lagrange 1788", "both",
               "Two particles on a line are one point in a plane (x₁, x₂); N particles in space are one point in 3N "
               "dimensions — about 10²⁴ dimensions for a gram of matter. The line x₁ = x₂ marks collisions.")
    a1, a2 = split(fig, ax, 2, "h", gap=0.02, ratios=[1, 1.2])
    clean(a1, equal=False, xlim=(0, 10), ylim=(0, 10))
    for k, (x1, x2) in enumerate([(2, 7), (3, 6), (4.2, 5.2)]):
        y = 8 - k * 3
        a1.plot([0.5, 9.5], [y, y], color=INK, lw=1)
        a1.add_patch(Circle((x1, y + 0.4), 0.35, fc=MATH))
        a1.add_patch(Circle((x2, y + 0.4), 0.35, fc=PHYS))
        a1.text(0.2, y + 1.1, f"t = {k}", fontsize=8.5, color=MUTED)
    a2.plot([0, 10], [0, 10], color=GRID, lw=1.5, ls="--")
    pts = np.array([(2, 7), (3, 6), (4.2, 5.2)])
    a2.plot(pts[:, 0], pts[:, 1], "-o", color=BOTH, lw=2)
    a2.set_xlabel("x₁", fontsize=10, color=MATH)
    a2.set_ylabel("x₂", fontsize=10, color=PHYS)
    a2.set_xlim(0, 10)
    a2.set_ylim(0, 10)
    a2.set_aspect("equal")
    a2.text(7.5, 6.8, "x₁ = x₂", fontsize=8.5, color=MUTED, rotation=45)
    a2.set_xticks([])
    a2.set_yticks([])

    ax = panel(fig, cs[3], 4, "Fields: infinitely many coordinates", "Faraday · Maxwell 1865", "phys",
               "A field assigns a value to every point. Sampled at N points it is a vector with N components; the "
               "true field is the limit N → ∞ — a point in an infinite-dimensional space.", plot=True)
    x = np.linspace(0, 1, 400)
    phi = np.sin(2 * np.pi * x) * np.exp(-x) + 0.3 * np.sin(7 * np.pi * x)
    ax.plot(x, phi, color=PHYS, lw=2.2)
    xs = np.linspace(0.02, 0.98, 16)
    ph = np.sin(2 * np.pi * xs) * np.exp(-xs) + 0.3 * np.sin(7 * np.pi * xs)
    ax.bar(xs, ph, width=0.035, color="#9bb6d8", ec=MATH, lw=0.6)
    ax.text(0.98, 0.95, "(φ₁, φ₂, …, φ₁₆) → (φ(x))ₓ", ha="right", fontsize=10, color=MATH)
    ax.axhline(0, color=INK, lw=0.8)
    ax.set_xlabel("position x")
    ax.set_ylabel("field value φ(x)")
    plotstyle(ax)

    ax = panel(fig, cs[4], 5, "Hilbert space", "von Neumann 1932", "both",
               "A quantum state is a unit vector |ψ⟩ = a|0⟩ + b|1⟩. Measurement projects it onto a basis; the "
               "probabilities are |a|² and |b|². Change the basis (dashed) and different questions get definite "
               "answers.")
    clean(ax, xlim=(-1.4, 1.5), ylim=(-0.45, 1.35))
    th = np.radians(35)
    ax.add_patch(Wedge((0, 0), 1, 0, 90, fc="none", ec=GRID, lw=1))
    ax.annotate("", xy=(1.25, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=INK))
    ax.annotate("", xy=(0, 1.25), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=INK))
    ax.text(1.28, -0.08, "|0⟩", fontsize=11)
    ax.text(-0.12, 1.27, "|1⟩", fontsize=11)
    v = np.array([np.cos(th), np.sin(th)])
    ax.annotate("", xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=BOTH, lw=2.5))
    ax.text(v[0] + 0.05, v[1] + 0.05, "|ψ⟩", fontsize=12, color=BOTH, weight="bold")
    ax.plot([v[0], v[0]], [0, v[1]], color=MATH, ls=":", lw=1.4)
    ax.plot([0, v[0]], [v[1], v[1]], color=PHYS, ls=":", lw=1.4)
    ax.text(v[0], -0.15, f"a = {v[0]:.2f}\n|a|² = {v[0] ** 2:.2f}", ha="center", fontsize=8.5, color=MATH, va="top")
    ax.text(-0.08, v[1], f"b = {v[1]:.2f}\n|b|² = {v[1] ** 2:.2f}", ha="right", fontsize=8.5, color=PHYS, va="center")
    for ang in (45, 135):
        r = np.radians(ang)
        ax.plot([0, 1.2 * np.cos(r)], [0, 1.2 * np.sin(r)], color="#3d8b5a", ls="--", lw=1.2)
    ax.text(0.86, 0.95, "|+⟩", color="#3d8b5a", fontsize=10)
    ax.text(-0.98, 0.95, "|−⟩", color="#3d8b5a", fontsize=10)

    ax = panel(fig, cs[5], 6, "Fock space: particles as excitations", "Fock 1932 · QFT 1930s–50s", "both",
               "In quantum field theory each mode of a field is an oscillator; the number of quanta in it is the "
               "number of particles. A state lists occupation numbers |n₁, n₂, n₃, …⟩ — particles can be created "
               "and destroyed.")
    clean(ax, equal=False, xlim=(0, 10), ylim=(-0.8, 7.5))
    occ = [2, 0, 1, 3, 0, 1]
    for k, n in enumerate(occ):
        x0 = 0.7 + k * 1.55
        xs = np.linspace(-0.6, 0.6, 50)
        ax.plot(x0 + xs, 1.1 + 8 * xs ** 2, color=MUTED, lw=1)
        for lvl in range(5):
            ax.plot([x0 - 0.12 - np.sqrt((lvl + 0.5) / 8) * 0.9, x0 + 0.12 + np.sqrt((lvl + 0.5) / 8) * 0.9],
                    [1.1 + (lvl + 0.5), 1.1 + (lvl + 0.5)], color=GRID, lw=1)
        ax.add_patch(Circle((x0, 1.1 + n + 0.5), 0.17, fc=BOTH, zorder=4))
        ax.text(x0, 0.35, f"k{k + 1}", ha="center", fontsize=9, color=MUTED)
        ax.text(x0, -0.35, f"n = {n}", ha="center", fontsize=9, color=BOTH)
    ax.text(5, 7.0, "|2, 0, 1, 3, 0, 1⟩  =  7 particles", ha="center", fontsize=11, color=BOTH)
    footer(fig)
    save(fig, "15-what-is-a-state.png")


if __name__ == "__main__":
    for f in (fig11, fig12, fig13, fig14, fig15):
        f()
