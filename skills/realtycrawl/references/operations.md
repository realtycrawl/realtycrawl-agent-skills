# Choosing an operation

Read `https://realtycrawl.dev/v1/openapi.json` for the current schema and `https://realtycrawl.dev/v1/meta/capabilities` for enablement. A defined endpoint is not proof that it is active.

- `GET /v1/meta/capabilities?platform=zillow&country=US`: public, free discovery.
- `POST /v1/{platform}/listings/search`: source crawl, 50 credits per successful platform. Selectors differ by source and market.
- `POST /v1/listings/search`: unified search. Reserve 50 credits per requested platform; unsuccessful sources refund their reservation.
- `GET /v1/listings/{listing_id}`: read an account-owned stored observation, 1 credit. Use `data[0].id` from a search, not a native source ID.
- `GET /v1/listings/{listing_id}/media`: stored collection, 1 credit per request. Preserve the original limit and use only returned cursors.

Stored observations expire after 24 hours and do not refresh the source. Inspect `meta.sources` and `meta.completeness` before describing completeness. Keep the complete response envelope in artifacts.

## Helper examples

Run from the skill directory; Python 3.9+ and its standard library are sufficient.

```bash
python3 scripts/realtycrawl_api.py GET /v1/meta/capabilities --parameters '{"platform":"zillow","country":"US"}'
python3 scripts/realtycrawl_api.py POST /v1/zillow/listings/search --parameters '{"location":{"kind":"bbox","bbox":[-97.82,30.2,-97.65,30.35]},"transaction":"sale","limit":1}' --max-credits 50 --idempotency-key unique-logical-search-id
```

The second command spends up to 50 credits. Set `REALTYCRAWL_API_KEY` in the environment. No automatic retries, redirects or pagination. Reuse the key and identical body after an interrupted request; a different logical operation needs a new key. HTTP failures include the request ID, while the API key remains out of output.

[Full documentation](https://docs.realtycrawl.dev)
