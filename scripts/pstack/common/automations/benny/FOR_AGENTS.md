# Set up Benny

Read the plugin's platform guide, then [skills/setup-benny/SKILL.md](skills/setup-benny/SKILL.md). Prepare two workflows for the user's named repository and Slack issue channel: triage and reproduction with optional draft fixes.

Copy this pack to `.pstack/automations/benny/` in the target repository, preserving destination-only files and surfacing conflicting edits. Keep configuration and secrets outside the copied pack. Do not write Cursor plugin settings or assume a Cursor automation API exists.

Pstack must be installed and discoverable in the environment that runs the automation. Read the operational files directly. Do not register the nested Benny skills as plugin skills.

Draft configuration and prompts first. Creating schedules, testing posts, and sending messages require authorization. A setup request does not by itself authorize live Slack messages.
