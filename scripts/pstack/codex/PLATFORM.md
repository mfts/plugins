# Pstack on Codex

These are the host-specific rules for this port. Apply them when a retained upstream playbook describes a capability in Cursor terms.

## Delegation and models

Use the subagent tools exposed in this session (`spawn_agent` and the corresponding send, wait, and status tools). Follow their actual schemas. Do not pass Cursor's `subagent_type`, `environment`, `readonly`, or `run_in_background` fields to Codex. `poteto-agent` and `comment-sicko` are bundled prompt files under `agents/`, not registered Codex agent types. For those roles, include the absolute prompt-file path and ask the child to read it first. For read-only investigators, say explicitly that no files or external records may be changed.

Read `${CODEX_HOME:-~/.codex}/pstack-models.md` when a workflow starts. Without a setting, inherit the parent model and effort by omitting overrides. `inherit-parent`, `inherit`, and `auto` are pstack aliases for omission, not model IDs. Only use explicit models and efforts supported by this session and chosen by the user. Pass model and reasoning effort separately, respecting any context-fork restrictions in the tool schema. Repeated panel entries still represent independent reviewers. Vary lenses if distinct models are unavailable and report that limitation.

Bound fan-out to available slots and process excess work in waves. Codex children may share the checkout; create separate worktrees for competing implementations and assign disjoint files for shared-tree work. A spawn does not provision a cloud VM. Cloud-specific playbooks require an available, authorized execution environment; use isolated local worktrees when equivalent, or report the missing capability. Do not create user-visible Codex tasks as a substitute for subagents unless the user requested new tasks. After a restart, inspect durable state and verify agent liveness; do not assume any child survived.

## Skills, tools, and history

Invoke skills using the names exposed by Codex (for example `$poteto-mode`), or read their bundled `SKILL.md` directly. Resolve file paths from the installed skill location. Project skills live in `.agents/skills/`; personal skills in `~/.agents/skills/`. The `create-skill` compatibility skill uses the installed skill-creator when available.

Use the available plan and question tools in the modes that support them. Otherwise keep a concise plan in text and ask in chat when needed. Discover MCP tools from the current tool inventory. Cursor's `mcps/` directory is not a Codex capability. `deslop`, `control-ui`, and `control-cli` are optional external skills, not bundled dependencies. If absent, inspect and simplify the diff directly, and use available browser/terminal tools or a project verification harness. Never claim a live verification that could not run.

For recall, reflection, and session pickup, prefer available task list/read tools, filtering to the active project before reading bodies. Otherwise use only a session log path explicitly supplied by the user or environment, or the visible conversation. Do not assume a Cursor transcript layout or scan unrelated projects. Record missing history as a limitation. Delegate only the scoped excerpts or paths actually obtained.

## Persistence and authority

Cursor `/loop`, cloud sleeper chains, and `/automate` are not Codex commands. For a user-requested recurring monitor, use Codex's automation tool if available, following its schema and scheduling instructions. Prefer a heartbeat for a current-task follow-up. Stay quiet when state is unchanged, and stop or retire the monitor when its predicate is met. If scheduling is unavailable, use a bounded foreground check and report that it will not continue after the turn. Never simulate persistence with a detached sleep process.

Pstack's autonomy language applies within the user's authorized scope and the host's permissions. It does not authorize messages, merges, deployments, destructive resets, or unrelated fixes. Prefer a fresh worktree over discarding another agent's edits. The Benny pack supplies operational templates, not live integrations; configuration and explicit user authorization are required before scheduling or sending messages.

## Runtime

The bundled orchestration and watch-pr tools require Bun and Git; GitHub operations require authenticated `gh`. `gt` and Origin are optional and should only be used where the playbook supports them and the CLI is available. The scripts bootstrap pinned dependencies from `bun.lock`; installation may need network access. Shell helpers target Unix-like hosts. None of these tools installs a scheduler or a webhook receiver.
