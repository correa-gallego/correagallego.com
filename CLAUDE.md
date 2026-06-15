# CLAUDE.md — correagallego.com — Full Redesign

Read this file completely before any action. It overrides all previous CLAUDE.md, BACKLOG.md, and ASSET_GUIDE.md files. Delete those files after reading this one.

---

## Identity

Sebastian Correa-Gallego. Biologist. B.Sc. Biology, Universidad EAFIT, Medellín, Colombia (2026). GPA: 4.44/5.00. Visiting Student Intern, ECSO Lab, Purdue University (Aug 2025 – Jan 2026). Currently preparing doctoral applications — target entry Fall 2027. Contact: scorreag6@eafit.edu.co.

---

## Objective of this session

Complete architectural redesign of correagallego.com. Three changes:

1. **Consolidate to a single page.** All content on `index.astro`. Delete all other page files except a 404. The CV is accessed via a direct PDF link — no `/cv/` subpage.
2. **Redesign visually.** Typography-driven, no video hero, no borrowed imagery. Restraint is the design language. The site must read like an editorial document — not a startup landing page, not a template.
3. **Migrate hosting to Cloudflare Pages.** Replace the GitHub Actions deploy workflow. The repo can remain on GitHub (may be made private). Cloudflare Pages connects to the repo directly.

---

## Site purpose and audience

Primary reader: PhD program committees, prospective advisors (Peay, Fukami, Koskella, Cavanaugh, Kuehn, Kocher). Secondary: collaborators, peers.

The site must answer three questions within 60 seconds:
1. Who is Sebastian scientifically?
2. What has he done?
3. Where is he going?

No motivational language. No self-promotion. No redundancy. Every sentence must earn its place. The CV.tex in the project root is the standard of objectivity — the web content must be at least as precise.

---

## Stack

- Framework: Astro (latest stable), static output
- Deploy: **Cloudflare Pages** (connected to GitHub repo, builds automatically on push)
- DNS: Cloudflare (domain: `correagallego.com`)
- Fonts: Libre Baskerville (serif, headings/name) + Inter (sans, body/UI)
- Content: Astro content collections in `src/content/` for projects and outputs
- Styling: `src/styles/global.css` — single file, no preprocessor, no Tailwind
- CNAME: **Delete `public/CNAME`** — Cloudflare Pages does not use CNAME files

---

## Architecture after redesign

```
src/
  components/
    Nav.astro            ← minimal top nav with scroll anchors
    Footer.astro         ← copyright, email, LinkedIn, GitHub
    ProjectCard.astro    ← research project block with image
    Entry.astro          ← compact CV-style entry (role + date + text)
    Media.astro          ← image with CSS placeholder fallback (keep existing)
  content/
    projects/
      cave.md            ← keep, update if needed
      yeast.md           ← keep, update if needed
    outputs/
      cave-manuscript.md
      yeast-manuscript.md
      symposium-presentation.md
      redcolsi-presentation.md   ← NEW (see CV.tex: XXIII Encuentro Departamental, RedCOLSI, Jan 2024)
      undergraduate-scholarship.md
    content.config.ts
  layouts/
    Base.astro           ← HTML shell, meta, schema, fonts
  pages/
    index.astro          ← THE SINGLE PAGE — all content here
    404.astro            ← keep
  styles/
    global.css           ← complete rewrite
public/
  assets/
    profile.jpg          ← keep
    favicon.svg          ← keep
    Correa-Gallego_CV.pdf ← keep
    images/              ← keep all existing images
    logo/                ← keep
    illustrations/       ← keep
```

**Delete these files:**
- `src/pages/research.astro`
- `src/pages/trajectory.astro`
- `src/pages/publications.astro`
- `src/pages/cv.astro`
- `src/components/HeroSection.astro` (replaced by inline hero in index.astro)
- `src/components/SectionDivider.astro` (unnecessary)
- `BACKLOG.md`
- `ASSET_GUIDE.md`
- `public/CNAME`

---

## Page structure: index.astro

