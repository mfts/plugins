---
name: setup-benny
description: Prepare the Benny triage and reproduction automation pack for a named repository and supported host scheduler.
---

Read [Claude Code platform guidance](../../../../PLATFORM.md) before following this workflow. It defines tool, model, history, and scheduling behavior for this port.


# Set up Benny

1. Resolve the target repository and channel. Copy the entire Benny pack to `.pstack/automations/benny/` without overwriting destination-only files or silently replacing local edits. Copy the plugin's platform guide alongside the pack as `PLATFORM.md` and update copied skill links to that file so the pack remains self-contained.
2. Confirm pstack and the required shared skills are installed in the execution environment. Confirm available Slack reads/posts, source control access, a real-app control harness, and a supported scheduler. Report missing capabilities; do not fabricate tools or host settings.
3. Read `../../templates/configuration.example.yaml` and the operational skills at `../triage-issue-reports/SKILL.md` and `../reproduce-and-fix-issues/SKILL.md`. Prepare secret-free user configuration outside the pack, such as `.pstack/benny/configuration.yaml`, a feature map, and a routing map. Keep secrets in environment variables or a secret manager. Ask for required channel/repository choices that cannot be observed.
4. Use only models available in the target host. Keep model IDs separate from effort settings. Match the execution environment's capabilities; do not copy Cursor defaults.
5. Draft the two prompts from `../../templates/`, pointing to the copied operational files and user-owned configuration. Preserve their triage, reproduction, deduplication, and verification constraints. Review the concrete prompts with the user before enabling a live workflow unless already authorized.
6. For Codex, use the available automation tool and its scheduling rules when the user asks to create the workflows. For Claude Code, use an installed scheduler only when supported and authorized. If no scheduler can deliver the requested trigger, leave the prompts ready and explain the blocker. A scheduled poll is not equivalent to a webhook trigger; do not silently substitute it.
7. Verify that the execution checkout contains every referenced file and can access its required integrations. Keep status quiet when nothing actionable has changed. Test live posts only when authorized and record what actually ran.

Report the copied pack path, configuration paths, prompt drafts, confirmed capabilities, and whether anything was enabled.
