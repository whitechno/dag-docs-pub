Instruction files and config directories across AI coding tools
===============================================================
July 12, 2026 (Updated August 9, 2026)

<!--
A survey of the CLAUDE.md equivalents and .claude/ equivalents in twenty-odd
agentic coding tools: Codex, Antigravity CLI, Muse Code, Grok Build, Kimi Code,
Cursor, Copilot, Devin, Junie, Cline, Perplexity, OpenClaw, Hermes, and others.
Each entry is verified against that tool's own documentation. Tool facts are
current as of August 2026; this part of the landscape changes on a scale of
months.
-->

Nearly every agentic coding tool has converged on the same two surfaces: a
Markdown instruction file that is injected into the prompt, and a dot-directory
holding what the file cannot express (path-scoped rules, invocable procedures,
subagents, hooks, MCP servers, permissions). What has changed over the past year
is that the file has largely standardized on
`AGENTS.md`, while the directories have not standardized at all. Anyone porting
a `.claude/` setup should expect the instructions to travel and the machinery to
stay behind.

Claude Code's own side of this comparison, meaning what `.claude/` holds and how
each component behaves, is covered in
`docs/reports/2026/07/13/dot-claude-folder-tech-note.md`. Here we take it as the
reference point and describe everything else relative to it.

The table lists only tools that are current as of August 2026. Two names that
would have appeared a year ago have been retired and are covered further down
under their successors: Gemini CLI, retired in favor of Antigravity CLI, and
Windsurf, rebranded as Devin Desktop with its Cascade agent replaced by Devin
Local. Three entries came in with the August revision: Meta's Muse Code and
xAI's Grok Build, both released after the July draft, and Moonshot AI's Kimi
Code, which was not new but was missing. The details that are easy to get wrong
follow the table.

| Tool               | Instruction file(s)                            | Project directory              | User directory            |
|--------------------|------------------------------------------------|--------------------------------|---------------------------|
| Claude Code        | `CLAUDE.md`                                    | `.claude/`                     | `~/.claude/`              |
| OpenAI Codex       | `AGENTS.md`                                    | `.codex/`                      | `~/.codex/`               |
| Antigravity CLI    | `AGENTS.md`                                    | `.agents/`                     | `~/.gemini/`              |
| Meta Muse Code     | `AGENTS.md`, `CLAUDE.md`                       | `.agents/`, `.muse/`           | `~/.config/muse/`         |
| xAI Grok Build     | `AGENTS.md`, `CLAUDE.md`, `.grok/rules/*.md`   | `.grok/`                       | `~/.grok/`                |
| Moonshot Kimi Code | `AGENTS.md`                                    | `.kimi-code/`, `.agents/`      | `~/.kimi-code/`           |
| Cursor             | `AGENTS.md`, `.cursor/rules/*.mdc`             | `.cursor/`                     | `~/.cursor/`              |
| GitHub Copilot     | `AGENTS.md`, `.github/copilot-instructions.md` | `.github/instructions/`        | `~/.copilot/`             |
| Devin Desktop      | `AGENTS.md`, `.windsurfrules`                  | `.devin/rules/`, `.windsurf/`  | `~/.codeium/windsurf/`    |
| Devin for Terminal | `AGENTS.md`                                    | `.devin/`                      | `~/.config/devin/`        |
| JetBrains Junie    | `AGENTS.md`, `.junie/guidelines.md`            | `.junie/`                      | `~/.junie/`               |
| Cline              | `AGENTS.md`, `.clinerules/`                    | `.clinerules/`, `memory-bank/` | `~/Documents/Cline/Rules` |
| Perplexity         | none (environment variables)                   | none                           | none                      |
| OpenClaw           | `AGENTS.md`, `SOUL.md` (workspace)             | `~/.openclaw/workspace/`       | `~/.openclaw/`            |
| Hermes             | `.hermes.md`, `AGENTS.md`, `CLAUDE.md`         | none                           | `~/.hermes/`              |

## OpenAI Codex

Codex resolves instructions in two stages. Globally it loads the first non-empty
of `~/.codex/AGENTS.override.md` and `~/.codex/AGENTS.md`. Per project, it walks
from the Git root down to the working directory and takes at most one file per
level: `AGENTS.override.md`, then `AGENTS.md`, then any name listed in
`project_doc_fallback_filenames`, which is how a repository that only has
`CLAUDE.md` or `CONTRIBUTING.md` still gets read. The pieces are concatenated
root-first and joined with blank lines, so files nearer the working directory
win by appearing later, up to `project_doc_max_bytes`
(32 KiB by default).

The directory is `~/.codex/`, relocatable with `CODEX_HOME`, holding
`config.toml`, prompts, skills, and local state; Codex also walks up looking for
`.codex/` project layers. Skills use the same `SKILL.md` convention as Claude
Code and can be disabled without deleting them through
`[[skills.config]]` entries in `~/.codex/config.toml`.

