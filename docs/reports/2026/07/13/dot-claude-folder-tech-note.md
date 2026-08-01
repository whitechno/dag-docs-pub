The .claude/ directory: purpose, capabilities, and common uses
==============================================================
July 13, 2026

<!--
A technical review of Claude Code's .claude/ project directory: what it is for,
what can live inside it, how each component behaves, and the common patterns
teams use it for. Verified against the official Claude Code documentation at
https://code.claude.com/docs as of July 2026. Revised August 1, 2026: complete
file inventory for both scopes, worked examples for rules, skills, subagents,
and settings, and a section on the .agents/ convention.
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

### Project scope

These live in the repository and are normally committed, so the whole team
shares them.

| Path                              | Purpose                                         | Committed      |
|-----------------------------------|-------------------------------------------------|----------------|
| `.claude/settings.json`           | Permissions, hooks, env vars, model config      | Yes            |
| `.claude/settings.local.json`     | Personal overrides of project settings          | No, gitignored |
| `.claude/CLAUDE.md`               | Project instructions (or `./CLAUDE.md` at root) | Yes            |
| `CLAUDE.local.md`                 | Personal project instructions                   | No, gitignored |
| `.claude/rules/`                  | Topic-scoped instructions, optional path globs  | Yes            |
| `.claude/skills/`                 | Invocable workflows with supporting files       | Yes            |
| `.claude/commands/`               | Single-file slash commands (legacy form)        | Yes            |
| `.claude/agents/`                 | Subagent definitions                            | Yes            |
| `.claude/workflows/`              | Saved multi-agent workflow scripts (`*.js`)     | Yes            |
| `.claude/output-styles/`          | Custom system-prompt sections                   | Yes            |
| `.claude/agent-memory/`           | Persistent subagent memory, `memory: project`   | Yes            |
| `.claude/agent-memory-local/`     | Persistent subagent memory, `memory: local`     | No, gitignored |
| `.mcp.json`                       | Project MCP servers, at the repo root           | Yes            |
| `.worktreeinclude`                | Gitignored files to copy into new worktrees     | Yes            |
| `.claude-plugin/marketplace.json` | Marketplace manifest, if the repo hosts one     | Yes            |

Three of these are easy to miss. `.claude/agent-memory-local/` is the gitignored
twin of `agent-memory/`, used when a subagent's accumulated notes are
project-specific but not worth sharing. `.worktreeinclude` lists gitignored
files (a `.env`, a local config) that should be copied into every new worktree,
which matters because subagents can run with `isolation: worktree`.
`.claude-plugin/marketplace.json` sits at the repo root, not under `.claude/`,
and turns the repository into a plugin marketplace others can add.

Note that `.mcp.json` and `.claude-plugin/` live at the project root rather than
inside `.claude/`.

### User scope

These live in the home directory and apply to every project on the machine. None
of them are committed.

| Path                             | Purpose                                      |
|----------------------------------|----------------------------------------------|
| `~/.claude/CLAUDE.md`            | Personal instructions for all projects       |
| `~/.claude/settings.json`        | Default settings for all projects            |
| `~/.claude/rules/`               | Personal rules, loaded before project rules  |
| `~/.claude/skills/`              | Personal skills                              |
| `~/.claude/commands/`            | Personal single-file commands                |
| `~/.claude/agents/`              | Personal subagents                           |
| `~/.claude/workflows/`           | Personal workflow scripts                    |
| `~/.claude/output-styles/`       | Personal output styles                       |
| `~/.claude/agent-memory/`        | Subagent memory for `memory: user`           |
| `~/.claude/keybindings.json`     | Custom keyboard shortcuts                    |
| `~/.claude/themes/`              | Custom color themes (`*.json`)               |
| `~/.claude/plugins/`             | Cloned marketplaces and installed plugins    |
| `~/.claude/projects/<p>/memory/` | Auto memory: Claude's own notes, per project |
| `~/.claude.json`                 | App state, auth, UI toggles, personal MCP    |

`keybindings.json`, `themes/`, and `plugins/` have no project-scope equivalent:
they are personal ergonomics rather than repository policy. Conversely,
`.mcp.json` and `.worktreeinclude` have no user-scope equivalent, since personal
MCP servers are recorded in `~/.claude.json` instead.

