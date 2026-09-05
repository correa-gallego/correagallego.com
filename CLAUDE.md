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

A single, static, one-page academic homepage — **two full-viewport screens and a footer that
carries the record**: a photo hero, then one research-narrative section, then a footer holding
standing and work. **The site is deliberately NOT a copy of the CV**: the CV lives in the PDF,
linked from the one visible button. No blog, no multi-page routing, no analytics, no third-party
scripts, **no JavaScript at all**.

**The division of labour is the whole design.** The two screens are argument and must stay pure —
no lists, no dates, no institutions beyond the hero's one line. The footer is record, and is where
anything factual goes. A reviewer's finding drove this: with no visible work, careful prose in an
applicant without publications reads as *compensatory*; with the thesis, the manuscript and the
presentations visible, the same prose reads as *earned*. Do not solve a "the site should mention
X" request by adding X to the screens.

## Stack & tooling

- **Astro 5**, static output (`output: 'static'`), `@astrojs/sitemap`.
- One page: `src/pages/index.astro` (+ `src/pages/404.astro`).
- Layout `src/layouts/Base.astro` (SEO meta + `og:image`, JSON-LD Person schema, footer).
- `src/components/Footer.astro` — the standing block (status line + three work bullets), then
  left-aligned inline-SVG icon links (email, ORCID brand-green mark, Google Scholar, GitHub,
  Bluesky), then copyright. **No LinkedIn**, **no profile photo**, **no CV icon** (the CV moved to
  the fixed top-right button in `Base.astro`). See the footer bullet under Design language.
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

- **Two typefaces, by role:** `Roboto Serif` **italic** is the "voice" — the hero **name** and the
  `.focus__lead` research question, both **medium (500)**; the hero phrase is 400. `Inter` for the
  rest — the narrative body (light, 300), figure labels (500), the degree line, the CV button.
  Both via Google Fonts. (No serif-upright, no sans for the name — Sebastian's split.)
  **Only five faces are downloaded** — Inter 300/400/500 and Roboto Serif 400/500 italic. Serif
  300/700 and Inter 600 were audited out once nothing used them; if you add a weight to the CSS,
  add it to the `<link>` in `Base.astro` too, and if you remove one, take it back out.
- **Hero** (`.hero`, 100svh, full-bleed) — unchanged and not to be redesigned: `field.webp`
  (Sebastian sampling in the cave), a dark scrim (heavier left, where the text sits; person is on
  the right), bottom fades to `--paper`. Content: **name on two lines** (`Sebastian` /
  `Correa-Gallego`), **"B.Sc. in Biology, Universidad EAFIT"** (the institution was added so a
  cold visitor gets the affiliation immediately), and the phrase. `.hero__cue` is an anchor →
  `#research`.
  **`field.webp` carries real `alt` text and no `aria-hidden` — do not "fix" it back to `alt=""`.**
  It looks like a background but it is the page's only evidence of fieldwork (Sebastian sampling in
  the Organal San Antonio, Támesis — he confirmed the location); the same sentence is the
  `og:image:alt` / `twitter:image:alt`. Keep the three in sync.
- **`.focus`** (100svh, vertically centred). **There is no eyebrow/kicker** — Sebastian removed
  "Research" and its rule ("si el contenido es meramente esa pestaña, no lo veo necesario"), so the
  lead **question** is the section's own masthead: Roboto Serif medium italic, **no `max-width`**,
  sized `clamp(1.35rem, 2.6vw, 1.8rem)` so it lands on exactly **two full-measure lines** across
  every desktop width. Below it a 2-column grid, `repeat(2, minmax(0,1fr))`, `align-items: start`
  -- **narrative left / SVG figure right**; the text column is top-aligned, the figure is
  `align-self: center` (it has no top label to align to).
  **The section is exactly one text block plus the figure** — Sebastian deleted the closing rule
  and coda ("solo me gustaría tener un bloque de texto"), and a later review cut the ladder
  sentence as well, so the body is now two paragraphs and stops on the mechanism.
  Two `@media` blocks keep it inside one screen: `max-height: 780px`
  (shrinks type) and `max-width: 860px` (stacks, figure first).
  **The two-line lead is load-bearing** — it replaces the deleted rule as the section's top edge; if
  the wording changes, re-check the line count before shipping.