## Antigravity CLI

Google's Antigravity CLI (binary `agy`) is the replacement for Gemini CLI and
the tool that has actually adopted `.agents/` as its project directory. It is
the closest structural match to `.claude/` on this list:

| Antigravity                                            | Claude Code equivalent    |
|--------------------------------------------------------|---------------------------|
| `.agents/rules/*.md`                                   | `.claude/rules/`          |
| `.agents/skills/<name>/SKILL.md`                       | `.claude/skills/`         |
| `.agents/agents/<name>.md` or `<name>/agent.md`        | `.claude/agents/`         |
| `.agents/workflows/<name>.md`, invoked as `/<name>`    | `.claude/commands/`       |
| `~/.gemini/antigravity-cli/plugins/<name>/plugin.json` | plugins                   |
| `~/.gemini/antigravity-cli/settings.json`              | `~/.claude/settings.json` |

Rules carry an activation mode rather than a plain glob: always on, model
decision (the description is shown and the body is fetched on demand), glob, or
manual via `@rule-name`. Rule and workflow files are capped at 12,000 characters
each. The singular `.agent/` spelling is still honored for backward
compatibility, and much of the published documentation still uses it, so both
should be expected in the wild. A plugin bundle is a directory with
`plugin.json` plus optional `mcp_config.json`, `hooks.json`, and `skills/`,
`agents/`, and `rules/` subdirectories, which is very close to Claude Code's
plugin shape.

The user directory is worth stating precisely because it is not named after the
product. Antigravity keeps its user scope inside Gemini CLI's old home,
`~/.gemini/`, and splits it in two: `~/.gemini/config/` holds what is shared
across Antigravity products (`skills/`, `agents/`, `mcp_config.json`), while
`~/.gemini/antigravity-cli/` holds what belongs to the CLI alone
(`settings.json`, `keybindings.json`, `plugins/`). Global rules remain
`~/.gemini/GEMINI.md`. There is no `~/.antigravity/` directory. Workspace MCP
servers go in `.agents/mcp_config.json`, and a project carried over from Gemini
CLI must have its `.gemini/skills/` folder renamed to `.agents/skills/`
before the skills are recognized.

## Gemini CLI (retired)

Gemini CLI is included here only because so much existing material references
it. Google announced its transition to Antigravity CLI in May 2026, and on June
18, 2026 Gemini CLI and the Gemini Code Assist IDE extensions stopped serving
requests for Google AI Pro and Ultra subscribers and for free individual Gemini
Code Assist users. Organizations on a Gemini Code Assist Standard or Enterprise
license keep access, as do users going through paid Gemini and Gemini Enterprise
Agent Platform API keys, so it survives inside enterprises rather than on
individual machines.

Its layout was `GEMINI.md` files loaded hierarchically, with settings in
`.gemini/settings.json` in the project overriding `~/.gemini/settings.json`, and
extensions declared by a `gemini-extension.json` naming `mcpServers`,
`contextFileName`, and `excludeTools`. Two pieces of it survive in Antigravity:
the `~/.gemini/` home directory, and `GEMINI.md` itself, which Antigravity still
parses both in the working directory and globally at
`~/.gemini/GEMINI.md`. The settings file did not survive: MCP servers moved out
of `settings.json` into a dedicated `mcp_config.json`.

## Meta Muse Code

Meta Superintelligence Labs released Muse Code (binary `muse`) in beta on August
5, 2026 for macOS and Linux, running on `muse-spark-1.2`. It is the newest entry
here and the most deliberate about not inventing a file of its own: there is no
`MUSE.md`. Muse Code reads `AGENTS.md` and falls back to
`CLAUDE.md`, walking up to the nearest `.git` boundary and taking one
instruction file per directory level, with deeper files winning and project
rules overriding user rules.

What is unusual is that the project surface is split across two directories.
Skills and memory go under `.agents/`, the same directory Antigravity CLI and
OpenHands settled on, while hooks go in `.muse/`:

| Muse Code                                          | Claude Code equivalent             |
|----------------------------------------------------|------------------------------------|
| `.agents/skills/<skill-id>/SKILL.md`               | `.claude/skills/`                  |
| `.agents/memory/MEMORY.md` plus topic files        | auto memory plus its `MEMORY.md`   |
| `.muse/hooks.json`                                 | `hooks` in `.claude/settings.json` |
| `~/.config/muse/settings.json`                     | `~/.claude/settings.json`          |
| `$XDG_CONFIG_HOME/muse/skills`, `~/.agents/skills` | `~/.claude/skills/`                |