Beyond the configuration we author, `~/.claude/` also accumulates data Claude
Code writes as it works: session transcripts under `projects/`, prompt history
in `history.jsonl`, pre-edit file snapshots under `file-history/`, plan files,
debug logs, and various caches. These are plaintext and unencrypted, so anything
a tool reads (including a `.env` a command happened to print) lands on disk. The
`cleanupPeriodDays` setting controls how long most of it is kept, and
`claude project purge` deletes the state held for one project.

### Machine and organization scope

A managed policy file deployed by IT sits outside both directories and cannot be
overridden: `/Library/Application Support/ClaudeCode/` on macOS,
`/etc/claude-code/` on Linux and WSL, and `C:\Program Files\ClaudeCode\` on
Windows. It holds `managed-settings.json` and optionally a `CLAUDE.md`.

### Everything else is ignored

Claude Code only looks for the names above. Any other file or directory under
`.claude/` is inert, which makes the directory a convenient home for supporting
material. Two conventions are common and worth adopting: `.claude/scripts/` for
scripts a skill or hook shells out to (this repository uses it for
`check-docs-style.sh`), and `.claude/hooks/` for hook programs referenced as
`${CLAUDE_PROJECT_DIR}/.claude/hooks/name.sh`. Neither is a special path; they
are ordinary directories that keep the tooling next to the configuration that
invokes it.

One genuine exception: a directory under `.claude/skills/` that contains a
`.claude-plugin/plugin.json` manifest is loaded as a plugin rather than a plain
skill, discovered in place with no install step.

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

Two details help in practice. Block-level HTML comments are stripped before the
file enters context, so we can leave maintainer notes (like the one at the top
of this report) without spending tokens on them. And in a monorepo,
`claudeMdExcludes` in settings skips ancestor CLAUDE.md files from other teams
by glob.

Alongside the files we write, Claude Code keeps an auto memory directory at
`~/.claude/projects/<project>/memory/`, where Claude records what it learns
across sessions. The `MEMORY.md` index there is loaded every session (first 200
lines or 25KB, whichever comes first) and topic files are read on demand. Auto
memory is machine-local and never committed, which is the cleanest way to think
about the split: `CLAUDE.md` is what we tell Claude, auto memory is what Claude
tells itself.

## Rules: `.claude/rules/*.md`

Rules are the newest instruction mechanism and the one this repository already
uses. Each rule is a Markdown file with optional YAML frontmatter. A rule
without `paths:` loads at session start, exactly like CLAUDE.md. A rule with
`paths:` loads conditionally: it is injected into context when Claude reads a
file matching one of the globs. This keeps prose-style guidance out of context
during unrelated work and makes rules the right home for topic-scoped
conventions. `paths` is the only supported frontmatter field.

A path-scoped rule for backend code, `.claude/rules/api-design.md`:

```
---
paths:
  - "src/api/**/*.ts"
---

# API conventions

- Every handler validates its input with a zod schema before use.
- Errors use the shared `ApiError` envelope, never a bare `throw`.
- New endpoints get an OpenAPI comment block above the handler.
```

A rule that spans several extensions and directories using brace expansion,
`.claude/rules/testing.md`:

```
---
paths:
  - "src/**/*.{test,spec}.{ts,tsx}"
  - "tests/**/*.py"
---

# Test conventions

- One behavior per test; the test name states the behavior, not the method.
- No network or filesystem access; use the fixtures in `tests/fixtures/`.
- Run `npm test -- --runInBand` before proposing a change to shared setup.
```

An unconditional rule with no frontmatter at all, `.claude/rules/commits.md`,
which loads every session because it applies to any work in the repo:

```
# Commit conventions

