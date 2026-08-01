---
name: docs-style-fix
description: Fix docs-style violations in docs/**/*.md files per
  .claude/rules/docs-style.md. Runs a deterministic script for the mechanical
  rules (ASCII-only, line width), fixes all violations including the judgment
  rules (American spelling, "we" voice, moderate formatting), then re-runs the
  script to verify. Use when the user asks to fix or apply docs style.
argument-hint: [ file-or-glob ... ]
allowed-tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Bash(.claude/scripts/check-docs-style.sh:*)
  - Bash(git status:*)
  - Bash(git diff:*)
---

# Docs style fix

Rule source of truth: @.claude/rules/docs-style.md

Mechanical check (script output):
!`.claude/scripts/check-docs-style.sh $ARGUMENTS`

Target files: $ARGUMENTS. If empty, the target is the set of docs/**/*.md files
changed vs HEAD (including untracked), as chosen by the script above.

Steps:

1. Fix every violation reported by the script output above. Replace an em-dash
   with a comma, colon, period, or parentheses as the sentence requires; replace
   other non-ASCII characters with their ASCII equivalents; rewrap long lines at
   80 characters or fewer.
2. Read each target file and also fix the judgment-based rules from the rule
   file: American spelling, first-person plural "we" voice, moderate formatting,
   properly aligned tables, and `$`/`$$` math delimiters.
3. Fix style only. Preserve the meaning of the text, do not rewrite content, and
   leave code blocks and fenced snippets untouched.
4. Re-run the mechanical check on the same files to verify the fixes:
   `.claude/scripts/check-docs-style.sh <files>` must report clean.
5. Report what was changed as a short list grouped by file, one line each:
   `file:line - rule - what changed`. If nothing needed fixing, say so.
