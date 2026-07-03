# CLAUDE.md — correagallego.com

Single source of context for this repository. Read fully before editing.

## Who this is for

Sebastian Correa-Gallego. Biologist, B.Sc. in Biology, Universidad EAFIT, Medellín,
Colombia (2022–2026), GPA 4.44/5.00. Research: microbial community ecology along a light
gradient in a tropical volcaniclastic cave (undergraduate thesis, EAFIT, sole author) and
proteome allocation in osmotrophic yeasts under carbon limitation (ECSO Lab, Purdue, visiting
intern 2025–2026, ongoing). Preparing doctoral applications in microbial ecology / evolutionary
biology. Audience: PhD admissions committees and prospective advisors — they value substance,
precision, and restraint. No self-promotion.

## What the site is

A single, static, one-page academic homepage. Personal CV/identity site — no blog, no
multi-page routing, no analytics, no third-party scripts.

## Stack & tooling

- **Astro 5**, static output (`output: 'static'`), `@astrojs/sitemap`.
- One page: `src/pages/index.astro` (+ `src/pages/404.astro`).
- Layout `src/layouts/Base.astro` (SEO meta, JSON-LD Person schema, background layers, footer).
- `src/components/Footer.astro` — inline-SVG icon links (email, LinkedIn, GitHub, CV).
- `src/styles/global.css` — the entire design system.
- Assets kept in `public/assets/`: `profile.jpg` (optimized ~64 KB), `Curriculum_Vitae.pdf`,
  `favicon.svg`. Nothing else — all other media was removed as unused.
- Content is inlined directly in `index.astro`. There are **no content collections** and no
  `src/content/`. Keep it that way unless the content grows substantially.

Commands: `npm run dev`, `npm run build` (must pass, no console errors).

## Design language (current) — "Field notes on a gradient"

Editorial, scientific, calm — clean on the surface, with a generative background that rewards a
closer look. The concept: a naturalist's field notebook.

- **One typeface: `Roboto Serif`** (variable, opsz+wght) for everything — chosen for a
  "frictionless", whisper-serif reading feel. No sans-serif, no monospace. Base 18px.
- **No ALL-CAPS anywhere** (Sebastian dislikes it) and **no middle-dot/interpunct separators
  except in the footer** — use em dashes, commas, or line breaks instead.
- **Cool paper with a subtle top→bottom gradient** (light → depth). Deep slate ink; one
  restrained **muted-teal accent** (`--accent`). Content column widened (`--content: 50rem`).
- **Generative backdrop** (`src/components/Backdrop.astro`): faint, hand-drawn microbial
  specimens (cocci, bacilli, filaments, diatoms, branching lineages, budding yeast) plus contour
  lines, scattered to the periphery, computed deterministically at build time. Three layers
  **drift and progressively emerge on scroll** (`animation-timeline: scroll()`) — a community
  assembling along the gradient. A radial mask keeps the reading column legible; frosted `.card`s
  (`backdrop-filter`) lift off it. Reduced-motion → static; near-empty on mobile.
- **Hero** (no eyebrow — just the person): photo + name + "Bachelor of Science in Biology" + the
  **italic organizing statement** (Sebastian likes it) with the key phrase in accent.
- **Section headings**: `01 — Orientation` etc., normal case, index in accent. `.reveal`
  entrances via `view()`. Contact is footer icon chips only (interpunct allowed there). Print B/W.

Section order: Hero → 01 Orientation → 02 Research → 03 Presentations → 04 Honors →
05 Academic Record → 06 Technical Profile → footer. "Orientation" prose = the CV research-interests
statement. Technical Profile includes R/Python, QGIS (spatial), LaTeX, Git.

## Who Sebastian is (for framing content — from his own field notebook, non-sensitive)

Organizing question: **how biological systems assemble, organize, and transform across time and
environment** — a *class of phenomenon*, not a field or organism. Intellectual frame: the tension
between **contingency and convergence** (do the forms life takes follow discoverable rules, or
history and chance?). Two windows: **outward** = microbial communities in natural systems;
**inward** = cellular physiology / evolutionary transitions under constraint; aim = the interface.
Microbial systems as the tractable platform; **gradients as the experimental axis**. The cave
thesis and the Purdue yeast work are two scales of the same logic: life reorganizing under
energetic constraint. Current direction phrase (safe to use): "cellular resource allocation and
the predictability of microbial community assembly."

## Content rules (important)

- **Do not invent.** The Purdue manuscript has no title and Sebastian would be at most second
  author — never fabricate a citation. Describe it as ongoing, manuscript in preparation.
- The thesis is public: <https://hdl.handle.net/10784/38213> (EAFIT repository, sole author).
- **Never surface sensitive material** from the Notion workspace: fellowship names/IDs, the
  school shortlist, psychological/strategic notes, interim plans, finalist dates. Only the
  committee-facing intellectual framing above is public.
- Keep prose compact; avoid duplicating facts across sections.

## Deployment

- Hosted on **Cloudflare Pages** (project `correagallego`), auto-deploys on every push to
  `main` via the connected GitHub App. **No GitHub Actions** — do not add `.github/workflows/`.
- DNS in Cloudflare: `correagallego.com` and `www` are proxied CNAMEs → `correagallego.pages.dev`.
- GitHub Pages is retired. The repo may be private without affecting deploys.
- Build settings: framework Astro, `npm run build`, output `dist`, `NODE_VERSION=20`.

## History (bitácora)

1. Migrated off GitHub Pages to Cloudflare Pages; cleaned DNS; retired the Actions workflow.
2. Consolidated a former multi-page site into one page; first editorial redesign.
3. Design-refinement pass (typography, spacing, hero depth, scroll progress, card panels).
4. Favicon → serif "SC" monogram on a navy tile.
5. **Current**: full minimalist redesign — single Baskerville typeface, pastel-blue background,
   no nav/buttons, content reduced to match the compact academic CV, contact moved to footer
   icons; removed all unused components, content collections, and media; repo cleaned to just
   the profile photo, CV, and favicon.
