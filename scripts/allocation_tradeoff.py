#!/usr/bin/env python3
"""Generate the proteome-allocation figure for correagallego.com.

Three panels built on the relations of Scott et al. 2010 (Science 330, 1099).

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
NARROW = np.sort(_rng.uniform(0.66, 1.02, 8))
WIDE = np.sort(_rng.uniform(0.15, 1.88, 8))


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


def math_text(ax, x, y, s, size=5.8, **kw):
    return ax.text(x, y, s, color=C_TEXT, fontsize=size, style="italic", **kw)


def draw_growth_laws(ax):
    lam = np.linspace(0, LAM_MAX, 200)
    ax.plot(lam, r_nutrient(lam), color=C_NUT, lw=1.3, zorder=4)

    for kn in KAPPA_N:
        lx = lam_crossing(kn)
        seg = np.linspace(0, min(lx * 1.06, LAM_MAX), 60)
        ax.plot(seg, r_inhibited(seg, kn), color=C_CM, lw=0.9, zorder=2)
        ax.plot([lx], [r_nutrient(lx)], marker="o", ms=3.4, ls="none",
                mfc=C_NUT, mec="none", zorder=5)

    math_text(ax, 1.36, 0.20, "r = r₀ + λ/κ_t", ha="center")
    math_text(ax, 0.42, 0.66, "r = r_max − λ/κ_n", ha="left")

    ax.set_xlim(0, LAM_MAX)
    ax.set_ylim(0, 0.8)
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    ax.set_ylabel("RNA / protein, r", color=C_TEXT, fontsize=6.4, labelpad=2)
    ax.set_title("two growth laws", color=C_TEXT, fontsize=7.2, pad=22)

    sec = ax.secondary_yaxis("right", functions=(lambda r: RHO * r, lambda p: p / RHO))
    sec.set_yticks([0, 0.2, 0.4])
    sec.set_ylabel("ribosomal fraction", color=C_TEXT, fontsize=6.2, labelpad=2)
    sec.tick_params(direction="out", length=2.4, width=0.8, color=C_AXIS,
                    labelcolor=C_TEXT, labelsize=5.4, pad=1.5)
    sec.spines["right"].set_color(C_AXIS)
    sec.spines["right"].set_linewidth(0.9)


def draw_partition(ax):
    lam = np.linspace(0, LAM_MAX, 200)
    top_of_r = PHI_Q + phi_ribosomal(lam)

    ax.fill_between(lam, 0, PHI_Q, color=C_CM, alpha=0.32, lw=0)
    ax.fill_between(lam, PHI_Q, top_of_r, color=C_NUT, alpha=0.22, lw=0)
    ax.fill_between(lam, top_of_r, 1.0, color=C_CM, alpha=0.68, lw=0)
    ax.plot(lam, top_of_r, color=C_NUT, lw=1.3, zorder=3)

    for xs, colour in ((NARROW, C_NARROW), (WIDE, C_WIDE)):
        ax.plot(xs, PHI_Q + phi_ribosomal(xs), marker="o", ms=2.6, ls="none",
                mfc=colour, mec="none", zorder=4)

    math_text(ax, 1.0, 0.21, "φ_Q", size=6.4, ha="right", va="center")
    ax.text(1.05, 0.21, "housekeeping", color=C_TEXT, fontsize=5.8, ha="left", va="center")
    math_text(ax, 1.42, 0.585, "φ_R", size=6.4, ha="right", va="center")
    ax.text(1.47, 0.585, "ribosomal", color=C_TEXT, fontsize=5.8, ha="left", va="center")
    math_text(ax, 0.62, 0.87, "φ_P", size=6.4, ha="right", va="center")
    ax.text(0.67, 0.87, "metabolic", color=C_TEXT, fontsize=5.8, ha="left", va="center")

    ax.set_xlim(0, LAM_MAX)
    ax.set_ylim(0, 1.0)
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_ylabel("proteome mass fraction", color=C_TEXT, fontsize=6.4, labelpad=2)
    ax.set_title("the partition it fixes", color=C_TEXT, fontsize=7.2, pad=22)


def draw_tradeoff(ax):
    lam = np.linspace(0.05, LAM_MAX, 200)
    ax.plot(lam, yield_from_allocation(lam), color=C_LINE, lw=1.3, zorder=2)

    for xs, colour in ((NARROW, C_NARROW), (WIDE, C_WIDE)):
        ax.plot(xs, yield_from_allocation(xs), marker="o", ms=3.6, ls="none",
                mfc=colour, mec="none", zorder=4)

    for xs, colour, y in ((NARROW, C_NARROW, 0.17), (WIDE, C_WIDE, 0.06)):
        ax.plot([xs[0], xs[-1]], [y, y], color=colour, lw=0.9, zorder=3)
        for x in (xs[0], xs[-1]):
            ax.plot([x, x], [y - 0.024, y + 0.024], color=colour, lw=0.9, zorder=3)
        ax.text(xs[-1] + 0.06, y, f"spread {xs[-1] - xs[0]:.2f}",
                color=C_TEXT, fontsize=5.4, va="center", ha="left")

    for k, (colour, label) in enumerate(
        ((C_NARROW, "narrow pool"), (C_WIDE, "wide pool"))
    ):
        y = 0.96 - k * 0.1
        ax.plot([1.04], [y], marker="o", ms=3.6, ls="none", mfc=colour, mec="none")
        ax.text(1.12, y, label, color=C_TEXT, fontsize=5.8, va="center", ha="left")

    ax.set_xlim(0, LAM_MAX)
    ax.set_ylim(0, 1.04)
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_ylabel("yield, relative to zero growth", color=C_TEXT, fontsize=6.4, labelpad=2)
    ax.set_title("the tradeoff it implies", color=C_TEXT, fontsize=7.2, pad=22)


def doubling_axis(ax):
    sec = ax.secondary_xaxis(
        "top", functions=(lambda lam: lam / np.log(2), lambda d: d * np.log(2))
    )
    sec.set_xticks([0, 1, 2])
    sec.set_xlabel("doublings per hour", color=C_TEXT, fontsize=6.0, labelpad=2)
    sec.tick_params(direction="out", length=2.4, width=0.8, color=C_AXIS,
                    labelcolor=C_TEXT, labelsize=5.4, pad=1.5)
    sec.spines["top"].set_color(C_AXIS)
    sec.spines["top"].set_linewidth(0.9)


def style(ax, letter):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(C_AXIS)
        ax.spines[side].set_linewidth(0.9)
    ax.tick_params(which="both", direction="out", length=2.6, width=0.8,
                   color=C_AXIS, labelcolor=C_TEXT, labelsize=5.6, pad=2)
    ax.patch.set_alpha(0)
    ax.grid(True, which="major", color=C_AXIS, lw=0.5, alpha=0.55, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel("growth rate λ (per hour)", color=C_TEXT, fontsize=6.4, labelpad=2)
    ax.text(-0.19, 1.30, letter, transform=ax.transAxes, color=C_TEXT,
            fontsize=8.2, fontweight=500, va="top", ha="left")


def build(out_path: Path) -> None:
    plt.rcParams["svg.fonttype"] = "none"
    fig, axes = plt.subplots(1, 3, figsize=(9.1, 3.3))
    draw_growth_laws(axes[0])
    draw_partition(axes[1])
    draw_tradeoff(axes[2])
    for ax, letter in zip(axes, "ABC"):
        style(ax, letter)
        doubling_axis(ax)
    fig.subplots_adjust(left=0.062, right=0.955, top=0.7, bottom=0.135, wspace=0.42)

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
