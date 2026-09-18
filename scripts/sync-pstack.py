#!/usr/bin/env python3
"""Regenerate both pstack ports from a local cursor/plugins checkout."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OVERLAYS = ROOT / 'scripts/pstack'
PORTS = {'claude': ROOT / 'pstack-claude', 'codex': ROOT / 'plugins/pstack'}
MODELS = ('claude-fable-5-1-thinking-max', 'claude-opus-5-thinking-xhigh',
          'gpt-5.6-sol-max', 'grok-4.6-fast-xhigh')


def dump(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def adapt(text, rel, platform, skills):
    config = '~/.claude/pstack-models.md' if platform == 'claude' else '${CODEX_HOME:-~/.codex}/pstack-models.md'
    text = text.replace('PSTACK_CONFIG_PATH', config)
    text = text.replace('[PR #123](url)', 'PR #123 (link to the actual source)')
    text = text.replace("Cursor's `/loop` command (a built-in, not a pstack skill)", 'the supported scheduling mechanism in the platform guide')
    text = text.replace("Cursor's `/loop` command", 'the supported monitoring mechanism in the platform guide')
    text = text.replace('arm a `/goal` with', 'record the task objective with')
    text = text.replace('The goal continues across turns until', 'Continue within the authorized session or supported scheduler until')
    text = text.replace('the armed /goal', 'the recorded task objective')
    text = text.replace('whether or not anything changed', 'only when something actionable changed or the user requested periodic updates')
    text = text.replace('Three transcript layouts: legacy flat (`<id>.jsonl`), current nested (`<id>/<id>.jsonl`), and subagent (`<parent>/subagents/<child>.jsonl`).', 'Use the schema returned by the actual history source, not an assumed transcript layout.')
    text = text.replace("For each candidate, read the first JSONL line and check that `message.content[0].text` contains the conversation's opening user prompt. Take the matching path.", "For each candidate, verify the project, session identity, and opening user prompt before reading its body.")
    text = text.replace('explicit `model:` on each', 'the configured model on each (omit overrides for inheritance)')
    text = text.replace('explicit model per', 'configured model per')
    text = text.replace('each a Cursor cloud agent', 'each an isolated worker')
    if rel.as_posix() == 'skills/poteto-mode/SKILL.md':
        start = text.index('## Subagents\n')
        end = text.index('## Writing the reply', start)
        delegation = '''## Subagents

Read the platform guide for the host's delegation API, concurrency limits, and isolation behavior. Read the model configuration before dispatching; absent a role setting, inherit the parent model and effort. Do not pass pstack's inheritance aliases as model IDs.

For playbook code delegates and ad-hoc helpers, use the bundled `agents/poteto-agent.md` instructions. In Claude Code the registered type is `pstack:poteto-agent`; in Codex pass its resolved prompt-file path to the child. Routed workflows (`how`, `why`, `interrogate`, `reflect`, `swarm`) supply their own role prompts. The comment reviewer uses `agents/comment-sicko.md` (Claude type `pstack:comment-sicko`).

Give writers isolated worktrees or disjoint ownership; give investigators explicit read-only scopes. Use file pointers for large context. Review each returned artifact yourself. Prefer independent models only when the host supports the user's configured choices; otherwise vary reviewer lenses and report the limitation. Use supported status/wait tools, not a resume merely to inspect status.

'''
        text = text[:start] + delegation + text[end:]
    text = text.replace('configured Cursor Slack actions', 'configured Slack connector actions')
    text = text.replace('each a isolated worker', 'each an isolated worker')
    text = text.replace('At each tick, re-read this playbook from trunk with `git show origin/main:pstack/skills/poteto-mode/playbooks/autopilot-full.md`, then re-read the armed `/goal`.', 'At each tick, re-read this installed playbook and the recorded task objective.')
    text = text.replace('At each tick, re-read this playbook from trunk with `git show origin/main:pstack/skills/poteto-mode/playbooks/autopilot-stack.md`, then re-read the armed `/goal`.', 'At each tick, re-read this installed playbook and the recorded task objective.')
    text = text.replace('A local root arms each tick as a real terminal `/loop`. The loop uses a monitored-shell 30-minute sleep and emits an output-notification sentinel. A cloud root uses the existing cloud-sleeper wake chain instead.', 'Schedule authorized audit ticks through the host mechanism in the platform guide. If persistent scheduling is unavailable, use bounded foreground checks and report that limit.')
    text = text.replace('In a local session, a real terminal `/loop`. In a cloud root, a cloud-sleeper wake chain.', 'Use the supported scheduling mechanism in the platform guide, with user authorization.')
    text = text.replace('Run `drive` and `background` under `/loop` in dynamic mode.', 'Run `drive` in the active session; schedule `background` only through the supported host mechanism described in the platform guide.')
    text = text.replace('Hold the watch under `/loop` in dynamic mode.', 'Hold the watch using the host mechanism described in the platform guide.')
    text = text.replace('a frontier watcher wake (arm it via the loop skill, with a long heartbeat fallback)', 'a frontier watcher wake (using the supported scheduler described in the platform guide)')
    text = text.replace('`/loop` is Cursor\'s built-in wake mechanism, not a pstack skill.', 'Persistent wakeups require the supported host scheduler described in the platform guide; pstack itself does not supply one.')
    text = text.replace('a cloud-sleeper wake chain', 'a supported host wake mechanism')

    text = text.replace('~/.cursor/rules/pstack-models.mdc', config)
    for model in MODELS:
        text = text.replace(model, 'inherit-parent')
    text = text.replace('~/.cursor/skills/', '~/.claude/skills/' if platform == 'claude' else '~/.agents/skills/')
    text = text.replace('.cursor/skills/', '.claude/skills/' if platform == 'claude' else '.agents/skills/')
    text = text.replace('~/.cursor/plugins/', '~/.claude/plugins/' if platform == 'claude' else '~/.codex/plugins/')
    text = text.replace('.cursor/automations/', '.pstack/automations/').replace('.cursor/benny/', '.pstack/benny/')
    text = text.replace("Cursor's built-in `create-skill`", 'the bundled `create-skill`')
    text = text.replace("Cursor's built-in for authoring SKILL.md files", 'the bundled compatibility skill for authoring SKILL.md files')
    text = text.replace("Cursor's built-in babysit skill", 'other PR-monitoring skills')
    text = text.replace('from the Cursor environment', 'from the current tool inventory')
    text = text.replace('Otherwise inspect the `mcps/` directory Cursor exposes for enabled MCP servers.', 'Otherwise use the host tool-discovery interface. Report unavailable sources instead of inventing tools.')
    # Transcript layouts are host-owned. Preserve the surrounding investigative workflow.
    text = re.sub(r'Transcripts live at `~/.cursor/projects/[^\n]+',
                  'Locate project-scoped history using the platform guide. Use only paths or task IDs actually supplied by the host; do not derive a transcript path from the workspace name.', text)
    text = text.replace("The system prompt names the active workspace's `agent-transcripts/` directory. Use that path.", 'Locate the active session history through the platform guide.')
    text = text.replace("The system prompt names the workspace's `agent-transcripts/` directory. Use only that path.", 'Locate project-scoped session history through the platform guide.')
    text = text.replace("under the active workspace's `agent-transcripts/` directory (the system prompt names the path)", 'using the scoped history source identified through the platform guide')
    text = text.replace("under the active workspace's `agent-transcripts/` directory (the system prompt names this path)", 'using the scoped history source identified through the platform guide')
    text = text.replace("under the active workspace's `agent-transcripts/` directory (the system prompt names the path.", 'from the scoped history source identified through the platform guide (')
    text = text.replace('`~/.cursor/projects/*/`', 'unrelated project histories')
    text = text.replace('ls -t <agent-transcripts>/*.jsonl <agent-transcripts>/*/*.jsonl <agent-transcripts>/*/subagents/*.jsonl 2>/dev/null | head -10', '# Use the scoped history interface or confirmed transcript paths described in PLATFORM.md.')
    text = text.replace('Readonly strips MCPs.', 'Confirm the delegate has the read tools needed for its evidence sources.')
    text = text.replace('Readonly/Ask mode strips MCPs and defeats that.', 'Confirm those read tools are available to the delegate.')
    text = text.replace('**Do not use readonly/Ask mode.** It strips MCP access, which disables MCP-backed investigators entirely.', 'Give investigators access to the necessary read-only MCP operations.')
    text = text.replace('agent mode (readonly strips MCP)', 'the tool access needed for the assigned work')
    text = text.replace('**Just do it.** Use any MCP tool. Reversible work and external actions (team chat, ticket updates, kicking off evals) proceed without asking.', '**Proceed within the user\'s authorized scope.** Use available tools under the host\'s permissions. External messages, ticket changes, deployments, and merges require authorization for that action; a workflow invocation alone does not grant it.')
    text = text.replace('or `git fetch && git reset --hard origin/<branch>` between them', 'with no destructive reset of shared or dirty work')
    text = text.replace('Cursor cloud agent', 'isolated worker').replace('Cursor dashboard', 'host agent-status interface')
    text = text.replace('a Cursor restart', 'a host restart').replace('After a Cursor restart: local agents are dead, cloud work is not.', 'After a host restart: verify which workers are still alive rather than assuming persistence.')
    text = text.replace('Always `environment: "cloud"` unless the task needs this machine:', 'Use an isolated execution environment supported by the host; local access is needed for:')
    text = text.replace('Restacks run in cloud. A local restack at this scale takes the laptop down.', 'Run restacks in a supported isolated environment with sufficient resources; serialize them per stack.')
    text = text.replace('on its own cloud VM', 'in its own isolated verification environment')
    text = text.replace('cloud agent\'s status', 'worker\'s status')
    text = text.replace('Spawn all N workers in one message with `subagent_type: generalPurpose`, `environment: "cloud"`, `run_in_background: true`, and the configured model. Use `environment: "local"` only when the worker needs access to something on the user\'s computer.', 'Spawn workers using the platform guide, in waves bounded by available slots. Give each writer an isolated worktree and each reviewer a read-only scope. Use the configured model only when supported.')
    if platform == 'claude':
        text = text.replace('AskQuestion', 'AskUserQuestion').replace('generalPurpose', 'general-purpose')
        text = text.replace('subagent_type: "poteto-agent"', 'subagent_type: "pstack:poteto-agent"')
        text = text.replace('subagent_type: "Comment Sicko"', 'subagent_type: "pstack:comment-sicko"')
        text = re.sub(r'^- `readonly`: `(?:true|false)`[^\n]*', '- Scope: read-only investigation; do not modify files or external records.', text, flags=re.M)
        text = text.replace('agent mode (`readonly: false`)', 'with access to the required read tools')
        text = text.replace('`Task`', '`Agent`').replace('Task subagent', 'Agent subagent').replace('Task `model`', 'Agent `model`')
    else:
        text = text.replace('Reviewers return findings in the `Task` response body.', 'Collect reviewer findings from completion messages or the available wait tool; spawning returns an agent handle, not the final report.')
        text = text.replace('Substituting `generalPurpose` skips that read and drifts.', 'Give each general worker this prompt-file path so it reads the mode before acting.')
        text = text.replace('`/loop`', 'the authorized monitoring loop').replace('/loop until', 'Keep working until')
        text = text.replace('`AskQuestion`', 'the available question tool').replace('AskQuestion', 'the available question tool')
        text = text.replace('`Task`', '`spawn_agent`').replace('Task subagent', 'subagent').replace('Task `model`', 'the delegation `model`')
        text = text.replace('`subagent_type: "poteto-agent"`', 'the bundled `agents/poteto-agent.md` prompt')
        text = text.replace('`subagent_type: "Comment Sicko"`', 'the bundled `agents/comment-sicko.md` prompt')
        text = text.replace('`subagent_type: generalPurpose`', 'a general worker instructed by its role prompt')
        text = re.sub(r'^- `subagent_type`: `generalPurpose`\n', '', text, flags=re.M)
        text = re.sub(r'^- `readonly`: `(?:true|false)`[^\n]*', '- Scope: read-only investigation; do not modify files or external records.', text, flags=re.M)
        text = text.replace('`run_in_background: true`', 'asynchronous spawning through the exposed tool')
        text = text.replace('agent mode (`readonly: false`)', 'with access to the required read tools')
        text = text.replace('(`subagent_type: generalPurpose`)', '(using the exposed subagent tool)')
        text = text.replace("Cursor's `/loop` command (a built-in, not a pstack skill)", 'the scheduling mechanism described in the platform guide')
        text = text.replace("Cursor's `/loop`", 'the scheduling mechanism described in the platform guide')
    # Only rewrite known skill invocations, never URL paths or filesystem components.
    for name in sorted(skills, key=len, reverse=True):
        replacement = '/pstack:' + name if platform == 'claude' else '$' + name
        text = re.sub(r'(?<![\w./:-])/' + re.escape(name) + r'(?![\w/-])', lambda m: replacement, text)
    if rel.name == 'SKILL.md':
        parts = text.split('---', 2)
        if len(parts) != 3 or parts[0]:
            raise ValueError(f'Invalid frontmatter: {rel}')
        header = re.sub(r'^name:.*$', f'name: {rel.parent.name}', parts[1], flags=re.M)
        header = re.sub(r'^(?:mode|icon|color|reminder):.*\n', '', header, flags=re.M)
        if platform == 'codex':
            header = re.sub(r'^(?:disable-model-invocation|paths):.*\n', '', header, flags=re.M)
        guide = os.path.relpath('PLATFORM.md', str(rel.parent))
        intro = f'\n\nRead [{"Codex" if platform == "codex" else "Claude Code"} platform guidance]({guide}) before following this workflow. It defines tool, model, history, and scheduling behavior for this port.\n'
        if rel.parent.name == 'poteto-mode':
            intro += '\nOnce invoked, apply this mode on later relevant turns until the user opts out. This is a conversational instruction, not a host persistence guarantee.\n'
        text = '---' + header + '---' + intro + parts[2]
    return text.rstrip() + '\n'


def generate(source, platform, commit):
    manifest = json.loads((source / '.cursor-plugin/plugin.json').read_text())
    skills = {p.parent.name for p in (source / 'skills').glob('*/SKILL.md')} | {'create-skill', 'babysit'}
    files = {}
    for path in source.rglob('*'):
        if not path.is_file() or '.cursor-plugin' in path.parts or 'node_modules' in path.parts:
            continue
        rel = path.relative_to(source)
        files[rel] = (path.read_bytes(), path.stat().st_mode & 0o777)
    for overlay in (OVERLAYS / 'common', OVERLAYS / platform):
        for path in overlay.rglob('*'):
            if path.is_file():
                files[path.relative_to(overlay)] = (path.read_bytes(), 0o644)
    for rel, (content, mode) in list(files.items()):
        if rel.as_posix() == 'skills/poteto-mode/scripts/worktree-audit.sh':
            content = re.sub(rb'# Transcripts dir:[^\n]*\nslug=[^\n]*\ntranscripts=[^\n]*', b'# Optional confirmed transcript directory for this project only.\ntranscripts="${PSTACK_TRANSCRIPTS_DIR:-}"', content)
        if rel.suffix == '.md' and rel.name != 'PLATFORM.md':
            text = content.decode().replace('PSTACK_UPSTREAM_VERSION', manifest['version'])
            content = adapt(text, rel, platform, skills).encode()
        files[rel] = (content, mode)
        upstream_file = source / rel
        explicit_only = (upstream_file.is_file() and
                         b'disable-model-invocation: true' in upstream_file.read_bytes())
        if platform == 'codex' and rel.name == 'SKILL.md' and explicit_only:
            title = rel.parent.name.replace('-', ' ').capitalize()
            ui = ('interface:\n  display_name: ' + json.dumps(title) +
                  '\n  short_description: ' + json.dumps('Pstack workflow: ' + rel.parent.name) +
                  '\npolicy:\n  allow_implicit_invocation: false\n')
            files[rel.parent / 'agents/openai.yaml'] = (ui.encode(), 0o644)
    for name in ('poteto-agent', 'comment-sicko'):
        rel = Path(f'agents/{name}.md')
        content, mode = files[rel]
        text = re.sub(r'^name:.*$', f'name: {name}', content.decode(), flags=re.M)
        text = re.sub(r'^is_background:.*\n', '', text, flags=re.M)
        files[rel] = (text.encode(), mode)
    common = {key: manifest[key] for key in ('name', 'version', 'description', 'author', 'license', 'keywords', 'skills')}
    common.update(repository='https://github.com/mfts/plugins', homepage='https://github.com/mfts/plugins')
    if platform == 'claude':
        common['agents'] = ['./agents/poteto-agent.md', './agents/comment-sicko.md']
        manifest_path = '.claude-plugin/plugin.json'
    else:
        common['interface'] = {
            'displayName': 'pstack', 'shortDescription': 'Rigorous engineering workflows, ported to Codex',
            'longDescription': manifest['description'], 'developerName': 'Lauren Tan; Codex port by mfts',
            'category': 'Developer Tools', 'capabilities': ['Read', 'Write'],
            'websiteURL': 'https://github.com/mfts/plugins', 'logo': './assets/logo.png',
            'defaultPrompt': ['Use $poteto-mode to investigate and fix this bug.', 'Use $interrogate to review this change.']}
        manifest_path = '.codex-plugin/plugin.json'
    files[Path(manifest_path)] = (dump(common), 0o644)
    files[Path('UPSTREAM.json')] = (dump({'repository': 'https://github.com/cursor/plugins', 'path': 'pstack', 'commit': commit, 'version': manifest['version']}), 0o644)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkout', type=Path, help='Local cursor/plugins git checkout')
    parser.add_argument('--check', action='store_true', help='Report drift without writing')
    args = parser.parse_args()
    source = args.checkout.resolve() / 'pstack'
    commit = subprocess.check_output(['git', '-C', str(args.checkout), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(args.checkout), 'status', '--porcelain', '--', 'pstack'], text=True)
    if dirty:
        parser.error('Upstream pstack must be clean so the recorded commit identifies the input.')
    changed = []
    for platform, dest in PORTS.items():
        files = generate(source, platform, commit)
        # Only plugin-owned paths are generated; unrelated root files are preserved.
        existing = {p.relative_to(dest) for p in dest.rglob('*') if p.is_file() and 'node_modules' not in p.parts}
        for rel in sorted(existing - files.keys()):
            changed.append(str((dest / rel).relative_to(ROOT)))
            if not args.check:
                (dest / rel).unlink()
        for rel, (content, mode) in sorted(files.items()):
            path = dest / rel
            if path.exists() and path.read_bytes() == content and path.stat().st_mode & 0o777 == mode:
                continue
            changed.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
                path.chmod(mode)
    print(f'{len(changed)} files ' + ('differ' if args.check else 'updated'))
    if args.check and changed:
        print('\n'.join(changed))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
