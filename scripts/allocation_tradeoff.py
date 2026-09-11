#!/usr/bin/env python3
"""Generate the proteome-allocation figure for correagallego.com.

Three panels built on the relations of Scott et al. 2010 (Science 330, 1099),
laid out two above and one below, centred, so that each panel is wide enough to
read on a page rather than squeezed into a third of the width.

Panel A reproduces the structure of their Figs. 1A and 2A. Two independent
perturbations move a cell along two different lines in the plane of growth rate
against RNA/protein ratio:

    nutrient quality        r = r0 + lambda / kappa_t      (positive slope)
    translational inhibition r = rmax - lambda / kappa_n   (negative slope)

kappa_t is the translational capacity and kappa_n the nutritional capacity, one
per medium. A drug-free culture sits where its medium's inhibition line meets
the nutrient line, and it is that crossing that pins the parameters down. This
is what makes the partition measurable rather than merely postulated, which is
the claim the page makes.

Panel B converts to mass fractions with phi_R = rho * r and adds the fixed
housekeeping sector, giving the Q, R and P partition of their Fig. 2B.

Panel C is the rate-yield tradeoff the partition implies, with two pools of
strains drawn on it. Yield is taken to scale with the P sector. That is an
inference, not a measurement in Scott et al., and the caption on the page says
so.

Parameter values are read from the published figures rather than from a table,
since the paper reports them graphically. They reproduce the plotted ranges.

Requires numpy and matplotlib, which are absent from the system Python under
PEP 668, so use a virtual environment.

    python3 scripts/allocation_tradeoff.py [output.svg]
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Scott et al. 2010, read off Figs. 1A and 2A.
R0 = 0.07             # RNA/protein ratio extrapolated to zero growth
KAPPA_T = 5.0         # translational capacity, per hour
R_MAX = 0.72          # RNA/protein ratio as translational capacity goes to zero
RHO = 0.76            # phi_R = rho * r
PHI_Q = 0.45          # fixed housekeeping sector
KAPPA_N = (1.0, 1.6, 2.4, 3.4, 4.6, 6.2)   # nutritional capacity, poor to rich
LAM_MAX = 2.0

# Canvas, in user units. The panels are placed by hand rather than by a grid,
# so that the third can be centred under the first two.
#
# **The plot area is square.** Every panel carries four intervals on each axis,
# so a square panel makes the grid cells square too, which is what makes these
# read as plots rather than as sketches. The canvas is derived from the panel
# rather than the other way round, so changing S is the only knob.
S = 120.0             # the side of the square plot area

LEFT = 52.0           # figure left to the plot area, for the y label and ticks
RIGHT_AX = 40.0       # panel A's second y axis, drawn outside it on the right
GUTTER = 65.0         # clear space between that axis and panel B's y label. It is
                      # wide on purpose. Two square panels stacked over one make
                      # an almost square figure, and an almost square figure is
                      # far too tall for the width the page gives it, so the
                      # gutter is what buys the aspect back. Panel C sits under
                      # it, so the space reads as composition rather than waste.
RIGHT = 16.0          # figure right margin
TOP = 48.0            # figure top to the upper plot areas, holding the title
                      # and, on panel A only, the doubling-rate scale
GAP = 72.0            # upper x label down to the lower title. It has to clear
                      # the upper x label block and then LETTER_UP again, or the
                      # lower title lands on top of the upper axis.
BOTTOM = 26.0         # lower x label to the figure edge

W = LEFT + S + RIGHT_AX + GUTTER + LEFT + S + RIGHT
H = TOP + S + GAP + S + BOTTOM
A_L = LEFT
B_L = LEFT + S + RIGHT_AX + GUTTER + LEFT
C_L = (A_L + B_L + S) / 2 - S / 2      # centred under the two above
LETTER_UP = 34.0      # panel letter and title, above the plot area

C_NUT, C_CM, C_LINE = "#1b4b9c", "#c5ccd4", "#a3abb4"
C_AXIS, C_TEXT, C_NARROW, C_WIDE = "#d6dadf", "#2b323b", "#8b929b", "#1b4b9c"
CSS = {
    C_NUT: "var(--link)",
    C_CM: "var(--fig-flow)",
    C_LINE: "var(--fig-traj)",
    C_AXIS: "var(--rule)",
    C_TEXT: "currentColor",
    C_NARROW: "var(--faint)",
}

# Type sizes are in user units, so the rendered size is these times W over the
# width the figure is given on the page. The canvas shrank with the square
# panels, so the same numbers already render larger; these are larger again.
FS_TICK, FS_LABEL, FS_SEC, FS_SECTICK = 7.4, 8.6, 8.0, 7.2
FS_TITLE, FS_NOTE, FS_MATH, FS_LETTER = 10.0, 7.8, 8.6, 11.0

TITLE = "The bacterial growth laws, the proteome partition, and the tradeoff it implies"
DESC = (
    "Three panels. The first plots the RNA to protein ratio against growth rate. A rising "
    "line follows changes in nutrient quality and a family of falling lines follows "
    "translational inhibition, one per growth medium, and each medium's drug-free culture "
    "sits where its two lines cross. The second converts that ratio into proteome mass "
    "fractions, showing a fixed housekeeping sector, a ribosomal sector that rises with "
    "growth rate, and a metabolic sector that falls by the same amount. The third shows the "
    "tradeoff between growth rate and yield that the partition implies, with two pools of "
    "strains marked on it, one occupying a narrow band of the axis and one spanning it."
)

_rng = np.random.default_rng(7)


def pool(lo, hi, n=8):
    """A pool of n strains spanning lo to hi. One strain per stratum, jittered
    inside it, so the drawn spread is the stated spread and not whatever eight
    free draws happened to give."""
    edges = np.linspace(lo, hi, n + 1)
    return edges[:-1] + _rng.uniform(0.12, 0.88, n) * np.diff(edges)


NARROW = np.sort(pool(0.64, 1.04))
WIDE = np.sort(pool(0.14, 1.90))


def r_nutrient(lam):
    return R0 + lam / KAPPA_T


def r_inhibited(lam, kn):
    return R_MAX - lam / kn


def lam_crossing(kn):
    """Where a medium's inhibition line meets the nutrient line, which is that
    medium's drug-free culture."""
    return (R_MAX - R0) / (1.0 / KAPPA_T + 1.0 / kn)


