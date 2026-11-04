# RealtyCrawl agent skills

Installable guidance and a Python helper for capability discovery, bounded source requests and real estate evidence interpretation.

## Install

```bash
git clone https://github.com/realtycrawl/realtycrawl-agent-skills.git
mkdir -p ~/.agents/skills
cp -R realtycrawl-agent-skills/skills/realtycrawl ~/.agents/skills/realtycrawl
```

If your agent uses a different skills directory, copy the complete `skills/realtycrawl` folder there. For an existing installation, review changes before replacing it. The skill includes `SKILL.md`, UI metadata, operation references and standard-library Python helpers. It supports REST or the hosted MCP server; no MCP dependency is required.

Set `REALTYCRAWL_API_KEY` in a protected environment for source calls. Metadata discovery is free. Zillow listing searches cost 3 credits per returned listing (default limit 10); other source crawls cost 50 credits per successful platform; stored reads cost 1. The helper requires an explicit positive budget for authenticated requests and a stable idempotency key for POST. It does not retry, follow redirects or paginate automatically.

Try: “Use $realtycrawl to check current Zillow coverage for US sale listings, then prepare a one-listing request capped at 50 credits.”

The skill covers Zillow search filters, fresh detail by ZPID, five retained detail sections, bounded 1–5-item batches, field selection and CSV/NDJSON exports. Read [operation selection](skills/realtycrawl/references/operations.md) for pricing and source limitations, or the [generated operation inventory](skills/realtycrawl/references/api-contract.md) for this release's complete route templates. The Python helper accepts export options in its parameters and moves them to the URL for GET and POST; export results retain text plus request, credit, row-count and replay metadata.

Run offline helper tests with `npm test`. Python 3.9+ is sufficient. The standalone [hosted skill](https://realtycrawl.dev/agent-onboarding/SKILL.md) links back to the full package.

[Documentation](https://realtycrawl.dev/docs) · [MCP](https://github.com/realtycrawl/realtycrawl-mcp) · [Agent skills](https://github.com/realtycrawl/realtycrawl-agent-skills) · [Examples](https://github.com/realtycrawl/realtycrawl-api-examples)

## Release compatibility

Zillow listing searches cost 3 credits per returned listing (default limit 10); fresh detail costs 50, including each successful batch item; other source crawls cost 50 credits per successful platform; stored-observation reads cost 1 credit. Metadata and idempotent replays are free. A batch reserves 50 per requested ID and refunds failures. `X-Max-Credits` is a maximum budget, not a charge; inspect the live operation contract and `X-Credits-Used` before quoting costs. Check platform-operation capabilities separately: documentation-backed beta coverage is callable but has not received fresh live source acceptance. Preserve its warnings.

## Cross-platform workflows

The contract supports retained property facts for 183 listing sources, source-detail batches for 31 additional platforms, and saved-observation batches across all 196 in-scope sources. Source availability remains operation-specific; new bindings are documentation/offline-test backed.

Use POST /v1/{platform}/listings/batch with items containing canonical URLs or supported native IDs (1–5), retaining existing selector requirements. Reserve 50 credits per item and charge only successful details. The existing Zillow native_ids batch contract is unchanged. Use POST /v1/observations/batch with resources containing a public read operation and returned ID (1–25); reserve 1 credit per item and charge only successful saved reads. Missing or expired observations remain per-item failures. No automatic retries or retention extension.

StreetEasy supplies school observations and Rightmove supplies embedded brokerage attribution where present. Tax history and nearby-home sections remain source-specific. FHFA state-market definitions can be read with GET /v1/markets/{market_id}.
