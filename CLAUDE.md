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

A single, static, one-page academic homepage: a photo hero, a short introduction band, then
**two full-viewport screens**, `#question` (the open problem) and `#approach` (the proposal), and
a footer. **The site is deliberately NOT a copy of the CV.** The CV lives in the PDF, linked from
the top-right pair. No blog, no multi-page routing, no analytics, no third-party scripts,
**no JavaScript at all**.

**The site carries four things about Sebastian**: his name, his degree, four sentences of
background in the introduction band, and the research argument. Everything else, thesis,
manuscript, presentations, service, honours, training, is in the CV, and the CV button is the
route to it.

**On the introduction band, because this has moved twice and the reasoning matters.** A full
standing block (status, thesis link, manuscript, presentations, BPP) was once built in the footer
after an outside review argued the site showed no evidence of work, and Sebastian removed it the
same day: *"no me parece presentable… con eso queda claro el tema de la educación, y para el resto
de contexto ir a CV."* **That block stays gone.** What replaced it, at Sebastian's own request
after feedback from Stanford's Biology Preview Program committee, is much smaller and does a
different job: the committee's point was that the page opened straight onto two research questions
with nothing about who was asking them. So the band says who he is and where he graduated in four
sentences, with a portrait, and stops. **Its size is the whole point.** Sebastian: *"que sea lo
suficientemente conciso para que el contenido principal de la web sigan siendo las dos preguntas
de investigación."* Do not let it grow back into a record of the CV.

## Stack & tooling

- **Astro 7**, static output (`output: 'static'`), `@astrojs/sitemap`. **Node 22 is pinned by
  `.nvmrc`**, which Cloudflare Pages reads ahead of the `NODE_VERSION` dashboard variable; that
  variable still says 20 and is now ignored, and 20 went end of life in April 2026.
- **`compressHTML: true` and `inlineStylesheets: 'always'` are both deliberate.** The stylesheet
  is small enough that inlining it removes the last render-blocking request, and the site has two
  pages, so nothing is lost by not caching it separately.
- **Astro 7 minifies CSS with Lightning CSS, which folds longhands into shorthands.** That is a
  trap here: written next to an `animation` shorthand, `animation-timeline: view()` gets folded
  into it, no browser parses `view()` inside the shorthand, and the whole declaration is dropped,
  so the scroll reveal silently stops working. `.reveal` therefore uses animation longhands and
  keeps `animation-timeline` in its own `@supports` block. **Do not tidy that back into a
  shorthand**, and check the emitted CSS, not the source, after any animation edit.
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
- `public/assets/fonts/` holds `inter-variable.woff2` and `pagella-italic.woff2` with their two
  licences, `INTER-OFL.txt` and `GUST-FONT-LICENSE.txt`. They are third-party binaries under free
  licences; **keep the licence files beside them**.
  **Inter is self-hosted and must stay that way.** The page used to pull four static weights from
  Google, latin and greek for each, 270 KB over two third-party origins, on a site whose whole
  claim is that it runs no third-party code. It is now one variable file, `wght` 300 to 600 with
  Inter's `opsz` axis kept, subset to Latin-1 plus Greek plus the maths signs the figures use,
  58 KB, preloaded from the same origin. Rebuild it by instancing `wght=300:600` off
  `InterVariable.ttf` from rsms/inter and running `pyftsubset`; the exact repertoire is in the
  entry-25 note below. A second `@font-face`, **`Inter Fallback`**, carries Inter's own metrics
  (`size-adjust: 108.32%`, `ascent-override: 89.43%`, `descent-override: 22.27%`) so the text does
  not reflow when the real face swaps in. Recompute those if the face ever changes.
