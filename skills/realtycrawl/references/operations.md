# Choosing an operation

Read `https://realtycrawl.dev/v1/openapi.json` for the current schema and `https://realtycrawl.dev/v1/meta/capabilities` for enablement. A defined endpoint is not proof that every platform supports it. A beta platform-operation capability uses documentation and offline tests, not fresh live verification. Preserve its evidence level and warnings. Unavailable, research and retired capabilities are not callable.

- `GET /v1/meta/capabilities?platform=zillow&country=US`: public, free discovery.
- `POST /v1/{platform}/listings/search`: source crawl, 3 credits per returned Zillow listing or 50 credits per successful other platform. Selectors differ by source and market.
- `POST /v1/listings/search`: unified search. Reserve 3 times limit for Zillow (default 10) and 50 credits per other requested platform; unused credits and unsuccessful sources refund their reservation.
- `GET /v1/listings/{listing_id}`: read an account-owned stored observation, 1 credit. Use `data[0].id` from a search, not a native source ID.
- `GET /v1/listings/{listing_id}/media`: stored collection, 1 credit per request. Preserve the original limit and use only returned cursors.
- `GET /v1/zillow/listings/{native_id}`: fetch fresh Zillow detail by ZPID, 50 credits. Optional `transaction=rent` or `status=sold` selects a documented source mode. Read its beta evidence and returned warnings.
- `POST /v1/zillow/listings/batch`: fetch 1–5 unique numeric ZPIDs from `native_ids`. Reserve 50 credits per requested ID; settle 50 per successful detail. Each item reports success or a sanitized error code. A shared 50-second deadline can leave explicit `BATCH_DEADLINE_EXCEEDED` failures; do not retry them automatically.
- `GET /v1/listings/{listing_id}/{facts|tax-history|schools|nearby|agent}`: read one source section from an account-owned retained Zillow detail, 1 credit. A search observation may lack these fields; collect supported fresh detail first. Missing sections return `CAPABILITY_UNAVAILABLE`, while published empty collections remain empty.

Zillow search supports documented USD price, bedroom/bathroom, living-area-in-sqft and property-type bounds, source order/price/newest sorts, and active sale/rent or sold sale modes. Its current location selector remains a US bounding box. Unsupported cursors, arbitrary polygons, `listed_since` and search expansions must not be inferred from another source's schema. Check capabilities and the live operation contract before constructing filters.

For the release's complete operation IDs and route templates, read [the generated operation inventory](api-contract.md).

Stored observations expire after 24 hours and do not refresh the source. Inspect `meta.sources` and `meta.completeness` before describing completeness. Keep the complete response envelope in artifacts.

## Helper examples

Run from the skill directory; Python 3.9+ and its standard library are sufficient.

```bash
python3 scripts/realtycrawl_api.py GET /v1/meta/capabilities --parameters '{"platform":"zillow","country":"US"}'
python3 scripts/realtycrawl_api.py POST /v1/zillow/listings/search --parameters '{"location":{"kind":"bbox","bbox":[-97.82,30.2,-97.65,30.35]},"transaction":"sale","limit":1}' --max-credits 50 --idempotency-key unique-logical-search-id
```

The second command permits up to 50 credits; with one returned Zillow listing the charge is 3. Set `REALTYCRAWL_API_KEY` in the environment. No automatic retries, redirects or pagination. Reuse the key and identical body after an interrupted request; a different logical operation needs a new key. HTTP failures include the request ID, while the API key remains out of output.

Native detail and a retained section are separate calls. Replace the placeholders with the ZPID and resulting RealtyCrawl listing ID:

```bash
python3 scripts/realtycrawl_api.py GET /v1/zillow/listings/ZPID --max-credits 50
python3 scripts/realtycrawl_api.py GET /v1/listings/LISTING_ID/facts --max-credits 1
python3 scripts/realtycrawl_api.py POST /v1/zillow/listings/batch --parameters '{"native_ids":["ZPID_ONE","ZPID_TWO"]}' --max-credits 100 --idempotency-key unique-batch-id
```

Response `fields` and `format` options belong in the query string for GET and POST. The helper takes them in `--parameters` and moves them to the query string. `fields` accepts up to 32 dotted paths with array indexes; projection leaves canonical source input and billing unchanged. CSV and NDJSON return `{format, content, meta}` through the helper, including request ID, credits, row count and replay metadata. Source failures retain JSON error handling.

```bash
python3 scripts/realtycrawl_api.py GET /v1/listings/LISTING_ID/facts --parameters '{"fields":"year_built,description","format":"csv"}' --max-credits 1
```

Nearby homes preserve an unknown price basis and are not verified sale comparables. School rating scales and distance units remain unknown when the source omits them. Tax history is source-reported rather than a verified tax bill. The `agent` section contains embedded listing attribution, not an independently verified professional profile. No Zestimate, valuation history or new building-unit contract is implied by these sections.

[Full documentation](https://realtycrawl.dev/docs)
