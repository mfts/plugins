# pstack for Codex

A Codex port of [pstack](https://github.com/cursor/plugins/tree/main/pstack) by [Lauren Tan](https://x.com/poteto). Rigorous workflows for understanding, designing, implementing, reviewing, and verifying software.

Upstream version **0.15.15**. The exact source commit is recorded in [UPSTREAM.json](UPSTREAM.json). The original MIT license is preserved in [LICENSE](LICENSE).

## Install

From a local checkout of this repository:

```bash
codex plugin marketplace add /absolute/path/to/plugins
codex plugin add pstack@mfts-plugins
```

After these changes are published, the repository can also be added with `codex plugin marketplace add mfts/plugins`. Open a new task after installation so it discovers the skills.

## Use

Start with `$setup-pstack` to configure model preferences, then `$poteto-mode` for engineering work. Defaults inherit your current model; explicit selections are validated against the host's available models. Project skills created by these workflows go in `.agents/skills/`.

Examples:

```text
$poteto-mode Reproduce this bug, fix its root cause, and verify it.
$how Explain how cancellation works in this repository.
$interrogate Review this diff for correctness and maintainability.
$swarm Check independent parts of this migration in parallel.
$babysit Check this PR and report outstanding work.
```

The port contains every upstream skill and playbook, plus `create-skill` and `babysit` compatibility entrypoints. New upstream workflows include `swarm`, `no-comments`, `technical-writing`, `bro`, stack shipping, and program orchestration. See the [guide](docs/guide/README.md) and [platform guidance](PLATFORM.md).

Codex loads skills through `.codex-plugin/plugin.json`. The files in `agents/` are role prompts passed to available subagents, not native agent registrations. Explicit-only upstream skills retain that policy through `agents/openai.yaml`.

## Dependencies and limits

Bun is needed for orchestration and PR monitoring helpers; GitHub operations also need authenticated `gh`. Scripts install their pinned dependencies on first use. `gt`, Origin, browser-control tools, and MCP connectors are optional capabilities checked at runtime.

Cursor cloud VMs, Grok Bot routines, and Cursor automation APIs are not included. Local worktrees and available Codex subagent tools support the portable workflows. Scheduling requires the host automation tool; webhook UI work requires a real provider. [Benny](automations/benny/README.md) is an optional template pack, not an enabled integration. Installation alone creates no automations or external messages.

## Maintenance

Edit `scripts/pstack/` overlays or `scripts/sync-pstack.py` at the repository root, then regenerate both ports. See the root README for commands. Do not edit generated port files directly.