The page is a single scroll with anchored sections. The Nav links to `#about`, `#research`, `#publications`, `#record`, `#contact`. Smooth scroll via CSS `scroll-behavior: smooth`.

### Section 1: Hero

Full-viewport height. Dark background — NOT an image, NOT a video.

Background: deep dark gradient evoking depth/earth (use oklch dark tones from the existing palette, e.g., `oklch(8% 0.02 248)` to `oklch(12% 0.025 240)`), with the existing SVG noise grain overlay at low opacity (~0.06). Subtle radial gradient accents for depth — dark greens and blues at very low opacity.

Content (centered vertically, left-aligned within a container):
- Profile photo: circular, ~130px, with a subtle warm border and shadow. Positioned to the left of or above the text depending on viewport.
- Name: `Sebastian Correa-Gallego` in Libre Baskerville, large (`clamp(2.4rem, 5vw, 3.8rem)`), white, tight letter-spacing.
- Below name: `Biologist · Universidad EAFIT · Medellín, Colombia` in Inter, small caps or uppercase, muted white (~0.7 opacity), tracked.
- Below that: one sentence in Inter, regular weight, ~0.88 opacity white: `Microbial ecology and cellular physiology, from subterranean systems to the yeast proteome.`
- Subtle scroll indicator at bottom (animated line, same as current).

**No buttons in the hero. No "Explore research" CTA. No fact cards. The hero is name, identity, one line.**

Entrance animation: name fades in and slides up gently over 0.8s. Subtitle and tagline follow with slight delay. Use CSS `@keyframes`, not JS.

### Section 2: About (`#about`)

White/paper background. Constrained width (max ~700px centered).

Heading: `About` — styled as the section-title class (Libre Baskerville, large).

Content: **Use this exact text, derived from the CV.tex Research Interests paragraph and the current site's About:**

> I study how microbial life organizes under constraint. My work spans two systems: the cultivable microbial communities of a tropical volcaniclastic cave, where community structure shifts along a light gradient, and the proteomic allocation of cellular resources in yeast under carbon limitation.
>
> These are different scales of a shared question — how biological systems negotiate energy, nutrients, and environmental restriction. I approach this through microbial ecology, evolutionary cell biology, and the integrative study of natural systems, with growing investment in quantitative and computational frameworks.

Two paragraphs. No more. This replaces the current four-paragraph About which is too long.

### Section 3: Research (`#research`)

Heading: `Research`

Subheading/lede (one sentence, Inter, muted): `Two active projects define the current scope of my work.`

Then two ProjectCard components, pulled from the content collections (`cave.md` and `yeast.md`). Each card:
- Project image (or CSS placeholder if no image)
- Title in Libre Baskerville
- Role + institution + advisor(s) in compact metadata format
- 2–3 sentence description from the .md body
- Status tag (e.g., "Thesis completed", "Manuscript in preparation")
- Keyword tags

Layout: on desktop, the two cards sit side by side or in an alternating image/text grid (as currently implemented). On mobile, stacked.

**Update cave.md:** Ensure the description mentions the Organal San Antonio at ~2350 m a.s.l. in Támesis, Antioquia (from CV.tex), R2A cultivation, and the three sectors (Entrance, Transition, Dark). Advisor: Prof. Nicolás Pinel Peláez, Ph.D. Group: GEBI.

**Update yeast.md:** The CV.tex says the project is "Proteome Allocation Rules in Osmotrophic Eukaryotes" investigating K. marxianus and V. polyspora under carbon limitation, not just "Yeast Mitochondria Project." Update the title to: `Proteome Allocation in Osmotrophic Eukaryotes across Carbon Regimes`. Update the description to mention chemostat/turbidostat operation, cell harvesting, and proteomics workflows. Keep "Yeast Mitochondria Project" only as a parenthetical familiar name if desired. Advisor: Dr. Shahed U. A. Shazib. PI: Dr. Sergio A. Muñoz-Gómez.

If the cave project has supporting illustrations (`cave_gradient.png`, `morphotypes_gradient.png`), include them below the cave project card as small figures with captions — same as current implementation.

