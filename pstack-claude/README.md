# pstack for Claude Code

A Claude Code port of [pstack](https://github.com/cursor/plugins/tree/main/pstack) by [Lauren Tan](https://x.com/poteto). Rigorous workflows for understanding, designing, implementing, reviewing, and verifying software.

Updated from **0.11.14 to 0.15.2**. The exact source commit is recorded in [UPSTREAM.json](UPSTREAM.json), and the original MIT license is preserved in [LICENSE](LICENSE).

## Install or update

```bash
claude plugin marketplace add mfts/plugins
claude plugin install pstack@mfts-plugins
```

For an existing installation, after these changes are published:

```bash
claude plugin marketplace update mfts-plugins
claude plugin update pstack@mfts-plugins
```

To test this checkout before publication, register its absolute path instead of `mfts/plugins`. Restart Claude Code after installation or update.

## Use

Start with `/pstack:setup-pstack`, then `/pstack:poteto-mode`. Existing preferences in `~/.claude/pstack-models.md` remain supported. Defaults inherit your session model; setup validates explicit choices against the current host instead of assuming Cursor model IDs are available.

```text
/pstack:poteto-mode Reproduce this bug, fix its root cause, and verify it.
/pstack:how Explain how cancellation works in this repository.
/pstack:interrogate Review this diff.
/pstack:swarm Check independent parts of this migration in parallel.
/pstack:babysit Check this PR and report outstanding work.
```

Every upstream skill and playbook is included. The existing `create-skill` and `babysit` entrypoints remain, with babysit now routing to the latest PR-monitoring playbook. Both `pstack:poteto-agent` and `pstack:comment-sicko` are registered. See the [guide](docs/guide/README.md) and [platform guidance](PLATFORM.md).

## Dependencies and limits

The bundled orchestration and watch-pr scripts require Bun; GitHub operations need authenticated `gh`. Scripts install pinned dependencies on first use. Browser-control skills, MCP connectors, `gt`, and Origin are optional and checked before use.

isolated workers, Grok Bot routines, and Cursor automation APIs are not supplied by this port. Parallel work uses the host's available subagent tools and isolated worktrees. Persistent monitoring needs a supported scheduler. The [Benny pack](automations/benny/README.md) provides templates, not live integrations.

## Maintenance

Both ports are generated from the same upstream commit. Edit the repository's `scripts/pstack/` overlays or `scripts/sync-pstack.py`, then regenerate using the root README instructions.
