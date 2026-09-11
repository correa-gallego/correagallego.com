#!/usr/bin/env python3
"""Generate the proteome-allocation figure for correagallego.com.

Panel A is the bacterial growth law of Scott et al. 2010. A cell's proteome
splits into a fixed housekeeping sector, a ribosomal sector whose mass fraction
rises linearly with growth rate, and a catabolic sector that takes what is left.

    phi_R(lambda) = phi_R0 + lambda / nu

Panel B is the rate-yield tradeoff that the same partition implies. Yield is
taken to scale with the catabolic sector, since that is the proteome left to
extract biomass per unit resource once translation has been paid for. Two pools
of strains are drawn on that line, one occupying a narrow range of the axis and
one spanning it, which is the contrast the doctoral question turns on.

The lines are computed from the parameterisation, not drawn. Strain positions
are sampled from fixed seeds so the figure is reproducible.

Requires numpy and matplotlib. Writes to the path given as the first argument,
defaulting to src/figures/allocation-tradeoff.svg, which index.astro inlines
with Astro's ?raw import so the CSS custom properties resolve against the page.

    python3 scripts/allocation_tradeoff.py [output.svg]
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Growth-law parameters, read off Fig. 1A of Scott et al. 2010. The ribosomal
# mass fraction runs from about 0.05 at zero growth to about 0.34 at 2 per hour,
# which fixes the intercept and the slope. The proteome is partitioned into a
# fixed housekeeping sector Q and a growth-dependent pair R and P, following the
# Q/R/P scheme of their Fig. 2B.
PHI_R0 = 0.05          # ribosomal fraction extrapolated to zero growth
NU = 7.0               # inverse slope of the growth law, per hour
PHI_Q = 0.45           # fixed housekeeping sector
LAM_MAX = 2.0          # growth rates plotted, per hour, as in the paper

C_RIBO, C_CATA, C_LINE = "#1b4b9c", "#c5ccd4", "#a3abb4"
C_AXIS, C_TEXT, C_NARROW, C_WIDE = "#d6dadf", "#2b323b", "#8b929b", "#1b4b9c"
CSS = {
    C_RIBO: "var(--link)",
    C_CATA: "var(--fig-flow)",
    C_LINE: "var(--fig-traj)",
    C_AXIS: "var(--rule)",
    C_TEXT: "currentColor",
    C_NARROW: "var(--faint)",
}

TITLE = "Proteome allocation and the rate-yield tradeoff"
DESC = (
    "Two panels. On the left, the bacterial growth law. The share of the proteome given "
    "to ribosomes rises in a straight line with growth rate, and the share left for "
    "catabolic enzymes falls by the same amount. On the right, the tradeoff this implies "
    "between growth rate and yield, with two pools of strains marked on it. One pool sits "
    "in a narrow band of the axis and the other spans it, which is the contrast the "
    "research question turns on."
)


# Two pools of eight strains each, sampled once so both panels show the same
# organisms. The narrow pool occupies a short stretch of the growth-rate axis and
# the wide pool spans it, which is the contrast the research question turns on.
_rng = np.random.default_rng(7)
NARROW = np.sort(_rng.uniform(0.66, 1.02, 8))
WIDE = np.sort(_rng.uniform(0.15, 1.88, 8))


def phi_ribosomal(lam):
    return PHI_R0 + lam / NU


def phi_metabolic(lam):
    """The P sector takes whatever the fixed and ribosomal sectors leave."""
    return 1.0 - PHI_Q - phi_ribosomal(lam)


def yield_from_allocation(lam):
    """Yield is taken to scale with the P sector, normalised to its value at zero
    growth. This is an inference from the partition, not a measurement in Scott
    et al., and the caption on the page says so."""
    return phi_metabolic(lam) / phi_metabolic(0.0)


def math_label(ax, x, y, symbol, word):
    """The symbol in italic, which the page renders in the serif, then the word
    in the figure sans, which is how a paper sets a labelled quantity."""
    ax.text(x, y, symbol, color=C_TEXT, fontsize=6.4, ha="right", va="center", style="italic")
    ax.text(x + 0.035, y, "  " + word, color=C_TEXT, fontsize=6.0, ha="left", va="center")


def draw_growth_law(ax):
    lam = np.linspace(0, LAM_MAX, 200)
    top_of_r = PHI_Q + phi_ribosomal(lam)

    ax.fill_between(lam, 0, PHI_Q, color=C_CATA, alpha=0.32, lw=0)
    ax.fill_between(lam, PHI_Q, top_of_r, color=C_RIBO, alpha=0.22, lw=0)
    ax.fill_between(lam, top_of_r, 1.0, color=C_CATA, alpha=0.68, lw=0)
    ax.plot(lam, top_of_r, color=C_RIBO, lw=1.3, zorder=3)

    math_label(ax, 1.0, 0.20, "\u03c6_Q", "housekeeping")
    math_label(ax, 1.44, 0.585, "\u03c6_R", "ribosomal")
    math_label(ax, 0.66, 0.86, "\u03c6_P", "metabolic")
    ax.text(
        0.06, 0.055, "\u03c6_R = 0.05 + \u03bb / 7.0",
        color=C_TEXT, fontsize=5.9, ha="left", style="italic",
    )

    # The same strains as panel B, shown where they sit in the partition.
    for xs, colour in ((NARROW, C_NARROW), (WIDE, C_WIDE)):
        ax.plot(
            xs, PHI_Q + phi_ribosomal(xs), marker="o", ms=2.8, ls="none",
            mfc=colour, mec="none", zorder=4,
        )

    ax.set_xlim(0, LAM_MAX)
    ax.set_ylim(0, 1.0)
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel("growth rate \u03bb (per hour)", color=C_TEXT, fontsize=6.4, labelpad=2)
    ax.set_ylabel("proteome mass fraction", color=C_TEXT, fontsize=6.4, labelpad=2)
    ax.set_title("the growth law", color=C_TEXT, fontsize=7.2, pad=24)


def draw_tradeoff(ax):
    lam = np.linspace(0.08, LAM_MAX - 0.05, 200)
    ax.plot(lam, yield_from_allocation(lam), color=C_LINE, lw=1.1, zorder=2)

    for xs, colour in ((NARROW, C_NARROW), (WIDE, C_WIDE)):
        ax.plot(
            xs, yield_from_allocation(xs), marker="o", ms=3.8, ls="none",
            mfc=colour, mec="none", zorder=4,
        )

    # The spread each pool occupies, which is the quantity the hypothesis is about.
    for xs, colour, y in ((NARROW, C_NARROW, 0.16), (WIDE, C_WIDE, 0.06)):
        ax.plot([xs[0], xs[-1]], [y, y], color=colour, lw=0.9, zorder=3)
        for x in (xs[0], xs[-1]):
            ax.plot([x, x], [y - 0.022, y + 0.022], color=colour, lw=0.9, zorder=3)
        ax.text(
            xs[-1] + 0.05, y, f"spread {xs[-1] - xs[0]:.2f}",
            color=C_TEXT, fontsize=5.6, va="center", ha="left",
        )

    # Legend in the upper right, which the declining line leaves empty.
    for k, (colour, label) in enumerate(
        ((C_NARROW, "narrow pool"), (C_WIDE, "wide pool"))
    ):
        y = 0.95 - k * 0.11
        ax.plot([1.06], [y], marker="o", ms=3.8, ls="none", mfc=colour, mec="none")
        ax.text(1.14, y, label, color=C_TEXT, fontsize=6.0, va="center", ha="left")

    ax.set_xlim(0, LAM_MAX)
    ax.set_ylim(0, 1.04)
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel("growth rate \u03bb (per hour)", color=C_TEXT, fontsize=6.4, labelpad=2)
    ax.set_ylabel("yield, relative to \u03bb = 0", color=C_TEXT, fontsize=6.4, labelpad=2)
    ax.set_title("the tradeoff it implies", color=C_TEXT, fontsize=7.2, pad=24)


def doubling_axis(ax):
    """Scott et al. carry a doubling-rate scale above the growth-rate axis.
    One doubling per hour is ln(2) per hour of exponential growth."""
    sec = ax.secondary_xaxis(
        "top",
        functions=(lambda lam: lam / np.log(2), lambda d: d * np.log(2)),
    )
    sec.set_xticks([0, 1, 2])
    sec.set_xlabel("doublings per hour", color=C_TEXT, fontsize=6.2, labelpad=2)
    sec.tick_params(
        direction="out", length=2.4, width=0.8,
        color=C_AXIS, labelcolor=C_TEXT, labelsize=5.4, pad=1.5,
    )
    sec.spines["top"].set_color(C_AXIS)
    sec.spines["top"].set_linewidth(0.9)


def style(ax, letter):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(C_AXIS)
        ax.spines[side].set_linewidth(0.9)
    ax.tick_params(
        which="both", direction="out", length=2.6, width=0.8,
        color=C_AXIS, labelcolor=C_TEXT, labelsize=5.6, pad=2,
    )
    ax.patch.set_alpha(0)
    ax.grid(True, which="major", color=C_AXIS, lw=0.5, alpha=0.55, zorder=0)
    ax.set_axisbelow(True)
    ax.text(
        -0.155, 1.26, letter, transform=ax.transAxes,
        color=C_TEXT, fontsize=8.2, fontweight=500, va="top", ha="left",
    )


def build(out_path: Path) -> None:
    plt.rcParams["svg.fonttype"] = "none"
    fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.95))
    draw_growth_law(axes[0])
    draw_tradeoff(axes[1])
    for ax, letter in zip(axes, "AB"):
        style(ax, letter)
        doubling_axis(ax)
    fig.subplots_adjust(left=0.088, right=0.985, top=0.7, bottom=0.135, wspace=0.30)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, format="svg", transparent=True, metadata={"Date": None})
    plt.close(fig)
    postprocess(out_path)


def postprocess(path: Path) -> None:
    import re

    svg = path.read_text()
    svg = svg[svg.index("<svg") :]
    for placeholder, token in CSS.items():
        svg = svg.replace(placeholder, token).replace(placeholder.upper(), token)
    svg = re.sub(r"\s*stroke:\s*#000000;\s*stroke-opacity:\s*0;?", "", svg)
    svg = re.sub(r"\s*font-family:[^;\"]*;?", "", svg)
    # Italic text is mathematics. Tag it so the page can set it in the serif.
    svg = re.sub(
        r'(<g style="[^"]*font-style:\s*italic[^"]*")',
        r'\1 class="fig__math"',
        svg,
    )
    svg = re.sub(
        r'(<text [^>]*?)style="([^"]*font-style:\s*italic[^"]*)"',
        r'\1class="fig__math" style="\2"',
        svg,
    )
    # Real subscripts for the sector symbols, which ASCII underscores only approximate.
    svg = re.sub(
        "\u03c6_([A-Za-z])",
        '\u03c6<tspan baseline-shift="sub" font-size="74%">\\1</tspan>',
        svg,
    )
    svg = re.sub(r"\d+\.\d{3,}", lambda m: f"{float(m.group()):.2f}".rstrip("0").rstrip("."), svg)

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
    target = (
        Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src/figures/allocation-tradeoff.svg")
    )
    build(target)
    print(f"wrote {target} ({target.stat().st_size / 1024:.1f} KB)")
    for lam in (0.0, 1.0, LAM_MAX):
        print(
            f"  growth rate {lam:.2f}/h  ribosomal {phi_ribosomal(lam):.3f}"
            f"  metabolic {phi_metabolic(lam):.3f}  yield {yield_from_allocation(lam):.3f}"
        )
