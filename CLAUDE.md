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
- Layout `src/layouts/Base.astro` (SEO meta + `og:image`, JSON-LD Person schema, footer).
- `src/components/Footer.astro` — left-aligned inline-SVG icon links (email, ORCID brand-green
  mark, GitHub, CV) + copyright. **No LinkedIn**, **no profile photo**.
- `src/styles/global.css` — the entire design system.
- Assets in `public/assets/`: `Sebastian-Correa-Gallego-CV.pdf`, `Sebastian-Correa-Gallego-Thesis.pdf`
  (defense deck), `favicon.svg` (black serif "S"), `field.webp` (hero), `logos/{EAFIT,Purdue}.svg`,
  and `profile.webp` (kept but currently unreferenced).
- **Image pipeline:** Sebastian drops originals into a `multimedia/` staging folder, then Claude
  optimizes with **sharp** (bundled via Astro) → WebP into `public/assets/` (referenced by plain
  `<img>`); sharp also rasterizes SVGs. **Delete `multimedia/` when done** (Sebastian's instruction).
  Keep shipped files small; **Cloudflare Pages rejects any file > 25 MiB** (the thesis deck had to be
  compressed 27 MB → 4.2 MB before hosting).
- Content is inlined directly in `index.astro`. **No content collections**, no `src/content/`.

Commands: `npm run dev`, `npm run build` (must pass, no console errors).

## Design language (current) — "Modern academic homepage"

The CV content, presented as a clean modern site: a full-bleed photo hero that fades into a light
body, subtle scroll reveals, **no figures** (removed — Sebastian preferred them out). One page.

- **Two typefaces, by role:** `Roboto Serif` **italic** is the "voice" — the hero **name** (bold
  italic), **section titles** (medium italic), and **dates** (light italic). `Inter` for the rest —
  body/bullets/skills (light, 300), entry roles & item titles (600), the degree line. Both via
  Google Fonts. (No serif-upright, no sans for the name — Sebastian's explicit split.)
- **Hero** (`.hero`, 100svh, full-bleed): `field.webp` (Sebastian sampling in the cave), a dark
  scrim (heavier left, where the text sits; person is on the right), bottom fades to `--paper`.
  Content: **name on two lines** (`Sebastian` / `Correa-Gallego`, Roboto Serif bold italic, white),
  "B.Sc. in Biology" (Inter), and the italic phrase.
- **Light, elegant cool-gray body** (`--paper: #eef0f2` — NOT blue, NOT dark: Sebastian tried a
  light-blue and a dark theme and rejected both; wants a very light neutral/cool gray). Dark text,
  sober **navy links** (`#1b4b9c`). `--wrap: 62rem`, text at `--measure: 47rem`.
- **Institution logos** (`logos/EAFIT.svg`, `Purdue.svg`) inline, **original colours** — EAFIT
  recoloured to its navy `#000066` (the SVG shipped black via an `icc-color` override that was
  stripped). **No ALL-CAPS, no interpunct `·` anywhere** (restore full wording + hyperlinks instead:
  ECSO Lab, Dept. of Biological Sciences; SIAB link; GEBI).
- **Thesis:** `[permanent link]` to the EAFIT repository **then** `[defense slides]` →
  `Sebastian-Correa-Gallego-Thesis.pdf` (the compressed 4.2 MB defense deck).
- **Footer:** left-aligned icon links (email, ORCID green, GitHub, CV) + © note. **No profile photo**
  in the footer (Sebastian asked to hide it; `profile.webp` stays in assets, unreferenced).
- Subtle `.reveal` on scroll (`view()` timeline), hero entrance, reduced-motion-safe. Print → B/W.

Section order: Hero → Research Interests (Inter-light statement) → Education → Research Experience →
Academic Service → Conferences & Presentations → Honors & Recognition → Certifications & Training →
Technical Skills → footer.

**Not used (by choice):** `eeb.jpg` (group photo — third-party/minor privacy). **No References
section** on the web (privacy). Reminder: Cloudflare Pages rejects any single file > 25 MiB.

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
6. Sober reset to a formal academic CV: removed the animated backdrop/gradient axis; content
   mirrors the LaTeX CV; removed the profile photo; added `Sebastian-Correa-Gallego-CV.pdf`;
   footer left-aligned, LinkedIn dropped, ORCID added; dropped References + masthead contact.
   Font churn: Palatino → Inter/white → back toward the Palatino version.
7. On the Palatino-version base: Source Serif 4, cool→warm background iterations, a bold "Biologist"
   subtitle, favicon changed to a black serif "S" on white; CV PDF refreshed with subtler wording.
8. Modern academic homepage: full-bleed cave-photo hero fading into the body; Inter + Roboto Serif
   italic; institution logos; figures in cards; footer signature. Added the sharp image pipeline.
9. **Current — refined homepage.** Removed the figures (kept the hero). Typography split: Roboto
   Serif italic for the name (two lines, bold), section titles (medium), and dates (light); Inter
   for the rest (statement/body in light 300). **Light, elegant cool-gray body** `#eef0f2` (a dark
   theme and a light-blue were both tried and rejected). EAFIT logo recoloured to navy `#000066`;
   logos in original colour. Restored full CV wording + hyperlinks (ECSO, SIAB) and removed all
   interpuncts. Added the compressed `[defense slides]` PDF after the thesis permanent link. Footer
   profile photo removed. `multimedia/` deleted after use.
