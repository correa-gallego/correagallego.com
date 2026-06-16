# CLAUDE.md — correagallego.com — Definitive Design Refinement

Read this file completely before any action. It replaces the previous CLAUDE.md.

---

## Who you are working for

Sebastian Correa-Gallego. Biologist. B.Sc. Biology, Universidad EAFIT, Medellín, Colombia (2026). GPA: 4.44/5.00. Research experience at two scales: microbial community ecology in a tropical volcaniclastic cave (thesis, EAFIT) and proteomic resource allocation in yeast under carbon limitation (ECSO Lab, Purdue University). Preparing doctoral applications in microbial ecology and evolutionary biology for Fall 2027.

Sebastian is not a designer, not a developer, not a startup founder. He is a young scientist at the beginning of a serious academic career. His intellectual identity is precise: he studies how biological systems negotiate constraint — energy, nutrients, light, carbon. He approaches this through fieldwork, cultivation, quantitative analysis, and evolutionary thinking. His philosophical disposition values clarity, restraint, rigor, and the kind of beauty that emerges from disciplined attention to natural systems.

The audience for this site is PhD admissions committees, prospective doctoral advisors, and scientific collaborators. These are people who read papers, not landing pages. They value substance, precision, and evidence of genuine scientific thinking. They are allergic to self-promotion.

---

## What you must do

The single-page architecture is already in place and working. The content is accurate and consolidated. Your task is not structural — it is aesthetic and experiential. You must take the existing site and refine it into something that communicates, through its visual craft alone, that the person behind it has taste, discipline, and intellectual seriousness.

This is the difference between a well-organized CV and a beautifully typeset scientific monograph. The information is the same. The experience of reading it is not.

---

## Your mandate

You have full autonomy to make design decisions. You do not need to ask for permission. You are expected to exercise judgment — the same judgment a senior editorial designer would bring to typesetting a scientific publication for Nature or Annual Review of Ecology, Evolution, and Systematics.

Your constraints are:
1. **No structural changes.** The page sections (Hero, About, Research, Publications, Academic Record, Technical Skills, Contact) stay in order. No new sections. No new pages.
2. **No content changes.** Do not alter the prose text, project descriptions, publication entries, or CV data. Fix typos if you find them, but do not rewrite.
3. **No external dependencies.** No JavaScript libraries, no animation frameworks, no icon libraries, no CDN-hosted anything except Google Fonts.
4. **Respect `prefers-reduced-motion`.** Every animation must degrade gracefully.
5. **Performance.** The page must score 95+ on Lighthouse Performance. No heavy assets. No render-blocking resources.

Within these constraints, you may change anything: CSS, layout, spacing, typography scale, color calibration, animation timing, hover states, transitions, responsive breakpoints, visual rhythm, section backgrounds, borders, shadows, grain texture, the hero treatment, the nav behavior, the footer design, the project card layout, the publication list styling — everything visual is yours to refine.

---

## Design research: what the best practices say in 2026

The following is a synthesis of current web design research. Use it as informed context, not as a checklist.

### Typography

Serif fonts are experiencing a strong return in editorial and academic web design, especially when paired with clean sans-serif body text. The combination communicates both tradition and contemporary clarity. The site already uses Libre Baskerville + Inter — this is correct. What matters now is the *scale*: headline sizes should be generous enough to create clear hierarchy, body text should be sized for sustained reading (~17–18px with 1.7–1.8 line-height), and metadata should be clearly subordinate without being invisible.

Variable fonts offer weight/width control from a single file, improving performance and enabling micro-typographic adjustments. Consider whether switching to a variable font (e.g., Source Serif 4 Variable or Literata Variable for the serif; Inter is already variable) would improve typographic control.

### Color

OKLCH is the correct color model for 2026. The site already uses it. The key insight is that OKLCH's lightness channel maps to perceived lightness — meaning you can adjust hue and chroma without accidentally breaking contrast ratios. Use `color-mix()` for hover states and variants rather than defining separate hex values. This makes the palette more systematic and maintainable.

Color in 2026 editorial design is used with intention and restraint: soft base tones, clearly defined accents, contrasts designed for readability. The current palette (warm paper, dark ink, muted greens/blues) is appropriate for a scientist studying subterranean and natural systems. Calibrate it — ensure the accent color has sufficient contrast for accessibility (WCAG AA minimum), ensure the body text color against paper background provides comfortable sustained reading.

### Scroll-driven animations

CSS-native scroll-driven animations are universally supported in 2026. The key properties:
- `animation-timeline: view()` — animation progresses based on element visibility in viewport
- `animation-range: entry 0% entry 70%` — defines when the animation starts and ends relative to viewport entry
- `animation-composition: accumulate` — allows stacking multiple scroll-driven effects

Best practice: use `view()` for reveal-on-scroll. Keep animations subtle (opacity + small translateY, 16–20px max). Avoid parallax, avoid rotation, avoid scale effects on text. The purpose is to make the page feel alive without distracting from reading.

New in 2026: `scroll-triggered` animations (CSS `animation-trigger` property) that fire once when a scroll threshold is crossed, then play on a normal time-based timeline. These are ideal for entrance effects that should play at normal speed once triggered, rather than being scrubbed by scroll position.

### Layout and space

Minimalism in 2026 is "bold minimalism" — it is not about emptiness but about knowing what deserves attention and amplifying it. Generous white space is the primary design element. Section padding should be large enough that each section feels like its own environment. Content max-width should be optimized for reading (~65–75ch for prose).

Asymmetric layouts add movement to minimalist compositions without losing coherence. Consider whether the project cards benefit from a subtle asymmetric treatment (e.g., one card slightly larger than the other, or offset vertically).