- **The figure** (`.fig`, inline SVG, no library) is a pair of **phase portraits**. Sebastian chose
  this over a 1D stability landscape and over a bifurcation diagram, for a reason worth keeping:
  his claim is about **arrival order, and arrival order is an initial condition** — this is the
  only one of the three that draws initial conditions. Left panel: one attractor every start flows
  to. Right: two attractors either side of a dashed separatrix through an **unstable saddle** (open
  circle; filled navy = stable, open = unstable, standard convention), with the two basins tinted.
  **Nothing in it is drawn by hand.** Trajectories are RK4 integrations of
  `dx/dt = μx − x³, dy/dt = −0.3y` — one family, one parameter: `μ = −0.8` gives a single node,
  `μ = +1.0` gives two nodes plus the saddle. The 24-arrow flow field per panel is the vector field
  sampled on a 5×5 grid; arrowheads sit at 34% along each trajectory. y relaxes more slowly than x
  on purpose — equal rates made the left panel a starburst instead of a portrait.
  **`node tools/phaseportrait.mjs` regenerates everything** (it prints JSON that
  `tools/assemble-figure.py` splices into the page). Change the parameter and re-run; never
  nudge coordinates. Axes are labelled "community composition, two of many axes" — i.e. an
  ordination-like projection, which is honest and matches his thesis methods. Trajectories draw in
  on scroll via `pathLength="1"` + `view()`; the field and frames stay static.
