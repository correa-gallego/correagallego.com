#!/usr/bin/env python3
"""Generate the two-regimes figure for correagallego.com.

A schematic drawn in this literature's own notation, synthesised from the two
places Fukami sets it out.

The layout is Fukami 2010, Fig. 4.1 (Community assembly dynamics in space, in
Verhoef and Morin, eds., OUP, pp. 45-54). One species pool feeds several local
communities; a deterministic assembly converges on the same composition
whatever the immigration history, a historically contingent one diverges with
it. That chapter figure is black and white throughout and writes a community as
set notation, {4, 5, 6}, which is kept here under each community.

The marks follow Fukami 2015, Fig. 2 (Annu. Rev. Ecol. Evol. Syst. 46:1-23),
whose caption fixes the convention this field uses:

    "Different symbol colors indicate different species. Symbol shapes denote
     the guilds or functional groups that the species belong to."

So colour is the species, nine of them, and shape is the guild, three of three.
Each local community holds one species per guild, which is what makes it a set
of filled niches rather than an arbitrary list. An earlier version of this
figure inverted that, putting the group on colour and the species on a numeral,
which read against the convention.

Species are numbered down the guilds, 1, 4 and 7 in the first, 2, 5 and 8 in
the second, 3, 6 and 9 in the third, so that the three possible communities are
the consecutive triads {1, 2, 3}, {4, 5, 6} and {7, 8, 9} of Fukami's chapter
figure and each holds one species of each guild.

The colours are Paul Tol's muted qualitative scheme, which is built to stay
separable for colour-blind readers. They are ordered so the three triads fall
into three colour families, which is what lets a reader see at a glance whether
two communities are the same.

The habitat condition row is an extension, not Fukami's. His chapter holds the
environment constant and says in prose that deterministic assembly is the case
where composition "is determined by environmental conditions". Crossing history
against habitat draws that sentence.

    python3 scripts/priority_effects.py [output.svg]
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

W, H = 552, 374
LABEL_X = 76                       # right edge of the row labels
LABEL_DY = 12.4                    # leading of the two-line row labels. The label is set
                                   # at 9.6px and a text run's box is about 1.2 times its
                                   # size, so anything under about 11.6 makes the two lines
                                   # collide, which is what 10.4 was doing.
COL_X = [118, 192, 266, 356, 430, 504]
PANEL_Y = (14, 202)                # top of each panel

POOL_Y, POOL_H = 22, 38            # the shared pool capsule
POOL_MARK_Y = 15                   # mark centre, from the top of the capsule
POOL_KEY_Y = 33                    # numeral baseline, from the top of the capsule
POOL_STEP = 30                     # between species within a triad
POOL_GAP = 58                      # between triads
POOL_PAD = 30                      # the capsule rounds off this far past the marks

HIST_Y = 82                        # the immigration-history letter
COMM_Y = 120                       # centre of the local-community box
COMM_W, COMM_UP, COMM_DOWN = 78, 25, 23
COMM_MARK_Y = -11                  # marks, relative to the box centre
COMM_SET_Y = 16                    # set notation, relative to the box centre
COMM_STEP = 21                     # between marks inside a community
HAB_Y = 158                        # the habitat-condition numeral

R_POOL, R_COMM = 9.6, 8.6          # mark radius in each row

# Tol muted. Nine species, ordered so the triads read as colour families.
SPECIES = (
    "var(--sp1)", "var(--sp2)", "var(--sp3)",
    "var(--sp4)", "var(--sp5)", "var(--sp6)",
    "var(--sp7)", "var(--sp8)", "var(--sp9)",
)
# Guild membership. Species n belongs to guild (n - 1) % 3, so every community,
# being a consecutive triad, holds exactly one species of each.
GUILD_SHAPE = ("triangle", "circle", "star")

HISTORIES = ("A", "B", "C", "A", "B", "C")
HABITATS = ("I", "I", "I", "II", "II", "II")
ROWS = (
    ("Species", "pool"),
    ("Immigration", "history"),
    ("Local", "community"),
    ("Habitat", "condition"),
)

# Which triad of species ends up in each column. Triad t is {3t+1, 3t+2, 3t+3}.
DETERMINISTIC = (0, 0, 0, 1, 1, 1)      # follows the habitat condition
CONTINGENT = (0, 1, 2, 0, 1, 2)         # follows the immigration history

TITLE = "Two regimes of community assembly from one species pool"
DESC = (
    "Two panels over the same pool of nine species, which fall into three guilds of three. "
    "Colour marks the species and shape marks the guild, so every local community holds one "
    "species of each guild and is written out beneath as a set of three numbers. Each panel "
    "crosses three immigration histories against two habitat conditions, giving six local "
    "communities. In the upper panel assembly is deterministic and the community that forms "
    "follows the habitat condition, so changing the immigration history makes no difference. "
    "In the lower panel assembly is historically contingent and the community follows the "
    "immigration history instead, so changing the habitat condition makes none."
)


def _poly(points, fill):
    d = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polygon class="fk__sp" fill="{fill}" points="{d}" />'


def mark(n, cx, cy, r):
    """One species. Colour is the species, shape is its guild."""
    fill = SPECIES[n - 1]
    shape = GUILD_SHAPE[(n - 1) % 3]
    if shape == "circle":
        return (f'<circle class="fk__sp" fill="{fill}" cx="{cx:.2f}" cy="{cy:.2f}" '
                f'r="{r * 0.92:.2f}" />')
    if shape == "triangle":
        # Equilateral, point up, nudged down so it sits on the optical centre.
        pts = [
            (cx + r * 1.24 * math.cos(math.radians(a)),
             cy + r * 1.24 * math.sin(math.radians(a)) + r * 0.14)
            for a in (-90, 30, 150)
        ]
        return _poly(pts, fill)
    # Five-pointed star.
    pts = []
    for k in range(10):
        rad = r * 1.06 if k % 2 == 0 else r * 0.45
        a = math.radians(-90 + k * 36)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return _poly(pts, fill)


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

    for y, words in zip(
        (top + POOL_Y + POOL_MARK_Y, top + HIST_Y, top + COMM_Y, top + HAB_Y), ROWS
    ):
        o.append(row_label(y, words))

    # The pool, shared by every column. The nine sit as the three triads they
    # can form, each triad holding one species of every guild.
    mid = (COL_X[0] + COL_X[-1]) / 2
    span = 3 * 2 * POOL_STEP + 2 * POOL_GAP
    left = mid - span / 2
    xs = [left + (k // 3) * (2 * POOL_STEP + POOL_GAP) + (k % 3) * POOL_STEP for k in range(9)]
    o.append(
        f'<rect class="fk__pool" x="{xs[0] - POOL_PAD:.1f}" y="{top + POOL_Y}" '
        f'width="{xs[-1] - xs[0] + 2 * POOL_PAD:.1f}" height="{POOL_H}" '
        f'rx="{POOL_H / 2}" />'
    )
    for k, x in enumerate(xs):
        o.append(mark(k + 1, x, top + POOL_Y + POOL_MARK_Y, R_POOL))
        o.append(
            f'<text class="fk__key" x="{x:.1f}" y="{top + POOL_Y + POOL_KEY_Y}" '
            f'text-anchor="middle">{k + 1}</text>'
        )

    for col, x in enumerate(COL_X):
        o.append(arrow(x, top + POOL_Y + POOL_H + 4, top + COMM_Y - COMM_UP - 4))
        o.append(
            f'<text class="fk__hist" x="{x + 9:.0f}" y="{top + HIST_Y + 4:.0f}">'
            f'{HISTORIES[col]}</text>'
        )
        o.append(
            f'<rect class="fk__comm" x="{x - COMM_W / 2:.1f}" '
            f'y="{top + COMM_Y - COMM_UP}" width="{COMM_W}" '
            f'height="{COMM_UP + COMM_DOWN}" rx="7" />'
        )
        base = assignment[col] * 3 + 1
        for k in range(3):
            o.append(mark(base + k, x + (k - 1) * COMM_STEP,
                          top + COMM_Y + COMM_MARK_Y, R_COMM))
        members = ", ".join(str(base + k) for k in range(3))
        o.append(
            f'<text class="fk__set" x="{x}" y="{top + COMM_Y + COMM_SET_Y}" '
            f'text-anchor="middle">{{{members}}}</text>'
        )
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
    for t, name in ((DETERMINISTIC, "deterministic"), (CONTINGENT, "contingent")):
        cols = ["{" + ", ".join(str(v * 3 + k + 1) for k in range(3)) + "}" for v in t]
        print(f"  {name:14} {' '.join(cols)}")