### Section 4: Publications (`#publications`)

Heading: `Publications & Presentations`

Render from `src/content/outputs/` collection, sorted by order. Three groups:

**Manuscripts in preparation:**
- Cave manuscript (authors: **S. Correa-Gallego**, N. Pinel Peláez)
- Yeast manuscript (authors: **S. Correa-Gallego**, S.U.A. Shazib, S.A. Muñoz-Gómez)

**Presentations:**
- Research Proposal Presentation, 2nd Symposium of Biology, Universidad EAFIT, 2024. Awarded Second Place.
- Oral Presentation, XXIII Encuentro Departamental de Semilleros de Investigación, RedCOLSI, Antioquia, Colombia, Jan 2024.

**Recognition:**
- Visiting Student Intern, UREP-C Program, Purdue University, 2025–2026.
- Undergraduate Scholarship, Comfama and Fundación Fraternidad Medellín, 2022.

Format: compact list, no cards. Author names in regular weight, Sebastian's name in bold. Title in 600 weight. Venue/status in italic muted. Same pub-list styling as current.

**Create `src/content/outputs/redcolsi-presentation.md`** for the RedCOLSI presentation (from CV.tex, currently missing from the site).

### Section 5: Academic Record (`#record`)

Heading: `Academic Record`

Compact entries using the Entry component. This replaces the entire "Trajectory" page. Include only:

**Education:**
- B.Sc. in Biology, Universidad EAFIT, 2022–2026. GPA: 4.44/5.00.

**Research positions** (compact, one entry each — no long descriptions):
- Visiting Student Intern, ECSO Lab, Purdue University, Aug 2025 – Jan 2026.
- Undergraduate Thesis Researcher, Universidad EAFIT, 2024–2026. Advisor: Prof. Nicolás Pinel Peláez.
- Research Monitor, Universidad EAFIT, Jul–Dec 2024.

**Academic service:**
- Student Director, Research Group on Microbiology and Astrobiology (SIAB), Universidad EAFIT, Oct 2023 – May 2025. Affiliated with GEBI.

**Certifications** (compact, no descriptions):
- Responsible Conduct of Research (RCR) Training, CITI Program, Aug 2025.

### Section 6: Technical Skills

Heading: `Technical Skills`

Four groups with keyword-style items (keep the dot-prefixed `.keyword` styling from current CSS):
- **Laboratory & biological methods:** microbial cultivation (chemostat, turbidostat), environmental sampling, ecological field records, morphotype characterization, cell physiology, proteomics sample preparation, microscopy.
- **Quantitative & computational:** R, Python, Linux/Bash, LaTeX, QGIS, biological data analysis, data visualization, introductory bioinformatics.
- **Scientific workflows:** scientific writing, research communication, literature synthesis, figure preparation.
- **Languages:** Spanish (native), English (professional proficiency).

Note: the CV.tex says "professional proficiency" for English. The current site says "working proficiency." Use "professional proficiency" to match the CV.

### Section 7: Contact (`#contact`)

Heading: `Contact`

One line: `Email is the best route for academic correspondence.`

Links: email, LinkedIn, GitHub, and a "Download CV" link pointing to `/assets/Correa-Gallego_CV.pdf` (opens in new tab or downloads directly).

The CV link replaces the entire /cv/ subpage.

### Section 8: Footer

Same as current: © 2026 Sebastian Correa-Gallego · Medellín, Colombia · email · LinkedIn · GitHub.

---

## Design system