- **The caption is a figure caption, not a sentence of prose** (his instruction: "que sea muy
  objetivo en su descripción"). It names what is drawn first — dots, arrows, attractors,
  separatrix, saddle — and only then the reading, and it ends with "Schematic". It is
  **left-aligned on the figure's own measure**, never centred: it runs five to six lines.
- **Light, elegant cool-gray body** (`--paper: #eef0f2` — NOT blue, NOT dark: Sebastian tried a
  light-blue and a dark theme and rejected both). Dark text, sober **navy** (`#1b4b9c`).
  `--wrap: 62rem`. **No ALL-CAPS, no interpunct `·` anywhere.**
- **CV button** (`.cv-link`, in `Base.astro`): the *only* visible button, `position: fixed`
  top-right, on every page. A dark translucent glass pill — deliberately the **same** style over
  the dark hero and the light body, so it needs no JS to re-theme. Opens
  `/assets/Sebastian-Correa-Gallego-CV.pdf` in a new tab, straight into the browser's own PDF
  viewer (Sebastian: "el CV abierto en Google, tal cómo está" — **never** an embedded subpage).
  Label "Curriculum Vitae", collapsing to "CV" under 560px.
- **Footer:** now three parts — a `.foot__standing` block (a `.foot__status` line giving degree,
  institution, conferral date and that he is applying for doctoral study; then `.foot__work`, three
  restrained bullets: thesis + permanent link, the Purdue manuscript in preparation + ECSO link,
  and "six conference presentations, 2022–2026. Stanford Biology Preview Program, 2026 cohort") —
  then the icon links (email, ORCID green, Google Scholar, GitHub, Bluesky), then the © note.
  **Six is the real count** (2022, 2023, 2024×2, Jan 2026, May 2026); don't round it. No profile
  photo, **no CV icon** (it moved to the top-right button). **Never list the fellowship here** —
  the sensitive-material rule below still holds.
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

- **Three citations are load-bearing and must stay.** The research prose carries
  `Fukami 2015` (priority effects, `10.1146/annurev-ecolsys-110411-160340`), `Hu et al. 2022`
  (phase mapping, `10.1126/science.abm7841`) and `Scott et al. 2010` (bacterial growth laws,
  `10.1126/science.1192588`), as DOI links. All three DOIs were verified against publisher pages.
  Without them a professor landing here sees an idea with no lineage; a reviewer called this the
  highest-return, lowest-effort improvement on the site.
- **The gap claim is deliberately narrow.** Not "no general rule says which outcome a community
  will take" — that is overstated, because Hu 2022 maps phases and Estrela 2022 explains
  functional attractors. The defensible claim, and the one on the page, is that what is missing is
  **a rule that predicts the regime from properties of the organisms themselves**. Do not widen it.
- **The hypothesis is hedged on purpose** ("I expect… may cross-feed"), not asserted with "should".
  The rate–yield tradeoff is contested; the hedge costs nothing and buys calibration.
- **Do not restore the deleted closing sentence.** "a quantity rather than a caveat", "continues
  upward", and "the thresholds at which cooperating parts cease to be separable" were cut together:
  all three were written for effect, and the third pointed at rung 4 of the ladder — the weakest,
  least defensible part of the frame. The most ornamental phrasing was sitting on the weakest claim.

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
   Then the hero photo got a real `alt` (see the hero bullet); the "no evidence of having done it"
   flag was closed by Sebastian — the CV *is* the evidence, and that is why the page is minimal.
12. **Current — scientific pass on the figure (Sep 2026).** Sebastian: the old SVG "parece solo un
   garabato… no sé si sea válido a nivel científico". He was right. It drew freehand bezier
   trajectories through no state space, and its caption ("the same species pool → two outcomes")
   illustrated the *textbook phenomenon* rather than his own contribution. Replaced with the
   stability landscape above, computed from a real potential and axed on the quantity he proposes
   to measure. Also deleted the closing `<hr>` + coda at his request (one text block only), folding
   the ladder into the body. **Read before touching the science:** his Notion *Field Notebook* —
   "Theoretical Framework — The Ladder" (glossary, the four rungs, the verified anchor list) and
   "The Question, The Program". Access is via the Notion connector; that notebook, not this file,
   is the source of truth for the framing. Sensitive-material rule still applies.
   **One correction found and reported:** the notebook credits Dubinkina et al. 2019 (eLife
   8:e49720) with showing that the growth–yield tradeoff generates multistability. That paper's
   mechanism is competition for two *essential nutrients* with differing C:N stoichiometry. The
   tradeoff→multistability bridge he wants is Manhart & Shakhnovich 2018 (Nat Commun 9:3214),
   already in his own anchor list. Left for him to fix in Notion; nothing on the site cites either.
13. **Type audit (Sep 2026).** Sebastian asked whether to move the site to Palatino, as
   in his CV's `mathpazo`/`\scshape` setup, or keep Inter + Roboto Serif. **Kept the current
   pairing**, for three reasons worth not relitigating: Linotype Palatino has no web licence and
   the free stand-in (TeX Gyre Pagella, the URW Palladio descendant `mathpazo` actually uses) would
   need self-hosting, while the system fallbacks — `Palatino`, `Book Antiqua` — are absent on Linux
   and Android, so a large share of visitors would see something else on a page that is almost
   entirely type; Palatino is a print face whose stroke contrast and modest x-height weaken on a
   backlit screen at body sizes; and matching the CV's type would make the site read as a document
   rather than as a page built on a photograph. **Honest caveat recorded:** Inter and Roboto Serif
   are very common choices, so the page is legible and contemporary rather than distinctive — if
   that ever bothers him, the move is a screen-designed scholarly serif (Literata, Newsreader,
   Source Serif 4, Spectral), not Palatino. Per his instruction, the hero name then dropped from
   **700 → 500** and `clamp(2.3rem, 5.6vw, 3.3rem)` → `clamp(2rem, 4.9vw, 2.9rem)`; 400 was tried
   and rejected (it lost its step above the phrase and went fragile over the lit rock).
14. **Current — the figure became a phase portrait (Sep 2026).** Sebastian was shown three
   options and picked the attractor map, then rejected the first draft of it as "gráficamente
   vago" — correctly: it was hand-drawn arcs with no flow field, no direction, and no saddle. It
   is now integrated rather than drawn (see the figure bullet above). The two rejected options are
   kept on the design canvas's "Superseded"/options pages, with the reasoning, so the choice does
   not get relitigated: the 1D landscape is more instantly legible but never shows a starting
   point; the bifurcation diagram is the most informative but assumes the reader knows a branch is
   an attractor. **The 3D Waddington valley was ruled out on substance, not taste** — that image is
   about a trajectory over developmental time, not about how many end states exist.
15. **Current — content pass after an outside review (Sep 2026).** A reviewer's critique, which
   Sebastian handed over in full, drove four changes. **Precision:** the gap claim was narrowed to
   organism-level prediction, and the two consecutive "should" became "I expect… may".
   **Lineage:** three DOI citations added — the first links in the body, which finally put the
   navy `--link` accent to work (styled as a hairline border, not an underline, so they read as
   citations rather than as loud links). **Cut:** the ornamental closing sentence, in full.
   **Information:** the reviewer's strongest point was that a visitor could not tell whether
   Sebastian is a current student, a graduate or an applicant, and that none of the work was
   visible. Fixed *without* touching the two screens — the hero degree line gained ", Universidad
   EAFIT", and the footer gained the standing block. This reverses his earlier "no habrá más
   contenido en la web" only for the footer; the screens stayed pure, which is the point.