Project memory is an index file plus topic notes, capped at 48 files indexed at
session start, which is the same shape as Claude Code's auto memory rather than
Cline's fixed six-file memory bank. The trust model has an asymmetry worth
knowing: project instruction files load only after workspace trust is granted,
but project memory loads even in an untrusted checkout, so Meta's own
documentation flags it as a prompt-injection surface. Skills are read from
`.claude/skills` and `.codex/skills` as well as the native path, and
`muse skills import --from claude` (or `--from codex`) converts them.

The settings file must carry `"schema_version": 1` or startup fails. It holds
model defaults, UI preferences, tool configuration, hooks at user scope, and an
`mcp_servers` block taking `stdio` or `streamable_http` transports. Each server
takes a `mode` that defaults to `required` and can be set to `optional`, so a
dead server degrades instead of aborting the session. Hook events are close to
Claude Code's list, adding `PreLLMCall`, `PostLLMCall`, `SubagentStart`, and
`SubagentStop`, with `muse hooks trust` for explicit trust and
`muse hooks run <key> --fixture ./fixture.json` for testing one in isolation.
Subagents can be given one git worktree each with
`--subagent-worktree-isolation`, and headless runs are `muse exec`, with
`--yolo` disabling approvals and the sandbox together.

## xAI Grok Build

xAI shipped Grok Build (binary `grok`) and open-sourced the harness, a Rust TUI
and tool layer, at `xai-org/grok-build` on July 15, 2026. It has the widest
compatibility net of anything on this list. Within each directory it reads
`AGENTS.md`, `Agents.md`, `AGENT.md`, `CLAUDE.md`, `Claude.md`, and
`CLAUDE.local.md`, plus every `*.md` under `.grok/rules/`, with `.claude/rules/`
and `.cursor/rules/` honored for compatibility. Discovery starts at `~/.grok/`
and walks down to the working directory, deeper files overriding shallower ones,
so a monorepo can carry different conventions per package. Files load in full
with no size cap, which makes Grok Build the exception to the 12,000-character
ceilings elsewhere in this note. `.gitignore` is respected, which is what keeps
a gitignored `CLAUDE.local.md` personal. For a single run, `--rules` appends
text to the system prompt and `--system-prompt-override` replaces it entirely.

Configuration is TOML rather than JSON, and `.grok/config.toml` is discovered at
every directory level, not just the repository root. The project directory holds
`skills/`, `plugins/`, `hooks/` (project hooks require an explicit
`/hooks-trust`), and `workflows/`. The user directory `~/.grok/` holds
`config.toml`, `auth.json` for OAuth and session credentials, `skills/`,
`plugins/` with marketplace installs under `plugins/marketplaces/` and a
`known_marketplaces.json`, `hooks/` (searched along `~/.grok/hooks-paths`),
`agents/`, `workflows/`, `sessions/`, `memory/`, and the managed `bin/`,
`downloads/`, and `completions/`. MCP servers are an `[mcp_servers]` table in
`config.toml`, taking stdio or HTTP transports with timeouts and environment
variables, and marketplaces are `[[marketplace.sources]]` entries. Beyond its
own paths it reads user-level `~/.agents/skills/` and `~/.agents/commands/`, and
Claude Code's marketplaces, plugins, skills, MCP servers, agents, hooks, and
`.claude/settings.json`.

Two pieces have no counterpart elsewhere. Workflows are `.rhai` scripts, in the
embedded Rust scripting language Rhai, stored at `.grok/workflows/<name>.rhai`
or `~/.grok/workflows/<name>.rhai`, so orchestration over subagents is written
as code rather than as Markdown prose; the feature is switched off with
`[workflows] enabled = false`. And `grok inspect` prints everything the harness
discovered in the current directory, meaning config sources, instruction files,
skills, plugins, hooks, and MCP servers, each with its path and token count,
which is the most direct answer any tool here gives to the question of what is
actually in the prompt. Permission modes are toggled with `/plan`, `/auto`, and
`/always-approve`, or by cycling through them with Shift+Tab.

## Moonshot Kimi Code

Moonshot AI shipped Kimi Code (binary `kimi`) on June 6, 2026, an MIT-licensed
TypeScript rewrite of its own Python `kimi-cli`, running on Kimi K3. It predates
this note and was simply missed in the July draft. It belongs here because it is
the strictest reading of the `AGENTS.md` convention on this list: there is no
`KIMI.md`, and unlike Muse Code and Grok Build there is no `CLAUDE.md` fallback
either. The only instruction filename it reads is `AGENTS.md`, at `AGENTS.md` or
`.kimi-code/AGENTS.md` in the project and at `$KIMI_CODE_HOME/AGENTS.md`
(default `~/.kimi-code/AGENTS.md`) or `~/.agents/AGENTS.md` at user scope. The
rest of the layout repeats that pairing of a branded directory with the generic
`.agents/` one, with project scope winning over user scope:

