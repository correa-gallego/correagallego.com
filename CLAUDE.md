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

A single, static, one-page academic homepage — **two full-viewport screens and a footer**:
a photo hero, then one research-narrative section. **The site is deliberately NOT a copy of
the CV**: the CV lives in the PDF, linked from the one visible button. No blog, no multi-page
routing, no analytics, no third-party scripts, **no JavaScript at all**.

## Stack & tooling

- **Astro 5**, static output (`output: 'static'`), `@astrojs/sitemap`.
- One page: `src/pages/index.astro` (+ `src/pages/404.astro`).
- Layout `src/layouts/Base.astro` (SEO meta + `og:image`, JSON-LD Person schema, footer).
- `src/components/Footer.astro` — left-aligned inline-SVG icon links (email, ORCID brand-green
  mark, Google Scholar, GitHub, Bluesky) + copyright. **No LinkedIn**, **no profile photo**,
  **no CV icon** (the CV moved to the fixed top-right button in `Base.astro`).
- `src/styles/global.css` — the entire design system.
- Assets in `public/assets/`: `Sebastian-Correa-Gallego-CV.pdf` (**the live CV — keep this exact
  filename so the shared URL never breaks**; replace the file in place when Sebastian sends a new
  version), `favicon.svg` (black serif "S"), `field.webp` (hero). Kept but **unreferenced**:
  `Sebastian-Correa-Gallego-Thesis.pdf` (4.2 MB defense deck), `logos/{EAFIT,Purdue}.svg`,
  `profile.webp` — retained because their URLs may already be circulating.
