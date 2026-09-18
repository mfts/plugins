# Benny automation templates

Benny triages Slack issue reports and reproduces confirmed bugs, optionally preparing a draft fix. This pack is adapted from pstack's Cursor automations. It is not an enabled automation, scheduler, or Slack integration.

Point the agent at [FOR_AGENTS.md](FOR_AGENTS.md) and name the target repository. Setup copies the pack to `.pstack/automations/benny/`, preserves local changes, and keeps user configuration outside that directory. The operational skills are read directly rather than registered as plugin skills.

A working setup needs pstack, Slack read/write capabilities, a real-app verification harness, and a scheduler supported by the host. Without those, setup can prepare configuration and prompts but must report what remains unavailable. Live creation and posting require the user's explicit authorization.
