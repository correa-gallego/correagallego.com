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

A single, static, one-page academic homepage — **three full-viewport screens and a footer**: a
photo hero, then `#question` (the open problem) and `#approach` (the proposal). **The site is deliberately NOT a copy of the CV**: the
CV lives in the PDF, linked from the one visible button. No blog, no multi-page routing, no
analytics, no third-party scripts, **no JavaScript at all**.

**The site carries exactly three facts about Sebastian**: his name, his degree (hero line and
footer), and the research argument. Everything else — thesis, manuscript, presentations, service,
honours, training — is in the CV, and the CV button is the route to it. A full standing block
(status + thesis link + manuscript + presentations + BPP) was built in the footer after an outside
review argued the site showed no evidence of work; Sebastian removed it the same day —
*"no me parece presentable… con eso queda claro el tema de la educación, y para el resto de
contexto ir a CV."* **Do not rebuild it.** If a future request asks the site to show more of the
record, the answer is the CV button, not a new section.

## Stack & tooling

- **Astro 5**, static output (`output: 'static'`), `@astrojs/sitemap`.
- One page: `src/pages/index.astro` (+ `src/pages/404.astro`).
- Layout `src/layouts/Base.astro` (SEO meta + `og:image`, JSON-LD Person schema, footer).
- `src/components/Footer.astro` — the degree line (EAFIT logo + text), then left-aligned
  inline-SVG icon links (email, ORCID brand-green mark, Google Scholar, GitHub, Bluesky), then
  copyright. **No LinkedIn**, **no profile photo**, **no CV icon** (the CV moved to the fixed
  top-right button in `Base.astro`).
- `src/styles/global.css` — the entire design system.
- Assets in `public/assets/`: **`CV.pdf` is the live CV**, and the button points at it. Sebastian
  named the file and asked that it not be renamed ("lo dejas con el nombre que le puse"). A
  byte-identical copy is kept at `Sebastian-Correa-Gallego-CV.pdf` because that URL was live for a
  while and may be circulating; **when a new CV arrives, overwrite both**. Also `favicon.svg` (black serif "S"), `field.webp` (hero), `logos/EAFIT.svg` (navy
  `#000066`, in the footer). Kept but **unreferenced**: `Sebastian-Correa-Gallego-Thesis.pdf`
  (4.2 MB defense deck), `logos/Purdue.svg`, `profile.webp` — retained because their URLs may
  already be circulating. Asset files are mode `644`; the logos shipped as `700` and were fixed.
