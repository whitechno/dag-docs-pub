The .claude/ directory: purpose, capabilities, and common uses
==============================================================
July 13, 2026

<!--
A technical review of Claude Code's .claude/ project directory: what it is for,
what can live inside it, how each component behaves, and the common patterns
teams use it for. Verified against the official Claude Code documentation at 
https://code.claude.com/docs as of July 2026.
-->

The `.claude/` directory is Claude Code's per-project configuration root. It is
the mechanism by which a repository teaches Claude Code how to behave in that
repository: what it may do (permissions), what it should know
(instructions and rules), what it can be asked to do (skills and commands), who
it can delegate to (subagents), and what runs automatically around its actions
(hooks). Everything in it is plain text, so it is versioned, diffed, and
reviewed like any other code, and every collaborator who clones the repo gets
the same Claude behavior.

There is a parallel user-level directory at `~/.claude/` with the same component
types. Project files win over user files, so personal defaults live in the home
directory, and team conventions live in the repo.

## Directory layout

| Path                          | Purpose                                         | Committed      |
|-------------------------------|-------------------------------------------------|----------------|
| `.claude/settings.json`       | Permissions, hooks, env vars, model config      | Yes            |
| `.claude/settings.local.json` | Personal overrides of project settings          | No, gitignored |
| `.claude/CLAUDE.md`           | Project instructions (or `./CLAUDE.md` at root) | Yes            |
| `CLAUDE.local.md`             | Personal project instructions                   | No, gitignored |
| `.claude/rules/`              | Topic-scoped instructions, optional path globs  | Yes            |
| `.claude/skills/`             | Invocable workflows with supporting files       | Yes            |
| `.claude/commands/`           | Single-file slash commands (legacy form)        | Yes            |
| `.claude/agents/`             | Subagent definitions                            | Yes            |
| `.claude/workflows/`          | Saved multi-agent workflow scripts              | Yes            |
| `.claude/output-styles/`      | Custom system-prompt sections                   | Yes            |
| `.claude/agent-memory/`       | Persistent memory for subagents                 | Yes            |

Note that MCP server configuration (`.mcp.json`) lives at the project root, not
inside `.claude/`.

## Instructions: CLAUDE.md and the memory hierarchy

`CLAUDE.md` is the always-loaded instruction file. At session start Claude Code
walks a hierarchy and concatenates every file it finds, the broadest scope
first:

1. Managed policy file (organization-wide, cannot be excluded).
2. User: `~/.claude/CLAUDE.md`.
3. Project ancestors, root down to the working directory: `./CLAUDE.md` or
   `./.claude/CLAUDE.md` (both locations work identically).
4. Local: `./CLAUDE.local.md` (gitignored, personal).
5. Subdirectory `CLAUDE.md` files load on demand, only when Claude reads files
   in that subdirectory.

Files are concatenated, not merged; later (more specific) files can refine
earlier ones. A `@path/to/file` line inside CLAUDE.md imports another file at
load time, up to four hops deep. The practical guidance from the docs is to keep
each file under roughly 200 lines, since shorter instruction files are followed
more reliably.

## Rules: `.claude/rules/*.md`

Rules are the newest instruction mechanism and the one this repository already
uses. Each rule is a Markdown file with optional YAML frontmatter:

```yaml
---
paths:
  - "docs/**/*.md"
---
```

A rule without `paths:` loads at session start, exactly like CLAUDE.md. A rule
with `paths:` loads conditionally: it is injected into context when Claude reads
a file matching one of the globs. This keeps prose-style guidance out of context
during unrelated work and makes rules the right home for topic-scoped
conventions (API design rules for `src/api/**`, test conventions for
`**/*.test.ts`, docs style for `docs/**/*.md`).

Rules support brace expansion in globs (`**/*.{ts,tsx}`), nested subdirectories
under `rules/`, and symlinks to rule directories shared across repositories.
`paths` is the only supported frontmatter field.

Two properties are worth keeping in mind:

- Rules are guidance, not enforcement. The harness guarantees injection of the
  rule text, but compliance is model judgment. Anything that must never slip
  through (a forbidden character, a lint failure) belongs in a hook or a
  pre-commit script instead.
- The trigger is file access. Reading a matching file is what loads the rule, so
  we do not need to name the rule in the prompt.

## Skills and commands: `.claude/skills/`, `.claude/commands/`

Skills are invocable workflows. Each lives in its own directory with a required
`SKILL.md` entrypoint plus any supporting files (templates, scripts, examples):

```text
.claude/skills/my-skill/
  SKILL.md
  scripts/check.sh
  template.md
```