def phi_ribosomal(lam):
    return RHO * r_nutrient(lam)


def phi_metabolic(lam):
    return 1.0 - PHI_Q - phi_ribosomal(lam)


def yield_from_allocation(lam):
    return phi_metabolic(lam) / phi_metabolic(0.0)


def math_text(ax, x, y, s, size=FS_MATH, **kw):
    return ax.text(x, y, s, color=C_TEXT, fontsize=size, style="italic", **kw)


def draw_growth_laws(ax):
    lam = np.linspace(0, LAM_MAX, 200)
    ax.plot(lam, r_nutrient(lam), color=C_NUT, lw=1.5, zorder=4)

    for kn in KAPPA_N:
        lx = lam_crossing(kn)
        seg = np.linspace(0, min(lx * 1.06, LAM_MAX), 60)
        ax.plot(seg, r_inhibited(seg, kn), color=C_CM, lw=1.0, zorder=2)
        ax.plot([lx], [r_nutrient(lx)], marker="o", ms=4.2, ls="none",
                mfc=C_NUT, mec="none", zorder=5)

    math_text(ax, 1.42, 0.18, "r = r₀ + λ/κ_t", ha="center")
    math_text(ax, 0.32, 0.755, "r = r_max − λ/κ_n", ha="left", va="center")

    ax.set_xlim(0, LAM_MAX)
    ax.set_ylim(0, 0.8)
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax.set_yticklabels(["0", "0.2", "0.4", "0.6", "0.8"])
    ax.set_ylabel("RNA / protein, r", color=C_TEXT, fontsize=FS_LABEL, labelpad=2)

    sec = ax.secondary_yaxis("right", functions=(lambda r: RHO * r, lambda p: p / RHO))
    sec.set_yticks([0, 0.2, 0.4])
    sec.set_yticklabels(["0", "0.2", "0.4"])
    sec.set_ylabel("Ribosomal fraction", color=C_TEXT, fontsize=FS_SEC, labelpad=3)
    sec.tick_params(direction="out", length=2.6, width=0.8, color=C_AXIS,
                    labelcolor=C_TEXT, labelsize=FS_SECTICK, pad=1.5)
    sec.spines["right"].set_color(C_AXIS)
    sec.spines["right"].set_linewidth(0.9)