| Kimi Code                                 | Claude Code equivalent             |
|-------------------------------------------|------------------------------------|
| `.kimi-code/skills/`, `.agents/skills/`   | `.claude/skills/`                  |
| `.kimi-code/agents/`, `.agents/agents/`   | `.claude/agents/`                  |
| `.kimi-code/mcp.json`                     | `.mcp.json`                        |
| `.kimi-code/local.toml`                   | `.claude/settings.local.json`      |
| `[[hooks]]` in `~/.kimi-code/config.toml` | `hooks` in `.claude/settings.json` |
| `~/.kimi-code/config.toml`                | `~/.claude/settings.json`          |

Two ideas here have no counterpart in `.claude/`. Workspace instructions are not
prepended to the prompt, they are interpolated: an agent definition is a
template, and `${agents_md}` marks the place where the `AGENTS.md` content is
substituted, so an agent can position that content or leave it out entirely.
Above that sits `$KIMI_CODE_HOME/SYSTEM.md`, which replaces the built-in system
prompt outright on every launch. That is closest to Claude Code's output styles,
but total rather than partial.

Configuration is TOML and deliberately lopsided. `~/.kimi-code/config.toml`
holds agent and runtime settings, `~/.kimi-code/tui.toml` holds terminal
preferences, and the project gets only `.kimi-code/local.toml` for workspace
settings that are not meant to be shared. There is no project `config.toml`, and
since hooks are `[[hooks]]` entries inside the user config, a checkout cannot
define hooks at all. That sidesteps the trust question every other tool here has
to answer, at the cost of any per-repository automation. A hook entry takes
exactly `event`, `matcher`, `command`, and `timeout`; any extra field fails the
whole config load. The event list is longer than most at around twenty, but only
`UserPromptSubmit`, `PreToolUse`, and `Stop` can block.

MCP servers are the familiar `mcpServers` object, in `~/.kimi-code/mcp.json`
merged with a project `.kimi-code/mcp.json` and the project winning per server
name, over stdio, HTTP, or SSE, with OAuth handled by `/mcp-config login` and
tokens kept in `~/.kimi-code/credentials/mcp/`. Skills use the standard
`SKILL.md` format with three frontmatter fields we have not seen elsewhere:
`type`, which is `prompt`, `inline`, or `flow`; `whenToUse`; and
`disableModelInvocation`. Plugins are a `kimi.plugin.json` manifest bundling
skills, agents, commands, MCP servers, hooks, and a `systemPromptPath`, copied
on install into `~/.kimi-code/plugins/managed/<id>/` and tracked in
`installed.json`. The rewrite moved the home directory from `~/.kimi/` to
`~/.kimi-code/`, relocatable with `KIMI_CODE_HOME`; `kimi migrate` copies
config, MCP servers, and session history across and leaves the old tree
untouched, but does not carry OAuth credentials, MCP authorizations, or
`kimi-cli` plugins.

## Cursor

Project rules live in `.cursor/rules/` and must use the `.mdc` extension: a
plain `.md` file placed there is ignored, because the rules system requires
frontmatter. The three frontmatter fields are `description` (used for
model-driven selection), `globs`, and `alwaysApply`, which map onto Claude
Code's `paths:` frontmatter plus the model's own judgment. Nested
`.cursor/rules/` directories in subprojects are supported, as are `AGENTS.md`
at the root and in any subdirectory. The legacy single file is `.cursorrules`.

The rest of the directory is `.cursor/commands/`, `.cursor/hooks.json`, and
`.cursor/mcp.json`, each with a `~/.cursor/` twin; where a server is defined in
both, the project file wins. Cursor hooks are processes speaking JSON over stdio
at fixed points in the agent loop (`beforeShellExecution`,
`beforeMCPExecution`, and others), the same design as Claude Code hooks with
different event names.

## GitHub Copilot

Copilot has the largest number of entry points and is the most Claude-aware of
the group. Repository-wide instructions go in
`.github/copilot-instructions.md`. Path-scoped instructions go in
`.github/instructions/NAME.instructions.md` with an `applyTo:` glob in
frontmatter, and when both a path-scoped file and the repository-wide file
match, both are used. `AGENTS.md` is read from anywhere in the tree with
nearest-file-wins, and `CLAUDE.md` and `GEMINI.md` at the repository root are
accepted as single-file alternatives.

Inside VS Code there is more: prompt files at `.github/prompts/*.prompt.md`
that become slash commands, chat modes in `*.chatmode.md`, MCP servers in
`.vscode/mcp.json`, and user-profile instruction locations including
`~/.copilot/instructions` and `~/.claude/rules`. VS Code will also read
`CLAUDE.md` from the workspace root, from `.claude/CLAUDE.md`, and from
`~/.claude/CLAUDE.md`. The behavior is governed by the settings
`chat.useAgentsMdFile`, `chat.useNestedAgentsMdFiles`, `chat.useClaudeMdFile`,
and `chat.instructionsFilesLocations`. In practice this means a repository with
a well-written `.claude/` needs almost no Copilot-specific files.

