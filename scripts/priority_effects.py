#!/usr/bin/env python3
"""Generate the priority-effects figure for correagallego.com.

A schematic, in the representation this literature uses. Fukami 2015 (Fig. 2)
draws a species pool, a set of initial niches, the arrival order of colonists
above an arrow, and the niches that end up filled, with different orders giving
different communities. Symbol shape denotes the guild whose niche a species can
occupy, and open symbols mark vacant niches. This figure follows that grammar
and is original artwork.

The mechanism drawn here is niche preemption. Three niches are available, one
per guild. Six strains make up the pool, two per guild, so two strains compete
for each niche and whichever arrives first takes it. The two rows hold the
arriving strains constant and change only their order, so the single difference
between the two communities is attributable to order alone.

It is deliberately a diagram, not a model output. The companion figure,
allocation-tradeoff.svg, is the computed one.

    python3 scripts/priority_effects.py [output.svg]
"""

from __future__ import annotations

import sys
from pathlib import Path

W, H = 566, 283
POOL_C, POOL_R = (70, 158), 50
NICHE_X, NICHE_Y = 182, (124, 158, 192)
ROW_Y = (112, 218)
SEQ_X = (268, 314, 360)
BOX_X, BOX_W = 410, 140
MARK = 11.0

TITLE = "Niche preemption, and why arrival order changes the community"
DESC = (
    "A schematic. On the left, a pool of six strains drawn as three shapes, two strains "
    "of each, one blue and one amber. Shape denotes the guild whose niche a strain can "
    "occupy. Three niches are "
    "vacant to begin with, one per guild. Two rows follow, holding the arriving strains "
    "constant and changing only their order. In each row the first strain of a guild to "
    "arrive takes that guild's niche, so the later competitor is excluded and the two "
    "resulting communities differ in one niche. The square niche stays vacant in both, "
    "because no strain of that guild arrived."
)

# Shape is the guild. Colour separates the two competitors within a guild, which
# is what the two rows turn on, so it has to carry real contrast. Blue and amber
# is the safest pair for colour-blind readers.
SHAPES = ("circle", "circle", "square", "square", "triangle", "triangle")
INK = ("var(--link)", "var(--fig-alt)") * 3
NICHE_SHAPES = ("circle", "square", "triangle")

POOL_AT = ((-24, -22), (8, -28), (28, -6), (-30, 6), (-4, 12), (22, 22))
ORDERS = ((0, 4, 1), (1, 4, 0))       # same three strains, two sequences
EXCLUDED = (2, 2)                      # the third arrival finds its niche taken
# Which strain ends up in each niche, or None where the niche stays vacant.
OUTCOMES = ((0, None, 4), (1, None, 4))


def path_for(shape, cx, cy, s):
    if shape == "circle":
        return f'cx="{cx:.1f}" cy="{cy:.1f}" r="{s / 2:.1f}"', "circle"
    if shape == "square":
        h = s / 2
        return (
            f'x="{cx - h:.1f}" y="{cy - h:.1f}" width="{s:.1f}" height="{s:.1f}" rx="1.1"',
            "rect",
        )
    h = s / 2 * 1.2
    pts = f"{cx:.1f},{cy - h:.1f} {cx + h * 1.05:.1f},{cy + h * 0.8:.1f} {cx - h * 1.05:.1f},{cy + h * 0.8:.1f}"
    return f'points="{pts}"', "polygon"


def mark(i, cx, cy, s=MARK, faded=False):
    geom, tag = path_for(SHAPES[i], cx, cy, s)
    fill = INK[i]
    cls = "pe__mark pe__mark--faded" if faded else "pe__mark"
    return f'<{tag} class="{cls}" fill="{fill}" {geom} />'


def niche(shape, cx, cy, s=MARK * 1.5):
    geom, tag = path_for(shape, cx, cy, s)
    return f'<{tag} class="pe__niche" {geom} />'


def arrow(x1, y, x2, cls="pe__arrow"):
    return (
        f'<path class="{cls}" d="M{x1:.1f},{y:.1f} H{x2:.1f} '
        f'M{x2 - 5:.1f},{y - 3.2:.1f} L{x2:.1f},{y:.1f} L{x2 - 5:.1f},{y + 3.2:.1f}" />'
    )


def build() -> str:
    out = [
        f'<svg class="fig" viewBox="0 0 {W} {H}" role="img" '
        f'aria-labelledby="pe-title pe-desc" preserveAspectRatio="xMidYMid meet">',
        f'<title id="pe-title">{TITLE}</title>',
        f'<desc id="pe-desc">{DESC}</desc>',
        f'<text class="pe__head" x="{POOL_C[0]}" y="44" text-anchor="middle">species pool</text>',
        f'<text class="pe__head" x="{NICHE_X}" y="44" text-anchor="middle">niches</text>',
        f'<text class="pe__head" x="{SEQ_X[1]}" y="44" text-anchor="middle">arrival order</text>',
        f'<text class="pe__head" x="{BOX_X + BOX_W / 2:.0f}" y="44" text-anchor="middle">community</text>',
        f'<circle class="pe__pool" cx="{POOL_C[0]}" cy="{POOL_C[1]}" r="{POOL_R}" />',
    ]
    for i, (dx, dy) in enumerate(POOL_AT):
        out.append(mark(i, POOL_C[0] + dx, POOL_C[1] + dy))

    for shape, y in zip(NICHE_SHAPES, NICHE_Y):
        out.append(niche(shape, NICHE_X, y))

    for y, order, excluded, outcome in zip(ROW_Y, ORDERS, EXCLUDED, OUTCOMES):
        out.append(arrow(NICHE_X + 22, y, SEQ_X[0] - 16))
        for k, strain in enumerate(order):
            out.append(mark(strain, SEQ_X[k], y, faded=(k == excluded)))
            if k < len(order) - 1:
                out.append(arrow(SEQ_X[k] + 9, y, SEQ_X[k + 1] - 9))
        out.append(arrow(SEQ_X[-1] + 13, y, BOX_X - 12))
        out.append(
            f'<rect class="pe__box" x="{BOX_X}" y="{y - 30:.1f}" '
            f'width="{BOX_W}" height="60" rx="4" />'
        )
        for k, (shape, strain) in enumerate(zip(NICHE_SHAPES, outcome)):
            cx = BOX_X + BOX_W * (k + 1) / 4
            if strain is None:
                out.append(niche(shape, cx, y, MARK * 1.5))
            else:
                out.append(niche(shape, cx, y, MARK * 1.5))
                out.append(mark(strain, cx, y))

    out.append(
        f'<text class="pe__note" x="{SEQ_X[2]}" y="{ROW_Y[1] + 40:.0f}" text-anchor="middle">'
        f'faded, arrived but found its niche taken</text>'
    )
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src/figures/priority-effects.svg")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build())
    print(f"wrote {target} ({target.stat().st_size / 1024:.1f} KB)")
