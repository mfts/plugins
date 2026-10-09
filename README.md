# plugins

mfts' plugin marketplace for Claude Code and Codex.

| Plugin | Host | Source | Marketplace |
| --- | --- | --- | --- |
| pstack | Codex | [plugins/pstack](plugins/pstack/) | [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json) |
| pstack | Claude Code | [pstack-claude](pstack-claude/) | [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) |
| review-kit | Claude Code | [review-kit](review-kit/) | [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) |

pstack is ported from [Lauren Tan's pstack](https://github.com/cursor/plugins/tree/main/pstack). Both ports track upstream **0.15.15** and preserve its MIT license. review-kit ships `/review-kit:review-security` and `/review-kit:thermo-nuclear-code-quality-review`, two reviewer subagents with a task ledger and an optional `--fix` loop; see its [README](review-kit/README.md) for arguments and remote-session setup.

## Codex

Test this checkout locally:

```bash
codex plugin marketplace add /absolute/path/to/plugins
codex plugin add pstack@mfts-plugins
```

After publication, use `codex plugin marketplace add mfts/plugins`. Start a new task and invoke `$setup-pstack` or `$poteto-mode`. Packaging follows the [official OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins).

## Claude Code

```bash
claude plugin marketplace add mfts/plugins
claude plugin install pstack@mfts-plugins
claude plugin install review-kit@mfts-plugins
```

For local testing, replace `mfts/plugins` with the checkout's absolute path. Existing users can update the marketplace and plugin after publication:

```bash
claude plugin marketplace update mfts-plugins
claude plugin update pstack@mfts-plugins
```

Restart Claude Code, then invoke `/pstack:setup-pstack`, `/pstack:poteto-mode`, or `/review-kit:review-security`.

Validate review-kit after editing it:

```bash
claude plugin validate ./review-kit
python3 scripts/validate-review-kit.py
```

## Updating pstack

Both plugin trees are generated. Keep host adaptations in `scripts/pstack/` and the transformation in `scripts/sync-pstack.py`.

```bash
git clone https://github.com/cursor/plugins.git /tmp/cursor-plugins
python3 scripts/sync-pstack.py /tmp/cursor-plugins
python3 scripts/sync-pstack.py /tmp/cursor-plugins --check
python3 scripts/validate-pstack.py
```

The sync script requires a clean upstream pstack tree, records its commit and version in each `UPSTREAM.json`, preserves executable modes, and removes stale generated files. Commit any local work before regenerating; direct edits to generated plugin files will be replaced. Review host-specific changes when upstream adds new APIs. The Codex catalog is maintained separately using the plugin-creator marketplace tools.

The native helper tests require Bun:

```bash
cd plugins/pstack/skills/poteto-mode/scripts
bun install --frozen-lockfile
bun test orch watch-pr
bun run typecheck
```

See each port's `PLATFORM.md` for runtime dependencies and capabilities requiring additional integrations. Installation creates no live automation or messages.