## Devin, and Windsurf before it

Windsurf no longer exists as a product name. Cognition acquired Codeium in 2025,
rebranded Windsurf as Devin Desktop on June 2, 2026 through an over-the-air
update, and retired the Cascade agent on July 1, 2026 in favor of Devin Local.
`docs.windsurf.com` now redirects to `docs.devin.ai`. Every path is being
renamed from windsurf to devin with the old names kept as fallbacks, so anyone
reading material written before mid-2026 should treat the two spellings as
interchangeable and prefer the devin one when writing new files.

For Devin Desktop, workspace rules are `.devin/rules/*.md` with
`.windsurf/rules/*.md` as fallback, plus the legacy single-file
`.windsurfrules` at the root, each capped at 12,000 characters. Global rules are
`~/.codeium/windsurf/memories/global_rules.md`, capped at 6,000 characters, in
the same directory that holds the agent's memories; note that this one has kept
both the codeium and windsurf names so far. Workflows are
`.windsurf/workflows/*.md`, invoked as `/name`. Rules use the same four
activation modes as Antigravity, spelled `always_on`,
`model_decision`, `glob`, and `manual`. `AGENTS.md` is honored at any depth:
at the root it behaves as always-on, in a subdirectory it is treated as an
implicit glob over that subtree. There is also a machine-wide tier for
enterprises, at `/Library/Application Support/Devin/rules/*.md`,
`/etc/devin/rules/*.md`, or `C:\ProgramData\Devin\rules\*.md`, which is the
analogue of Claude Code's managed settings.

Devin for Terminal reads `AGENTS.md` at the root, plus `AGENTS.local.md` for
personal gitignored rules, and accepts `AGENT.md`, `.windsurfrules`, and
`CLAUDE.md` as alternatives. Global rules are `~/.config/devin/AGENTS.md` (or
`%APPDATA%\devin\AGENTS.md`) and it will also read `~/.claude/CLAUDE.md`.
Configuration is `.devin/config.json` in the project and
`~/.config/devin/config.json` globally, and its `read_config_from` object
explicitly selects which other tools' formats to honor, naming
`.cursor/rules/*.{md,mdc}`, `.windsurf/rules/*.md`,
`.windsurf/global_rules.md`, and `.claude/`. Skills are
`.devin/skills/<name>/SKILL.md` and `~/.config/devin/skills/<name>/SKILL.md`.
Notably, Devin's own documentation recommends skills over rules because skills
are only injected when relevant, which is the same argument Claude Code makes
for preferring skills over a large `CLAUDE.md`.

## JetBrains Junie

Junie looks for guidelines in order: `.junie/AGENTS.md`, then `AGENTS.md` at the
project root, then the legacy `.junie/guidelines.md` file or
`.junie/guidelines/` folder. Global guidelines are `~/.junie/AGENTS.md`
(`%USERPROFILE%\.junie\AGENTS.md` on Windows). When both scopes exist, Junie
includes both marks, which is which, and deduplicates identical content; project
guidelines win on conflict.

The rest of `.junie/` is `mcp/mcp.json` for MCP servers, with a
`~/.junie/mcp/mcp.json` user-scope twin, `memory/` for accumulated local memory,
and `plans/` for multi-step plans. JetBrains treats `.junie/memory/`
as local development state and recommends gitignoring `**/.junie/memory/`, which
puts it in the same category as `.claude/agent-memory-local/`. This repository
already carries `.junie/memory/` and `.junie/plans/` alongside
`.claude/`. One behavior has no Claude Code counterpart: for projects marked
untrusted, Junie declines to load project configuration, plans, or memory at
all, and redirects any skills or MCP servers added during the session to a
temporary directory outside the repository.

## Cline

Workspace rules are the `.clinerules/` directory at the project root, from which
every `.md` and `.txt` file is loaded; numeric filename prefixes for ordering
are a convention, not a requirement. A single `.clinerules` file is the older
form. Global rules come from `~/Documents/Cline/Rules` (or
`Documents\Cline\Rules` on Windows, with `~/Cline/Rules` also accepted on Linux
and WSL). Cline additionally auto-detects other tools' formats present in the
workspace, specifically `.cursorrules`, `.windsurfrules`, and
`AGENTS.md`, plus `~/.agents/AGENTS.md` globally.

Cline's much-copied memory bank is worth understanding correctly: it is a
convention, not a feature. It is a `memory-bank/` folder of `projectbrief.md`,
`productContext.md`, `activeContext.md`, `systemPatterns.md`,
`techContext.md`, and `progress.md`, held together by a rule instructing Cline
to read all of them at the start of every task. Claude Code's auto memory under
`~/.claude/projects/<project>/memory/` covers the same ground as a built-in,
with an indexed `MEMORY.md` rather than a fixed file set.

## Perplexity