The frontmatter controls how and when a skill runs. The most useful fields:

| Field                      | Purpose                                        |
|----------------------------|------------------------------------------------|
| `description`              | Tells Claude when to auto-invoke the skill     |
| `argument-hint`            | Syntax hint shown in the `/` menu              |
| `disable-model-invocation` | `true` makes the skill user-only               |
| `user-invocable`           | `false` hides it from the `/` menu             |
| `allowed-tools`            | Tool allowlist while the skill runs            |
| `model`, `effort`          | Model and reasoning-effort overrides           |
| `context: fork`            | Runs the skill in a subagent instead of inline |

A skill is invoked by the user (`/skill-name args`) or auto-invoked by the model
when the task matches the `description`. The body supports
`$ARGUMENTS` and positional `$1`, `$2` substitution, `!`-prefixed lines that
execute shell commands and inject their output, and `@file`
references. Skill content loads only when invoked, so unused skills cost nothing
in context.

The older `.claude/commands/*.md` mechanism (one Markdown file per slash
command) still works and uses the same invocation syntax, but commands and
skills have been merged into one system and skills are the preferred form for
new work, because they can bundle supporting files.

## Subagents: `.claude/agents/*.md`

An agent file defines a specialized subagent Claude can delegate to: a name, a
description (which drives delegation), an optional tool allowlist, and optional
model, effort, permission-mode, and memory settings. Typical uses are a
read-only code-reviewer agent, a test-runner agent restricted to `Bash` and
`Read`, or a docs-writer agent pinned to a cheaper model. Project agents
override user agents of the same name.

## Settings: `.claude/settings.json`

Settings are configuration, not prose. The main sections:

- `permissions`: `allow`, `deny`, and `ask` lists of tool patterns, for example
  `Bash(npm run *)` or `Read(./.env)`. Deny takes precedence, and patterns merge
  across scopes. This is how a repo pre-approves safe commands (fewer prompts)
  and hard-blocks dangerous ones.
- `hooks`: shell commands (or HTTP, MCP, prompt, and agent hooks) attached to
  lifecycle events such as `PreToolUse`, `PostToolUse`,
  `UserPromptSubmit`, `SessionStart`, and `Stop`. A hook that exits with code 2
  blocks the action and feeds its stderr back to the model; this is the
  deterministic-enforcement counterpart to rules. Common uses:
  auto-format after every edit, block edits to generated files, run a linter
  before commit.
- `env`: environment variables for all sessions and subprocesses.
- `model`, `effortLevel`, `statusLine`, and similar harness options.

Precedence, highest to lowest: managed (enterprise) settings, command-line
flags, `.claude/settings.local.json`, `.claude/settings.json`,
`~/.claude/settings.json`.

## How the pieces fit together

A useful way to think about the directory is by binding time and by strength:

| Mechanism       | Loaded                       | Strength                |
|-----------------|------------------------------|-------------------------|
| `CLAUDE.md`     | Always, at session start     | Guidance                |
| Rules (no path) | Always, at session start     | Guidance                |
| Rules (`paths`) | When a matching file is read | Guidance                |
| Skills          | Only when invoked            | Guidance plus procedure |
| Agents          | Only when delegated to       | Guidance plus isolation |
| Permissions     | Always, enforced by harness  | Hard                    |
| Hooks           | On lifecycle events          | Hard (exit 2 blocks)    |

The pattern that falls out: universal context goes in `CLAUDE.md`, scoped
conventions go in path-scoped rules, repeatable procedures go in skills, and
anything that must be guaranteed goes in permissions or hooks.

## Common uses

- Team onboarding: commit `CLAUDE.md` with build, test, and architecture notes
  so every contributor's Claude session starts informed.
- Scoped conventions: path-scoped rules for docs style (this repo), API design,
  test structure, or migration policies.
- Repeatable workflows: skills for release checklists, changelog generation,
  report scaffolding, or style checks with a bundled script.
- Guardrails: permission denies for secrets and destructive commands; PreToolUse
  hooks that block writes to protected paths.
- Automation: PostToolUse hooks that run formatters, SessionStart hooks that
  inject dynamic context (current ticket, branch state).
- Delegation: agents for review, exploration, or long-running verification with
  restricted tools.

## References

- Directory overview: https://code.claude.com/docs/en/claude-directory.md
- Memory and rules:    https://code.claude.com/docs/en/memory.md
- Skills and commands: https://code.claude.com/docs/en/skills.md
- Subagents:           https://code.claude.com/docs/en/sub-agents.md
- Settings:            https://code.claude.com/docs/en/settings.md
- Hooks:               https://code.claude.com/docs/en/hooks.md
