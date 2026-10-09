# review-kit

Two strict code reviews for Claude Code, each run by a read-only reviewer subagent and driven to completion by a task ledger.

| Skill | Agent | What it does |
| --- | --- | --- |
| `/review-kit:review-security` | `review-kit:security-review` | Finds concrete, reachable vulnerabilities introduced by the diff. Reports a severity table. |
| `/review-kit:thermo-nuclear-code-quality-review` | `review-kit:thermo-nuclear-code-quality-review` | Harsh maintainability audit: code-judo simplifications, the 1k-line rule, spaghetti growth, boundary and type cleanliness. Ends with an approve or changes-requested verdict. |

Both skills take the same arguments:

```text
[PR link | PR number | branch | uncommitted] [--base <branch>] [--fix] [extra instructions]
```

- No arguments reviews the current branch against the merge-base with the default branch, including committed, staged, and unstaged changes.
- `uncommitted` reviews only the working tree.
- A PR or branch is checked out first. If the checkout is blocked, the skill asks before stashing.
- `--fix` applies the findings and re-runs the review, up to three rounds, until it is clean. Nothing is committed.

## How a run proceeds

1. The skill opens a task ledger (one task per step) with the host's task tools, so the run cannot silently stop halfway.
2. It launches exactly one reviewer subagent with the repository path and diff mode. The subagent computes the diff itself and has only `Bash`, `Read`, `Grep`, and `Glob`, so it cannot edit files.
3. The parent verifies each finding against the code before reporting it.
4. With `--fix`, the parent applies the fixes, runs cheap tests, and re-reviews.

If the plugin's agent type is not available on a host, the skill falls back to performing the review inline from the agent definition in `agents/`.

## Install

Local, from this checkout:

```bash
claude plugin marketplace add /absolute/path/to/mfts-plugins
claude plugin install review-kit@mfts-plugins
```

From GitHub, which also works in remote and cloud sessions:

```bash
claude plugin marketplace add mfts/plugins
claude plugin install review-kit@mfts-plugins
```

To make the plugin available in every session of a repository, including remote sessions started from claude.ai, commit this to the repository's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "mfts-plugins": {
      "source": { "source": "github", "repo": "mfts/plugins" }
    }
  },
  "enabledPlugins": {
    "review-kit@mfts-plugins": true
  }
}
```

Restart Claude Code and run `/review-kit:review-security` or `/review-kit:thermo-nuclear-code-quality-review`.

## Origin

Ported from Cursor skills. In Cursor the security skill relied on the built-in `security-review` subagent and the quality skill on a parent that pre-collected the diff. Here both reviewers are plugin agents that gather their own input.