Perplexity is the outlier: it does not ship a repository coding agent, so there
is no instruction file and no configuration directory to compare. What it ships,
as of July 2026, is `pplx`, a single-binary CLI that puts its Search API in the
terminal for whichever agent we are already running. It is configured by
environment rather than by file: `PERPLEXITY_API_KEY` (required for agents and
CI, because `pplx auth login` is TTY-only and hard-rejects non-interactive use)
and `PPLX_OUTPUT_DIR` for saved results, which land at
`{dir}/web/{rand}.json` and `{dir}/fetch/{rand}.json`. Success is exit 0 with
one JSON object on stdout; failure is one JSON error object on stderr.

Perplexity distributes it as an Agent Skill, `skills/pplx-cli/SKILL.md` in
`perplexityai/api-platform-developers`, and that repository doubles as a Claude
Code plugin marketplace (`/plugin marketplace add
perplexityai/api-platform-developers`). So Perplexity's relationship to
`.claude/` is that it fills it rather than competes with it, and the Agent
Skills format is the interface it chose to ship through.

## OpenClaw

OpenClaw is a self-hosted, multi-channel agent gateway (WhatsApp, Telegram,
Discord, Slack), not a repository coding agent, so the equivalence is real but
inverted: the instruction files belong to the agent, not to the project. Each
agent has a workspace, by default `~/.openclaw/workspace` or
`~/.openclaw/workspace-<profile>`, overridable with `OPENCLAW_WORKSPACE_DIR`.
Its Markdown files are injected into the system prompt every turn:

| File                   | Role                                               |
|------------------------|----------------------------------------------------|
| `AGENTS.md`            | Operating instructions and how to use memory       |
| `SOUL.md`              | Persona, tone, boundaries                          |
| `IDENTITY.md`          | The agent's name, vibe, and emoji                  |
| `USER.md`              | Optional: stable preferences and relationships     |
| `MEMORY.md`            | Optional: curated long-term memory                 |
| `BOOT.md`              | Optional: startup checklist run on gateway restart |
| `BOOTSTRAP.md`         | One-time first-run ritual for a new workspace      |
| `memory/YYYY-MM-DD.md` | Daily memory logs                                  |
| `skills/`              | Workspace skills, highest precedence on name clash |
| `canvas/`              | Canvas UI files for node displays                  |

Configuration is separate and sits directly under `~/.openclaw/`:
`openclaw.json` (JSON5: models, channel connections, tool permissions) and
per-agent state in `~/.openclaw/agents/<agentId>/`, including a SQLite session
database and an `agent.md` identity file. The documentation is explicit that
`~/.openclaw/` holds credentials and session data and should not be committed,
while the workspace is the part worth versioning. Skill precedence runs
workspace, then project agent skills, then personal, managed, bundled, and
finally `skills.load.extraDirs`.

Mapped onto our vocabulary: `AGENTS.md` plus `SOUL.md` are the `CLAUDE.md`
equivalent, the workspace directory is the `.claude/` equivalent, and
`~/.openclaw/` is closer to `~/.claude.json` plus accumulated application state.

## Hermes

Nous Research's Hermes Agent keeps everything under `~/.hermes/`, which each
profile can relocate through `HERMES_HOME`:

```
~/.hermes/
  config.yaml     # non-secret settings: model, terminal, compression
  .env            # API keys and secrets, never loaded into the prompt
  auth.json       # OAuth provider credentials
  SOUL.md         # primary agent identity
  memories/       # persistent memory files
  skills/         # agent-created skills
  cron/           # scheduled jobs
  sessions/       # gateway sessions
  logs/           # error and gateway logs
  plugins/        # installed plugin repos
```

`hermes config set` routes values automatically, sending API keys to `.env`
and everything else to `config.yaml`. Precedence is CLI arguments, then
`config.yaml`, then `.env`, then built-in defaults. Two 2026 policy changes
pushed code out of the tree and into `~/.hermes/plugins/`: memory backends
(May) and third-party integrations (June) must now ship as standalone plugin
repositories that users install there.

Project scope is handled not by a directory but by context files scanned in the
working directory, and the list is deliberately promiscuous: `SOUL.md`,
`.hermes.md`, `AGENTS.md`, `CLAUDE.md`, and `.cursorrules`. So `.hermes.md` is
the native `CLAUDE.md` equivalent, but a repository that already has a
`CLAUDE.md` needs no Hermes-specific file at all. There is no project-scoped
`.hermes/` directory: skills, memory, and cron are all agent-scoped, the same
inversion we saw in OpenClaw.

## Others worth knowing

- Amp reads `AGENTS.md` at the root and in subdirectories, including it when
  working in the corresponding area. Its global instruction file is
  `~/.config/AGENTS.md` and its settings are `~/.config/amp/settings.json`. It
  moved from the singular `AGENT.md` to `AGENTS.md` in 2025.
