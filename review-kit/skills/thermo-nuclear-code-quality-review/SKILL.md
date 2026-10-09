---
name: thermo-nuclear-code-quality-review
description: Run an extremely strict maintainability review for abstraction quality, giant files, and spaghetti-condition growth using the read-only thermo-nuclear-code-quality-review subagent. Use for a thermo-nuclear code quality review, thermonuclear review, deep code quality audit, or especially harsh maintainability review. Pass --fix to also apply the restructurings and re-review until the verdict is approve.
disable-model-invocation: true
argument-hint: "[PR link | PR number | branch | uncommitted] [--base <branch>] [--fix] [extra instructions]"
---

# Thermo-Nuclear Code Quality Review

Run an unusually strict maintainability audit of code changes with the `review-kit:thermo-nuclear-code-quality-review` subagent, then report its findings. With `--fix`, keep going until the verdict is approve.

Arguments: `$ARGUMENTS`

The full rubric (code-judo simplification, the 1k-line rule, spaghetti growth, boundary and type cleanliness, approval bar) lives in [the agent definition](../../agents/thermo-nuclear-code-quality-review.md). The subagent applies it. You orchestrate, verify, and report.

## 1. Open the task ledger

Before doing anything else, create one task per step below with the session's task tools (`TaskCreate`, or `TodoWrite` on older hosts). If no task tool is exposed, keep the ledger as a numbered checklist in your own reply and update it as you go.

1. Resolve the review target and check it out.
2. Launch the code quality review subagent.
3. Verify every reported finding against the code.
4. Report the result.
5. Only with `--fix`: apply the restructurings and re-review until the verdict is approve.

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

## 3. Launch the subagent

Launch exactly one agent with the `Agent` tool:

- `subagent_type: "review-kit:thermo-nuclear-code-quality-review"`
- `description: "Code Quality Review"`
- foreground, unless the user asked for background execution

The subagent computes the diff and reads the changed files itself. Do not paste the diff into the prompt. Use this exact prompt shape:

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

If the `review-kit:thermo-nuclear-code-quality-review` agent type is not available on this host, do not invent one. Read the agent definition linked above, gather the diff and changed-file contents it describes, and perform that review yourself in this same turn with the same rubric, tone, output order, and approval bar.

## 4. Verify findings

For each finding, open the cited file and confirm the line exists and the claim holds: the branch really is new, the helper really already exists, the file really crosses 1000 lines. For each proposed code-judo move, check that the simpler shape actually preserves behavior; name the behavior that would change if it does not. Drop findings that do not survive and say that you dropped them.

## 5. Report

- No diff: say in one sentence that there was no diff to review.
- Otherwise, present the surviving findings in the subagent's priority order, each with `file:line`, the problem, and the remedy. Keep the verdict line (`approve` or `changes requested`) and the list of blockers.

Without `--fix`, stop here. Do not restructure code or rerun the review unless the user asks.

## 6. Fix loop (only with `--fix`)

Repeat until the verdict is approve, at most three rounds:

1. Apply the blockers first, then the highest-priority remaining findings. Preserve behavior. Prefer deleting complexity to rearranging it, and reuse the canonical helper the review pointed at.
2. Run the project's tests and type check for the touched files if they are cheap to run. Fix any breakage you caused. If a restructuring cannot be made to pass, revert that one change and note it.
3. Launch the subagent again with the same prompt shape and verify its findings as in step 4.
4. If a finding remains and the fix would change behavior or needs a product decision, do not guess. Leave it for the final report.

Do not commit. After the loop, report: the restructurings applied, the files touched with before and after line counts for any file near the 1k threshold, the final verdict, and any findings that remain with one sentence each on why they were left.

## Completion check

Before ending the turn, re-read the ledger. Every task must be complete or explicitly blocked with a reason the user can act on. A review that stopped at "the subagent is running" or "findings pending verification" is not done. Finish it.