def draw_partition(ax):
    lam = np.linspace(0, LAM_MAX, 200)
    top_of_r = PHI_Q + phi_ribosomal(lam)

    ax.fill_between(lam, 0, PHI_Q, color=C_CM, alpha=0.45, lw=0)
    ax.fill_between(lam, PHI_Q, top_of_r, color=C_NUT, alpha=0.22, lw=0)
    ax.fill_between(lam, top_of_r, 1.0, color=C_LINE, alpha=0.55, lw=0)
    ax.plot(lam, top_of_r, color=C_NUT, lw=1.5, zorder=3)

    for xs, colour in ((NARROW, C_NARROW), (WIDE, C_WIDE)):
        ax.plot(xs, PHI_Q + phi_ribosomal(xs), marker="o", ms=3.0, ls="none",
                mfc=colour, mec="none", zorder=4)

    for y, sym, name in ((0.21, "φ_Q", "Housekeeping"),
                         (0.585, "φ_R", "Ribosomal"),
                         (0.88, "φ_P", "Metabolic")):
        math_text(ax, 0.94, y, sym, size=FS_MATH + 0.8, ha="right", va="center")
        ax.text(1.02, y, name, color=C_TEXT, fontsize=FS_NOTE, ha="left", va="center")

    ax.set_xlim(0, LAM_MAX)
    ax.set_ylim(0, 1.0)
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_ylabel("Proteome mass fraction", color=C_TEXT, fontsize=FS_LABEL, labelpad=2)


def draw_tradeoff(ax):
    lam = np.linspace(0.05, LAM_MAX, 200)
    ax.plot(lam, yield_from_allocation(lam), color=C_LINE, lw=1.5, zorder=2)

    for xs, colour in ((NARROW, C_NARROW), (WIDE, C_WIDE)):
        ax.plot(xs, yield_from_allocation(xs), marker="o", ms=4.2, ls="none",
                mfc=colour, mec="none", zorder=4)

    for xs, colour, y in ((NARROW, C_NARROW, 0.18), (WIDE, C_WIDE, 0.07)):
        ax.plot([xs[0], xs[-1]], [y, y], color=colour, lw=1.0, zorder=3)
        for x in (xs[0], xs[-1]):
            ax.plot([x, x], [y - 0.026, y + 0.026], color=colour, lw=1.0, zorder=3)
        ax.text(xs[-1] + 0.07, y, f"Spread {xs[-1] - xs[0]:.2f}",
                color=C_TEXT, fontsize=FS_NOTE - 0.4, va="center", ha="left")

    for k, (colour, label) in enumerate(
        ((C_NARROW, "Narrow pool"), (C_WIDE, "Wide pool"))
    ):
        y = 0.94 - k * 0.11
        ax.plot([1.28], [y], marker="o", ms=4.2, ls="none", mfc=colour, mec="none")
        ax.text(1.38, y, label, color=C_TEXT, fontsize=FS_NOTE, va="center", ha="left")

    ax.set_xlim(0, LAM_MAX)
    ax.set_ylim(0, 1.0)
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0", "0.25", "0.5", "0.75", "1"])
    ax.set_ylabel("Yield, relative to zero growth", color=C_TEXT,
                  fontsize=FS_LABEL, labelpad=2)


def doubling_axis(ax):
    sec = ax.secondary_xaxis(
        "top", functions=(lambda lam: lam / np.log(2), lambda d: d * np.log(2))
    )
    sec.set_xticks([0, 1, 2])
    sec.set_xlabel("Doublings per hour", color=C_TEXT, fontsize=FS_SEC, labelpad=4)
    sec.tick_params(direction="out", length=2.6, width=0.8, color=C_AXIS,
                    labelcolor=C_TEXT, labelsize=FS_SECTICK, pad=2.5)
    sec.spines["top"].set_color(C_AXIS)
    sec.spines["top"].set_linewidth(0.9)