- **Cloudflare rewrites the HTML at the edge, and the strict CSP collides with it.** Two features
  are on in the dashboard and neither is visible in the build output, so both can only be caught on
  the live site.
  **Email Address Obfuscation** rewrites the footer's `mailto:` into a
  `/cdn-cgi/l/email-protection#...` link and injects a decoder script to undo it in the browser.
  The CSP blocks that script, so the link went to a Cloudflare notice page instead of opening a
  mail client. The footer link is therefore wrapped in `<!--email_off-->` and `<!--/email_off-->`,
  Cloudflare's own opt-out, which makes it serve the raw `mailto:` and inject nothing.
  `compressHTML` keeps those comments; check they survive if that setting ever changes. The
  obfuscation bought nothing here anyway, since the JSON-LD carries the address in clear.
  **Cloudflare Web Analytics** injects a beacon from `static.cloudflareinsights.com`. The CSP
  blocks it, which is the only reason this site's "no analytics, no third-party scripts" claim is
  currently true. **It is on in Sebastian's dashboard and he should decide.** Turning it off is
  the honest fix; leaving it on and relaxing the CSP to admit it would make the claim false.
- **`public/_headers` is the Cloudflare Pages header file.** It sets `default-src 'none'`, which
  the site can state honestly because it runs no JavaScript, and holds the two generated
  directories for a year. `style-src` needs `'unsafe-inline'` for the inlined stylesheet and for
  the style attributes inside the generated figures. **`Cross-Origin-Resource-Policy` is left out
  on purpose**; it would stop another origin's browser context from loading the hero photograph,
  and that photograph is the og:image behind every link preview of this site.
- **The hero photograph is a `srcset`.** `scripts/hero_images.mjs` emits 640, 960, 1280 and 1600
  WebP into `public/assets/hero/`; the 1920 entry is the untouched original, which is also the
  og:image and must not be re-encoded. A phone takes 90 KB where it used to take 247. The list
  lives in `src/lib/hero.ts` so the page and the preload in the layout cannot drift apart.
  **AVIF was measured and rejected**, coming out larger at every width on a dark grainy photograph
  that is already a WebP.
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
    that conceptual layout, and **the caption credits it**. Nine species in three guilds of three;
    colour is the species and shape the guild, in the convention Fukami 2015 states. Two habitat
    conditions by three immigration histories per panel. **The whole point is which axis each panel follows**:
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
  - **Panel titles are left-aligned and start with a capital, and so does every axis label,
    legend entry and row label.** Sentence case with an initial capital is the journal
    convention and Sebastian asked for it; centred panel titles were his first correction.
  - **The species-pool capsule in figure 1 is sized by `COL_X`, not by the marks.** Sized to the
    marks it stopped short of the outer columns and the first and last arrows began in mid air
    instead of leaving the pool.
  - **The gap between figure 1's two panels has to clear a two-line row label against the next
    panel's title.** `PANEL_Y[1]` minus `HAB_Y` must leave room for the habitat label's second
    line plus its descender under the title's cap height; at 226 against 190 they touched.
  - **When checking a figure for collisions, include the container rects, not just the text.**
    Two rounds of "no overlaps" were reported from a text-only sweep while every neighbouring
    `.fk__comm` box in figure 1 overlapped its neighbour by 4px, because `COMM_W` was wider than
    the space between column centres. The rule the layout has to keep is `COMM_W + 8 <= the
    within-group column step`.
  - Both carry quantitative axes with ticks, numerals, units and panel letters, and true
    subscripts via `tspan`. **Do not strip those.** Sebastian's test is whether the authors of
    those papers would read it as a figure, and unlabelled axes are what fails that test.
  - Figure 1 is 568x430, figure 2 is 544x493. **Figure 2's plot areas are square**, 120 units a
    side, and every axis carries four intervals, so the grid cells are square too. That is what
    Sebastian meant by "plots formales con relaciones adecuadas en las gradillas". Square panels
    stacked two over one make an almost square figure, which is far too tall for the width the page
    gives it, so `GUTTER` is wide on purpose; it is the knob that buys the aspect back, and panel C
    sits under it so the space reads as composition. **The doubling-rate scale is drawn once, on
    panel A**, where Scott et al. put it; three copies were furniture.
    **Row labels in figure 1 need `LABEL_DY` of at least about 11.6.** They are set at 9.6px and a
    text run's box is roughly 1.2 times its size, so a tighter leading makes the two lines collide,
    which is what 10.4 was doing across all four labels in both panels.
  - Figure 1 was 552x396, figure 2 was 552x372. **Both are near 3:2 on purpose.** They were
    664x404 and 655.2x237.6, which stretched wide and flat across the page and left the marks
    small. Figure 1 was narrowed by clustering the pool into three triads, wrapping the row
    labels to two lines and closing the columns up, and its marks were drawn larger. Figure 2
    went from three panels in a row to **two above and one centred below**, which is Sebastian's
    layout ("de manera triangular"). Its panels are placed by hand with `fig.add_axes`, not by a
    grid, because a gridspec cannot centre the third one.
  - **Each figure sits in a `.fig-wrap`.** Below 860px that box scrolls horizontally and the SVG
    keeps a 28rem minimum, because axis numerals at phone width are unreadable. **The grid track
    must be `minmax(0, 1fr)` and not `1fr`.** A bare `1fr` takes its automatic minimum from that
    28rem and widens the whole page, which is what put a horizontal scrollbar on the page itself
    and pushed the text out of the margin.
  - **The two research sections run wider than the rest of the page**, `--focus-wrap: 70rem` against
  `--wrap: 62rem`, applied through `.focus__inner`. At 62rem the content used 1077px of a 1512px
  window and Sebastian read the sections as mostly margin. Widening also *shortens* the text
  column, since a wider measure takes fewer lines, which is what paid for the larger figures. The
  hero and the footer keep 62rem; widening those would move the hero text off the scrim.
