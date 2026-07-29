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
- Layout `src/layouts/Base.astro` (SEO meta, JSON-LD Person schema, footer). No background layers.
- `src/components/Footer.astro` — left-aligned inline-SVG icon links: email, ORCID (brand-green
  mark), GitHub, CV. **No LinkedIn** (Sebastian: not used by scientists).
- `src/styles/global.css` — the entire design system.
- Assets kept in `public/assets/`: `Sebastian-Correa-Gallego-CV.pdf`, `favicon.svg`. Nothing else.
  **No profile photo** (removed at Sebastian's request). No web fonts (Palatino is a system stack).
- Content is inlined directly in `index.astro`. There are **no content collections** and no
  `src/content/`. Keep it that way unless the content grows substantially.

Commands: `npm run dev`, `npm run build` (must pass, no console errors).

## Design language (current) — "The CV, on the web"

Sober, formal, document-like — the site is Sebastian's academic CV rendered as a clean web page,
mirroring the LaTeX/Palatino PDF as closely as is sensible. **No decoration, no background art, no
scroll animations.** This was a deliberate reset from an earlier animated design; keep it minimal
unless Sebastian asks to reintroduce flourishes.

- **One typeface: Palatino** via system stack (`"Palatino Linotype","Book Antiqua",Palatino,
  "URW Palladio L",Georgia,serif`). No web-font request — faithful to the CV's `mathpazo`, and fast.
- **Neutral pale-gray background** (`--paper: #f4f4f1`) — solid, no gradient. **No blue / no
  non-neutral hues** (Sebastian's explicit preference). Text near-black `--ink`, headings gray
  `--head`, sober **navy links** (`--link: #133a80`, matching the PDF's `RGB(0,0,102)`).
- **No ALL-CAPS in body/section titles**; the name uses `font-variant: small-caps`. Interpunct
  `·` only in the masthead contact line and footer note.
- **CV layout**: left-aligned single column (`--content: 48rem`). Masthead = name + one italic
  subtitle line ("Biologist — microbial ecology and evolutionary biology"), rule under. **No
  contact line under the name** — all contact lives in the footer only (Sebastian's call).
  Sections = bold gray title + thin rule. Entries use a **left date gutter** (`.entry` is a
  `8.5rem 1fr` grid: italic muted date | `.entry__body` with bold title, meta, gray bullets);
  collapses to stacked on ≤620px. Skills as `strong:` labelled paragraphs. `.entry__title-sub` =
  the non-bold degree/detail after a bold institution.
- **The site is NOT a 1:1 copy of the PDF.** Notably: **no References section** (privacy) and no
  masthead contact block, even though the PDF has both.
- **Footer**: left-aligned icon links (email, ORCID green mark, GitHub octocat, CV) + a
  `© {year} Sebastian Correa-Gallego` copyright note. Print styles flatten to black-on-white.

Section order: Masthead → Research Interests → Education → Research Experience → Academic
Service → Conferences and Presentations → Honors and Recognition → Certifications and Training →
Technical Skills → footer.

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

- **Source of truth is the CV.** The site content mirrors Sebastian's LaTeX academic CV
  (Palatino/`mathpazo`). When he shares an updated CV, reconcile the page to it. Do not invent.
- **Contact email is `correagsebastian2204@gmail.com`** (the CV's; not the old EAFIT address).
  ORCID: `0009-0007-8703-3188` — keep `rel="me"` on ORCID links (identity cross-referencing).
- The Purdue manuscript has no public citation; describe the internship work as the CV does
  (project *Proteome Allocation Rules in Osmotrophic Eukaryotes*), never a fabricated paper.
- The thesis is public: <https://hdl.handle.net/10784/38213> (EAFIT repository, sole author).
- **References** (Pinel, Muñoz-Gómez) are published with emails per Sebastian's instruction and
  the PDF; offer to switch to "available on request" if he wants to shield them from scrapers.
- **Never surface sensitive material** from the Notion workspace: fellowship names/IDs, the
  school shortlist, psychological/strategic notes, interim plans, finalist dates.

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
5. Minimalist redesign (Baskerville, pastel), then an editorial "field notes on a gradient" phase:
   Roboto Serif + a generative Darwin-tree / microbial backdrop with scroll animation.
6. **Current**: sober reset to a formal academic CV. Removed the entire animated backdrop and
   gradient axis; switched to Palatino on a neutral pale-gray solid background with navy links;
   rebuilt content to mirror the LaTeX CV (added Certifications, References, extra bullets/entries,
   new Research Interests). Removed the profile photo and old CV; added
   `Sebastian-Correa-Gallego-CV.pdf`. Footer left-aligned, LinkedIn dropped, ORCID added.