- Zed reads nine instruction files in a fixed precedence order: `.rules`,
  `.cursorrules`, `.windsurfrules`, `.clinerules`,
  `.github/copilot-instructions.md`, `AGENT.md`, `AGENTS.md`, `CLAUDE.md`,
  `GEMINI.md`. Personal instructions live at `~/.config/zed/AGENTS.md`, and
  project instructions override them on conflict. As of Zed v1.4.0 the rules
  library was replaced by Skills, with reusable rules becoming skills and
  default rules becoming personal instructions. Zed can also drive external
  agents such as OpenHands and opencode over ACP.
- opencode reads `AGENTS.md` with configuration in `opencode.json` or
  `~/.config/opencode/opencode.json`.
- OpenHands has adopted the Agent Skills standard and now recommends
  `.agents/skills/`, with `~/.agents/skills/` for user scope and
  `.openhands/skills/` and `.openhands/microagents/` kept for backward
  compatibility. Skill frontmatter carries `name`, `description`, and optional
  `triggers` or `paths`, so a skill can fire on a keyword or deterministically
  when the agent first touches a matching file. It also reads `AGENTS.md`,
  `CLAUDE.md`, and `GEMINI.md` from the repository root.
- Kiro is spec-driven: `.kiro/steering/` holds long-lived project knowledge
  (`product.md`, `tech.md`, `structure.md` by default) with `~/.kiro/steering/`
  as the global scope, `.kiro/specs/` holds requirements, design, and task
  documents per feature, and `.kiro/hooks/` holds event-triggered actions.
  Steering files take an inclusion mode in frontmatter (`always`, `fileMatch`,
  `manual` via `#file-name`, or `auto`); an `AGENTS.md` is accepted but has no
  inclusion mode and is therefore always loaded.
- Kilo Code, maintained by former Roo Code developers, reads `.kilocode/rules/`
  and migrates `.roo/rules/` and `.roomodes` automatically on startup; Roo
  Code's own layout was `.roo/rules/` in the project and `~/.roo/rules/`
  globally.
- Continue loads every rule file in `.continue/rules/`, either as YAML entries
  or as Markdown with `name` and `globs` properties.
