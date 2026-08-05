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
- `src/components/Footer.astro` — footer **signature**: rounded profile photo + name + title +
  inline-SVG icon links (email, ORCID brand-green mark, GitHub, CV) + copyright. **No LinkedIn**.
- `src/styles/global.css` — the entire design system.
- Assets in `public/assets/`: `Sebastian-Correa-Gallego-CV.pdf`, `favicon.svg` (black serif "S"),
  `field.webp` (hero), `symposium.webp`, `morphotypes.webp`, `profile.webp`, `logos/{EAFIT,Purdue}.svg`.
- **Image pipeline:** Sebastian drops originals into a `multimedia/` staging folder (git-ignored).
  Optimize with **sharp** (bundled via Astro) → WebP into `public/assets/`, referenced by plain
  `<img>`. sharp also rasterizes SVGs (e.g. the 8.7 MB `library.svg` → 66 KB `morphotypes.webp`).
  Keep shipped images small; **Cloudflare Pages rejects any file > 25 MiB** (why `thesis.pdf`, 27 MB,
  is NOT hosted — needs compression first).
- Content is inlined directly in `index.astro`. **No content collections**, no `src/content/`.

Commands: `npm run dev`, `npm run build` (must pass, no console errors).

## Design language (current) — "Modern academic homepage"

The CV content, presented as a clean modern site: a full-bleed photo hero that fades into a very
light-blue body, editorial figures, and subtle scroll reveals. Content/ideas stay coherent with the
CV; the effort is on visual quality. Still one page, no subpages.

- **Two typefaces, by role:** `Inter` (300–700) for structure — name, section titles, body, dates,
  UI. `Roboto Serif` **italic** (the "voice") for the hero phrase, the Research-Interests statement,
  and figure captions (Sebastian finds Roboto Serif more beautiful in italic). Both via Google Fonts.
- **Hero** (`.hero`, 100svh, full-bleed): `field.webp` (Sebastian sampling in the cave) as the
  background, a dark scrim gradient (heavier on the left, where the text sits; person is on the
  right), and the scrim's bottom fades to `--paper` so it connects seamlessly to the body on scroll.
  Content: name (Inter bold, white) + "B.Sc. in Biology" + the italic phrase.
- **Very light-blue body** (`--paper: #edf2fa`). Deep slate text; sober **navy links** (`#1b4b9c`).
  Reduced margins: wide container (`--wrap: 64rem`); text at a readable `--measure: 44rem`; **figures
  break wider** than the text, in white rounded cards with a soft shadow + italic caption.
- **Institution logos** (`logos/EAFIT.svg`, `Purdue.svg`) inline next to institutions, small and
  grayscale (subtle). **No ALL-CAPS, no interpunct in body** (only `·` in inst/footer meta lines).
- **Figures used:** Purdue → `symposium.webp` (title slide, no unpublished data). Thesis →
  `morphotypes.webp` (Entrance/Transition/Dark plates) + thesis `[permanent link]`.
- **Footer signature:** rounded `profile.webp` + name + "Biologist — B.Sc. …" + icon links + © note.
- Subtle `.reveal` on scroll (`view()` timeline), hero entrance, all reduced-motion-safe. Print
  flattens to B/W.

Section order: Hero → Research Interests (italic statement) → Education → Research Experience →
Academic Service → Conferences & Presentations → Honors & Recognition → Certifications & Training →
Technical Skills → footer.

**Not used (by choice):** `eeb.jpg` (group photo — third-party/minor privacy); `thesis.pdf` (27 MB
> Cloudflare's 25 MiB limit — needs compression). **No References section** on the web (privacy).

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
8. **Current — modern academic homepage.** Full-bleed cave-photo hero (`field.webp`) fading into a
   very light-blue body; Inter + Roboto Serif italic; institution logos; editorial figures
   (`symposium.webp`, `morphotypes.webp`) in cards; footer signature with `profile.webp`; subtle
   scroll reveals. Added the sharp image-optimization pipeline + git-ignored `multimedia/` staging.
   Held `thesis.pdf` (25 MiB Cloudflare limit) and skipped `eeb.jpg` (privacy).
