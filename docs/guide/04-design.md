# Design before you write code

One attempt at a hard design locks in the first shape the model thought of. These three skills exist so that doesn't happen. `/pstack:architect` settles types and boundaries before implementation. `/pstack:arena` runs several attempts in parallel and merges the best parts. `/pstack:interrogate` has other models try to break the result.

![Three robots draft competing bridge models at their own tables under /architect, /arena, and /interrogate panels, while a judge robot with a clipboard inspects skeptically.](./images/design.jpg)

## Settle the shape with `/pstack:architect`

```text
/pstack:architect design the import pipeline before writing any code. i care most about how callers use it.
```

[`/pstack:architect`](../../skills/architect/SKILL.md) grounds itself first, running `/pstack:how` over the code the design touches and `/pstack:why` when it moves ownership or layers. Then it runs `/pstack:arena` to produce competing design sketches, with the caller's usage written first in each, followed by types, signatures, and a module map.

By default it proceeds straight from the synthesized design into implementation. If you want to see the design first, say so:

```text
/pstack:architect with checkpoint. stop and show me before implementing.
```

## Fan out attempts with `/pstack:arena`

```text
/pstack:arena take my prompt to the arena verbatim. i want to compare their proposals with yours.
```

[`/pstack:arena`](../../skills/arena/SKILL.md) is the general tool underneath. N subagents attempt the same task in parallel, each writing to its own worktree or directory. A read-only judge, on a different model family when your configuration allows one, scores every candidate against a rubric. The coordinator reads each candidate end to end, picks a base, grafts in the best ideas from the losers, and verifies the result.

```mermaid
flowchart LR
    A[One task] --> B[Configured panel]
    B --> C[Candidate 1]
    B --> D[Candidate 2]
    B --> E[Candidate N]
    C --> F[Cross-judge]
    D --> F
    E --> F
    F --> G[Pick a base]
    G --> H[Graft the best parts]
    H --> I[Verify]
```

The panel comes from your [`/pstack:setup-pstack`](../../skills/setup-pstack/SKILL.md) configuration, and you can adjust it per task. Ask for more candidates when the decision matters, fewer when it doesn't:

```text
/pstack:arena this, 5 candidates. the cache key format is expensive to change later.
```

## Break it with `/pstack:interrogate`

```text
/pstack:interrogate the whole branch, but skeptically. no nitpicks unless it's an actual bug or regression.
```

[`/pstack:interrogate`](../../skills/interrogate/SKILL.md) sends the same diff, intent, and rubric to several reviewers on different model families. Model diversity is the point. Different models have different blind spots, so a finding two models raise independently is high-confidence signal. The lead sorts everything into `Act on`, `Consider`, `Noted`, and `Dismissed`, with a reason for each dismissal, and applies nothing automatically.

Read the dismissals too. The lead is a pragmatic senior engineer, not an oracle, and you can override it.

## How much design work does a task deserve?

You might be wondering whether every change needs this. No. Most changes need none of it. A rough ladder:

- A small, finished change you're unsure about needs `/pstack:interrogate` alone.
- A change that crosses function boundaries or moves ownership earns `/pstack:architect`, which brings `/pstack:arena` with it.
- A standalone decision where independent attempts would help, like naming, formats, or an algorithm, is `/pstack:arena` directly.
- A contested design that's expensive to reverse gets `/pstack:architect`, then `/pstack:interrogate` before shipping.

`/pstack:poteto-mode` already applies this ladder. Boundary-crossing work triggers `/pstack:architect` on its own, so you reach for these directly mainly when you want more or less scrutiny than the default.

Next: [Build and clean the change](./05-build-and-clean.md).
