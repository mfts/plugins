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

From GitHub:

```bash
claude plugin marketplace add mfts/plugins
claude plugin install review-kit@mfts-plugins
```

### Local sessions for a whole repository

Commit this to the repository's `.claude/settings.json`. Local Claude Code sessions register the marketplace after the contributor accepts the workspace trust dialog and enable the plugin at session start. The key and the `@` suffix must match the marketplace's `name`, which is `mfts-plugins`.

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

### Cloud and remote sessions

A cloud session does not install the plugins a repository enables in `.claude/settings.json`, because that path needs the trust dialog a cloud session never shows (see [cloud environments](https://code.claude.com/docs/en/cloud-environments)). Install the plugin in the cloud environment's setup script instead. Open the environment at claude.ai/code, edit its **Setup script**, and add:

```bash
claude plugin marketplace add mfts/plugins
claude plugin install review-kit@mfts-plugins
```

The script runs before Claude Code launches and its result is cached, so later sessions start with the plugin already installed. `github.com` is on the default network allowlist, so no extra network access is needed for this public marketplace.

To make the install travel with the repository instead, add a `SessionStart` hook to `.claude/settings.json` that runs only in the cloud:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "[ \"$CLAUDE_CODE_REMOTE\" = \"true\" ] || exit 0; claude plugin marketplace add mfts/plugins >/dev/null 2>&1; claude plugin install review-kit@mfts-plugins"
          }
        ]
      }
    ]
  }
}
```

Hooks run after Claude Code launches, so a plugin installed this way may need `/reload-plugins` or the next session to appear. Prefer the setup script when you control the environment.

Restart Claude Code and run `/review-kit:review-security` or `/review-kit:thermo-nuclear-code-quality-review`.

## Origin

Ported from Cursor skills. In Cursor the security skill relied on the built-in `security-review` subagent and the quality skill on a parent that pre-collected the diff. Here both reviewers are plugin agents that gather their own input.