- Subject line in the imperative mood, 72 characters or fewer.
- One logical change per commit; never mix a refactor with a fix.
- Reference the issue as `Refs #123` in the body, not the subject.
```

The docs-style rule in this repository is the same shape as the first example,
scoped to `docs/**/*.md`.

Rules support nested subdirectories under `rules/` (all `.md` files are
discovered recursively) and symlinks to rule files or directories shared across
repositories. Two properties are worth keeping in mind:

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

Claude Code skills follow the Agent Skills open standard, with Claude-specific
extensions for invocation control and subagent execution. The frontmatter
controls how and when a skill runs. The most useful fields:

| Field                      | Purpose                                          |
|----------------------------|--------------------------------------------------|
| `description`              | Tells Claude when to auto-invoke the skill       |
| `when_to_use`              | Extra trigger phrases, appended to `description` |
| `argument-hint`            | Syntax hint shown in the `/` menu                |
| `disable-model-invocation` | `true` makes the skill user-only                 |
| `user-invocable`           | `false` hides it from the `/` menu               |
| `allowed-tools`            | Tools pre-approved while the skill runs          |
| `disallowed-tools`         | Tools removed from the pool while it runs        |
| `model`, `effort`          | Model and reasoning-effort overrides             |
| `paths`                    | Globs limiting when the skill auto-activates     |
| `context: fork`            | Runs the skill in a subagent instead of inline   |
| `agent`, `background`      | Which subagent, and whether to wait for it       |

A user-only skill that takes an argument,
`.claude/skills/new-report/SKILL.md`:

```
---
description: Scaffold a dated report under docs/reports/YYYY/MM/DD/
argument-hint: [report-slug]
disable-model-invocation: true
allowed-tools: Bash(mkdir:*), Write
---

Create `docs/reports/$(date +%Y/%m/%d)/$1.md` from `@template.md`,
filling in today's date and a title derived from `$1`. Report the path.
```

An auto-invoked skill that bundles a script and pre-approves the tools it needs,
`.claude/skills/docs-style-check/SKILL.md`:

```
---
description: >
  Report docs-style violations in docs/**/*.md against
  .claude/rules/docs-style.md. Reports only, never edits files.
when_to_use: check docs style, lint the docs, docs style report
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/../../scripts/check-docs-style.sh:*), Read
---

Run the mechanical check, then review the judgment rules by hand:

!`${CLAUDE_PROJECT_DIR}/.claude/scripts/check-docs-style.sh`

Read `@../../rules/docs-style.md` and report spelling, voice, and formatting
violations the script cannot see. Do not edit any file.
```

A skill that runs in a subagent so its output never enters the main context,
`.claude/skills/audit-deps/SKILL.md`:

```
---
description: Audit dependencies for known advisories and stale majors
context: fork
agent: general-purpose
background: false
model: haiku
effort: low
---

