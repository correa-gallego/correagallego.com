#!/usr/bin/env python3
"""Generate the phase-portrait figure for the research section of correagallego.com.

Two panels of the same two-species Lotka-Volterra competition model. Only the
interspecific competition coefficients differ between them.

    dN1/dt = r1 * N1 * (1 - N1 - a12 * N2)
    dN2/dt = r2 * N2 * (1 - N2 - a21 * N1)

Carrying capacities are scaled to 1, so a12 and a21 measure interspecific
competition relative to intraspecific competition.

    Left panel   a12 = a21 = 0.6, product 0.36 < 1
                 One globally stable coexistence state.
    Right panel  a12 = a21 = 1.6, product 2.56 > 1
                 Each species can exclude the other. Two stable states at the
                 single-species equilibria and an unstable saddle between them,
                 whose stable manifold is the separatrix.

Nothing in the output is placed by hand. Fixed points are found with
scipy.optimize.fsolve and classified from the eigenvalues of the analytic
Jacobian. Trajectories and the separatrix are integrated with
scipy.integrate.solve_ivp. The flow field is the right-hand side evaluated on
a grid.

Requires numpy, scipy and matplotlib. Writes the SVG to the path given as the
first argument, defaulting to src/figures/phase-portraits.svg, which
index.astro inlines at build time so that the CSS custom properties and
currentColor resolve against the page. The background is transparent.

    python3 scripts/phase_portraits.py [output.svg]
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

# Growth rates. Only the interspecific coefficients change between panels.
R1, R2 = 1.0, 0.85
PANELS = (
    {"a12": 0.6, "a21": 0.6, "title": "weak competition", "sub": "one stable state"},
    {"a12": 1.6, "a21": 1.6, "title": "strong mutual competition", "sub": "two stable states"},
)
LIM = 1.32  # axis limit, in units of carrying capacity

# Placeholder colours, rewritten as CSS custom properties after export.
C_FLOW, C_TRAJ, C_SEP = "#c5ccd4", "#a3abb4", "#6d7883"
C_AXIS, C_STABLE, C_UNSTABLE, C_TEXT, C_START = "#d6dadf", "#1b4b9c", "#eef0f2", "#2b323b", "#8b929b"
CSS = {
    C_FLOW: "var(--fig-flow)",
    C_TRAJ: "var(--fig-traj)",
    C_SEP: "var(--fig-sep)",
    C_AXIS: "var(--rule)",
    C_STABLE: "var(--link)",
    C_UNSTABLE: "var(--paper)",
    C_TEXT: "currentColor",
    C_START: "var(--faint)",
}

TITLE = "Phase portraits of a two-species competition model"
DESC = (
    "Two panels of the same Lotka-Volterra competition model, differing only in how "
    "strongly each species competes with the other. On the left, weak interspecific "
    "competition gives a single stable state that every starting composition flows to. "
    "On the right, competition strong enough for either species to exclude the other "
    "gives two stable states, one for each species, separated by a curve running "
    "through an unstable saddle. Which state a community reaches depends on the "
    "composition it starts from."
)


def rhs(_t, n, a12, a21):
    """Right-hand side of the competition model."""
    n1, n2 = n
    return [R1 * n1 * (1 - n1 - a12 * n2), R2 * n2 * (1 - n2 - a21 * n1)]


def jacobian(n, a12, a21):
    n1, n2 = n
    return np.array(
        [
            [R1 * (1 - 2 * n1 - a12 * n2), -R1 * a12 * n1],
            [-R2 * a21 * n2, R2 * (1 - 2 * n2 - a21 * n1)],
        ]
    )


def fixed_points(a12, a21):
    """Solve for the equilibria, then classify each from its Jacobian."""
    guesses = [(0, 0), (1, 0), (0, 1), (0.5, 0.5), (0.3, 0.7), (0.7, 0.3)]
    found: list[np.ndarray] = []
    for g in guesses:
        sol, _, ok, _ = fsolve(lambda n: rhs(0, n, a12, a21), g, full_output=True)
        if ok != 1 or np.any(sol < -1e-9) or np.any(sol > LIM):
            continue
        sol = np.clip(sol, 0.0, None)
        if not any(np.allclose(sol, f, atol=1e-6) for f in found):
            found.append(sol)

    classified = []
    for p in found:
        ev = np.linalg.eigvals(jacobian(p, a12, a21))
        kind = "stable" if np.all(ev.real < -1e-9) else "unstable"
        classified.append({"point": p, "kind": kind, "eigenvalues": ev})
    return classified


def separatrix(saddle, a12, a21):
    """The saddle's stable manifold, traced by integrating the flow backwards."""
    ev, evec = np.linalg.eig(jacobian(saddle, a12, a21))
    stable_dir = np.real(evec[:, int(np.argmin(ev.real))])
    branches = []
    for sign in (1, -1):
        start = saddle + sign * 1e-4 * stable_dir
        if np.any(start < 0):
            continue
        sol = solve_ivp(
            lambda t, n: [-v for v in rhs(t, n, a12, a21)],
            (0, 40),
            start,
            dense_output=True,
            max_step=0.05,
            rtol=1e-9,
            atol=1e-11,
        )
        pts = sol.y.T
        keep = np.all((pts >= -1e-6) & (pts <= LIM), axis=1)
        branches.append(pts[keep])
    return branches


