import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ base: './src/content/projects', pattern: '**/*.md' }),
  schema: z.object({
    order: z.number(),
    title: z.string(),
    role: z.string(),
    advisor: z.string().optional(),
    pi: z.string().optional(),
    status: z.string(),
    lede: z.string(),
    image: z.string(),
    imageAlt: z.string(),
    aspectRatio: z.string().default('4 / 3'),
    tags: z.array(z.string()).default([]),
  }),
});

const outputs = defineCollection({
  loader: glob({ base: './src/content/outputs', pattern: '**/*.md' }),
  schema: z.object({
    order: z.number(),
    kind: z.enum(['manuscript', 'presentation', 'award']),
    title: z.string(),
    authors: z.array(z.string()).default([]),
    venue: z.string().optional(),
    year: z.number().optional(),
    status: z.string().optional(),
  }),
});

export const collections = { projects, outputs };