- **Image pipeline:** Sebastian drops originals into a `multimedia/` staging folder, then Claude
  optimizes with **sharp** (bundled via Astro) → WebP into `public/assets/` (referenced by plain
  `<img>`); sharp also rasterizes SVGs. **Delete `multimedia/` when done** (Sebastian's instruction).
  Keep shipped files small; **Cloudflare Pages rejects any file > 25 MiB** (the thesis deck had to be
  compressed 27 MB → 4.2 MB before hosting).
- `public/assets/fonts/` holds the three Pagella WOFF2 files and `GUST-FONT-LICENSE.txt`. They are
  third-party binaries under a free licence; **keep the licence file beside them**.
- Content is inlined directly in `index.astro`. **No content collections**, no `src/content/`.

Commands: `npm run dev`, `npm run build` (must pass, no console errors).

## Design language (current) — "Two screens"

Hero, then two research sections, then the footer. The page is **hero (100svh) → `#question`
(`.focus`) → `#approach` (`.focus`) → footer**. Splitting the argument in two is what brought each
section back inside one screen after entry 17 made it overflow. **Both sections fit** at
1512x830, 1440x900, 1366x700, 1280x720 and 1024x640. Keep them balanced: if you add text to one,
take some out or move it to the other, and re-measure.

- **`Inter` sets the entire page**, at 300 for prose, 400 and 500 for labels, 600 for the name and
  the two mastheads. Sebastian settled this after trying Source Serif 4 and a full-Palatino page:
  "podría mejor usarse la tipografía inter en toda la página web y solo dejar las palatino para las
  ecuaciones."
- **Palatino survives only as mathematics.** `TeX Gyre Pagella` **italic alone** is self-hosted at
  `public/assets/fonts/pagella-italic.woff2` (about 36 KB, GUST Font License beside it) and is
  reached only through `--math`, which `.fig__math` applies. Inside a figure that means `phi_Q`,
  `phi_R`, `phi_P` and the growth-law equation; everything else in a figure is Inter. This is the
  journal convention and it is his instruction. The roman and bold cuts were deleted once nothing
  used them.
- **Nothing on the page is italic except that mathematics.** Mastheads and the name are roman.
- **Hero** (`.hero`, 100svh, full-bleed) — unchanged and not to be redesigned: `field.webp`
  (Sebastian sampling in the cave), a dark scrim (heavier left, where the text sits; person is on
  the right), bottom fades to `--paper`. Content: **name on two lines** (`Sebastian` /
  `Correa-Gallego`), **"B.Sc. in Biology, Universidad EAFIT"** (the institution was added so a
  cold visitor gets the affiliation immediately), and the phrase. `.hero__cue` is an anchor →
  `#question`.
  **`field.webp` carries real `alt` text and no `aria-hidden` — do not "fix" it back to `alt=""`.**
  It looks like a background but it is the page's only evidence of fieldwork (Sebastian sampling in
  the Organal San Antonio, Támesis — he confirmed the location); the same sentence is the
  `og:image:alt` / `twitter:image:alt`. Keep the three in sync.
- **`.focus`** (100svh, vertically centred). **There is no eyebrow/kicker** — Sebastian removed
  "Research" and its rule ("si el contenido es meramente esa pestaña, no lo veo necesario"), so the
  lead is the section's own masthead: Source Serif 4 semibold roman, **no `max-width`**, sized
  `clamp(1.32rem, 2.5vw, 1.74rem)` so it lands on **two full-measure lines** across every desktop
  width. Below it a 2-column grid, `repeat(2, minmax(0,1fr))`, `align-items: start`
  -- **narrative left / SVG figure right**; the text column is top-aligned, the figure is
  `align-self: center` (it has no top label to align to).
  **Each section is text plus one figure, nothing else.** No closing rule, no coda, no kicker.
  `#question` states the open problem, `#approach` the proposal.
  Two `@media` blocks trim both sections on small viewports: `max-height: 780px` (shrinks type,
  tightens leading and the caption) and `max-width: 860px` (stacks, figure first).
  **The two-line lead is load-bearing** — it replaces the deleted rule as the section's top edge; if
  the wording changes, re-check the line count before shipping.
