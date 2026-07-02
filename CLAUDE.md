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

## Design language (current)

Minimal, calm, editorial — the aesthetic of an early-career scientist's page: simple, ordered,
nothing redundant.

- **One typeface only: Libre Baskerville** (serif), loaded from Google Fonts. No sans-serif.
- **Pastel light-blue background** across the whole page (`--paper` / `--paper-deep`), deep
  slate-navy text. No dark hero, no top nav bar, no buttons, no name banner.
- **Intro**: profile photo + name (modest size, not full-screen) + one line only,
  "Bachelor of Science in Biology".
- **Subtle boxes** (`.card`) for the Research items — the user likes these; keep them soft.
- **Dynamic background**: a soft light bloom (`.bg-glow`) descends on scroll
  (`animation-timeline: scroll()`), evoking a cave light gradient; faint horizontal strata
  (`.bg-texture`); section reveals on scroll (`.reveal`, `view()` timeline). All gated behind
  `prefers-reduced-motion`.
- Contact lives **only in the footer**, as icon links. No contact section.
- Print styles flatten to clean black-on-white.

Section order: Intro → About → Research → Presentations → Honors & Recognition →
Academic Record → Technical Profile → footer.

## Content rules (important)

- **Do not invent.** The Purdue manuscript has no title and Sebastian would be at most second
  author — never fabricate a citation. Describe it as ongoing, manuscript in preparation.
- The thesis is public: <https://hdl.handle.net/10784/38213> (EAFIT repository, sole author).
- Keep prose compact; avoid duplicating the same facts across sections.
- The "About" text is the Research Interests statement from the CV.

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
