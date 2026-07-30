---
name: setup-pstack
description: Configure which models pstack uses per role. Detects your available models and writes a config file that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", or changing pstack's model choices.
---

# Setup pstack

Write `~/.claude/pstack-models.md`, a config file that sets pstack's model per role. The skills read it and fall back to their inline defaults when a line is absent, so this is an override layer, not a requirement.

## Steps

### 1. Detect available models

Enumerate the model aliases you can pass to a `Task` subagent in this session; that is the dependable source. Claude Code's aliases are `opus`, `sonnet`, `haiku`, and `fable`; full IDs such as `claude-opus-5` also work. Check `/model` for the entitled list when you need completeness. If you cannot detect any, ask the user to paste the aliases they have access to. Never write an alias you have not confirmed is available. The alias `inherit` is always valid even though it is not a detected model.

Entitlements vary by plan. A user without `opus` needs the opus roles remapped, so detect rather than assume.

### 2. Load current state

The default role-to-model mapping is the config shape shown in step 5 below. If `~/.claude/pstack-models.md` already exists, read it and treat its values as the current choices. Otherwise start from those defaults.

### 3. Map and confirm

Show every role with its current model, marking any model not in the detected set as needing a choice. Ask whether to accept as-is or change specific roles, offering the detected models plus `inherit` (meaning: this role runs on the parent chat model) as the options. Prefer AskUserQuestion over free text. For panel roles (how critics, arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it that differs from the parent's model when possible.

Claude Code offers fewer distinct model families than a multi-vendor setup, so panel diversity comes from two axes rather than one. Vary the model where you can, and vary each reviewer's assigned lens (correctness, security, performance, maintainability) for the rest. A panel of four across two models still beats a panel of four running one prompt.

### 4. Validate

Every model written must be in the detected set; `inherit` always passes. If a chosen model is not available, stop and ask again. A config pointing at a model the user cannot use breaks every delegation that reads it.

### 5. Write the config

Write `~/.claude/pstack-models.md` with one line per role, using the same labels poteto-mode uses. Overwrite the whole file so re-runs stay idempotent. Shape:

```
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit` as a value: the role runs on the parent chat model (omit Task `model`). Alias entries in a panel list still count toward its fan-out.
feature, refactoring: sonnet
bug-fix: opus
perf-issue: opus
hillclimb: opus
judgment and prose: fable
hardest tasks: fable
how explorer: sonnet
how explainer: fable
how critics: fable, opus, sonnet, haiku
why investigators: sonnet
why synthesizer: fable
reflect tooling: opus
reflect judgment, divergent, synthesizer: fable
arena runners: fable, opus, sonnet, haiku
arena cross-judge pool: fable, opus, sonnet, haiku
architect runners: fable, opus, sonnet, haiku
interrogate reviewers: fable, opus, sonnet, haiku
```

The skills read this file on demand at delegation time. It is not loaded into every session, so it costs no context until a delegation fires.

### 6. Confirm

Tell the user the config was written and where. It applies immediately. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, an existing harness, or Claude Code's `/run` and `/verify` already taught about this repo). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with `/pstack:create-verification-skill`, or Claude Code's bundled `/run-skill-generator` can teach `/run` and `/verify` about this repo." On yes, invoke the chosen one. On no, move on without pushing.
