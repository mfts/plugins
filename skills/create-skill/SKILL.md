---
name: create-skill
description: "Author or revise a SKILL.md so a cold agent can execute it correctly. Use for /create-skill, \"write a skill for this\", \"turn this into a skill\", or whenever another pstack skill or playbook routes skill-authoring work here."
---

# Create skill

**You are writing instructions a future agent will follow with none of your context.** Cursor ships this as a built-in; Claude Code does not, so pstack carries it. Every pstack path that says "route skill authoring here" lands on this file.

A skill is worth writing when the same instructions keep getting pasted into chat, or when a section of `CLAUDE.md` has grown from a fact into a procedure. A skill's body loads only when used, so reference material costs nothing until needed. If the content is a standing fact rather than a procedure, it belongs in `CLAUDE.md` instead. Say so and stop.

## Steps

### 1. Settle the trigger before the body

Write the `description` first. It is the only part an agent sees before deciding to load the skill, so it decides whether the skill ever fires. Name what the skill does and when to reach for it, leading with the key use case. Include the literal phrases a user would type. Claude Code truncates `description` plus `when_to_use` at 1,536 characters in the listing, so spend that budget on triggers, not prose.

A description that says what the skill *is* without saying *when* it applies is the single most common authoring failure. "TypeScript best practices" never fires. "Use when reading or editing any .ts or .tsx file" does.

### 2. Place it

| Scope | Path | Applies to |
| --- | --- | --- |
| Personal | `~/.claude/skills/<name>/SKILL.md` | all your projects |
| Project | `.claude/skills/<name>/SKILL.md` | this repo, committed and shared |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | wherever the plugin is enabled |

Directory name is kebab-case and becomes the `/` command. Plugin skills are namespaced `/plugin-name:skill-name`, so they never collide with personal or project skills.

### 3. Write the frontmatter

```yaml
---
name: my-skill
description: "What it does, and the phrases that should trigger it."
---
```

Everything else is optional. Reach for these only when the skill needs them:

- `disable-model-invocation: true` when the skill has side effects the user must time (deploy, commit, send). It also removes the description from context and blocks the Skill tool, so never set it on a skill another skill routes to.
- `allowed-tools` to pre-approve the exact tools the skill runs, scoped to the invoking turn.
- `disallowed-tools` to remove a tool while the skill is active, such as `AskUserQuestion` on an autonomous loop.
- `model` and `effort` when the work needs a specific tier.
- `context: fork` (with `agent:`) to run the whole skill in a subagent.
- `paths` to auto-load the skill only when the files in play match a glob.
- `argument-hint` and `arguments` for `$ARGUMENTS` substitution.

Use `${CLAUDE_SKILL_DIR}` to reference bundled scripts and references, never a hardcoded install path.

### 4. Write the body for a cold reader

- Imperative and specific. "Run `pnpm test --filter web`", not "run the tests".
- Standing instructions, not a one-time checklist. The rendered content stays in context for the session and is never re-read, so anything that must hold throughout the task is written as a rule.
- Ground every claim in something the agent can observe: a command to run, a file to read, an artifact to inspect.
- Push long reference material into sibling files (`references/`, `playbooks/`) and link them with one line saying what each contains and when to open it. The body stays small; the references load on demand.
- No placeholders. A `TODO` or `<fill this in>` in a shipped skill becomes an instruction some agent follows literally.

Run the draft through the **unslop** skill before shipping. Agent-facing prose carries a higher bar than human prose, because an unhelpful sentence becomes an instruction.

### 5. Test it before you ship it

A skill that has never been invoked is a draft. Start a fresh session, invoke it by its `/` name on a real task, and watch what the agent actually does. The failure modes are always the same three:

1. It never fired. The `description` is missing the trigger phrase.
2. It fired and the agent improvised. A step is ambiguous or assumes context the cold agent lacks.
3. It fired and the agent did the wrong thing. A step is wrong, not vague.

Fix and re-run. For a change whose effect on agent behavior is contested, use the Eval playbook (`playbooks/eval.md` in the **poteto-mode** skill) and grade blinded from transcripts rather than self-report.

### 6. Validate and ship

For a plugin skill, run `claude plugin validate <plugin-dir> --strict`. Check that every relative link resolves and that the frontmatter parses. Ship through the Opening a PR playbook.

**Reply:** the skill's path, its trigger phrase, and what the test run showed it actually did.
