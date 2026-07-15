About docs-style rules in .claude/
==================================

Claude rules in `.claude/rules/` folder are a set of guidelines that help
maintain a consistent and readable style in the documentation of the Claude
project. These rules are designed to improve the overall quality and clarity of
the documentation, making it easier for users to understand and navigate the
project.

Created `.claude/rules/docs-style.md`, scoped to `docs/**/*.md` via the paths:
frontmatter.

Since the rule is already scoped to docs/**/*.md, you don't need to name the
rule at all — Claude Code auto-injects docs-style.md into context whenever a
matching file gets read. Just ask directly:
```
Apply docs-style rules and report violations in docs/xxx.md
```
or if you want fixes applied in the same pass:
```
Apply docs-style rules and fix any violations in docs/xxx.md
```

A few useful clarifications:

- **The trigger is file access, not the rule name.** Simply opening/reading
  docs/xxx.md (which happens automatically once you reference it) loads
  docs-style.md into context — you don't need to say "docs-style" explicitly,
  though it doesn't hurt as a hint.
- **This is a suggestion, not enforcement.** The harness guarantees the rule
  text gets injected, but it's still up to the model to actually catch every
  em-dash, non-ASCII character, or British spelling. It's judgment-based, not a
  hard linter.
- **If you want a guaranteed check** (not just best-effort review), that would
  require a script or hook rather than a rules file — e.g., a small grep/regex
  check for em-dashes and non-ASCII characters run as a pre-commit hook.

## `.claude/` folder in the root of the repo or project

What `.claude/` is for generally: it's Claude Code's config directory -
settings, custom slash commands, subagent definitions, skills, and now rules.
It's not inherently "instructions storage" except for the `.claude/rules/` files
specifically.

```text
# Always load:
.claude/CLAUDE.md
.claude/rules/*.md
subdir/CLAUDE.md # Loads only when Claude reads files in that subdirectory
CLAUDE.local.md # Gitignored, personal-only (not shared with teammates)

# Only load when explicitly invoked (/command-name) or matched:
.claude/settings.json # This is config (permissions, hooks, model)
.claude/commands/
.claude/agents/
.claude/skills/
```