- **Two figures, and they are different kinds of object. The caption must say which is which.**
  - `scripts/priority_effects.py` emits `src/figures/priority-effects.svg`, a **schematic after
    Fukami 2010, Fig. 4.1** (*Community assembly dynamics in space*, in Verhoef and Morin, eds.,
    OUP, pp. 45-54), which sets the deterministic and the historically contingent cases over one
    species pool and crosses immigration history against habitat condition. Original artwork on
    that conceptual layout, and **the caption credits it**. Nine species in three groups of three;
    colour carries the group so the pattern reads before any numeral does. Two habitat conditions
    by three immigration histories per panel. **The whole point is which axis each panel follows**:
    deterministic follows the habitat, contingent follows the history. Do not collapse it to one
    panel; the contrast is the figure.
  - `scripts/allocation_tradeoff.py` emits `src/figures/allocation-tradeoff.svg`, the **computed**
    one, in three panels on the relations of Scott et al. 2010.
    **Panel A is their Figs. 1A and 2A**: two perturbations move a culture along two different
    lines in the plane of growth rate against RNA/protein ratio, `r = r0 + lambda/kappa_t` for
    nutrient quality and `r = rmax - lambda/kappa_n` for translational inhibition, one line per
    medium. Each drug-free culture sits where its two lines cross, and **those crossings are what
    fix the parameters**. That is why the page can say the partition is measurable rather than
    assumed, so do not drop this panel as decoration; it carries the claim.
    **Panel B** converts with `phi_R = rho * r` and adds the fixed sector, giving their Q/R/P
    partition. **Panel C** is the rate-yield line the partition implies, an inference, since Scott
    et al. do not measure yield, and the caption says so.
    Values, read off the published figures since the paper reports them graphically:
    `r0 = 0.07`, `kappa_t = 5.0/h`, `rmax = 0.72`, `rho = 0.76`, `phi_Q = 0.45`, and six
    `kappa_n` from 1.0 to 6.2/h. They reproduce the plotted crossings, `lambda` 0.54 to 1.80/h at
    `r` 0.18 to 0.43. **`phi_Q = 0.45` is the reported housekeeping fraction**, with
    `phi_C + phi_R + phi_E = 1 - phi_Q` fixing the rest at 0.55. Do not alter these without a
    source.
  - Both carry quantitative axes with ticks, numerals, units and panel letters, and true
    subscripts via `tspan`. **Do not strip those.** Sebastian's test is whether the authors of
    those papers would read it as a figure, and unlabelled axes are what fails that test.
  - Figure 1 is 664x404, figure 2 is 655.2x237.6. Figure 1 is taller because it stacks two
    panels of four rows; figure 2 is wide and short because it runs three panels in a row.
  - **Each figure sits in a `.fig-wrap`.** Below 860px that box scrolls horizontally and the SVG
    keeps a 30rem minimum, because three panels at phone width are unreadable. The page itself
    never scrolls sideways; only the figure box does.
  - **The figures run into the right margin.** `.focus__figure` carries a negative right margin,
    `clamp(0rem, (100vw - var(--wrap)) / 2 - 2.2rem, 11rem)`, so a figure is about 650px at 1512
    and falls back to the column width below 1100. A 25rem box read as too small next to the
    journals this is measured against. The margin collapses to zero under 860px.
  - **`--fig-alt` (#a8762e) is the second functional colour.** Blue and amber is the safest pair
    for colour-blind readers. In the schematic, shape is the guild and colour separates the two
    competitors within a guild, which is the whole point of the two rows; with fill-versus-outline
    the difference was invisible at figure size.
  - Other colours are `--fig-flow`, `--fig-traj`, `--fig-sep`, `--rule`, `--link`, `--paper`,
    `--faint` and `currentColor`, so both follow the theme. Label sizes are tuned so the two
    render at a comparable scale; re-check if you resize either canvas.
  - Both need numpy and matplotlib, absent from the system Python under PEP 668, so use a venv.
    `index.astro` inlines both with Astro's `?raw` import, which is what lets the custom properties
    resolve. **Never hand-edit the SVGs**; re-run the scripts.
- **Captions carry the citation and nothing about the repository.** Sebastian removed the
  `.fig__source` line that named the generating script: "solo deja el caption, de manera objetiva".
  A caption states what is drawn and credits its source, and that is all. Figure 1 ends "After
  Fukami 2010, Fig. 4.1"; figure 2 attributes the left panel to Scott et al. 2010 and marks the
  right as an inference. The caption runs the full width of the figure, not a narrower measure.
- **Captions are figure captions, not prose** (his instruction: "que sea muy objetivo en su
  descripción"). Each names what is drawn first and only then the reading, and each ends with a
  `.fig__source` line giving the script and, where it matters, what is computed and what is
  inferred. **Left-aligned on the figure's own measure**, never centred.
- **Light, elegant cool-gray body** (`--paper: #eef0f2` — NOT blue, NOT dark: Sebastian tried a
  light-blue and a dark theme and rejected both). Dark text, sober **navy** (`#1b4b9c`).
  `--wrap: 62rem`. **No ALL-CAPS, no interpunct `·` anywhere.**
- **CV button** (`.cv-link`, in `Base.astro`): the *only* visible button, `position: fixed`
  top-right, on every page. A dark translucent glass pill — deliberately the **same** style over
  the dark hero and the light body, so it needs no JS to re-theme. Opens
  `/assets/Sebastian-Correa-Gallego-CV.pdf` in a new tab, straight into the browser's own PDF
  viewer (Sebastian: "el CV abierto en Google, tal cómo está" — **never** an embedded subpage).
  Label "Curriculum Vitae", collapsing to "CV" under 560px.
- **Footer:** three parts — `.foot__degree` (the navy EAFIT mark at `height: 1.45em` beside
  "B.Sc. in Biology, Universidad EAFIT, 2026", the logo/text lockup from the old `.entry__inst`
  style Sebastian asked to bring back), then the icon links (email, ORCID green, Google Scholar,
  GitHub, Bluesky), then the © note. The text sits in its own `<span>` with `text-wrap: balance`
  so it breaks evenly at phone width instead of orphaning "2026". The logo takes **`alt=""`** —
  correct here, unlike the hero photo, because the words beside it already say Universidad EAFIT.
  No profile photo, **no CV icon**. **Never list the fellowship here** — the sensitive-material
  rule below still holds.
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

## Prose rules (hard constraints, apply to every visible string)

Sebastian set these explicitly. They cover the page, the figure caption, the meta description
and the 404, not just the research prose.

- **No em dashes anywhere.** Rewrite the sentence; do not swap the dash for a comma and leave the
  same clause structure.
- **No colons introducing an explanatory clause.**
- **Continuous prose. Short sentences. No lists in the narrative sections.**
- **Mark modality consistently.** Use "whether", "may", "the hypothesis is that". Do **not** use
  "I expect", and do not use "because" for a link that is a hypothesis rather than a published
  result.

## Content rules (important)

- **Five citations are load-bearing and must stay**, all as DOI links, all verified against
  publisher pages: `Fukami 2015` (priority effects, `10.1146/annurev-ecolsys-110411-160340`),
  `Goldford et al. 2018` (coarse-grained convergence, `10.1126/science.aat1168`),
  `Estrela et al. 2022` (functional attractors, `10.1016/j.cels.2021.09.011`),
  `Scott et al. 2010` (bacterial growth laws, `10.1126/science.1192588`) and
  `Vannette and Fukami 2014` (niche decomposition predicts priority-effect strength,
  `10.1111/ele.12204`). **Note the last one.** Sebastian supplied `10.1111/ele.12238`, which is a
  different paper; the correct DOI for *Historical contingency in species interactions* is
  `.12204`. Verify any DOI before shipping it. `Hu et al. 2022` was **removed** from the first
  paragraph, having been over-attributed there.
- **The gap claim is deliberately narrow.** Not "no general rule says which outcome a community
  will take" — that is overstated, because Hu 2022 maps phases and Estrela 2022 explains
  functional attractors. The defensible claim, and the one on the page, is that what is missing is
  **a rule that predicts the regime from properties of the organisms themselves**. Do not widen it.
- **The hypothesis is hedged on purpose**, in the register fixed by the prose rules above
  ("I ask whether", "may sit below", "The hypothesis is that"). The rate-yield tradeoff is
  contested, so the hedge costs nothing and buys calibration.
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
16. **Current — the footer went back to one line (Sep 2026).** The standing block from entry 15
   lasted a day. Sebastian: *"No me parece presentable el footer. Lo mejor para mí es solo insertar
   el grado, con el estilo que usamos con el logo de EAFIT."* So the status line, the thesis link,
   the manuscript, the presentations and the BPP all came out, and the footer now carries the
   degree with the EAFIT mark and nothing else. The reviewer's other three fixes — the narrowed
   gap claim, the hedges, the three DOI citations — all stayed, and those were the substantive
   ones. **What this costs, on the record:** the site now links to no scholarly output of his own;
   the thesis handle (`hdl.handle.net/10784/38213`) lives only in the CV PDF. He accepted that
   trade knowingly. Don't reopen it unprompted.
17. **Current — prose rules, five citations, computed figure (Sep 2026).** Sebastian imposed the
   style constraints now recorded above, replaced the hero phrase, the section heading and both
   paragraphs with exact text, and asked for the figure to be regenerated from a real
   Lotka-Volterra competition model with scipy rather than from the earlier normal-form sketch.
   **One correction made to his brief:** the DOI he gave for Vannette and Fukami 2014 was
   `10.1111/ele.12238`, which is a different paper. Shipped `.12204`, the correct one.
   **One consequence to be aware of:** the specified text is about half again as long as what it
   replaced, so `.focus` no longer fits inside one screen except on 1080-tall displays. It needs
   roughly 1010 to 1050px against 830 available at 1512x830, and overflows by about 115 to 185px
   on common laptop viewports. `min-height: 100svh` means it simply grows rather than clipping, so
   nothing breaks, but the "two screens" reading is now "hero, then a section you scroll through".
   Fixing it needs either shorter text or a typographic change, both of which he ruled out, so it
   was shipped as specified and reported.
18. **Current — audit against the primary literature (Sep 2026).** Sebastian sent the newest CV,
   his Stanford SOP and the submitted Simons LOI, then the PDFs of Blount 2008, Fukami 2015 and
   Scott 2010, and asked that the figures be compared against the figures in those papers. That
   comparison changed the work twice, and the practice is worth repeating.
   **First**, Fukami's Fig. 2 showed that this field draws priority effects as pool, arrival order,
   resulting community, not as a phase portrait. The Lotka-Volterra phase portrait from entry 17
   was retired for a schematic in that grammar, and `scripts/phase_portraits.py` was deleted. It is
   in git history if the dynamical view is ever wanted again.
   **Second**, Scott's Fig. 1A showed the growth-law slope in the new allocation figure was nearly
   double the published value. Fixed. Opening the paper is what caught it.
   **Structure:** the research section split into `#question` and `#approach`, which fixed the
   entry-17 overflow and matches the argument. Prose rewritten in paper register, organised around
   the three advisors named in the SOP: Fukami for priority effects, Cremer for allocation from
   inside the cell, Petrov for evolution during assembly. Seven citations, all DOIs verified.
   **Moran et al. 2026 is deliberately absent.** Sebastian cited it in the LOI for emergent
   predictability and later established the attribution does not hold. Do not reintroduce it.
   **Also still wrong in the submitted LOI, for his records, not the site:** reference 5 credits
   Dubinkina et al. 2019 with the rate-yield route to multistability. That paper's mechanism is
   competition for essential nutrients with differing stoichiometry. Manhart and Shakhnovich 2018,
   his own reference 4, is the right one, and it is what the site cites.
19. **Current — type audit, second pass (Sep 2026).** Sebastian asked whether the typefaces suited
   his scientific aspiration, with freedom to replace them. Three problems had accumulated. The
   page was running **three families** (Inter, Roboto Serif, and the Palatino stack the figures
   picked up in entry 18), which reads as drift rather than intent. Roboto Serif was used **only in
   italic**, and with two section mastheads that had stopped being a device and become a mannerism.
   And Inter is an interface face doing the job of running prose with citations.
   **Replaced with Source Serif 4 for everything editorial and Source Sans 3 for chrome.** Source
   Serif 4 is a text face built for screen reading in technical publishing, which is the job here,
   and the two are a designed pair. Mastheads moved to roman semibold; italic is now the name only.
   `--fig-type` became an alias for `--serif`, so the figures cannot drift again.
   **Entry 13's reasoning against Palatino still stands for body text** (no web licence, the free
   stand-in needs self-hosting, the system fallbacks are absent on Linux and Android, and it is a
   print face at body sizes). What changed is that the honest caveat recorded there, that Inter and
   Roboto Serif were legible but generic, was worth acting on once the page had become a short
   paper rather than a photograph with a caption.
20. **Current — Palatino, properly (Sep 2026).** Sebastian rejected the Source Serif 4 of entry 19
   outright ("esa tan fea") and gave two acceptable paths, Palatino or an all-Inter page with light
   body and heavy titles. Took Palatino, but only by removing the reason it had been refused twice:
   **TeX Gyre Pagella is now self-hosted**, subset, about 103 KB for three faces, so the Linux and
   Android fallback problem disappears. Inter stays, for chrome and figure labels only.
   **Figure typography follows his instruction**: sans for everything except the mathematics, which
   takes Pagella italic through `.fig__math`. Both figures were brought to a common 2:1 aspect and
   the schematic given more vertical air.
   **What this reverses, and why it is not a contradiction:** entries 13 and 19 argued against
   Palatino on availability and on it being a print face. The availability half is solved by
   self-hosting. The screen half is a real but modest cost, accepted knowingly, and it buys a page
   set in the same face as every other document he submits.
21. **Current — Inter everywhere, bigger figures, the niche layer (Sep 2026).** Three things.
   **Typography settled**: Inter for the whole page, Pagella italic kept only for the mathematics
   inside figures. That is Sebastian's call after Source Serif 4 was rejected and full Palatino
   tried; the two unused Pagella cuts were deleted.
   **Figures enlarged.** They read as too small against the journals this is measured against, so
   `.focus__figure` now runs into the right margin, reaching about 650px at 1512 and collapsing
   back to the column below 1100. Both sections still fit one screen.
   **Figure 1 rebuilt with the niche layer**, which the first version omitted even though it is the
   substance of Fukami's Fig. 2, and given a second functional colour so the difference between the
   two communities is visible rather than a solid-versus-outline distinction lost at figure size.
   **Figure 2 validated rather than changed**: `phi_Q = 0.45` is the reported housekeeping fraction
   and the sectors sum correctly, so the proportions stand.
22. **Current — figure 1 rebuilt on Fukami's own layout (Sep 2026).** Sebastian sent the figure
   from Fukami's website and the 2010 chapter behind it. The niche-preemption version from entry 21
   was communicating vaguely and leaned on a faded-circle device that confused more than it showed.
   Replaced with the layout of **Fukami 2010, Fig. 4.1**: one species pool, immigration history
   crossed against habitat condition, deterministic above and historically contingent below. That
   figure says exactly what the masthead asks, which the previous one did not.
   Also: the caption now runs the full figure width rather than a narrower measure, the
   `.fig__source` script-path lines are gone from both captions, and figure 2 gained the
   doublings-per-hour scale that Scott's Fig. 1A carries. Figure 2 was otherwise checked and left
   alone; adding the translational-inhibition family of lines from Scott's Fig. 2A was considered
   and rejected as tangential to the argument on the page.
23. **Current — figure 2 rebuilt on Scott's own mathematics (Sep 2026).** Sebastian: "Scott es
   mas especifico y preciso en sus figuras... tienes el paper y la matematica". He was right, and
   **entry 22 was wrong to call the translational-inhibition lines tangential.** They are not a
   side result: the crossing of the nutrient line with a medium's inhibition line is what pins the
   parameters, which is exactly why the page can claim the partition is measurable. Leaving them
   out weakened the claim the figure exists to support.
   Figure 2 is now three panels, A the two growth laws with the six inhibition lines and their
   crossings, B the Q/R/P partition, C the tradeoff with the two pools. Parameters are in the
   figure bullet above. It came out wider and shorter than the two-panel version, so every section
   gained headroom rather than losing it.
   Also added `.fig-wrap`, since three panels at phone width were illegible.
