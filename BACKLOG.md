# BACKLOG.md — correagallego.com

Prioritized task list for this session. Execute in order. Mark done with `[x]`.
Do not skip ahead. Run `npm run build` at the end of Phase 1 and Phase 2 before Phase 3.

---

## Phase 1 — Content (no build required between tasks)

- [x] **C1** Update degree status everywhere (see CLAUDE.md C1 for full replacement table)
  - `src/pages/index.astro` — eyebrow prop, tagline, about text, profile-panel list
  - `src/layouts/Base.astro` — default meta description
  - `src/pages/trajectory.astro` — education entry, about text, current stage bullets
  - `src/pages/research.astro` — page intro lede
  - `src/content/projects/cave.md` — status field

- [x] **C2** Delete the sentence "This website records that process of narrowing rather than presenting a finished identity." from `trajectory.astro`

- [x] **C3** Add doctoral direction sentence to `trajectory.astro` Current direction section

- [x] **C4** Add GEBI affiliation in `cave.md` and `trajectory.astro` thesis Entry

- [x] **C5** Add Research Interests paragraph to `research.astro` (verbatim from CLAUDE.md C5)

- [x] **C6** Remove `<aside class="profile-panel">` from `index.astro`. Update grid class on about section. Remove related CSS from `global.css`.

- [x] **C7** Update all meta descriptions (remove "undergraduate", reflect completed degree)

- [x] **C8** Update JSON-LD `jobTitle` in `Base.astro`

### Build check 1
```bash
npm run build
```
Fix any errors before proceeding.

---

## Phase 2 — Technical

- [x] **T1** Add Astro View Transitions to `Base.astro` + transition CSS to `global.css`

- [x] **T2** Replace IntersectionObserver scroll reveal with CSS `animation-timeline: view()` in `global.css`. Remove the `<script>` block from `Base.astro`. Remove `.reveal-stagger` rules.

- [x] **T3** Migrate `:root` hex values to oklch in `global.css` (see CLAUDE.md T3 palette)

- [x] **T4** Add `@layer` structure at top of `global.css`. Assign existing rule blocks to layers. Resolve any specificity regressions.

- [x] **T5** Add `container-type: inline-size` to `.project` and add `@container` query

### Build check 2
```bash
npm run build
```
Fix any errors before proceeding.

---

## Phase 3 — Deploy

- [x] Verify `public/CNAME` still contains `correagallego.com`
- [x] Stage all changes: `git add -A`
- [x] Commit: `git commit -m "Graduate status update, content audit, View Transitions, oklch palette, scroll-driven animations"`
- [x] Push: `git push origin main`
- [x] Confirm GitHub Actions workflow starts (visible in repo Actions tab)

---

## Out of scope for this session — do not add

- Dark mode toggle
- Blog / writing section
- Analytics
- External JS libraries
- Font changes
- New pages
