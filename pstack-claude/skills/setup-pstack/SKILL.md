---
name: setup-pstack
description: Configure pstack models per role and reasoning budget. Use for setup-pstack, configure pstack models, pstack budget, or changing its model choices.
---

Read [Claude Code platform guidance](../../PLATFORM.md) before following this workflow. It defines tool, model, history, and scheduling behavior for this port.


# Setup pstack

Read the platform guide before configuring delegation. Store choices in `~/.claude/pstack-models.md`. This is a pstack data file read by its skills, not an automatically loaded host rule.

1. Inspect the current session's delegation tool schema for supported models and effort settings. Do not guess model IDs or append effort names to them. If no model list is exposed, retain `inherit-parent` or ask the user for an available model. `auto` and legacy `inherit` mean `inherit-parent` in this file; omit the model argument for all three.
2. Read the existing file when present. Preserve role choices and unrelated settings. Otherwise use the defaults below.
3. Ask for the desired reasoning budget (inherit, low, medium, high, or another value actually supported by this session). Show the role table and let the user accept or change specific roles. Model choice and reasoning effort are separate settings. If the delegation API cannot set effort, say so and leave it inherited.
4. Validate every explicit model and effort against the exposed schema. A panel list has one entry per runner even when entries repeat. When only one model is available, diversify reviewer lenses; do not describe the result as cross-model review.
5. Write the confirmed role choices to `~/.claude/pstack-models.md`, preserving unrelated content. The directory may need to be created. Re-running setup updates this file without editing the host's global configuration.

```text
# pstack model configuration
# budget: inherit
feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
hillclimb: inherit-parent
judgment and prose: inherit-parent
hardest tasks: inherit-parent
how explorer: inherit-parent
how explainer: inherit-parent
why investigators: inherit-parent
why synthesizer: inherit-parent
reflect tooling: inherit-parent
reflect judgment, divergent, synthesizer: inherit-parent
arena runners: inherit-parent, inherit-parent, inherit-parent, inherit-parent
arena cross-judge pool: inherit-parent, inherit-parent, inherit-parent, inherit-parent
swarm workers: inherit-parent
architect runners: inherit-parent, inherit-parent, inherit-parent, inherit-parent
interrogate reviewers: inherit-parent, inherit-parent, inherit-parent, inherit-parent
```

Confirm the path written. Pstack reads it when a workflow starts; re-read it after setup in this session. If the project lacks a real-app verification harness, offer the **create-verification-skill** skill once.