### Micro-interactions

Every interactive element should provide feedback through subtle motion: links underline on hover, cards elevate slightly, buttons shift. These are not decorative — they are functional signals that the interface is responsive. Keep durations short (150–250ms). Use `cubic-bezier(0.22, 1, 0.36, 1)` for natural easing.

### Grain and texture

Subtle noise/grain overlays on backgrounds create warmth and tactility that distinguish a site from generic flat design. The site already has this. Calibrate the opacity — too much grain looks grungy, too little is invisible. The target is: noticeable on close inspection, invisible when reading.

### The editorial standard

The reference is not Dribbble or Awwwards. The reference is the typographic quality of journals like *Nature*, *Science*, *Annual Reviews*, *The New Yorker*, *Works That Work*. Clean, warm, confident typography with generous margins, clear hierarchy, and nothing that exists without purpose.

---

## Specific areas to evaluate and improve

These are not instructions — they are prompts for your own judgment. Evaluate each, decide whether improvement is needed, and act accordingly.

### 1. The hero

Is the hero visually compelling enough to hold attention for the 2–3 seconds before the viewer scrolls? Does the typography have sufficient presence? Is the dark gradient rich enough or does it feel flat? Does the grain texture add warmth? Is the profile photo well-integrated or does it feel pasted on? Is the scroll indicator necessary and well-timed?

Consider: a very subtle, slow CSS animation on the background gradient (shifting the radial gradient positions over 20–30s) could add depth without distraction. A slight vignette effect around the edges could increase focus on the content.

### 2. Typography scale and rhythm

Is the heading hierarchy clear and consistent? Does the section title size create enough visual weight to mark section transitions during scrolling? Is there enough vertical space between sections to let each breathe? Is the body text comfortable for extended reading?

Consider: using `clamp()` more aggressively for a responsive type scale that feels generous on large screens and tight on mobile without breakpoint jumps.

### 3. The research project cards

Are they visually distinct enough from the surrounding content? Do the images (or placeholders) contribute to the visual story or do they feel like afterthoughts? Is the metadata (advisor, institution, status) presented clearly without competing with the project description?

Consider: the project cards could benefit from a subtle background panel (slightly different from the main paper background) to create visual containment. Institution logos add credibility — ensure they are well-sized and integrated.

### 4. The publications list

Is it formatted like a proper academic bibliography? Are author names, titles, and status clearly differentiated typographically? Does it look like something you'd see in a CV or a journal's reference list?

### 5. The academic record section

Is it compact enough to not feel like a second CV? Is the chronological information scannable? Do the Entry components provide clear visual hierarchy between title, role, and date?

### 6. The nav

Does it feel integrated with the page or bolted on? On the dark hero, is the text legible? After scrolling past the hero, does the transition to solid background feel smooth? Is the scroll-spy highlighting working and perceptible?

Consider: a thin progress indicator bar at the top of the viewport that fills as the user scrolls through the page. This is a common editorial pattern that adds polish.

### 7. Mobile experience

Test the full page at 375px width. Is every section readable? Does the hero text remain impactful? Do the project cards stack gracefully? Is the nav hamburger menu well-styled within the dark hero context?

### 8. Print styles

If someone prints the page (for a committee review), does it degrade to clean black-on-white with no background textures, no animations, and no nav?

### 9. Performance

Audit the CSS for unused rules. Ensure fonts are loaded with `font-display: swap`. Verify that images use `loading="lazy"` and `decoding="async"`. Check that the grain texture SVG is not causing paint thrashing.

### 10. The overall feeling

Scroll the page from top to bottom. Does it feel like a coherent, intentional experience? Or does it feel like sections assembled from different templates? Is there a visual thread — a consistent rhythm — that connects hero to footer? Does it feel like it was made by someone who cares about craft?

---

## Execution

1. Read all source files in `src/` and `public/` to understand the current state.
2. Open `npm run dev` and inspect the site in the browser at desktop (1440px) and mobile (375px) widths.
3. Identify every area where the design falls short of the editorial standard described above.
4. Make all changes. Work through `global.css` systematically, then adjust component files and `index.astro` as needed.
5. Test: `npm run build` must succeed. Check the dev server at both viewport sizes. No console errors.
6. Commit: `git add -A && git commit -m "Design refinement: typography, spacing, animation, visual polish"`.
7. Push: `git push origin main`.

Cloudflare Pages rebuilds automatically on push. The changes will be live within 2 minutes.

---

## What not to do

- Do not add new pages or sections.
- Do not change the text content.
- Do not add JavaScript animation libraries.
- Do not add a dark mode toggle.
- Do not add analytics, tracking, or third-party scripts.
- Do not add a blog section.
- Do not change the font families (Libre Baskerville + Inter) unless you find a strictly superior variable-font alternative and can justify it.
- Do not add decorative elements that serve no informational purpose (decorative lines, ornamental dividers, geometric shapes).
- Do not add parallax scrolling effects.
- Do not make the hero full-screen on mobile if it pushes content below the fold excessively.

---

## Quality standard

The site belongs to a person who studies how life organizes under constraint. The design must embody that same principle: every element constrained to its essential form, every relationship between elements precisely calibrated, nothing present that does not contribute to the whole. The beauty of the page, like the beauty of a well-designed experiment, should emerge from the logic of its structure — not from ornament applied on top.

When finished, the page should pass this test: if a prospective PhD advisor at Stanford, Harvard, Princeton, Berkeley, or Chicago visits correagallego.com for 60 seconds, they should leave with three impressions — this person is scientifically serious, this person has clear research identity, and this person has uncommon attention to craft. The third impression is your responsibility.
