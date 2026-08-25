---
name: retrieval-vastdb-read
description: >-
  Read the VSS VastDB store directly with the vastdb Python SDK, list catalog
  (databases/schemas/tables) and inspect rows in your team's collection and prompts table.
  Use for raw DB inspection/debugging that bypasses the backend API (no JWT), e.g.
  verifying what actually got written.
---

# Retrieval: VastDB read

Direct, backend-independent access to the store the pipeline writes and the backend
queries. Uses the `vastdb` Python SDK, not the JWT backend. Best for debugging "did this
segment actually land in VastDB?".

## Your team's tables

| Thing | Environment variable |
|-------|----------------------|
| Database (bucket) | `$VASTDB_BUCKET` |
| Schema | `$VDB_SCHEMA` |
| Main table | `$VDB_COLLECTION` (segment rows: `source`, `original_video`, `reasoning_content`, `vectors` (256d text), `vectors_visual`, metadata, timing) |
| Prompts table | `$VDB_PROMPTS_COLLECTION` (prompt-suggester output) |

Endpoint and credentials are already in the environment as `VDB_ENDPOINT`, `ACCESS_KEY`,
`SECRET_KEY`. `VDB_ENDPOINT` may point at the same host as `S3_ENDPOINT`; use
`VDB_ENDPOINT` so the intent is clear. The endpoint is reachable directly from your VM, so
there is no tunnel to set up and no `.env` to create. The `vastdb` SDK is already
installed.

## List the catalog

[list_catalog.py](list_catalog.py) prints database → schema → tables via the SDK
(`tx.catalog()`).

```bash
python .cursor/skills/retrieval/vastdb-read/list_catalog.py                      # whole catalog
python .cursor/skills/retrieval/vastdb-read/list_catalog.py --bucket "$VASTDB_BUCKET"
```

## Read rows

```python
import os, vastdb

session = vastdb.connect(
    endpoint=os.environ["VDB_ENDPOINT"],
    access=os.environ["ACCESS_KEY"],
    secret=os.environ["SECRET_KEY"],
    ssl_verify=False,
)
with session.transaction() as tx:
    table = (tx.bucket(os.environ["VASTDB_BUCKET"])
               .schema(os.environ["VDB_SCHEMA"])
               .table(os.environ["VDB_COLLECTION"]))
    # Exclude vector columns from projections (large / not needed for inspection):
    cols = [c.name for c in table.columns() if c.name not in ("vectors", "vectors_visual")]
    rows = table.select(columns=cols).read_all().to_pylist()
    print(len(rows), rows[0] if rows else "empty")
```

Selecting `vectors`/`vectors_visual` (fixed-size lists) can fail without the vector-select
patch the pipeline functions use. For inspection, just exclude them.

## Common checks

- **Row count / recent writes**: count rows, sort by `timestamp`/`upload_timestamp`.
- **Missing segment**: filter by `original_video` or `source` to confirm a specific clip was written (the writer skips duplicate `source`).
- **Dims**: `vectors` length must be **256** (Cosmos-Embed1).

## Agent instructions

1. Run `list_catalog.py` first to confirm connectivity and see what tables exist.
2. Read endpoint, keys, and table names from the environment. Never hardcode them and never print `SECRET_KEY`.
3. Exclude vector columns unless you specifically need them.
4. This bypasses backend ACLs, so it sees every row in your team's collection. For user-scoped views use `retrieval/dashboard` or `retrieval/videos`.
5. This is your team's own database. Read freely; don't write to it from here.