Run the audit for this project's package manager, group findings by severity,
and return a table of package, current version, fixed version, and advisory ID.
Return the table only, no prose.
```

The body supports `$ARGUMENTS` and positional `$1`, `$2` substitution, named
arguments declared in an `arguments` field, `!`-prefixed lines that execute
shell commands and inject their output, `@file` references, and variables such
as `${CLAUDE_SKILL_DIR}` and `${CLAUDE_PROJECT_DIR}`. Skill content loads only
when invoked, so unused skills cost nothing in context; only the `description`
sits in the listing.

The older `.claude/commands/*.md` mechanism (one Markdown file per slash
command) still works and uses the same invocation syntax, but commands and
skills have been merged into one system and skills are the preferred form for
new work, because they can bundle supporting files.

## Subagents: `.claude/agents/*.md`

An agent file defines a specialized subagent Claude can delegate to. Only `name`
and `description` are required; the body becomes the subagent's entire system
prompt. The fields we reach for most often:

| Field             | Purpose                                             |
|-------------------|-----------------------------------------------------|
| `name`            | Lowercase-hyphen identifier, also the `agent_type`  |
| `description`     | When Claude should delegate to this subagent        |
| `tools`           | Tool allowlist; inherits everything if omitted      |
| `disallowedTools` | Tools removed from the inherited or listed set      |
| `model`, `effort` | Cost and depth controls per agent                   |
| `permissionMode`  | `plan`, `acceptEdits`, `dontAsk`, and so on         |
| `skills`          | Skills preloaded into the subagent's context        |
| `memory`          | `user`, `project`, or `local` persistent memory     |
| `isolation`       | `worktree` gives the agent its own copy of the repo |
| `maxTurns`        | Hard cap on agentic turns                           |
| `color`           | Display color in the task list and transcript       |

A read-only reviewer, `.claude/agents/code-reviewer.md`:

```
---
name: code-reviewer
description: Reviews a diff for correctness, security, and convention drift
tools: Read, Glob, Grep, Bash(git diff:*), Bash(git log:*)
model: opus
color: purple
---

You review code. Read the diff, then the surrounding files needed to judge it.
Report only defects you can point at with a file and line, ordered by severity.
Do not restate what the change does and do not edit files.
```

A cheap test runner that cannot touch the working tree,
`.claude/agents/test-runner.md`:

```
---
name: test-runner
description: Runs the test suite and summarizes failures
tools: Bash, Read
disallowedTools: Write, Edit
model: haiku
effort: low
maxTurns: 12
---

Run the project's test command. If it fails, read the failing test and the code
under test, and return the failing test name, the assertion, and your
one-sentence diagnosis. Return nothing else.
```

A migration agent that works on an isolated checkout and remembers what it
learned, `.claude/agents/migrator.md`:

```
---
name: migrator
description: Applies a mechanical codemod across many files
permissionMode: acceptEdits
isolation: worktree
memory: project
skills: [codemod-conventions]
---

You apply one mechanical transformation at a time across the repository. Change
nothing that the transformation does not require. When you discover a file or
pattern that needs a hand-written exception, record it in your memory so the
next run skips it.
```

Project agents override user agents of the same name, and `memory: project`
writes to `.claude/agent-memory/<name>/` so the agent's accumulated knowledge is
reviewable in a pull request like anything else.

## Settings: `.claude/settings.json`

Settings are configuration, not prose. The main sections:

- `permissions`: `allow`, `deny`, and `ask` lists of tool patterns, for example
  `Bash(npm run *)` or `Read(./.env)`. Deny takes precedence, and patterns merge
  across scopes. This is how a repo pre-approves safe commands (fewer prompts)
  and hard-blocks dangerous ones.
- `hooks`: shell commands (or HTTP, MCP, prompt, and agent hooks) attached to
  lifecycle events. The set is large; the ones we use most are `PreToolUse`,
  `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, and `Stop`,
  with `SubagentStart` and `SubagentStop` for delegated work.
- `env`: environment variables for all sessions and subprocesses.
- `model`, `effortLevel`, `statusLine`, `cleanupPeriodDays`, `claudeMdExcludes`,
  and roughly a hundred other harness options.

Permissions, the most common starting point:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ],
    "ask": [
      "Bash(git push *)"
    ]
  }
}
```

Hooks are nested three deep: event, then matcher group, then handlers. This
example formats after every edit and blocks writes to generated files:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write ."
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/protect-generated.sh"
          }
        ]
      }
    ]
  }
}
```

Environment and harness defaults, the third common block:

```json
{
  "model": "opus",
  "effortLevel": "high",
  "cleanupPeriodDays": 7,
  "env": {
    "NODE_ENV": "development",
    "PYTHONHASHSEED": "0"
  },
  "claudeMdExcludes": [
    "**/monorepo/other-team/**"
  ]
}
```

Precedence, highest to lowest: managed (enterprise) settings, command-line
flags, `.claude/settings.local.json`, `.claude/settings.json`,
`~/.claude/settings.json`.

## How the pieces fit together

A useful way to think about the directory is by binding time and by strength:

| Mechanism       | Loaded                       | Strength                 |
|-----------------|------------------------------|--------------------------|
| `CLAUDE.md`     | Always, at session start     | Guidance                 |
| Rules (no path) | Always, at session start     | Guidance                 |
| Rules (`paths`) | When a matching file is read | Guidance                 |
| Auto memory     | `MEMORY.md` at session start | Guidance                 |
| Skills          | Only when invoked            | Guidance plus procedure  |
| Agents          | Only when delegated to       | Guidance plus isolation  |
| Permissions     | Always, enforced by harness  | Hard                     |
| Hooks           | On lifecycle events          | Hard on blockable events |

The one nuance in that last row: exit code 2 blocks the action only on events
that are blockable, such as `PreToolUse`, `UserPromptSubmit`, `Stop`, and
`PreCompact`, where stderr is fed back to the model as an error. On
`PostToolUse` and the other after-the-fact events, exit 2 surfaces the message
but the action has already happened. A guard that must actually prevent
something therefore belongs in `PreToolUse` or in a permission deny rule, not in
`PostToolUse`.

The pattern that falls out: universal context goes in `CLAUDE.md`, scoped
conventions go in path-scoped rules, repeatable procedures go in skills, and
anything that must be guaranteed goes in permissions or `PreToolUse` hooks.

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

## The `.agents/` directory and AGENTS.md

`AGENTS.md` is the cross-vendor counterpart to `CLAUDE.md`: an open format,
originally driven by OpenAI with Google, Cursor, and Factory, donated to the
Linux Foundation's Agentic AI Foundation in December 2025 and supported by
twenty-odd tools. It is a single Markdown file at the repository root, with
nested files in subprojects and nearest-file-wins resolution.

Claude Code does not read `AGENTS.md`. The supported interop is to point
`CLAUDE.md` at it, either by import:

```
@AGENTS.md

## Claude Code

Use plan mode for changes under `src/billing/`.
```
or by symlink:
```bash
ln -s AGENTS.md CLAUDE.md
```

The import form is preferable when we want Claude-specific additions, and it is
the only option on Windows without Developer Mode. Running `/init` with
`CLAUDE_CODE_NEW_INIT=1` also reads `AGENTS.md`, along with Cursor, Copilot,
Windsurf, Devin, and Cline rule files, and folds the relevant parts into a
generated `CLAUDE.md`.

A `.agents/` directory is a different matter, and the honest answer is that it
is not yet a standard. The AGENTS.md specification itself defines no such
directory. What exists are two community proposals that extend the AGENTS.md
idea from one file to a directory tree:

- `bgreenwell/dotagents`, explicitly labeled Draft 0.1.0, proposing
  `.agents/personas/`, `.agents/skills/`, `.agents/settings/`, and optional
  `.agents/memory/` and `.agents/logs/`.
- `agentsstandard.com` (maintained by an individual, nbiish), proposing
  `.agents/AGENTS.md`, `.agents/mcp-settings.json`, and `.agents/skills/`
  at both repository and home-directory scope.

Neither has organizational backing, and no tool is documented as reading
`.agents/` natively today. Both are best read as an observation that agent
configuration has outgrown a single file, which is the same observation
`.claude/rules/` and `.claude/skills/` respond to.

So: is `.agents/` compatible with `.claude/`? In the weak sense, yes. Claude
Code ignores every path it does not recognize, so a `.agents/` directory sits in
a repository without conflict, and a project can carry both. In the strong
sense, no: nothing in `.agents/` is loaded, and its contents have no effect
until we bridge them explicitly.

Bridging is cheap where the formats already agree. `.agents/skills/` in both
proposals uses `SKILL.md` directories, which is the same Agent Skills standard
Claude Code implements, and both `.claude/skills/` and `.claude/rules/` follow
symlinks. So a repository that wants one source of truth can do this:

```bash
ln -s ../../AGENTS.md .claude/rules/agents.md
ln -s ../../.agents/skills/validate-schema .claude/skills/validate-schema
```

The first line makes the shared instructions load as an unconditional rule (an
alternative to the `@AGENTS.md` import, useful when `CLAUDE.md` is already
crowded). The second exposes a shared skill under its Claude Code name. Personas
map onto `.claude/agents/*.md` only by hand, since the frontmatter schemas
differ, and `.agents/settings/` has no vendor-neutral format to translate from
yet.

Our recommendation for now: keep `AGENTS.md` as the portable, human-readable
contract if the repository serves several agent tools, keep `.claude/` as the
place where Claude Code's enforceable configuration lives, and link rather than
duplicate wherever the formats coincide. Adopting `.agents/` as a layout is a
reasonable bet on where things are heading, but it should be treated as
organization for our own benefit, not as configuration any tool will honor.

## References

- Directory overview: https://code.claude.com/docs/en/claude-directory.md
- Memory and rules:    https://code.claude.com/docs/en/memory.md
- Skills and commands: https://code.claude.com/docs/en/skills.md
- Subagents:           https://code.claude.com/docs/en/sub-agents.md
- Settings:            https://code.claude.com/docs/en/settings.md
- Hooks:               https://code.claude.com/docs/en/hooks.md
- Plugins reference:   https://code.claude.com/docs/en/plugins-reference.md
- AGENTS.md format:    https://agents.md/
- Agent Skills:        https://agentskills.io
- dotagents proposal:  https://github.com/bgreenwell/dotagents
- Agents Standard:     https://agentsstandard.com/
