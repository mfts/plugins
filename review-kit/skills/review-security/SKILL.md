---
name: review-security
description: Security review of branch or uncommitted changes using the read-only security-review subagent. Use for /review-security, "security review", "review this PR for security", or "any vulnerabilities in my changes". Pass --fix to also fix the findings and re-review until clean.
disable-model-invocation: true
argument-hint: "[PR link | PR number | branch | uncommitted] [--base <branch>] [--fix] [extra instructions]"
---

# Review Security

Run a security review of code changes with the `review-kit:security-review` subagent, then report the findings. With `--fix`, keep going until the review comes back clean.

Arguments: `$ARGUMENTS`

## 1. Open the task ledger

Before doing anything else, create one task per step below with the session's task tools (`TaskCreate`, or `TodoWrite` on older hosts). If no task tool is exposed, keep the ledger as a numbered checklist in your own reply and update it as you go.

1. Resolve the review target and check it out.
2. Launch the security review subagent.
3. Verify every reported finding against the code.
4. Report the result.
5. Only with `--fix`: fix findings and re-review until clean.

Mark each task in progress when you start it and complete when it is verified done. Do not end the turn while a task is open. If a step fails, retry it per the rules below before marking it blocked, and never present a blocked step as finished.

## 2. Resolve the target

Parse `$ARGUMENTS`:

- `uncommitted`, `local`, `dirty`, `working tree`: review `uncommitted changes`.
- A PR link, PR number, or branch name: review `branch changes` on that branch.
- `--base <branch>`: pass `Base Branch`.
- `--fix`: enable step 5.
- Anything else is `Custom Instructions`.

Default to `branch changes`, which reviews the current branch against the merge-base with the repository's default branch, including committed, staged, and unstaged changes.

Set the repository path to the absolute path of the git repository that contains the changes. It may be a subfolder of the workspace; run `git rev-parse --show-toplevel` from the relevant directory to find it.

When a specific PR or branch was requested:

- Resolve it with `gh pr view <number-or-url> --json headRefName` or the branch name as given.
- If it is already checked out, continue.
- Otherwise run `git fetch` and switch to it. If Git refuses because local files would be overwritten or there are conflicts, stop and ask whether to stash local changes. Stash only after the user confirms, then retry the switch.
- Launch the subagent only after the target is checked out locally.

Do not provide `Base Branch` unless the user asked for one or you know the branch was cut from a non-default branch.

## 3. Launch the subagent

Launch exactly one agent with the `Agent` tool:

- `subagent_type: "review-kit:security-review"`
- `description: "Security Review"`
- foreground, unless the user asked for background execution

The subagent computes the diff itself. Do not compute or paste the diff into the prompt. Use this exact prompt shape:

```text
Full Repository Path: <absolute repository path>
Diff: <one of: "branch changes", "uncommitted changes">
Base Branch: <only when reviewing branch changes against a known specific base branch>
Custom Instructions: <only when the user gave specific review instructions>
```

Retry rules:

- If the failure text shows you called it incorrectly (missing `Full Repository Path`, missing `Diff`, wrong prompt shape, wrong subagent type), correct the invocation and retry once immediately.
- For any other failure, retry once with the same prompt.
- If the same failure persists, mark the task blocked, tell the user in one or two sentences what blocked it, and stop. Do not keep retrying.

If the `review-kit:security-review` agent type is not available on this host, do not invent one. Read [the agent definition](../../agents/security-review.md), compute the diff it describes, and perform that review yourself in this same turn with the same rules.

## 4. Verify findings

For each finding the subagent reported, open the cited file and confirm the line exists, the attacker-controlled data really reaches the sink, and no existing control already blocks it. Drop findings that do not survive and say that you dropped them. Keep the table's line numbers accurate to the current working tree.

## 5. Report

- No diff: say in one sentence that there was no diff to review.
- No findings: one line, for example `Security review found no issues`.
- Findings: one compact markdown table, sorted by severity (highest first), with exactly these columns: Severity, Location (file:line), Finding. Location is `file:line`.

Without `--fix`, stop here. Do not fix findings or rerun the review unless the user asks.

## 6. Fix loop (only with `--fix`)

Repeat until the review is clean, at most three rounds:

1. Fix every Critical and High finding, and every Medium finding with a clear local fix, in the smallest change that closes the attack path. Prefer the codebase's existing controls (its validator, its parameterized query helper, its auth middleware) over new ones.
2. Run the project's relevant tests or type check for the touched files if one is cheap to run. Fix any breakage you caused.
3. Launch the subagent again with the same prompt shape and verify its findings as in step 4.
4. If findings remain and a fix is unclear or would change behavior, do not guess. Leave them for the final report.

Do not commit. After the loop, report: the findings fixed, the files touched, and any findings that remain with one sentence each on why they were left.

## Completion check

Before ending the turn, re-read the ledger. Every task must be complete or explicitly blocked with a reason the user can act on. A review that stopped at "the subagent is running" or "findings pending verification" is not done. Finish it.
