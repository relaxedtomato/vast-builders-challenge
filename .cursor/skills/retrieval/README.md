# Retrieval

Query the indexed archive through the backend API at `$INGRESS_URL`, prefix `/api/v1`.
Every route except `/metadata/ingest-config` needs a JWT — start with `login`.

## Skills → routes

| Skill | Route(s) |
|-------|----------|
| [login](login/SKILL.md) | `POST /auth/login`, `GET /auth/me` |
| [search](search/SKILL.md) | `POST /search` (+ `tools/search`, `agent/search-and-answer`) |
| [list-metadata](list-metadata/SKILL.md) | `GET /metadata/schema`, `/metadata/values`, `/metadata/ingest-config` |
| [dashboard](dashboard/SKILL.md) | `GET /dashboard/stats` |
| [suggest-prompts](suggest-prompts/SKILL.md) | `GET /suggestions` |
| [videos](videos/SKILL.md) | `/videos/explore`, `/stream`, `/playback-url`, `/detections`, `/metadata`, `POST /videos/synthesize` |
| [agent-qa](agent-qa/SKILL.md) | `POST /agent/ask`, `/agent/search-and-answer`, `tools/*` |
| [vastdb-read](vastdb-read/SKILL.md) | raw VastDB via the Python SDK (bypasses the backend) |

## Auth pattern

```bash
TOKEN=$(curl -s -X POST "$INGRESS_URL/api/v1/auth/login" -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
curl -s "$INGRESS_URL/api/v1/..." -H "Authorization: Bearer $TOKEN"
```

`/videos/stream` and `/videos/playback-url` take the JWT as a `?token=` query param (HTML5
`<video>` can't set headers); everything else uses the `Authorization` header.

## Routes that do NOT exist (don't invent)

No `/reports`, `/alerts`, `/analytics`, `/videos/ask`, `/tags`, `/locations`, or
`/extra-metadata`. Reporting and summaries are `POST /videos/synthesize`; Q&A is
`POST /agent/ask`; filter discovery is `/metadata/*`; aggregates are `/dashboard/stats`.

## Backing store

VastDB `$VASTDB_BUCKET` / `$VDB_SCHEMA` / `$VDB_COLLECTION` (plus
`$VDB_PROMPTS_COLLECTION`), with Cosmos-Embed1 256-dim hybrid vectors (`vectors` for
caption text, `vectors_visual` for the visual embedding). All row access through the
backend is ACL-filtered to the calling user.
