---
name: create-skill
description: Author or revise a SKILL.md for a future agent. Use when writing a skill, turning a workflow into a skill, or when a pstack playbook routes skill authoring here.
---

# Create skill

Use the host's skill-creator skill when available. Otherwise follow this portable workflow.

1. Settle the trigger in `description`: what the skill does and when it applies. Keep the scope specific to the user's request.
2. Preserve an existing skill's location. For new project or personal skills, use the paths in the platform guide. Plugin skills live at `skills/<kebab-case-name>/SKILL.md`.
3. Use YAML frontmatter with `name` and `description`. Keep the body focused on decisions, constraints, and procedures the agent would not otherwise know. Link supporting references and scripts relative to this file.
4. Keep tool instructions grounded in capabilities exposed in the target environment. A skill does not confer permission for unrelated external actions. Preserve the user's invocation policy.
5. Check frontmatter, relative links, and executable helpers. For a substantial behavioral change, exercise a realistic request in an isolated workspace and inspect the actual output. Do not mistake static validation for behavioral proof.
6. Run the host's skill/plugin validator when available and report what was tested.

Use **unslop** for prose. The **poteto-mode** playbook at `../poteto-mode/playbooks/eval.md` covers blinded behavioral comparisons when needed.
