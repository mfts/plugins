#!/usr/bin/env python3
"""Check review-kit structure: manifest, registered agents, skill frontmatter, links, read-only agents."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'review-kit'
errors = []


def require(ok, message):
    if not ok:
        errors.append(message)


def frontmatter(path):
    match = re.match(r'---\n(.*?)\n---\n', path.read_text(), re.S)
    require(match is not None, f'{path}: missing frontmatter')
    return match[1] if match else ''


manifest = json.loads((PLUGIN / '.claude-plugin/plugin.json').read_text())
require(manifest['name'] == 'review-kit', 'wrong plugin name')
require((PLUGIN / manifest['skills']).is_dir(), 'skills path missing')

catalog = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
entry = next((p for p in catalog['plugins'] if p['name'] == 'review-kit'), None)
require(entry is not None, 'review-kit missing from marketplace.json')
if entry:
    require((ROOT / entry['source']).samefile(PLUGIN), 'marketplace source does not resolve to review-kit')

agents = {}
for rel in manifest.get('agents', []):
    path = PLUGIN / rel
    require(path.is_file(), f'missing registered agent {rel}')
    if not path.is_file():
        continue
    header = frontmatter(path)
    name = re.search(r'^name: (.+)$', header, re.M)
    require(name and name[1] == path.stem, f'{path}: agent name must match file name')
    require(re.search(r'^description: .+', header, re.M), f'{path}: missing description')
    tools = re.search(r'^tools: (.+)$', header, re.M)
    require(tools is not None, f'{path}: reviewer agent must declare tools')
    if tools:
        declared = {t.strip() for t in tools[1].split(',')}
        require(not declared & {'Edit', 'Write', 'MultiEdit', 'NotebookEdit'}, f'{path}: reviewer agent must be read-only')
    agents[path.stem] = path

skills = {p.parent.name: p for p in (PLUGIN / 'skills').glob('*/SKILL.md')}
require({'review-security', 'thermo-nuclear-code-quality-review'} <= skills.keys(), 'missing skills')
for name, path in skills.items():
    header = frontmatter(path)
    text = path.read_text()
    require(f'name: {name}\n' in header + '\n', f'{path}: invalid skill name')
    require(re.search(r'^description: .+', header, re.M), f'{path}: missing description')
    require(re.search(r'^argument-hint: .+', header, re.M), f'{path}: missing argument-hint')
    require('$ARGUMENTS' in text, f'{path}: does not read $ARGUMENTS')
    for section in ('task ledger', 'Completion check', '--fix', 'Retry rules'):
        require(section in text, f'{path}: missing "{section}" section')
    used = set(re.findall(r'subagent_type: "review-kit:([a-z-]+)"', text))
    require(used and used <= agents.keys(), f'{path}: launches an unregistered agent {used - agents.keys()}')

for path in PLUGIN.rglob('*.md'):
    prose = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
    for link in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', prose):
        target = link.split('#')[0]
        if not target or '://' in target or target.startswith(('/', 'mailto:')):
            continue
        require((path.parent / target).exists(), f'{path.relative_to(ROOT)}: broken link {target}')

for message in errors:
    print(f'error: {message}')
print('review-kit valid' if not errors else f'{len(errors)} error(s)')
sys.exit(1 if errors else 0)