- Warp reads `WARP.md` or `AGENTS.md` from the repository, or rules stored in
  Warp Drive, with configuration under `~/.warp/` (`%APPDATA%\warp\` on
  Windows).
- Aider has no auto-loaded instruction file. A conventions file is passed
  explicitly with `aider --read CONVENTIONS.md`, which marks it read-only and
  enables prompt caching, or pinned with `read: CONVENTIONS.md` in
  `.aider.conf.yml`. Aider loads that config from the home directory, the git
  root, and the current directory, in that order, with later files winning.
- Factory's droid reads `~/.factory/AGENTS.md` globally, and Jules, Augment,
  Replit, Ona, and Semgrep are also listed as reading `AGENTS.md` natively.

## What actually ports

Three things travel between all of these. `AGENTS.md` is now the common
instruction file, and Claude Code participates through an `@AGENTS.md` import or
a symlink. The Agent Skills `SKILL.md` format is shared by Claude Code, Codex,
Antigravity, Muse Code, Grok Build, Kimi Code, Devin, OpenHands, OpenClaw, Amp,
and Zed, so a skills directory is close to portable, subject to differences in
the optional frontmatter fields. MCP server definitions are the same JSON shape
everywhere, differing only in which file holds them: `.mcp.json`,
`.cursor/mcp.json`, `.vscode/mcp.json`, `.junie/mcp/mcp.json`,
`.kimi-code/mcp.json`, `mcp_config.json`, an `mcp_servers` block in Muse Code's
`settings.json`, an `[mcp_servers]` table in Grok Build's `config.toml`.

Nothing else ports. Permissions, hooks, subagent definitions, output styles, and
settings precedence are per-tool inventions with no shared vocabulary, and the
rule-activation models differ in kind: Claude Code and Cursor attach globs to
rules, while Antigravity, Devin Desktop, and Kiro make the activation mode
itself an explicit field with a model-decision option. Character limits are
another trap for anyone porting outward, since Antigravity and Devin Desktop cap
rule files at 12,000 characters where Claude Code, and now Grok Build, have no
such limit.

Churn is the other thing to plan for. In the eight months to August 2026 alone,
Gemini CLI was retired, Windsurf was renamed and its agent replaced, Zed
replaced its rules library with skills, OpenHands moved its skills directory,
Kimi Code was rewritten from Python to TypeScript and moved its home from
`~/.kimi/` to `~/.kimi-code/`, and two more first-party lab CLIs arrived within
six weeks of each other, Grok Build in July and Muse Code in August. Pinning our
documentation to a date, as this note does, is not pedantry.

The practical consequence for a repository serving several tools is to keep the
shared prose in `AGENTS.md`, keep skills in one directory and symlink it where
each tool expects to find it, and accept that enforcement, meaning permissions
and hooks, has to be written once per tool that supports it. The one shortcut
worth knowing is that Copilot, Devin, Zed, OpenHands, Hermes, Muse Code, and
Grok Build all read `.claude/` or `CLAUDE.md` directly, so a good `.claude/` is
already doing double duty in seven other tools. Grok Build goes furthest: it
reads not only `CLAUDE.md` and `.claude/rules/` but Claude Code's marketplaces,
plugins, skills, MCP servers, agents, hooks, and `.claude/settings.json`, which
makes it the one tool here that a `.claude/` setup ports to essentially whole.
Kimi Code is the counterexample, and a useful reminder that the convergence is
on `AGENTS.md` and not on `.claude/`: it reads `AGENTS.md` and `.agents/` and
nothing of ours, so a repository that has only written for Claude Code hands it
nothing at all.

## References

- AGENTS.md format:    https://agents.md/
- Agent Skills:        https://agentskills.io
- Claude Code `.claude/`: https://code.claude.com/docs/en/claude-directory.md
- Codex AGENTS.md:
  https://learn.chatgpt.com/docs/agent-configuration/agents-md
- Codex config:        https://developers.openai.com/codex/config-advanced
- Antigravity rules:   https://antigravity.google/docs/rules-workflows
- Antigravity skills:  https://antigravity.google/docs/skills
- Antigravity agents:  https://antigravity.google/docs/cli/subagents
- Antigravity plugins: https://antigravity.google/docs/cli/plugins
- Antigravity settings: https://antigravity.google/docs/cli/settings
- Gemini CLI migration: https://antigravity.google/docs/cli/gcli-migration
- Gemini CLI retirement:
  https://developers.googleblog.com/en/an-important-update-transitioning-gemini-cli-to-antigravity-cli/
- Gemini CLI extensions:
  https://google-gemini.github.io/gemini-cli/docs/extensions/
- Muse Code overview:  https://dev.meta.ai/docs/muse-code
- Muse Code configuration:
  https://dev.meta.ai/docs/muse-code/configuration
- Muse Code extending: https://dev.meta.ai/docs/muse-code/extending
- Meta Model API coding agents:
  https://dev.meta.ai/docs/coding-agents
- Grok Build overview: https://docs.x.ai/build/overview
- Grok Build project rules:
  https://docs.x.ai/build/features/project-rules
- Grok Build skills and plugins:
  https://docs.x.ai/build/features/skills-plugins-marketplaces
- Grok Build modes and commands:
  https://docs.x.ai/build/modes-and-commands
- Grok Build source:   https://github.com/xai-org/grok-build
- Kimi Code overview:  https://www.kimi.com/code/docs/en/
- Kimi Code data locations:
  https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/data-locations.html
- Kimi Code agents:
  https://www.kimi.com/code/docs/en/kimi-code-cli/customization/agents.html
- Kimi Code skills:
  https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html
- Kimi Code hooks:
  https://www.kimi.com/code/docs/en/kimi-code-cli/customization/hooks.html
- Kimi Code migration:
  https://www.kimi.com/code/docs/en/kimi-code-cli/guides/migration.html
- Kimi Code source:    https://github.com/MoonshotAI/kimi-code
- Cursor rules:        https://cursor.com/docs/context/rules
- Cursor hooks:        https://cursor.com/docs/hooks
- Copilot repository:
  https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions
- Copilot in VS Code:
  https://code.visualstudio.com/docs/copilot/customization/custom-instructions
- Cascade memories:    https://docs.devin.ai/desktop/cascade/memories
- Devin rules:         https://docs.devin.ai/cli/extensibility/rules
- Devin AGENTS.md:     https://docs.devin.ai/onboard-devin/agents-md
- Devin Desktop FAQ:   https://docs.devin.ai/desktop/devin-desktop-faq
- Junie guidelines:
  https://junie.jetbrains.com/docs/guidelines-and-memory.html
- Junie MCP:
  https://junie.jetbrains.com/docs/junie-cli-mcp-configuration.html
- Cline rules:         https://docs.cline.bot/features/cline-rules
- Cline memory bank:   https://docs.cline.bot/features/memory-bank
- Zed instructions:    https://zed.dev/docs/ai/instructions
- OpenHands skills:
  https://docs.openhands.dev/usage/prompting/microagents-overview
- Kiro steering:       https://kiro.dev/docs/steering/
- Aider conventions:   https://aider.chat/docs/usage/conventions.html
- pplx skill:
  https://github.com/perplexityai/api-platform-developers/blob/main/skills/pplx-cli/SKILL.md
- OpenClaw workspace:  https://docs.openclaw.ai/concepts/agent-workspace
- Hermes config:
  https://hermes-agent.nousresearch.com/docs/user-guide/configuration
