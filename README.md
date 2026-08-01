# plugins

my Claude Code plugin marketplace.

## install

```bash
claude plugin marketplace add mfts/plugins
```

then install whichever plugin you want:

```bash
claude plugin install pstack@mfts-plugins
```

## plugins

| plugin | description |
|---|---|
| [pstack](./pstack-claude/) | rigorous agent workflows you can parallelize with confidence. Claude Code port of [pstack](https://github.com/cursor/plugins/tree/main/pstack) by [Lauren Tan](https://x.com/poteto). MIT. |

## adding a plugin

drop the plugin directory at the repo root, give it a `.claude-plugin/plugin.json`, and add an entry to
[`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json) pointing `source` at it:

```json
{
	"name": "your-plugin",
	"source": "./your-plugin",
	"description": "what it does"
}
```

each plugin keeps its own README and LICENSE.