def starting_points(bistable):
    """Ten starting compositions, none of them on the separatrix."""
    if bistable:
        raw = [
            (0.10, 0.28), (0.28, 0.10), (0.06, 0.95), (0.95, 0.06),
            (0.45, 0.95), (0.95, 0.45), (0.20, 0.62), (0.62, 0.20),
            (0.75, 1.20), (1.20, 0.75),
        ]
    else:
        raw = [
            (0.05, 0.05), (1.20, 0.08), (0.08, 1.20), (1.20, 1.20),
            (0.60, 0.05), (0.05, 0.60), (1.25, 0.55), (0.55, 1.25),
            (0.22, 0.95), (0.95, 0.22),
        ]
    return [np.array(p) for p in raw]


def draw_panel(ax, cfg):
    a12, a21 = cfg["a12"], cfg["a21"]
    bistable = a12 * a21 > 1

    # Flow field, evaluated from the equations on a grid.
    g = np.linspace(0.08, LIM - 0.06, 7)
    X, Y = np.meshgrid(g, g)
    U = np.empty_like(X)
    V = np.empty_like(Y)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            U[i, j], V[i, j] = rhs(0, (X[i, j], Y[i, j]), a12, a21)
    mag = np.hypot(U, V)
    mag[mag == 0] = 1.0
    ax.quiver(
        X, Y, U / mag, V / mag,
        color=C_FLOW, angles="xy", pivot="mid",
        scale=17, width=0.006, headwidth=3.4, headlength=4.0, headaxislength=3.4,
    )

    points = fixed_points(a12, a21)

    if bistable:
        saddle = next(
            p["point"] for p in points
            if p["kind"] == "unstable" and np.all(p["point"] > 1e-6)
        )
        for branch in separatrix(saddle, a12, a21):
            ax.plot(branch[:, 0], branch[:, 1], color=C_SEP, lw=0.9, ls=(0, (3, 3)), zorder=3)

    def settled(_t, n, *_a):
        return float(np.hypot(*rhs(0, n, a12, a21)) - 2e-4)

    settled.terminal = True
    settled.direction = -1

    for p0 in starting_points(bistable):
        sol = solve_ivp(
            rhs, (0, 80), p0, args=(a12, a21),
            dense_output=True, events=settled, rtol=1e-9, atol=1e-11,
        )
        # Sample densely early, where the curvature is, and sparsely once it settles.
        t_end = sol.t[-1]
        ts = t_end * np.linspace(0, 1, 55) ** 1.8
        curve = sol.sol(ts)
        ax.plot(curve[0], curve[1], color=C_TRAJ, lw=0.9, ls="-", zorder=4)
        ax.plot(
            [p0[0]], [p0[1]], marker="o", ms=2.2,
            color=C_START, mec="none", ls="none", zorder=5,
        )

    for p in points:
        n1, n2 = p["point"]
        if n1 < -1e-6 or n2 < -1e-6 or (n1 < 1e-6 and n2 < 1e-6):
            continue  # the origin is never reached and only adds clutter
        if p["kind"] == "stable":
            ax.plot(
                [n1], [n2], marker="o", ms=6.4,
                color=C_STABLE, mec="none", ls="none", zorder=6,
            )
        elif n1 > 1e-6 and n2 > 1e-6:  # the interior saddle, not the boundary ones
            ax.plot(
                [n1], [n2], marker="o", ms=5.6, color=C_SEP,
                mfc=C_UNSTABLE, mec=C_SEP, mew=1.1, ls="none", zorder=6,
            )

    ax.set_xlim(0, LIM)
    ax.set_ylim(0, LIM)
    ax.set_aspect("equal")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(C_AXIS)
        ax.spines[side].set_linewidth(0.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("abundance of species 1", color=C_TEXT, fontsize=6.4, labelpad=3)
    ax.set_ylabel("abundance of species 2", color=C_TEXT, fontsize=6.4, labelpad=3)
    ax.set_title(cfg["title"], color=C_TEXT, fontsize=7.4, fontweight="500", pad=9)
    ax.text(
        0.5, 1.005, cfg["sub"], transform=ax.transAxes,
        ha="center", va="bottom", color=C_TEXT, fontsize=6.4, alpha=0.75,
    )
    ax.patch.set_alpha(0)


def build(out_path: Path) -> None:
    plt.rcParams["svg.fonttype"] = "none"
    plt.rcParams["font.family"] = "Inter, system-ui, sans-serif"

    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.15))
    for ax, cfg in zip(axes, PANELS):
        draw_panel(ax, cfg)
    fig.subplots_adjust(left=0.07, right=0.985, top=0.86, bottom=0.11, wspace=0.30)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, format="svg", transparent=True, metadata={"Date": None})
    plt.close(fig)
    postprocess(out_path)


