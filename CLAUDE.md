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

Editorial, scientific, calm — clean on the surface, with one signature idea that rewards a
closer look. The concept: the page's **side margins are Sebastian's research made ambient**.

- **Two typefaces, deliberate**: `Source Serif 4` (variable) for all reading/voice; `IBM Plex
  Mono` used *only* for "instrument" labels — section indices (01–06), the eyebrow, dates,
  card meta tags. Base 18px.
- **Cool paper with a subtle top→bottom gradient** (`--paper-top` → `--paper-bottom`), echoing a
  descent from light to depth. Deep slate ink. One restrained **muted-teal accent** (`--accent`).
- **The margin instruments** (hidden < 1180px, reduced-motion safe):
  - Left = `GradientAxis.astro`: a vertical light→deep gradient scale with tick marks and a
    reading-head (`.axis__marker`) that **descends on scroll** (`@property --marker-y` animated
    via `animation-timeline: scroll()`). It is the *environmental gradient* + a scroll indicator.
  - Right = `CommunityField.astro`: a build-time-computed scatter of "morphotypes/colonies"
    whose size/spread peak through the penumbra — the *community response*, with gentle scroll
    drift. Together they render "environment as sculptor, community as response."
- **Hero**: eyebrow (mono) + photo + name + "Bachelor of Science in Biology" (mono) + the
  **organizing statement** ("I study how biological systems *assemble, organize, and transform*
  …") with the key phrase in accent.
- **Cards** for Research (kept — Sebastian likes them). `.bg-glow` descends on scroll; `.reveal`
  section entrances via `view()`. Contact is footer icon chips only. Print flattens to B/W.

Section order: Hero → 01 Orientation → 02 Research → 03 Presentations → 04 Honors →
05 Academic Record → 06 Technical Profile → footer.

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
