# Ingest

Video is already indexed for your team. Ingest here means **re-running footage through the
pipeline with a different prompt**, not uploading new files.

## Skills

| Skill | Use it to |
|-------|-----------|
| [reingest-videos](reingest-videos/SKILL.md) | Re-run a whole indexed video or stream with a new prompt or metadata |
| [reingest-chunk](reingest-chunk/SKILL.md) | Re-run one specific chunk, found by filename, scene, date, or camera |

## Why re-ingest

Every segment is described by a model following an ingestion prompt. Anything that prompt
didn't ask about was never written down, so it can't be searched for. Changing the prompt
and re-ingesting is how you get descriptions that match what you're building.

`reingest-videos` is the one to reach for. Use `reingest-chunk` when the user names a single
clip and only that clip should be re-run.

Both take a few minutes: each segment is captioned, embedded, and detected again before it
becomes searchable. Check progress with `retrieval/dashboard`.

Auth: JWT via `retrieval/login`. Credentials and endpoints are already in your environment.
