---
paths: [ "docs/**/*.md" ]
---

# Documentation prose style

These conventions apply to Markdown files under `docs/` that are read by human
readers (reports, posts, collections). They do not apply to fenced code blocks
or inline code embedded in these files. Always fence code blocks (backtick or
tilde fences) rather than indenting them, so the exemption is unambiguous.

- No em-dashes (—). Use a comma, colon, period, or parentheses instead.
- ASCII only, with exactly two permitted exceptions: the center dot `·` (as a
  better-looking alternative to vertical bar `|`) and the multiplication sign
  `×`, both applied in tasteful moderation. Everything else is ASCII: no curly
  quotes, smart apostrophes, or ellipsis characters. Write `->` for arrows,
  `alpha` for the Greek letter, `<=` for inequalities.
- American spelling (e.g. `color` not `colour`, `organize` not `organise`,
  `neighbor` not `neighbour`; likewise `behavior`, `analyze`, `center`, and so
  on).
- Moderate formatting. Avoid heavy use of bold, italics, or nested bullet lists
  where plain prose reads fine. Reserve formatting for genuine emphasis or
  structure (headings, code, tables), not decoration.
- First-person plural: always `we`. Address the reader as `we` not `you` and not
  `I`. "We compute the forest first" rather than "you compute" or "I compute".
  Use `our` for the possessive. This keeps a single, collaborative voice across
  all documents.
- Line width should not exceed 80 characters, except fenced code blocks and
  tables. URLs do not count toward the limit.
- Tables should be formatted to have all columns properly aligned. Tables may
  exceed 80 characters width.
- Use `$` symbols for inline math and `$$` for displayed math.

## Maintenance

The mechanical subset of these rules (ASCII-only, line width) is also enforced
by the script `.claude/scripts/check-docs-style.sh`, which is run by the
`docs-style-check` and `docs-style-fix` skills and is suitable for a pre-commit
hook. When adding or changing a mechanically checkable rule here, update that
script in the same change. Judgment-based rules (spelling, voice, formatting)
need no such sync: the skills read this file at run time.