### Colors (oklch, keep existing palette)

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

    /* Hero-specific darks */
    --hero-bg-start: oklch(8% 0.018 248);
    --hero-bg-end:   oklch(12% 0.022 240);
}
```

### Typography

- Headings/name: Libre Baskerville, 700
- Body: Inter, 400 (regular), 500 (medium for UI), 600 (semibold for emphasis)
- Metadata/dates: Inter at smaller sizes
- No monospace font needed — remove JetBrains Mono references. Use Inter for dates too.

### Spacing

- Generous section padding: `clamp(5rem, 10vw, 8rem)` between major sections.
- Content max-width: 700px for text blocks, 1200px for project grids.
- The page should breathe. White space is not wasted space — it is the primary design element.

### Animations

Use **CSS-native scroll-driven animations only**. No JavaScript for animations.

```css
@media (prefers-reduced-motion: no-preference) {
    .reveal {
        animation: reveal-up linear both;
        animation-timeline: view();
        animation-range: entry 0% entry 70%;
    }
    @keyframes reveal-up {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }
}
@media (prefers-reduced-motion: reduce) {
    .reveal { opacity: 1; transform: none; animation: none; }
}
```

Apply `.reveal` to each section content block. The hero does NOT use scroll-reveal — it uses a load animation (`animation: heroIn 0.8s ease both`).

### Micro-interactions

- Nav links: underline slides in from left on hover (current behavior, keep).
- Contact links and CV download: subtle translateX(2px) on hover.
- Project cards: slight elevation (`translateY(-3px)`) and shadow increase on hover.
- Keywords: no hover effect. They are informational, not interactive. Remove the current hover-lift behavior.
- Profile photo in hero: very subtle scale(1.02) on hover. No rotation.

### Grain texture

Keep the existing SVG noise overlay on body::before. Reduce opacity to 0.04 for the light sections. The hero section applies its own grain at slightly higher opacity (~0.06).

### Paper background

Keep the subtle gradient background on body and the faint radial gradient accents. These are well-calibrated in the current CSS.

---

## Navigation

The Nav becomes a **scroll-spy style navigation** for the single page:

```
Sebastian Correa-Gallego    About  Research  Publications  Record  Contact
```

- On the hero (dark background), nav text is white/translucent (keep current `variant-full` behavior).
- After scrolling past the hero, nav should have a solid paper background (add a scroll-based class or use `backdrop-filter: blur()` with a semi-transparent background).
- On mobile: hamburger menu (keep current behavior).
- Links are anchor hrefs: `#about`, `#research`, `#publications`, `#record`, `#contact`.
- Clicking "Sebastian Correa-Gallego" scrolls to top.
- Active section highlighting via IntersectionObserver (this is the one place JS is needed for scroll spy).

---

## Cloudflare Pages migration

### Step 1: Update deploy workflow

Delete `.github/workflows/deploy.yml`.

Create `.github/workflows/deploy.yml` with this content (or delete the file entirely — Cloudflare Pages can build directly from the repo without GitHub Actions):

Actually, **the simplest approach**: delete the `.github/workflows/` directory entirely. Cloudflare Pages connects to the GitHub repo directly and runs the build itself. No GitHub Actions needed.

### Step 2: Build configuration for Cloudflare Pages

When Sebastian sets up the Cloudflare Pages project in the dashboard:
- Framework preset: Astro
- Build command: `npm run build`
- Build output directory: `dist`
- Node.js version: 20 (set via environment variable `NODE_VERSION=20`)

### Step 3: DNS

The DNS records in Cloudflare already point to GitHub Pages IPs. After Cloudflare Pages is set up:
- Delete the four A records pointing to GitHub Pages IPs (185.199.108-111.153)
- Delete the CNAME record for www pointing to GitHub
- Cloudflare Pages automatically provisions the custom domain when you add `correagallego.com` in the Pages project settings

### Step 4: Delete `public/CNAME`

Cloudflare Pages does not use CNAME files. Delete it.

### Step 5: GitHub Pages

In the GitHub repo Settings → Pages, disable GitHub Pages (set source to "None").

---

## Content accuracy checklist (compare against CV.tex)

Before committing, verify these details match the CV.tex exactly:

- [ ] GPA: 4.44/5.00
- [ ] Education dates: 2022–2026 (no "expected")
- [ ] Purdue dates: Aug 2025 – Jan 2026
- [ ] Thesis dates: 2024–2026
- [ ] Research Monitor dates: Jul 2024 – Dec 2024
- [ ] Student Director dates: Oct 2023 – May 2025
- [ ] Thesis title: "Cultivable Microbial Community Structure Along a Light Gradient in a Tropical Volcaniclastic Cave"
- [ ] Purdue project: "Proteome Allocation Rules in Osmotrophic Eukaryotes" (from CV.tex)
- [ ] Organisms: K. marxianus and V. polyspora (from CV.tex), not just "yeast"
- [ ] Methods: chemostat and turbidostat cultivation, cell harvesting, proteomics workflows
- [ ] Cave: Organal San Antonio, ~2350 m a.s.l., Támesis, Antioquia
- [ ] Cave sectors: Entrance, Transition, Dark
- [ ] Cultivation medium: R2A
- [ ] English proficiency: "professional proficiency" (not "working proficiency")
- [ ] Advisor thesis: Prof. Nicolás Pinel Peláez, Ph.D.
- [ ] Advisor Purdue: Dr. Shahed U. A. Shazib (advisor), Dr. Sergio A. Muñoz-Gómez (PI)
- [ ] RedCOLSI presentation exists (XXIII Encuentro Departamental, Jan 2024)
- [ ] RCR Training: CITI Program, Credential ID 71597371, Aug 2025, valid through Aug 2029
- [ ] SIAB is the group acronym (Research Group on Microbiology and Astrobiology)
- [ ] Valeska Villegas-Escobar and Shahed Shazib are references (do NOT list references on the website — CV only)

---

## What to preserve

- All images in `public/assets/` (profile.jpg, field.jpeg, mito.png, illustrations, logos)
- The Astro content collection system (projects/*.md, outputs/*.md)
- The Media component with CSS placeholder fallback
- The JSON-LD person schema in Base.astro (update jobTitle to "Biologist and Researcher")
- The favicon
- The grain texture system
- The oklch color palette

## What NOT to do

- Do not add a blog, notes, or writing section
- Do not add analytics, tracking, or comment systems
- Do not add dark mode
- Do not add external JavaScript libraries (no GSAP, no anime.js, no framework)
- Do not use images from NASA or any external source that is not Sebastian's own work
- Do not add philosophical quotes or references to non-scientific thinkers
- Do not invent biographical facts
- Do not add keywords hover effects (keywords are informational labels, not buttons)
- Do not add a "trajectory" narrative section — the Academic Record section is factual and compact
- Do not write motivational, promotional, or ornamental language anywhere
- Do not include the childhood weather observation story (this has been removed from scope)

---

## Execution order

1. Read all existing source files to understand current state
2. Delete files listed in the deletion list above
3. Create `src/content/outputs/redcolsi-presentation.md`
4. Update `src/content/projects/cave.md` and `yeast.md` per accuracy checklist
5. Rewrite `src/styles/global.css` completely
6. Rewrite `src/layouts/Base.astro` (remove View Transitions import — single page doesn't need it)
7. Rewrite `src/components/Nav.astro` for scroll-anchor navigation
8. Simplify `src/components/Footer.astro` if needed
9. Rewrite `src/pages/index.astro` as the single consolidated page
10. Update `src/pages/404.astro` (only link back to `/`)
11. Delete `.github/workflows/deploy.yml`
12. Delete `public/CNAME`
13. Delete `BACKLOG.md` and `ASSET_GUIDE.md`
14. Run `npm run build` — fix any errors
15. `git add -A && git commit -m "Single-page redesign, content consolidation, Cloudflare Pages prep" && git push`

After push, Sebastian will:
- Set up Cloudflare Pages project in dashboard (connect to GitHub repo)
- Configure build settings (Astro preset, `npm run build`, output `dist`)
- Add custom domain `correagallego.com`
- Remove old GitHub Pages DNS records
- Disable GitHub Pages in repo settings

---

## Quality standard

When a prospective PhD advisor at Stanford, Harvard, or Princeton visits correagallego.com, they should see a page that loads instantly, communicates scientific identity in under 30 seconds, contains no fluff, and demonstrates taste through typography and restraint rather than spectacle. The site should feel like opening a well-typeset scientific paper — warm paper color, clear hierarchy, generous margins, and every element earning its place.
