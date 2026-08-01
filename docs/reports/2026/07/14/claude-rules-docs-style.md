About docs-style rules in .claude/
==================================
July 14, 2026

<!--
How we use Claude Code's .claude/rules/ to keep a consistent prose style in
docs/**/*.md, and the docs-style-check / docs-style-fix skills that add a
deterministic script check on top of the rule. 
A full technical review of the .claude/ directory is in
docs/reports/2026/07/13/dot-claude-folder-tech-note.md.
-->

Claude rules in the `.claude/rules/` folder are a set of guidelines that help
maintain a consistent and readable style in the documentation of this project.
These rules are designed to improve the overall quality and clarity of the
documentation, making it easier for readers to understand and navigate the
project.

We created `.claude/rules/docs-style.md`, scoped to `docs/**/*.md` via the
`paths:` frontmatter.

Since the rule is already scoped to `docs/**/*.md`, we do not need to name the
rule at all: Claude Code auto-injects docs-style.md into context whenever a
matching file gets read.

We can request to apply the docs style rules to a specific file `xxx.md` and to
**report** violations:
```
Report docs-style violations in xxx.md
```
Or, we can request to apply the docs style rules to a specific file `xxx.md`
and to **fix** violations:
```
Fix docs-style violations in xxx.md
```

A few useful clarifications:

- **The trigger is file access, not the rule name.** Simply opening or reading
  docs/xxx.md (which happens automatically once we reference it) loads
  docs-style.md into context. We do not need to say "docs-style" explicitly,
  though it does not hurt as a hint.
- **This is a suggestion, not enforcement.** The harness guarantees the rule
  text gets injected, but it is still up to the model to actually catch every
  em-dash, non-ASCII character, or British spelling. It is judgment-based, not a
  hard linter.
- **For a guaranteed check** (not just best-effort review) we use a script
  rather than the rules file alone: see the skills below, which wrap
  `.claude/scripts/check-docs-style.sh`. The same script is suitable for a
  pre-commit hook.

## docs-style skills

Two skills in `.claude/skills/` put a deterministic floor under the rule:

- `/docs-style-check [file ...]` reports violations and never edits files.
- `/docs-style-fix [file ...]` fixes violations, then re-checks to verify.

Both skills start by running `.claude/scripts/check-docs-style.sh`, which
guarantees detection of the mechanical rules: non-ASCII characters outside code
fences (with the permitted `·` and `×` exceptions) and lines over 80 characters
(excluding table rows, with URLs not counted toward the limit). The model then
reviews the judgment-based rules (American spelling, `we` voice, moderate
formatting) against the rule file, which remains the single source of truth.
With no argument, the skills target the docs/**/*.md files changed vs HEAD,
including untracked files.

Usage examples (in Claude Code prompt):
```
/docs-style-check
/docs-style-check docs/reports/2026/07/14/claude-rules-docs-style.md
/docs-style-fix
/docs-style-fix docs/site/hacker-news-alt.md
Check docs style in the report we just edited
Fix docs-style violations in docs/xxx.md
```
The last two work because the skills are model-invocable: natural-language
requests route to them automatically, based on the skill descriptions.

## `.claude/` folder in the root of the repo or project

What `.claude/` is for generally: it is Claude Code's config directory, holding
settings, custom slash commands, subagent definitions, skills, and now rules. It
is not inherently "instructions storage" except for the `.claude/rules/` files
specifically.

```text
# Loaded automatically as instructions:
.claude/CLAUDE.md     # always, at session start (or ./CLAUDE.md at root)
.claude/rules/*.md    # at session start; rules with paths: frontmatter
                      # load only when a matching file is read
subdir/CLAUDE.md      # when Claude reads files in that subdirectory
CLAUDE.local.md       # always; gitignored, personal-only

# Applied by the harness (config, not instructions):
.claude/settings.json # permissions, hooks, env, model

# Loaded only when invoked (/name) or delegated to:
.claude/commands/
.claude/skills/
.claude/agents/
```

## How this repository uses it today

As of this review the repo has a single component:
`.claude/rules/docs-style.md`, path-scoped to `docs/**/*.md`, which encodes the
prose conventions for published documents (ASCII only, no em-dashes, American
spelling, `we` voice, 80-character lines, moderate formatting). Natural next
steps, in increasing order of rigor:

1.[x] Add skills (`/docs-style-check`, `/docs-style-fix`) that bundle a small
  grep script for the mechanical rules, giving a guaranteed detection pass for
  non-ASCII characters and long lines while leaving spelling and voice to model
  judgment.
2.[ ] Add a `.claude/settings.json` with a small permission allowlist for the
  read-only commands used in doc work.
3.[ ] If violations must never land in `main`, add a pre-commit hook
  (`.git/hooks/pre-commit`) or a Claude Code hook (`.claude/settings.json`
  `PreToolUse`/`Stop`) that runs the same grep script and fails on matches.
