#!/usr/bin/env python3
"""Generate the priority-effects figure for correagallego.com.

A schematic, in the representation this literature uses for priority effects.
Fukami 2015 (Fig. 2) draws a species pool, the arrival order of colonists above
an arrow, and the community that results, with different orders giving different
communities. This figure follows that grammar and is original artwork.

It is deliberately a diagram and not a model output. The companion figure,
allocation-tradeoff.svg, is the computed one. The caption on the page says which
is which.

Layout is generated from the parameters below rather than positioned by hand, so
the figure is reproducible and easy to re-balance.

    python3 scripts/priority_effects.py [output.svg]
"""

from __future__ import annotations

import sys
from pathlib import Path

W, H = 452, 196
POOL_C, POOL_R = (54, 104), 40
ROW_Y = (78, 146)
SEQ_X = (136, 163, 190)
BOX_X, BOX_W = 252, 78
MARK = 7.0

TITLE = "The same three strains, two arrival orders, two communities"
DESC = (
    "A schematic. On the left, a pool of six strains drawn as six different symbols. "
    "Two rows run to the right. Each row shows the same three strains arriving in a "
    "different order, then the community that results. Each community keeps the strain "
    "that arrived first, so the two communities differ although the pool and the "
    "conditions are the same."
)

# Six strains, distinguished by shape and by whether they are filled, so the
# figure survives greyscale and colour-blind viewing.
SHAPES = ("circle", "square", "triangle", "circle", "square", "triangle")
FILLED = (True, True, True, False, False, False)

POOL_AT = ((-20, -16), (6, -22), (24, -2), (-24, 8), (-2, 6), (16, 20))
# The same three strains in two sequences. Each community keeps the strain that
# arrived first, plus one of the others, so the outcome is always a subset of
# what actually arrived and the priority effect is legible.
ORDERS = ((0, 4, 2), (2, 0, 4))
OUTCOMES = ((0, 2), (2, 4))


def mark(i, cx, cy, s=MARK):
    fill = "var(--link)" if FILLED[i] else "var(--paper)"
    cls = f'class="pe__mark" fill="{fill}"'
    shape = SHAPES[i]
    if shape == "circle":
        return f'<circle {cls} cx="{cx:.1f}" cy="{cy:.1f}" r="{s / 2:.1f}" />'
    if shape == "square":
        h = s / 2
        return f'<rect {cls} x="{cx - h:.1f}" y="{cy - h:.1f}" width="{s:.1f}" height="{s:.1f}" rx="0.8" />'
    h = s / 2 * 1.18
    pts = f"{cx:.1f},{cy - h:.1f} {cx + h:.1f},{cy + h * 0.82:.1f} {cx - h:.1f},{cy + h * 0.82:.1f}"
    return f'<polygon {cls} points="{pts}" />'


def arrow(x1, y, x2):
    return (
        f'<path class="pe__arrow" d="M{x1:.1f},{y:.1f} H{x2:.1f} '
        f'M{x2 - 4:.1f},{y - 2.6:.1f} L{x2:.1f},{y:.1f} L{x2 - 4:.1f},{y + 2.6:.1f}" />'
    )


def build() -> str:
    out = [
        f'<svg class="fig" viewBox="0 0 {W} {H}" role="img" '
        f'aria-labelledby="pe-title pe-desc" preserveAspectRatio="xMidYMid meet">',
        f'<title id="pe-title">{TITLE}</title>',
        f'<desc id="pe-desc">{DESC}</desc>',
        '<text class="pe__head" x="54" y="46" text-anchor="middle">species pool</text>',
        '<text class="pe__head" x="163" y="46" text-anchor="middle">arrival order</text>',
        f'<text class="pe__head" x="{BOX_X + BOX_W / 2:.0f}" y="46" text-anchor="middle">community</text>',
        f'<circle class="pe__pool" cx="{POOL_C[0]}" cy="{POOL_C[1]}" r="{POOL_R}" />',
    ]
    for i, (dx, dy) in enumerate(POOL_AT):
        out.append(mark(i, POOL_C[0] + dx, POOL_C[1] + dy))

    for row, (y, order, outcome) in enumerate(zip(ROW_Y, ORDERS, OUTCOMES)):
        out.append(arrow(POOL_C[0] + POOL_R + 6, y, SEQ_X[0] - 12))
        for k, strain in enumerate(order):
            out.append(mark(strain, SEQ_X[k], y))
            if k < len(order) - 1:
                out.append(arrow(SEQ_X[k] + 6, y, SEQ_X[k + 1] - 6))
        out.append(arrow(SEQ_X[-1] + 10, y, BOX_X - 8))
        out.append(
            f'<rect class="pe__box" x="{BOX_X}" y="{y - 19:.1f}" '
            f'width="{BOX_W}" height="38" rx="3" />'
        )
        for k, strain in enumerate(outcome):
            out.append(mark(strain, BOX_X + BOX_W * (k + 1) / (len(outcome) + 1), y))
        out.append(
            f'<text class="pe__row" x="{BOX_X + BOX_W + 10}" y="{y + 3.4:.1f}">'
            f'community {row + 1}</text>'
        )

    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src/figures/priority-effects.svg")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build())
    print(f"wrote {target} ({target.stat().st_size / 1024:.1f} KB)")
