# Is the constancy of the speed of light just a postulate?

It isn't a pure postulate, and it isn't fully derived either. Some of it can be derived, some of it is a convention, and some of it has to be measured.

## A correction first

The constancy of the speed of light is a postulate of **special** relativity, not general relativity. Special relativity has two postulates:

1. **The principle of relativity:** the laws of physics are the same in every inertial frame.
2. **Light's speed is independent of the source:** light in vacuum travels at speed \(c\) no matter how its source is moving.

General relativity starts from different assumptions: the equivalence principle, general covariance, and the Einstein field equations. In general relativity, \(c\) is constant only **locally**. Any freely falling observer measures light passing them at \(c\). Over larger distances, the coordinate speed of light can vary, which is why light is delayed when it passes near the Sun (the Shapiro delay). So "constancy of \(c\)" is a different kind of statement in general relativity.

## What can be derived

**1. Maxwell's equations plus the relativity principle.** Maxwell's equations predict electromagnetic waves that travel at
\[
c = \frac{1}{\sqrt{\mu_0 \varepsilon_0}},
\]
and this formula doesn't depend on how the source or observer is moving. If Maxwell's equations are true laws, the relativity principle says they hold in every inertial frame. Then every inertial observer gets the same \(c\). Einstein's second postulate mostly works as a way to commit to Maxwell over Newtonian mechanics without assuming any particular theory of matter.

**2. An invariant speed follows from symmetry alone ("relativity without light").** In 1910–1911, Ignatowsky, and separately Frank and Rothe, showed you can drop the light postulate altogether. They assumed only:

- the principle of relativity,
- that space and time are homogeneous (the same everywhere and at all times),
- that space is isotropic (the same in every direction),
- that the transformations between frames form a group, and that cause comes before effect.

From these, the only possible transformations between frames have the form
\[
x' = \gamma (x - vt), \quad t' = \gamma\left(t - \kappa v x\right), \quad \gamma = \frac{1}{\sqrt{1 - \kappa v^2}},
\]
where \(\kappa\) is a universal constant. There are three cases:

- \(\kappa = 0\) gives the Galilean transformations of Newtonian mechanics.
- \(\kappa > 0\) gives the Lorentz transformations, with an invariant speed \(1/\sqrt{\kappa}\).
- \(\kappa < 0\) is ruled out, because it would let time mix with space like a rotation and break the order of cause and effect.

So the structure "there is one invariant speed, possibly infinite" is a theorem, not an assumption. What symmetry can't tell you is whether that speed is finite, or what its value is. That has to come from experiment.

**3. Why light travels at that speed.** Once an invariant speed exists, special relativity requires every massless particle to travel at it. So the question becomes why the photon is massless. In quantum field theory, the electromagnetic gauge symmetry (called U(1)) forbids a photon mass term. That is a real theoretical reason, but gauge symmetry is itself assumed, so the explanation moves the postulate somewhere else rather than removing it. Experiments put the photon's mass below about \(10^{-18}\) eV.

## What is convention

**Only the round-trip speed of light can be measured.** To measure light's speed in one direction, you need two clocks at different places that are already synchronized. But synchronizing them requires knowing the one-way speed of light. Reichenbach and later Edwards showed that assuming different one-way speeds in the two directions, with the same round-trip average, makes identical predictions for every experiment. So part of "light has the same speed in every direction" is a choice of how to synchronize clocks (Einstein's choice), not a fact about nature. The round-trip speed is the part that is genuinely physical.

**The numerical value of \(c\) carries no physical content.** Since 1983, \(c = 299{,}792{,}458\) m/s exactly, by definition: the metre is defined from it. A quantity that has units can't be explained in a meaningful way, because changing units changes the number. The meaningful questions are about dimensionless quantities such as the fine-structure constant \(\alpha \approx 1/137\), and nobody can derive that one either.

## What is empirical

These experiments tie the theory to reality:

- **Michelson–Morley** (1887): no change in light's speed with direction.
- **Kennedy–Thorndike** (1932): no change with the observer's velocity.
- **Ives–Stilwell** (1938): time dilation measured in moving sources.
- **Double-star observations** (de Sitter, 1913, and later X-ray versions): light's speed doesn't depend on how fast its source moves.
- **GW170817** (2017): gravitational waves and light from the same neutron-star merger arrived almost together. This showed gravity travels at \(c\) to about one part in \(10^{15}\), which supports the idea that \(c\) is a property of spacetime itself, not of light in particular.

## Summary

| Part of the claim | Status |
|---|---|
| A universal invariant speed exists | Derived from relativity + symmetry + causality |
| That speed is finite | Empirical |
| Light travels at it | Follows from photon masslessness (gauge symmetry, itself assumed) |
| Equal speed in all directions | Partly a clock-synchronization convention; the round-trip speed is physical |
| Its numerical value | Unit convention, with no physical content |
| Locally constant in general relativity | Follows from the equivalence principle |

In modern terms, \(c\) is best understood as a conversion factor between units of time and units of space in the geometry of spacetime. Light just happens to be something that travels at it. The real postulate underneath is the relativity principle and the symmetries of spacetime. Why nature chose a finite invariant speed (\(\kappa > 0\)) rather than an infinite one (\(\kappa = 0\)) is the part nobody has explained.