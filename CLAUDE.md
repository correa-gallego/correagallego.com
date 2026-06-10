# CLAUDE.md — correagallego.com

This file is the persistent project context for Claude Code sessions on this repository.
Read it fully before any action. It overrides all defaults.

---

## Identity

Sebastian Correa-Gallego. Researcher and recent graduate, Universidad EAFIT,
Medellín, Colombia (2026). Field and laboratory research experience at EAFIT
and at Purdue University (2025–2026). Currently preparing doctoral applications.
Contact: scorreag6@eafit.edu.co.

---

## Site purpose and audience

Academic personal website. Primary reader: potential PhD advisors, program committees, funding bodies.
Secondary reader: collaborators and peers.

The site must answer three questions within 90 seconds:
1. Who is Sebastian scientifically?
2. What has he done?
3. Where is he going?

No self-promotion. No motivational language. No abstract self-description. No redundancy.
Every sentence must earn its place against that reader.

---

## Stack

- Framework: Astro 5.18.1, static output (`output: 'static'`)
- Deploy: GitHub Pages via GitHub Actions (`.github/workflows/deploy.yml`)
- DNS: Cloudflare (domain: `correagallego.com`, DNS-only, no proxy)
- Fonts: Libre Baskerville (serif, display/headings) + Inter (sans, body/UI/mono fallback)
- Google Fonts via `@import` in `global.css`
- Content: Astro content collections in `src/content/` — collections: `projects`, `outputs`
- Styling: `src/styles/global.css` — single file, no preprocessor, no Tailwind

The CNAME file in `public/CNAME` contains `correagallego.com`. Do not delete it.

---

## Design system — values are constraints, not suggestions

These variables form the site's visual identity. Do not reassign or invent new ones.
Values will be migrated to oklch in this session (see BACKLOG T3), but the names are permanent.

```
--ink            deep navy, primary text
--ink-soft       slightly lighter navy, secondary emphasis
--body           readable body text
--muted          secondary text, labels
--light          tertiary text, dates, captions
--paper          page background (warm off-white)
--paper-warm     card/panel background
--surface        subtle section background
--border         dividers
--border-light   subtle dividers
--accent         #284f69 equivalent — primary interactive color
--accent-hover   darkened accent for hover
--accent-subtle  very light accent for backgrounds
--serif          Libre Baskerville
--sans           Inter
--content        700px max content width
--content-wide   1560px max wide content width
--gutter         responsive horizontal padding
--section-y      responsive vertical section spacing
--ease           cubic-bezier(0.22, 1, 0.36, 1)
```

---

## Architecture — preserve this exactly

```
src/
  components/
    Base.astro          ← HTML shell, meta, schema, scripts
    Nav.astro           ← site navigation
    Footer.astro        ← copyright, links
    HeroSection.astro   ← full-viewport hero component
    ProjectCard.astro   ← research project card
    Entry.astro         ← CV entry (role + date + content)
    Media.astro         ← image with CSS placeholder fallback
    SectionDivider.astro
  content/
    projects/
      cave.md           ← thesis project
      yeast.md          ← Purdue project
    outputs/
      cave-manuscript.md
      yeast-manuscript.md
      symposium-presentation.md
      undergraduate-scholarship.md
    content.config.ts   ← collection schemas
  layouts/
    Base.astro          ← page layout wrapper
  pages/
    index.astro
    research.astro
    trajectory.astro
    publications.astro
    cv.astro
    404.astro
  styles/
    global.css
public/
  assets/
    profile.jpg
    favicon.svg
    Correa-Gallego_CV.pdf
    images/field.jpeg, mito.png, perpetual-ocean-salinity.jpg
    logo/EAFIT.svg, Purdue.svg
    illustrations/cave_gradient.png, morphotypes_gradient.png
    video/perpetual_ocean2_CLOSE_103_salinity_1080p30.mp4  (external URL, not local)
  CNAME
```

Do not rename, move, or delete any asset files. Do not change component filenames.

---

## What to preserve without modification

- All prose in `src/content/projects/cave.md` and `src/content/projects/yeast.md`
- All entries in `src/content/outputs/`
- The childhood weather observation biographical detail (appears in `index.astro` and `trajectory.astro`) —
  this is the single most important biographical detail on the site
- The hero (NASA Perpetual Ocean video background)
- The CSS media placeholder system (`.media--cave`, `.media--yeast`, `.media--field`)
- The hero section visual system (`.hero-full`, overlays, scroll hint animation)
- The JSON-LD person schema in `Base.astro`

---

## Content changes — execute before technical changes

### C1. Degree status — update all instances

The degree is complete. Replace throughout all pages and components:

| Find | Replace with |
|------|-------------|
| `Biology undergraduate` | `B.Sc. Biology, Universidad EAFIT (2026)` |
| `Biology undergraduate in Colombia` | `Biologist. Universidad EAFIT, 2026.` |
| `undergraduate` (current status context) | `graduate` or remove |
| `2022–2026 (expected)` | `2022–2026` |
| `finishing the B.Sc.` | `completed the B.Sc.` |
| `Finishing the B.Sc. in Biology at Universidad EAFIT.` | `B.Sc. in Biology, Universidad EAFIT (2026).` |
| `Thesis in progress` | `Thesis completed` |
| `thesis in progress` | `thesis completed` |
| `Writing a thesis on` | `Thesis on` |
| `Undergraduate thesis` (role label) | `Undergraduate thesis` → keep this one, it's the role name, factually correct |

Files to check: `src/pages/index.astro`, `src/pages/trajectory.astro`, `src/layouts/Base.astro`
(meta description), `src/content/projects/cave.md`, `src/pages/research.astro`, `src/pages/publications.astro`.

Also update the `HeroSection` tagline in `src/pages/index.astro` from:
> "Biology undergraduate in Colombia working on cultivable cave microbiology and on mitochondrial physiology in yeast."

To:
> "Biologist. Microbial ecology and cellular physiology, from cave systems to the yeast proteome."

And the `eyebrow` prop:
> "Biology undergraduate · Colombia" → "B.Sc. Biology · Microbial ecology · Colombia"

### C2. Delete this exact sentence from `trajectory.astro`

In the "Current direction" section, locate and remove entirely:

> "This website records that process of narrowing rather than presenting a finished identity."

Do not replace it with anything. The paragraph is better without it.

### C3. Add doctoral direction line in `trajectory.astro`

In the "Current direction" section, at the end of the existing final paragraph (after the deletion in C2),
add this sentence:

> "Doctoral applications in microbial ecology and evolutionary biology are the immediate next horizon — target entry Fall 2027."

### C4. Add GEBI affiliation

In `src/content/projects/cave.md`, after `advisor: Prof. Nicolás Pinel Peláez`, add a new field or
inline note: the thesis group is **GEBI — Research Group on Geosciences and Biodiversity, Universidad EAFIT**.

In `src/pages/trajectory.astro`, in the thesis `Entry` component, update the role text to include the group:
> "Universidad EAFIT · GEBI (Research Group on Geosciences and Biodiversity)"

### C5. Add Research Interests to Research page

In `src/pages/research.astro`, after the `page-intro` header block and before the Projects section,
insert a new full-width text block styled as a pull paragraph (use `section-lede` class or a dedicated
`research-interests` container with generous max-width ~68ch and larger font size ~1.05rem).

Content — use this verbatim:

> "Evolution and ecology are not subfields of biology — they are its organizing logic, present from the emergence of cellular complexity to the structure of communities in extreme environments. My research interests sit at this intersection: I am drawn to microbial systems as tractable windows into how life assembles, persists, and transforms under ecological and energetic constraint. This includes questions about community organization along environmental gradients, the physiological and molecular strategies that underlie ecological success, and the eco-evolutionary dynamics that connect cellular function to community-level patterns. I am also interested in the quantitative and computational frameworks that make these questions formally tractable, and in connecting field-based inquiry with analytical rigor across biological scales."

No section heading needed. Style as a distinguished prose paragraph, not a bullet list.

### C6. Simplify the index page about section

Remove the entire `<aside class="profile-panel">` block (including `profile-panel__eyebrow`,
`profile-panel__list`, `institution-strip`, and `profile-panel__link`) from `src/pages/index.astro`.

This content duplicates the hero facts. The about section prose is sufficient.

Update the `.about--split` grid in `global.css` to a two-column layout:
photo (140px fixed) + body (1fr). Remove the third column. Remove `.about--split` class from the
template and replace with `.about`. Remove the `profile-panel`, `institution-strip`, and related CSS
from `global.css` if they have no other uses.

### C7. Update meta descriptions

In `src/layouts/Base.astro`, update the default `description` prop from:
> "Biology undergraduate researcher working across microbial ecology..."

To:
> "Sebastian Correa-Gallego — biologist. Microbial ecology of cave systems, cellular physiology in yeast. B.Sc. Biology, Universidad EAFIT (2026). Visiting researcher, Purdue University."

Update the page-level descriptions in `research.astro`, `trajectory.astro`, and `publications.astro`
to remove "undergraduate" and reflect the completed degree.

### C8. Update JSON-LD schema in `Base.astro`

Change `jobTitle` from `"Undergraduate Biology Researcher"` to `"Biologist and Researcher"`.
Update affiliation order: EAFIT first, Purdue second.

---

## Technical changes — execute after content changes and a clean build

### T1. Astro View Transitions

In `src/layouts/Base.astro`:
1. Add import: `import { ViewTransitions } from 'astro:transitions';`
2. Add `<ViewTransitions />` inside `<head>`, before the closing tag.

