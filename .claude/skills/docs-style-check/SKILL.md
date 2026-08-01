---
name: docs-style-check
description: Report docs-style violations in docs/**/*.md files against
  .claude/rules/docs-style.md. Runs a deterministic script for the mechanical
  rules (ASCII-only, line width), then reviews the judgment rules (American
  spelling, "we" voice, moderate formatting). Reports only, never edits files.
  Use when the user asks to check, lint, or report docs style violations.
argument-hint: [ file-or-glob ... ]
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(.claude/scripts/check-docs-style.sh:*)
  - Bash(git status:*)
  - Bash(git diff:*)
---

# Docs style check

Rule source of truth: @.claude/rules/docs-style.md

Mechanical check (script output):
!`.claude/scripts/check-docs-style.sh $ARGUMENTS`

Target files: $ARGUMENTS. If empty, the target is the set of docs/**/*.md files
changed vs HEAD (including untracked), as chosen by the script above.

Steps:

1. The script output above already covers the mechanical rules: non-ASCII
   characters (outside code fences, with the permitted center dot and
   multiplication sign exceptions) and lines over 80 characters. Treat every
   reported line as a confirmed violation; do not re-derive these checks.
2. Read each target file and review it against the judgment-based rules in the
   rule file: American spelling, first-person plural "we" voice, moderate
   formatting, properly aligned tables, and `$`/`$$` math delimiters. Skip code
   blocks and fenced snippets.
3. Report all violations as a single list grouped by file, one line each:
   `file:line - rule - short excerpt`. If there are no violations, state that
   the target files pass docs-style.

Do not edit any files. This skill reports only; to apply fixes, use
/docs-style-fix.
