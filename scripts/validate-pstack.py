#!/usr/bin/env python3
"""Check pstack package structure, provenance, internal links, and host boundaries."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PORTS = [ROOT / 'pstack-claude', ROOT / 'plugins/pstack']
errors = []


def require(ok, message):
    if not ok:
        errors.append(message)


inventories = []
provenance = []
for root in PORTS:
    label = str(root.relative_to(ROOT))
    codex = root.name == 'pstack'
    manifest = json.loads((root / ('.codex-plugin' if codex else '.claude-plugin') / 'plugin.json').read_text())
    source = json.loads((root / 'UPSTREAM.json').read_text())
    provenance.append(source)
    require(manifest['version'] == source['version'], f'{label}: version differs from upstream record')
    require(re.fullmatch(r'[0-9a-f]{40}', source['commit']), f'{label}: missing upstream commit')
    require(manifest['name'] == 'pstack', f'{label}: wrong plugin name')
    require((root / manifest['skills']).is_dir(), f'{label}: skills path missing')
    skills = {p.parent.name for p in (root / 'skills').glob('*/SKILL.md')}
    inventories.append(skills)
    require({'poteto-mode', 'setup-pstack', 'swarm', 'no-comments', 'babysit', 'create-skill'} <= skills,
            f'{label}: missing workflow entrypoints')
    for path in root.rglob('*.md'):
        if 'node_modules' in path.parts:
            continue
        text = path.read_text()
        if path.name == 'SKILL.md':
            match = re.match(r'---\n(.*?)\n---\n', text, re.S)
            require(match is not None, f'{path}: missing frontmatter')
            if match:
                header = match[1]
                require(f'name: {path.parent.name}\n' in header + '\n', f'{path}: invalid skill name')
                require(re.search(r'^description: .+', header, re.M), f'{path}: missing description')
                require('PLATFORM.md)' in text, f'{path}: missing host guidance')
                if codex:
                    require(not re.search(r'^(mode|icon|color|reminder|disable-model-invocation):', header, re.M),
                            f'{path}: Cursor-only frontmatter')
        # Ignore fenced examples. Only concrete relative Markdown links are package dependencies.
        prose = re.sub(r'```.*?```', '', text, flags=re.S)
        for link in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', prose):
            target = unquote(link.split('#')[0])
            if not target or '://' in target or target.startswith(('/', 'mailto:', '$', '<')):
                continue
            require((path.parent / target).exists(), f'{path.relative_to(ROOT)}: broken link {target}')
        if 'skills' in path.relative_to(root).parts and path.name != 'PLATFORM.md':
            require('~/.cursor/' not in text, f'{path}: unported Cursor user path')
            require('.cursor/skills/' not in text, f'{path}: unported project skill path')
            require(not re.search(r'(claude-fable-5|claude-opus-5-5|claude-opus-5-thinking|grok-4\.[67]|gpt-5\.6-sol-max|pstack-models\.mdc|environment: \"cloud\")', text), f'{path}: unported model ID')
    for agent in manifest.get('agents', []):
        require((root / agent).is_file(), f'{label}: missing registered agent {agent}')
    for path in (root / 'skills').rglob('*.sh'):
        require(path.stat().st_mode & 0o111, f'{path}: shell helper is not executable')

require(inventories[0] == inventories[1], 'Skill inventories differ across ports')
require(provenance[0] == provenance[1], 'Ports use different upstream revisions')
for catalog_path, codex in [('.agents/plugins/marketplace.json', True), ('.claude-plugin/marketplace.json', False)]:
    catalog = json.loads((ROOT / catalog_path).read_text())
    entry = next(p for p in catalog['plugins'] if p['name'] == 'pstack')
    path = entry['source']['path'] if codex else entry['source']
    require((ROOT / path).is_dir(), f'{catalog_path}: source does not resolve')
    if codex:
        require({'installation', 'authentication'} <= entry['policy'].keys(), 'Codex catalog lacks policies')
        require(bool(entry['category']), 'Codex catalog lacks category')

# Platform-neutral runtime helpers must be identical in both distributions.
left = PORTS[0] / 'skills/poteto-mode/scripts'
right = PORTS[1] / 'skills/poteto-mode/scripts'
for path in left.rglob('*'):
    if path.is_file() and 'node_modules' not in path.parts:
        peer = right / path.relative_to(left)
        require(peer.is_file() and path.read_bytes() == peer.read_bytes(), f'Runtime helper differs: {path.name}')

if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f'Validated both ports: {len(inventories[0])} skills each, manifests, provenance, links, and matching helpers.')