In `src/styles/global.css`, add transition animations:

```css
/* View Transitions */
@media (prefers-reduced-motion: no-preference) {
  ::view-transition-old(root) {
    animation: vt-out 0.2s ease-in both;
  }
  ::view-transition-new(root) {
    animation: vt-in 0.2s ease-out both;
  }
}
@keyframes vt-out {
  to { opacity: 0; transform: translateY(-5px); }
}
@keyframes vt-in {
  from { opacity: 0; transform: translateY(5px); }
}
```

### T2. Replace IntersectionObserver with CSS scroll-driven animations

Remove the entire `<script>` block in `src/layouts/Base.astro` that handles the `.reveal` class
with IntersectionObserver (look for the comment "Scroll reveal").

Replace the existing `.reveal` and `.reveal.visible` CSS rules in `global.css` with:

```css
/* Scroll-driven reveal — CSS native, no JS */
@media (prefers-reduced-motion: no-preference) {
  .reveal {
    animation: reveal-up linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 75%;
  }
  @keyframes reveal-up {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
  }
}

@media (prefers-reduced-motion: reduce) {
  .reveal {
    opacity: 1;
    transform: none;
    animation: none;
  }
}
```

Remove the `.reveal-stagger` and child delay rules — they are incompatible with scroll-driven
animations. Elements animate individually based on their own viewport entry. The stagger effect
happens naturally from position.

Keep all `.reveal` class attributes on elements in the Astro pages — they are still needed.

### T3. Migrate palette to oklch

Replace all hex values in the `:root` block in `global.css`. Use this exact oklch palette
(same perceptual identity as the original, now in uniform color space):

```css
:root {
  --ink:           oklch(15% 0.028 248);
  --ink-soft:      oklch(21% 0.030 248);
  --body:          oklch(40% 0.030 248);
  --muted:         oklch(54% 0.024 245);
  --light:         oklch(65% 0.018 245);
  --paper:         oklch(98.5% 0.006 230);
  --paper-warm:    oklch(96% 0.009 230);
  --surface:       oklch(94.5% 0.012 234);
  --border:        oklch(88% 0.016 235);
  --border-light:  oklch(93% 0.010 234);
  --accent:        oklch(35% 0.068 233);
  --accent-hover:  oklch(27% 0.060 233);
  --accent-subtle: oklch(94% 0.018 233);
  --shadow-sm:     0 1px 3px oklch(12% 0.020 248 / 0.06);
  --shadow-md:     0 4px 16px oklch(12% 0.020 248 / 0.08);
  --shadow-lg:     0 12px 40px oklch(12% 0.020 248 / 0.12);
}
```

### T4. Add CSS @layer structure

At the very top of `global.css`, before any rules, add:

```css
@layer reset, base, layout, components, utilities;
```

Then assign existing rule blocks to layers using `@layer base { ... }`, `@layer layout { ... }`, etc.
Approximate assignment:
- `reset`: the `*, *::before, *::after` block and `html` base
- `base`: `body`, `a`, `:focus-visible`, `::selection`, `p`, `em`
- `layout`: `.container`, `.section`, nav, footer, `.skip-link`
- `components`: hero, project cards, entries, about, pub-list, CV, work-grid, media
- `utilities`: `.reveal`, `.keywords`, `.plain-list`, print styles

This is a non-visual refactor. If adding @layer causes any style regression, it indicates a
specificity dependency — resolve it before pushing.

### T5. Container queries for project cards

In `.project` (the `ProjectCard` rule in global.css), add:
```css
.project {
  container-type: inline-size;
  container-name: project-card;
}
```

Add an `@container project-card` rule to handle narrow widths (replaces part of the `@media (max-width: 900px)` block for the project grid specifically).

---

## Build and deploy

Run `npm run build` after completing C1–C8 (content phase). Fix any errors before proceeding to technical changes.

Run `npm run build` again after T1–T5 (technical phase). Fix any errors.

If build is clean:
```bash
git add -A
git commit -m "Graduate status update, content audit, modern CSS, View Transitions, oklch palette"
git push origin main
```

GitHub Actions deploys automatically. Deployment completes in ~2 minutes.

You have full permission to commit and push to `main`.

---

## Do not do

- Do not add blog, notes, or writing sections
- Do not add comment systems, analytics scripts, or tracking
- Do not change font families (Libre Baskerville + Inter)
- Do not add dark mode toggle (not in scope for this session)
- Do not modify `.github/workflows/deploy.yml`
- Do not rename any files in `public/assets/`
- Do not add external JavaScript libraries
- Do not change the hero video source URL
- Do not add quotes from or references to philosophers, literary figures, or non-scientific thinkers
- Do not add a blog, publications RSS, or any dynamic content system
- Do not invent biographical facts — if uncertain, leave a comment `<!-- TODO: verify -->`