def style(ax, letter, title):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(C_AXIS)
        ax.spines[side].set_linewidth(0.9)
    ax.tick_params(which="both", direction="out", length=2.8, width=0.8,
                   color=C_AXIS, labelcolor=C_TEXT, labelsize=FS_TICK, pad=2)
    ax.patch.set_alpha(0)
    ax.grid(True, which="major", color=C_AXIS, lw=0.5, alpha=0.55, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xticklabels(["0", "0.5", "1", "1.5", "2"])
    ax.set_xlabel("Growth rate λ (per hour)", color=C_TEXT, fontsize=FS_LABEL, labelpad=2)
    # Letter and title share a baseline above the panel, and the title is set
    # from the left, as a journal sets it.
    y = 1.0 + LETTER_UP / S
    ax.text(-28.0 / S, y, letter, transform=ax.transAxes, color=C_TEXT,
            fontsize=FS_LETTER, fontweight=600, va="baseline", ha="left")
    ax.text(0.0, y, title, transform=ax.transAxes, color=C_TEXT,
            fontsize=FS_TITLE, va="baseline", ha="left")


def build(out_path: Path) -> None:
    plt.rcParams["svg.fonttype"] = "none"
    fig = plt.figure(figsize=(W / 72.0, H / 72.0))

    def place(left, top):
        return fig.add_axes([left / W, (H - top - S) / H, S / W, S / H])

    axA = place(A_L, TOP)
    axB = place(B_L, TOP)
    axC = place(C_L, TOP + S + GAP)

    draw_growth_laws(axA)
    draw_partition(axB)
    draw_tradeoff(axC)
    for ax, letter, title in (
        (axA, "A", "Two growth laws"),
        (axB, "B", "The partition it fixes"),
        (axC, "C", "The tradeoff it implies"),
    ):
        style(ax, letter, title)
    # The doubling-rate scale is a relabelling of the same x axis, so it is
    # drawn once, on the panel about growth rate, which is where Scott et al.
    # put it in their Fig. 1A. Three copies were furniture, not information.
    doubling_axis(axA)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, format="svg", transparent=True, metadata={"Date": None})
    plt.close(fig)
    postprocess(out_path)


def postprocess(path: Path) -> None:
    svg = path.read_text()
    svg = svg[svg.index("<svg") :]
    for placeholder, token in CSS.items():
        svg = svg.replace(placeholder, token).replace(placeholder.upper(), token)
    svg = re.sub(r"\s*stroke:\s*#000000;\s*stroke-opacity:\s*0;?", "", svg)
    svg = re.sub(r"\s*font-family:[^;\"]*;?", "", svg)
    svg = re.sub(r"\d+\.\d{3,}", lambda m: f"{float(m.group()):.2f}".rstrip("0").rstrip("."), svg)
    # Italic text is mathematics; the page sets it in the serif.
    svg = re.sub(r'(<g style="[^"]*font-style:\s*italic[^"]*")', r'\1 class="fig__math"', svg)
    svg = re.sub(r'(<text [^>]*?)style="([^"]*font-style:\s*italic[^"]*)"',
                 r'\1class="fig__math" style="\2"', svg)
    # Real subscripts for the symbols.
    svg = re.sub("([φrκ])_([A-Za-z]+)",
                 '\\1<tspan baseline-shift="sub" font-size="74%">\\2</tspan>', svg)
    svg = svg.replace("r₀", 'r<tspan baseline-shift="sub" font-size="74%">0</tspan>')

    root = ET.fromstring(svg)
    ns = "{http://www.w3.org/2000/svg}"
    for meta in root.findall(f"{ns}metadata"):
        root.remove(meta)
    for attr in ("width", "height"):
        root.attrib.pop(attr, None)
    root.set("class", "fig")
    root.set("role", "img")
    root.set("aria-labelledby", "alloc-title alloc-desc")
    root.set("preserveAspectRatio", "xMidYMid meet")

    title = ET.Element(f"{ns}title", {"id": "alloc-title"})
    title.text = TITLE
    desc = ET.Element(f"{ns}desc", {"id": "alloc-desc"})
    desc.text = DESC
    root.insert(0, desc)
    root.insert(0, title)

    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    path.write_text(ET.tostring(root, encoding="unicode"))


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src/figures/allocation-tradeoff.svg")
    build(target)
    print(f"wrote {target} ({target.stat().st_size / 1024:.1f} KB)")
    print("  drug-free cultures, one per medium:")
    for kn in KAPPA_N:
        lx = lam_crossing(kn)
        print(f"    kappa_n {kn:4.1f}  ->  lambda {lx:.3f}/h   r {r_nutrient(lx):.3f}"
              f"   phi_R {phi_ribosomal(lx):.3f}")