- **The figures run a little into the right margin.** `.focus__figure` carries a negative right
    margin, `clamp(0rem, (100vw - var(--wrap)) / 2 - 2.2rem, 5.75rem)`, so a figure is about
    560px at 1512 and falls back to the column width below 1100. The bleed was 11rem and is held
    shorter now; a wider box forces a flatter canvas, and the canvas was the problem. On a short
    screen (`max-height: 780px`) the bleed goes to zero, because there height is what binds.
  - **`--fig-alt` (#a8762e) is the second functional colour.** Blue and amber is the safest pair
    for colour-blind readers. It earns its place in figure 2, where the narrow and the wide pool
    must separate; fill-versus-outline was invisible at figure size.
  - **Figure 1 encodes colour and shape the way this field does, and that mapping is fixed.**
    **Colour is the species, shape is the guild.** It is not a house choice; it is the sentence
    Fukami 2015, Fig. 2 puts in its own caption, "different symbol colors indicate different
    species... symbol shapes denote the guilds or functional groups". Triangle, circle and star are
    his three shapes. **Do not invert it** to put a group on colour, which is what an earlier
    version did.
    Species are numbered **down** the guilds, so 1, 4 and 7 are triangles, 2, 5 and 8 circles,
    3, 6 and 9 stars. That is what makes each community, being a consecutive triad, hold one
    species of every guild, the filled-niche structure of Fukami 2015, while keeping the literal
    sets {1, 2, 3}, {4, 5, 6} and {7, 8, 9} of Fukami 2010.
    **The set notation under each community is Fukami 2010's own**, and it doubles as the text
    backup for colour; keep it.
    **The nine colours are `--sp1` to `--sp9`, Paul Tol's muted qualitative scheme**, ordered so
    the three triads fall into three colour families, which is what makes same-versus-different
    readable at a glance. Two of them, the sand and the cyan, sit near 1.5:1 against this paper,
    well under the 3:1 a graphical object needs, so **every mark carries a hairline dark edge**
    (`.fk__sp`) and the fill is left to carry identity. Do not remove that edge.
    **What the figure adds to Fukami 2010, and what the caption must keep admitting.** The chapter
    figure is black and white, has three columns, and holds the environment constant. The habitat
    row here crosses history against habitat, which draws his prose sentence that deterministic
    assembly is the case where composition "is determined by environmental conditions". The caption
    therefore credits the two sources separately, "Layout after Fukami 2010, Fig. 4.1, in the
    notation of Fukami 2015, Fig. 2". **Do not collapse that into a single claim of reproduction.**
    Fukami is one of the three advisors named in the SOP, so a reader who knows the convention is
    the likely reader.
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
- **Introduction band** (`.intro`, in `index.astro`): the portrait at
  `/assets/portrait-256.webp` beside four sentences and the profile links. **A band, not a
  screen**, so the two research sections remain the page; it has no `min-height` and ends on a
  hairline rule. The hero cue points at it. See the reasoning under "What the site is" before
  changing its length.
- **`src/components/ProfileLinks.astro` is used twice**, in the band and in the footer: email,
  ORCID, Google Scholar, GitHub, Bluesky. **Email repeats in three places on purpose** (here,
  the footer, and the top-right pair); an address that is easy to find is the whole point of the
  BPP note. Sebastian asked whether all five should move to the top bar instead. They did not,
  because five pills over the hero photograph compete with his name, and because ORCID, Scholar,
  GitHub and Bluesky are identifiers rather than contact, so they belong beside the person. Email
  and the CV, which are what an advisor actually needs, are the two that sit up top.
- **Top-right pair** (`.topbar` with two `.top-link` pills, in `Base.astro`): **Email** then
  **Curriculum Vitae**, on every page, `position: fixed`. Dark translucent glass pills,
  deliberately the **same** style over the dark hero and the light body, so they need no JS to
  re-theme. The CV opens `/assets/CV.pdf` in a new tab, straight into the browser's own PDF viewer
  (Sebastian: "el CV abierto en Google, tal cómo está", **never** an embedded subpage). Labels
  collapse to "CV" under 560px and to icons alone under 400px.
  **Email is up here because of the same BPP feedback**: a visitor who never scrolls never sees
  the footer, so an advisor could read the whole argument and leave without the address. It is
  still in the footer too. **Its `mailto` must stay wrapped in `<!--email_off-->`**, like the
  footer's, or Cloudflare rewrites it at the edge and the policy blocks the decoder.
- **The white space between sections is `(100svh - content) / 2` on each side, not padding.**
  While the content is shorter than the space left, padding changes nothing a reader can see; it
  only moves white from inside the section to between them. So the way to close the gap is to make
  the content taller, which is why the figures are sized to nearly fill their sections. Sebastian
  asked for this twice before it was diagnosed correctly.
  **The two halves of `.focus`'s padding are deliberately unequal**, much more above than below.
  A centred block sits optically high when its lower right corner is a figure caption, which is
  small grey text carrying little weight. Moving the same total to the top drops the block by half
  the difference and costs no height. This is Sebastian's instruction, not a flourish.
- **Footer:** two parts, the `ProfileLinks` row and the copyright note. **The degree line was
  removed** once the introduction band and the hero both stated it; Sebastian: it "podría ser
  removido de el pie de página". The EAFIT mark went with it.
  **The profile links stay, and that was a judgement call Sebastian left open.** They are kept
  because the end of the page is where someone who has just read both sections acts, and making
  them scroll back up to the band is friction; because the fixed pair carries only email and the
  CV, so ORCID, Scholar and GitHub would otherwise exist in one place; and because a footer of a
  lone copyright line reads unfinished. Easy to reverse if he disagrees.
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
24. **Current - the figures were reshaped to fit the page (Sep 2026).** Sebastian: the figures run
   too far along the horizontal, so they cannot be read on a laptop and on a phone they "ocupan
   mas del margen de la pagina web desplazando contenido". **He was right about the phone, and
   entry 23's verification missed it.** The `.fig-wrap` from that entry did scroll, but the grid
   track was `1fr`, whose automatic minimum came from the SVG's own 30rem floor, so the track
   widened to 480px and carried the whole page with it. At 375 the document scrolled sideways by
   126px. It is `minmax(0, 1fr)` now, and the page measures 375 of 375.
   The shape problem was real too, and the fix is the one he specified. Figure 1 is narrower and
   its marks are bigger. Figure 2 is two panels above and one centred below. Both land near 3:2,
   the margin bleed was cut from 11rem to 5.75rem so the canvas is not stretched wide again, and
   figure 2's panels are about 60 per cent wider than they were in a row of three.
   Two things changed on their own merits while the figures were open. The pools in figure 2's
   panel C were eight free uniform draws, and the "wide" one had come out spanning 0.94/h against
   the narrow one's 0.32, which undersold the contrast the panel exists to show; they are drawn
   one per stratum now, so the plotted spread is the stated spread, 1.50 against 0.36. And the
   housekeeping and metabolic sectors in panel B were two alphas of the same grey and did not
   read apart, so the metabolic sector took `--fig-traj`.
   Both sections still fit one screen at 1512x830, 1440x900, 1366x768, 1366x700, 1280x720 and
   1024x640; the last two needed a further trim, so a `max-height: 680px` branch was added.
25. **Current - the platform pass (Sep 2026).** Sebastian asked for research into current practice
   and left the choices open. Four things came out of it, all measured rather than assumed.
   **Fonts.** The head carried a render-blocking Google stylesheet pulling four static weights of
   Inter, latin and greek each, **270 KB from two third-party origins**, which is both the largest
   thing on the page and a contradiction of the site's own no-third-party premise. One
   self-hosted variable file replaces it at **58 KB**, and it brings the optical-size axis the
   static weights never had, which slightly tightened the prose and gave `#approach` more
   headroom rather than less. The subset is Latin-1, Greek letters, and the punctuation and maths
   signs a scientific page needs, deliberately wider than the 92 characters the page happens to
   use today so an edit cannot land on a missing glyph.
   **The photograph.** One 1920 file was going to every visitor. A phone now takes 90 KB.
   **Headers.** `public/_headers` states a policy the site can actually keep.
   **The framework.** Astro 5.18.1 carried ten advisories, one of them critical against Astro
   itself, and the Cloudflare build was on Node 20, which is end of life. Upgrading to **Astro 7
   on Node 22** clears all ten. The critical one never applied here, since the site uses no
   `define:vars` and no server islands, but the version it was filed against was the one running.
   **One regression the upgrade caused, and it would have been invisible.** Astro 7 minifies with
   Lightning CSS, which folded `animation-timeline: view()` into the neighbouring `animation`
   shorthand and killed the scroll reveal outright. It is recorded in the stack section above
   because nothing about the source file looks wrong; only the built CSS shows it.
   Total on a phone went from about 573 KB across three origins to about 199 KB from one.
26. **Current - figure 1 put into the field's own notation (Sep 2026).** Sebastian asked whether
   its colours were faithful to Fukami. **They were not, and neither was the encoding.** Checked
   against both papers. Fukami 2010, Fig. 4.1 has no colour at all; its vector fills are
   near-black (#231F20), white and a light grey, and it writes a community as set notation rather
   than as marks. Fukami 2015, Fig. 2 does use colour, and its caption states the convention
   outright, colour for the species and shape for the guild. The figure had that inverted, putting
   the triad on colour and the species on a numeral.
   It now follows the convention, with the numbering arranged so the two sources agree rather than
   compete; the details are in the figure bullet above. The set notation came back from the 2010
   chapter as the text backup for colour, which makes the result more accessible than either
   source on its own. The canvas came out shorter, 552x374 against 552x396, so the section gained
   room, and the caption was trimmed to rebalance the two sections at 28 and 43 spare pixels.
   **Worth keeping as a working rule.** Both times a figure here was checked against the paper it
   claims, the check changed the figure. Entry 18 caught a growth-law slope at nearly twice the
   published value and a whole wrong representation; this one caught an inverted encoding. Reading
   the caption of the figure being adapted is what did it, not reading the prose.
27. **Current - square plots, and a face on the page (Sep 2026).** Three things, two of them from
   outside review.
   **Figure 1** had its two-line row labels overlapping by about a pixel each, all four of them, in
   both panels. Caught by walking the rendered bounding boxes rather than by looking.
   **Figure 2** went to square plot areas with square grid cells, which is what makes a plot read
   as a plot. The cost is real and worth knowing: two square panels over one is an almost square
   figure, the page gives the figure 560px of width, and an almost square figure at that width is
   about 500px tall against a budget near 460. The gutter absorbs part of it and **the caption paid
   the rest**, coming down from seven lines to four. Panels went from 195x116 to 144x144 and the
   type is about 37 per cent larger.
   **The introduction band** came from the Stanford BPP committee, via Sebastian. Two points, both
   fair. The page opened on two research questions with nothing about who was asking them, and the
   contact address sat in a footer a visitor might never scroll to. So there is now a short band
   with a portrait and four sentences, and Email sits beside the CV in the fixed top-right.
   **This is the third position the site has taken on how much of the record to show**, and it is
   not a drift back to the CV copy of entry 10. The footer standing block stays deleted. What is
   new is small, biographical rather than evidentiary, and its brevity is the instruction.
28. **Current - width, and a collision that two checks missed (Sep 2026).** Sebastian reported the
   sections feeling empty and figure 1 still overlapping. Both were right and the second was mine.
   **The overlap was the community boxes, not the text.** `COMM_W` was 78 against a column step of
   74, so every neighbouring box overlapped by 4px, in both panels, on every build since the boxes
   were introduced. Two rounds of automated checking reported it clean because the sweep compared
   `<text>` elements and explicitly skipped the container rects. The rule is in the figure bullet
   above; the lesson is that an exclusion added to make a check readable is where the bug hides.
   **The emptiness was horizontal.** The content used 1077px of a 1512px window. The two research
   sections now run at `--focus-wrap: 70rem`, which widened the figures from 558 to 626px and, by
   widening the text measure, shortened the text column enough to pay for it. Figure 2's panels
   went to 149px square. Nothing had to be cut.
29. **Current - filling the screen instead of padding it (Sep 2026).** Sebastian, a third time, on
   white space, and this time the diagnosis was right. **The gap between two sections is
   `(100svh - content) / 2` on each side.** Padding does nothing while the content is shorter than
   the space left, which is why the two earlier attempts at trimming padding changed nothing he
   could see. The fix is taller content, so both figures grew into the room: figure 1 to 568x428
   and figure 2 to square panels of 183px, up from 149. The gap at 1512x830 went from 141px to 87.
   He then asked for the block to sit lower to balance the caption, which is the optical-centring
   correction recorded in the layout section above.
   The footer lost the degree line, now that the hero and the band both carry it, and was tightened
   to match; it went from 193px to 152.
30. **Current - three figure corrections (Sep 2026).** All three from Sebastian, all three real.
   **The species-pool capsule** did not reach the outer columns, so the first and last arrows left
   from nothing. It is now sized by `COL_X`. **Panels A and B came closer and panel C dropped**,
   `GUTTER` 58 to 40 and `GAP` 72 to 80, and the panels grew to 198px.
   **What that cost, since the arithmetic is not obvious.** The gutter is the only thing holding
   figure 2's aspect down. Narrowing it makes the figure relatively taller, and at the width the
   page gives it the aspect sits near 0.90 whatever the panel size, so there is no panel size that
   pays for the change. **Figure 2's caption went from three lines to two** to buy the height, and
   with it the clause explaining why panel C is an inference. The panel is still marked as one. If
   that clause matters more than the panel size, restoring it costs about 23px and the panels go
   back to roughly 183.
   A fourth overlap surfaced while measuring, figure 1's habitat label against the lower panel's
   title, and the clearance rule is in the figure bullet above.