def postprocess(path: Path) -> None:
    """Strip the chrome matplotlib adds and hand colour control to the page."""
    import re

    svg = path.read_text()
    svg = svg[svg.index("<svg") :]

    for placeholder, token in CSS.items():
        svg = svg.replace(placeholder, token).replace(placeholder.upper(), token)

    # matplotlib paints an invisible black stroke on every marker.
    svg = re.sub(r"\s*stroke:\s*#000000;\s*stroke-opacity:\s*0;?", "", svg)
    # The page owns the type, so drop the embedded fallback stack.
    svg = re.sub(r"\s*font-family:[^;\"]*;?", "", svg)
    # Six decimals of coordinate precision is far more than a 440px figure needs.
    svg = re.sub(r"\d+\.\d{3,}", lambda m: f"{float(m.group()):.2f}".rstrip("0").rstrip("."), svg)

    root = ET.fromstring(svg)
    ns = "{http://www.w3.org/2000/svg}"
    for meta in root.findall(f"{ns}metadata"):
        root.remove(meta)

    # Size from the page, not from matplotlib's inches.
    for attr in ("width", "height"):
        root.attrib.pop(attr, None)
    # Tag the trajectories so the page can draw them in on scroll.
    for el in root.iter(f"{ns}path"):
        if "var(--fig-traj)" in el.get("style", ""):
            el.set("class", "fig__draw")
            el.set("pathLength", "1")

    root.set("class", "fig")
    root.set("role", "img")
    root.set("aria-labelledby", "fig-title fig-desc")
    root.set("preserveAspectRatio", "xMidYMid meet")

    title = ET.Element(f"{ns}title", {"id": "fig-title"})
    title.text = TITLE
    desc = ET.Element(f"{ns}desc", {"id": "fig-desc"})
    desc.text = DESC
    root.insert(0, desc)
    root.insert(0, title)

    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    path.write_text(ET.tostring(root, encoding="unicode"))


if __name__ == "__main__":
    target = (
        Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src/figures/phase-portraits.svg")
    )
    build(target)
    print(f"wrote {target} ({target.stat().st_size / 1024:.1f} KB)")
    for cfg in PANELS:
        pts = fixed_points(cfg["a12"], cfg["a21"])
        label = f"a12={cfg['a12']} a21={cfg['a21']} product={cfg['a12'] * cfg['a21']:.2f}"
        print(f"  {label}")
        for p in sorted(pts, key=lambda q: tuple(q["point"])):
            n1, n2 = p["point"]
            ev = ", ".join(f"{v.real:+.3f}" for v in p["eigenvalues"])
            print(f"    ({n1:.4f}, {n2:.4f})  {p['kind']:<8} eigenvalues {ev}")
