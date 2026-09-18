# Pstack on Claude Code

These are the host-specific rules for this port. Apply them when a retained upstream playbook describes a capability in Cursor terms.

Use the session's `Agent` tool (or `Task` on older hosts) and only fields its schema supports. Plugin agents are `pstack:poteto-agent` and `pstack:comment-sicko`; general delegates use `general-purpose`. Request background execution only when supported. There is no Cursor `environment: "cloud"` or `readonly` flag: instruct investigators not to write, and use worktree isolation when supported or create separate git worktrees explicitly. Do not assume children have separate working directories or survive a restart.

Read `~/.claude/pstack-models.md` when a workflow starts. The default is to omit model overrides and inherit the parent. `inherit-parent`, `auto`, and legacy `inherit` all mean omission. Do not send these aliases as real model IDs. Only use model aliases/IDs confirmed by the current tool schema or host model list. Do not assume Cursor's multi-vendor models are available. Reasoning effort is separate from a model ID and must remain inherited when the subagent API cannot set it. Use different review lenses when multiple model families are unavailable and say that the review was not cross-model. Limit concurrency to the host's capacity.

Invoke plugin skills as `/pstack:<skill-name>`. A routed skill can also be read by its bundled path even when its invocation policy is explicit-only. Project skills use `.claude/skills/`; personal skills use `~/.claude/skills/`. Resolve references relative to the installed skill, never a hardcoded plugin cache path. The bundled `create-skill` and `babysit` compatibility entrypoints remain available.

Use `AskUserQuestion` and the available task-list tools when exposed. Discover integrations through the current MCP tool inventory, not Cursor's `mcps/` directory. `deslop`, `control-ui`, and `control-cli` from cursor-team-kit are optional external capabilities, not Claude built-ins. Use an installed equivalent or inspect the diff and drive the app with available tools; report unavailable verification honestly.

Locate transcripts through the active session's supplied path or a supported history interface. Scope to the current project before reading; do not guess Cursor-style directory slugs or search unrelated private chats. If history is unavailable, work from the visible conversation and say what is missing.

Use `/loop` only if the installed Claude Code host actually exposes it, and respect its session lifetime. Persistent automation requires a supported scheduler and explicit user authorization. Do not invent Cursor automation APIs or cloud wake chains. Without a scheduler, perform bounded foreground checks and report the persistence limitation. The Benny pack is an operational template, not an installed Slack connector or scheduler.

Autonomy is bounded by the user's scope and the host's permissions. Pstack does not authorize unrelated messages, destructive resets, deployments, or merges. Isolate work instead of discarding another agent's changes.

The orchestration and watch-pr scripts require Bun and Git; GitHub operations require authenticated `gh`. Origin and `gt` are optional where supported. First use installs pinned dependencies from `bun.lock` and may require network access. Shell helpers target Unix-like hosts.