- **Image pipeline:** Sebastian drops originals into a `multimedia/` staging folder, then Claude
  optimizes with **sharp** (bundled via Astro) → WebP into `public/assets/` (referenced by plain
  `<img>`); sharp also rasterizes SVGs. **Delete `multimedia/` when done** (Sebastian's instruction).
  Keep shipped files small; **Cloudflare Pages rejects any file > 25 MiB** (the thesis deck had to be
  compressed 27 MB → 4.2 MB before hosting).
- Content is inlined directly in `index.astro`. **No content collections**, no `src/content/`.

Commands: `npm run dev`, `npm run build` (must pass, no console errors).

## Design language (current) — "Two screens"

Hero, then one research section, then the footer. Nothing else. The whole page is
**hero (100svh) → `.focus` (100svh) → footer**; total scroll ≈ two screens.

- **Two typefaces, by role:** `Roboto Serif` **italic** is the "voice" — the hero **name** (bold
  italic) and the `.focus__lead` research question (medium italic). `Inter` for the rest — the
  narrative body (light, 300), the eyebrow and figure labels (500), the degree line, the CV
  button. Both via Google Fonts. (No serif-upright, no sans for the name — Sebastian's split.)
- **Hero** (`.hero`, 100svh, full-bleed) — unchanged and not to be redesigned: `field.webp`
  (Sebastian sampling in the cave), a dark scrim (heavier left, where the text sits; person is on
  the right), bottom fades to `--paper`. Content: **name on two lines** (`Sebastian` /
  `Correa-Gallego`), "B.Sc. in Biology", and the phrase. `.hero__cue` is now an anchor → `#research`.
- **`.focus`** (100svh, vertically centred). **There is no eyebrow/kicker** — Sebastian removed
  "Research" and its rule ("si el contenido es meramente esa pestaña, no lo veo necesario"), so the
  lead **question** is the section's own masthead: Roboto Serif medium italic, **no `max-width`**,
  sized `clamp(1.35rem, 2.6vw, 1.8rem)` so it lands on exactly **two full-measure lines** across
  every desktop width. Below it a 2-column grid, `repeat(2, minmax(0,1fr))`, `align-items: start`
  -- **narrative left / SVG figure right**, the figure nudged `margin-top: .35rem` so its top label
  sits on the first line of body text. The section closes with a full-width `<hr class="focus__rule">`
  and a muted `.focus__coda` capped at 62ch. Two `@media` blocks keep it inside one screen:
  `max-height: 780px` (shrinks type) and `max-width: 860px` (stacks, figure first).
  **The two-line lead is load-bearing** — it replaces the deleted rule as the section's top edge; if
  the wording changes, re-check the line count before shipping.
- **The figure** (`.fig`, hand-authored inline SVG, no library): one species pool → a bifurcation →
  a **convergent** bundle closing on one filled navy node with a ring, versus a **contingent** fan
  ending on three open nodes. Both bundles have the same footprint so the contrast reads as the
  *ending*, not the size, and a `.fig__baseline` hairline puts both outcomes on a shared axis
  instead of leaving them afloat. Lines draw in on scroll via `pathLength="1"` + `view()` timeline.
- **Light, elegant cool-gray body** (`--paper: #eef0f2` — NOT blue, NOT dark: Sebastian tried a
  light-blue and a dark theme and rejected both). Dark text, sober **navy** (`#1b4b9c`).
  `--wrap: 62rem`. **No ALL-CAPS, no interpunct `·` anywhere.**
- **CV button** (`.cv-link`, in `Base.astro`): the *only* visible button, `position: fixed`
  top-right, on every page. A dark translucent glass pill — deliberately the **same** style over
  the dark hero and the light body, so it needs no JS to re-theme. Opens
  `/assets/Sebastian-Correa-Gallego-CV.pdf` in a new tab, straight into the browser's own PDF
  viewer (Sebastian: "el CV abierto en Google, tal cómo está" — **never** an embedded subpage).
  Label "Curriculum Vitae", collapsing to "CV" under 560px.
- **Footer:** left-aligned icon links (email, ORCID green, Google Scholar, GitHub, Bluesky) + ©
  note. No profile photo, **no CV icon** (it moved to the top-right button).
- Subtle `.reveal` on scroll (`view()` timeline), hero entrance, reduced-motion-safe. Print → B/W.

**Not on the site (by choice):** no education, experience, service, presentations, honours,
certifications or skills — that is what the CV PDF is for. No References (privacy). `eeb.jpg`
(group photo — third-party/minor privacy). Reminder: Cloudflare Pages rejects any file > 25 MiB.

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
9. Refined homepage. Removed the figures (kept the hero). Typography split: Roboto Serif italic for
   the name (two lines, bold), section titles (medium), and dates (light); Inter for the rest.
   **Light, elegant cool-gray body** `#eef0f2` (a dark theme and a light-blue were both tried and
   rejected). EAFIT logo recoloured to navy `#000066`. Restored full CV wording + hyperlinks (ECSO,
   SIAB) and removed all interpuncts. Footer profile photo removed. `multimedia/` deleted after use.
   Then added Google Scholar and Bluesky to the footer icon row.
10. **Current — "two screens" (Sep 2026).** Sebastian sent `CV_v25.pdf` and his Stanford
   `SOP_v21.pdf` and asked to stop mirroring the CV: *"Ya existe un CV en PDF, por ello no tiene
   sentido que la página web figure como el mismo PDF."* So **every CV-derived section was deleted**
   (education, experience, service, presentations, honours, certifications, skills). What remains is
   the hero plus one new full-viewport `.focus` section carrying the research narrative, drawn from
   the SOP and the CV's Research Interests: the organising question (order from previously
   autonomous parts — rules or history?), microbial community assembly as the tractable case,
   proteome allocation as the measurable handle, and the coda pointing upward toward the thresholds
   at which cooperating parts cease to be separable. Added a hand-authored SVG figure
   (convergent vs. contingent assembly from one pool). Hero phrase rewritten to be plainer and more
   scientific: *"On how microbial communities assemble — and whether the state they reach is
   predictable from the cells themselves."* CV moved out of the footer into the single fixed
   top-right glass button; new CV installed under the existing filename to preserve the URL.
11. **Current — design review pass (Sep 2026).** Ran the research screen through a design canvas
   (as-shipped vs. two directions) and shipped the recommended one. **Three copy corrections:**
   "It is most tractable" → "The question is most tractable" (the old "It" referred to the heading,
   which is not part of the body's grammar); "it cannot yet predict which one" → "no general rule
   yet says which one" (the original overstated the gap — priority-effect theory does predict in
   some systems, and a committee may well include people who work on it); and the caption's
   "…is the quantity I want to predict" → "One pool, two regimes. Predicting which one governs a
   given community is the open problem" (it had called a categorical outcome a *quantity*, two
   sentences after "contingency becomes a quantity"). **Composition:** eyebrow deleted, question
   set to two full-measure lines, equal top-aligned columns, figure enlarged to 24.5rem and given
   a baseline, coda lifted out of the text column to sit full-width under an `<hr>`.
   **Left open, deliberately:** the hero photo still carries `alt=""` though it is the page's most
   content-rich element; and nothing on the page evidences that Sebastian has *done* any of this
   (the CV button carries it — his brief forbids experience content, so this is a flag, not a bug).
