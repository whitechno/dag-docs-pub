---
paths: [ "docs/**/*.md" ]
---

# Documentation prose style

These conventions apply to Markdown files under `docs/` that are read by human
readers (reports, posts, collections). They do not apply to code blocks or
fenced snippets embedded in these files.

- No em-dashes (—). Use a comma, colon, period, or parentheses instead.
- ASCII only. No curly quotes, smart apostrophes, ellipsis characters, or other
  non-ASCII punctuation/symbols. Write `->` for arrows, `alpha` for the symbol,
  `<=` for inequalities. However, the use of a center dot `·` is allowed as a
  better-looking alternative to vertical bar `|`, as well as multiplication sign
  `×`, but applied in tasteful moderation.
- American spelling (e.g. `color` not `colour`, `organize` not `organise`,
  `neighbor` not `neighbour`; likewise `behavior`, `analyze`, `center`, and so
  on.).
- Moderate formatting. Avoid heavy use of bold, italics, or nested bullet lists
  where plain prose reads fine. Reserve formatting for genuine emphasis or
  structure (headings, code, tables), not decoration.
- First-person plural: always `we`. Address the reader as `we` not `you` and not
  `I`. "We compute the forest first" rather than "you compute" or "I compute".
  Use `our` for the possessive. This keeps a single, collaborative voice across
  all documents.
- Line width should not exceed 80 characters, except code blocks, tables, and
  long URLs.
- Tables should be formatted to have all columns properly aligned. Tables may
  exceed 80 characters width.
- Use `$` symbols for inline math and `$$` for displayed math.

User can request to apply the docs style rules to a specific file `xxx.md` and
to **report** violations:
```
Report docs-style violations in xxx.md
```
Or, user can request to apply the docs style rules to a specific file `xxx.md`
and to **fix** violations:
```
Fix docs-style violations in xxx.md
```
