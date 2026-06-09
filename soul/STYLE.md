# MeetMind Style Guide

## Voice & tone (product copy)

- **Calm and competent.** Like a great chief-of-staff: brief, useful, never breathless.
- **Plain language.** No jargon, no "synergy." Say "tasks," not "actionables."
- **Active and specific.** "Sam owns the migration by Friday," not "A migration is
  to be undertaken."
- Empty states are encouraging, not cute: "No action items yet — paste a transcript
  to get started."

## Visual language

- **Theme:** clean, content-first, generous whitespace. The transcript and its
  insights are the hero.
- **Dark mode is first-class.** Every surface must look intentional in both light
  and dark. Use Tailwind `dark:` variants (class strategy on `<html>`).
- **Color**
  - Neutral base: slate/zinc grays.
  - Accent: indigo (`indigo-600` light / `indigo-400` dark) for primary actions.
  - Semantic: green = done, amber = medium priority, red = high priority / risk.
- **Type:** system font stack; clear hierarchy via size + weight, not many colors.
- **Spacing:** prefer `gap-*` and consistent `p-4` / `p-6` rhythm. Rounded `rounded-xl`
  cards, subtle `shadow-sm`, `border` in `slate-200` / `dark:slate-800`.

## Component conventions

- Cards for each entity type (Summary, Action Items, Nuggets, People).
- Priority and category render as small pills/badges with semantic colors.
- Loading: skeletons, not spinners, where possible.
- Buttons: primary = filled indigo; secondary = bordered neutral.

## Code style echoes design

- Keep components small and named for what they show (`ActionItemCard`,
  `NuggetList`). Tailwind utilities inline; no ad-hoc CSS files.
