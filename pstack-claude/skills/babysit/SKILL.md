---
name: babysit
description: "Watch an open pull request to green: poll CI, triage review comments from humans and bots on their merits, push fixes, and land it. Use for /babysit, \"watch this PR\", \"babysit the stack\", after opening a PR, or when Bugbot or an automated security review comments."
---

# Babysit

**A PR is not shipped when it is opened. It is shipped when it is merged.** Cursor ships this as a built-in; Claude Code does not, so pstack carries it. Every pstack path that says "after opening a PR" lands here.

You own the PR until it merges or you hand back a specific blocker. Do not report "PR opened" and stop.

## Steps

### 1. Establish the target

`gh pr view <number> --json number,title,state,mergeable,headRefName,statusCheckRollup` for the facts. No number given means the PR for the current branch. Read PR status from `gh`, never from memory of what you pushed.

For a stack, the target is the whole stack in order. A merged parent that leaves a child unrebased is not done.

### 2. Watch CI

`gh pr checks <number> --watch` blocks until the run resolves and is the cheap path. For a long run, or when you also want to react to review comments as they land, drive the loop with Claude Code's `/loop` skill and pick the interval from how long the run actually takes. Do not poll every 30 seconds against an 8-minute suite.

On a failure, read the failing job's log (`gh run view <id> --log-failed`) before touching code. Then classify:

- **A real break from this diff.** Fix it. Trace it to the root cause per **principle-fix-root-causes** rather than adjusting the assertion until it passes.
- **A flake.** Re-run once (`gh run rerun --failed`). A second failure is not a flake; treat it as real. Never re-run more than twice to manufacture a green.
- **Broken on main already.** Confirm by checking main's latest run. Say so, and do not absorb the fix into this PR unless it blocks the merge.

Each fix is its own commit with a message naming what broke. Push, then return to watching.

### 3. Triage review comments

Human reviewers, Bugbot, and agentic security reviews all file into the same list, and they file real catches and noise in the same list. Take a skeptical posture toward every one of them. For each comment, decide one of three:

- **Fix.** The comment identifies a real problem. Change the code and reply naming the commit.
- **Dismiss.** The comment is a non-issue, a nitpick, or a misread of the intent. Reply with the concrete reason. "This is guarded by the type at the call site in `router.ts:40`" is a dismissal. Silence is not, and neither is churning the code to make a bot stop talking.
- **Ask.** The comment reveals a genuine product or preference fork you cannot settle by observation. Surface it to the user with the options.

Judge each comment against the PR's intent. A reviewer asking for scope you deliberately excluded gets a "not in this PR, here's why", not a widened diff. Push back when feedback drifts from intent; that is part of the job.

### 4. Keep the branch mergeable

Rebase on `main` before substantial work and whenever `mergeable` goes false. For a stack, rebase in order from the bottom. Never force-push to a shared branch without saying so first; that is the irreversible-action exception to autonomy.

### 5. Land it

When checks are green and reviews are resolved, merge if the user has authorized merging (an explicit "land it", "merge when green", or an autonomous run whose predicate is a merge). Otherwise report ready-to-merge and stop. Merging is the user's call by default.

After a merge in a stack, rebase and re-watch the next PR. The run ends when the last one lands.

### 6. Report

**Reply:** the PR link as `https://github.com/<owner>/<repo>/pull/<number>`, its final state, what CI did (including any failure you fixed and how), each review comment with its fix / dismiss / ask verdict and one line of reasoning, and anything still open. Write it per the **poteto-mode** skill's reply rules.

Never claim a check passed without having read its status from `gh`.
