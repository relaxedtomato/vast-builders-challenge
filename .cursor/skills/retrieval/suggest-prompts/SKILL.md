---
name: retrieval-suggest-prompts
description: >-
  Fetch AI-generated search prompt chips and key events via GET /api/v1/suggestions,
  produced by the prompt-suggester enrichment job from recent VastDB segments. Use to
  seed the search box with relevant example queries or surface notable recent events.
---

# Retrieval: suggest prompts

Returns the latest batch of **search prompt suggestions** + **key events** the enrichment `prompt-suggester` computed from recent segments and wrote to VastDB (`$VDB_PROMPTS_COLLECTION`). Requires a JWT (`retrieval/login`).

## Request — `GET /api/v1/suggestions`

```bash
curl -s "$INGRESS_URL/api/v1/suggestions" -H "Authorization: Bearer $TOKEN"
```

Content is ACL-filtered to the caller. Use the returned prompts as ready-to-run `query` strings for `retrieval/search`, and key events as highlights.

## May be empty early in the day

These come from a scheduled enrichment job that reads recent segments and writes to
`$VDB_PROMPTS_COLLECTION`. It runs on the shared stack, not something you deploy.

An empty response is normal and not a bug. It usually means the job hasn't run since your
team started ingesting, or the lookback window found no new segments. Check
`retrieval/dashboard` to confirm segments are indexing, then fall back to writing your own
`query` strings for `retrieval/search`. If it stays empty after your videos are clearly
indexed, mention it to an organizer.

## Agent instructions

1. Ensure a JWT.
2. Treat items as suggestions, not guarantees — feed prompts into `retrieval/search`.
3. If empty, check the enrichment pipeline/trigger and recent ingest before assuming a bug.
