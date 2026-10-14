# RealtyCrawl agent skills

Installable guidance and a Python helper for capability discovery, bounded source requests and real estate evidence interpretation.

## Install

```bash
git clone https://github.com/realtycrawl/realtycrawl-agent-skills.git
mkdir -p ~/.agents/skills
cp -R realtycrawl-agent-skills/skills/realtycrawl ~/.agents/skills/realtycrawl
```

If your agent uses a different skills directory, copy the complete `skills/realtycrawl` folder there. For an existing installation, review changes before replacing it. The skill includes `SKILL.md`, UI metadata, operation references and standard-library Python helpers. It supports REST or the hosted MCP server; no MCP dependency is required.

Set `REALTYCRAWL_API_KEY` in a protected environment for source calls. Metadata discovery is free. Source crawls cost 50 credits per successful platform; stored reads cost 1. The helper requires an explicit positive budget for authenticated requests and a stable idempotency key for POST. It does not retry, follow redirects or paginate automatically.

Try: “Use $realtycrawl to check current Zillow coverage for US sale listings, then prepare a one-listing request capped at 50 credits.”

Run offline helper tests with `npm test`. Python 3.9+ is sufficient. The standalone [hosted skill](https://realtycrawl.dev/agent-onboarding/SKILL.md) links back to the full package.

[Documentation](https://docs.realtycrawl.dev) · [MCP](https://github.com/realtycrawl/realtycrawl-mcp) · [Agent skills](https://github.com/realtycrawl/realtycrawl-agent-skills) · [Examples](https://github.com/realtycrawl/realtycrawl-api-examples)

## Release compatibility

The examples target the application’s 50-credit-per-platform source-crawl update. At verification on 2026-10-14, the live OpenAPI still advertised the previous 1-credit source price. `X-Max-Credits` is a maximum budget, not a charge; the deployed contract and `X-Credits-Used` determine the actual cost. Coordinate the documentation cutover with the application release.
