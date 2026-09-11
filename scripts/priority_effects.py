#!/usr/bin/env python3
"""Generate the two-regimes figure for correagallego.com.

A schematic, in the representation this literature uses. Fukami sets the
deterministic and the historically contingent cases side by side over the same
species pool, crossing immigration history against habitat condition, so that
each regime is read off which axis the resulting community follows. This figure
uses that conceptual layout with original artwork.

    Deterministic   the community follows the habitat condition, and the three
                    immigration histories leave no mark.
    Contingent      the community follows the immigration history, and the
                    habitat condition leaves no mark.

Nine species in three groups of three. Colour carries the group, so the pattern
is visible before any numeral is read; the numerals identify species within a
group. Two habitat conditions by three immigration histories gives six columns
per panel.

The canvas is deliberately narrow. The species marks carry the figure, so the
columns sit close together and the marks are drawn large, rather than the
reverse. Row labels wrap to two lines to keep the left margin off the drawing.

It is deliberately a diagram, not a model output. The companion figure,
allocation-tradeoff.svg, is the computed one.

    python3 scripts/priority_effects.py [output.svg]
"""

from __future__ import annotations

import sys
from pathlib import Path

W, H = 552, 396
LABEL_X = 76                       # right edge of the row labels
LABEL_DY = 10.4                    # leading of the two-line row labels
COL_X = [118, 192, 266, 356, 430, 504]
PANEL_Y = (14, 216)                # top of each panel
POOL_Y, POOL_H = 26, 32
HIST_Y = 80
COMM_Y, COMM_R = 126, 30
HAB_Y = 168
POOL_PAD = 32                      # the pool rounds off this far past the end columns
POOL_STEP = 34                     # between species within a group
POOL_GAP = 84                      # between the three groups

GROUPS = ("var(--link)", "var(--fig-alt)", "var(--fig-sep)")
HISTORIES = ("A", "B", "C", "A", "B", "C")
HABITATS = ("I", "I", "I", "II", "II", "II")
ROWS = (
    ("Species", "pool"),
    ("Immigration", "history"),
    ("Local", "community"),
    ("Habitat", "condition"),
)

# Which group of three species ends up in each column.
DETERMINISTIC = (0, 0, 0, 1, 1, 1)      # follows the habitat condition
CONTINGENT = (0, 1, 2, 0, 1, 2)         # follows the immigration history

TITLE = "Two regimes of community assembly from one species pool"
DESC = (
    "Two panels over the same pool of nine species, arranged in three groups of three. "
    "Each panel crosses three immigration histories against two habitat conditions, giving "
    "six local communities. In the upper panel assembly is deterministic and the community "
    "that forms follows the habitat condition, so changing the immigration history makes "
    "no difference. In the lower panel assembly is historically contingent and the community "
    "follows the immigration history instead, so changing the habitat condition makes no "
    "difference."
)


def species(n, cx, cy, r):
    """A numbered species mark. Colour is the group, the numeral the identity."""
    fill = GROUPS[(n - 1) // 3]
    return (
        f'<circle class="fk__sp" fill="{fill}" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" />'
        f'<text class="fk__num" x="{cx:.1f}" y="{cy + r * 0.36:.1f}" '
        f'text-anchor="middle">{n}</text>'
    )


def arrow(x, y1, y2):
    return (
        f'<path class="fk__arrow" d="M{x:.1f},{y1:.1f} V{y2:.1f} '
        f'M{x - 3.4:.1f},{y2 - 5.0:.1f} L{x:.1f},{y2:.1f} L{x + 3.4:.1f},{y2 - 5.0:.1f}" />'
    )


def row_label(y, words):
    """Two lines, right-anchored, centred on the row."""
    top = y - LABEL_DY / 2 + 3.4
    return "".join(
        f'<text class="fk__row" x="{LABEL_X}" y="{top + k * LABEL_DY:.1f}" '
        f'text-anchor="end">{w}</text>'
        for k, w in enumerate(words)
    )


def panel(top, assignment, title):
    o = [f'<text class="fk__title" x="0" y="{top:.0f}">{title}</text>']

    # Row labels, once per panel so each panel reads on its own.
    for y, words in zip(
        (top + POOL_Y + POOL_H / 2, top + HIST_Y, top + COMM_Y, top + HAB_Y), ROWS
    ):
        o.append(row_label(y, words))

    # The species pool, shared by every column of the panel.
    o.append(
        f'<rect class="fk__pool" x="{COL_X[0] - POOL_PAD}" y="{top + POOL_Y}" '
        f'width="{COL_X[-1] - COL_X[0] + 2 * POOL_PAD}" height="{POOL_H}" '
        f'rx="{POOL_H / 2}" />'
    )
    # The nine sit as three triads, so the grouping reads off the pool itself
    # and not only off the colour.
    mid = (COL_X[0] + COL_X[-1]) / 2
    left = mid - (3 * 2 * POOL_STEP + 2 * POOL_GAP) / 2
    for k in range(9):
        cx = left + (k // 3) * (2 * POOL_STEP + POOL_GAP) + (k % 3) * POOL_STEP
        o.append(species(k + 1, cx, top + POOL_Y + POOL_H / 2, r=10.4))

    for col, x in enumerate(COL_X):
        o.append(arrow(x, top + POOL_Y + POOL_H + 4, top + COMM_Y - COMM_R - 4))
        o.append(
            f'<text class="fk__hist" x="{x + 9:.0f}" y="{top + HIST_Y + 4:.0f}">'
            f'{HISTORIES[col]}</text>'
        )
        o.append(f'<circle class="fk__comm" cx="{x}" cy="{top + COMM_Y}" r="{COMM_R}" />')
        base = assignment[col] * 3 + 1
        for k, (dx, dy) in enumerate(((-11, 6), (0, -10), (11, 7))):
            o.append(species(base + k, x + dx, top + COMM_Y + dy, r=9.4))
        o.append(
            f'<text class="fk__hab" x="{x}" y="{top + HAB_Y + 4:.0f}" '
            f'text-anchor="middle">{HABITATS[col]}</text>'
        )
    return o


def build() -> str:
    out = [
        f'<svg class="fig" viewBox="0 0 {W} {H}" role="img" '
        f'aria-labelledby="fk-title fk-desc" preserveAspectRatio="xMidYMid meet">',
        f'<title id="fk-title">{TITLE}</title>',
        f'<desc id="fk-desc">{DESC}</desc>',
    ]
    out += panel(PANEL_Y[0], DETERMINISTIC, "Deterministic assembly")
    out += panel(PANEL_Y[1], CONTINGENT, "Historically contingent assembly")
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src/figures/priority-effects.svg")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build())
    print(f"wrote {target} ({target.stat().st_size / 1024:.1f} KB)")
