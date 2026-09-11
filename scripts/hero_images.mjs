/* Build the small end of the responsive hero set from public/assets/field.webp.
 *
 * The hero is full-bleed, so the browser needs roughly viewport width times
 * device pixel ratio. One 1920-wide file was going to every visitor, phones
 * included. This emits four narrower WebP files; the 1920 entry in the srcset
 * stays the original, which is also the og:image and must not be re-encoded.
 *
 * AVIF was measured and dropped. The source is a dark, grainy cave photograph
 * already saved as WebP, and at matching quality AVIF came out larger at every
 * width; the settings where it was smaller were low enough to risk blotching in
 * the shadows, which is most of this picture.
 *
 * sharp comes in with Astro rather than from package.json, so run this from the
 * project root with node_modules installed.
 *
 *     node scripts/hero_images.mjs
 */
import sharp from 'sharp';
import { mkdir } from 'node:fs/promises';

const SRC = 'public/assets/field.webp';
const OUT = 'public/assets/hero';
const WIDTHS = [640, 960, 1280, 1600];

await mkdir(OUT, { recursive: true });
const meta = await sharp(SRC).metadata();
console.log(`source ${meta.width}x${meta.height}`);

for (const w of WIDTHS) {
  const file = `${OUT}/field-${w}.webp`;
  const info = await sharp(SRC)
    .resize({ width: w, withoutEnlargement: true })
    .webp({ quality: 72, effort: 6 })
    .toFile(file);
  console.log(`  ${w}px  ${(info.size / 1024).toFixed(1)} KB`);
}

/* The portrait in the introduction band. The original stays untouched at
   public/assets/profile.webp, since that URL may be circulating; this is the
   size the band actually needs at two times density. */
const P_OUT = 'public/assets/portrait-256.webp';
const p = await sharp('public/assets/profile.webp')
  .resize({ width: 256, height: 256, fit: 'cover' })
  .webp({ quality: 82, effort: 6 })
  .toFile(P_OUT);
console.log(`portrait  ${(p.size / 1024).toFixed(1)} KB`);
