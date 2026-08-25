# Ingest

Get video into the pipeline by landing **fixed-length MP4 chunks** in your team's
`$S3_CHUNKS_BUCKET`. The ingest pipeline reacts to S3 events only. It does not call the
streaming or batch-sync services.

## Skills

| Skill | Mechanism | Purpose |
|-------|-----------|---------|
| [upload-videos](upload-videos/SKILL.md) | `POST /videos/upload`, or direct `aws s3 cp` | Upload 1..N fixed-length chunk files from disk |
| [stream-capture](stream-capture/SKILL.md) | `POST /streaming/start`, `GET /status`, `POST /stop` | Capture from an RTSP / HTTP / file-URL source (not YouTube) |

## Fixed length (important)

Chunks are **not** arbitrary full-length videos. Each object should be one time-bounded
clip (typically ~30s). The segmenter then splits it into ~5s segments in
`$S3_SEGMENTS_BUCKET`, and those segments are what get captioned, embedded, and indexed.

| Path | How chunks arrive | Nominal chunk size |
|------|-------------------|--------------------|
| Upload | You put fixed-length MP4s in `$S3_CHUNKS_BUCKET` | ~30s (your choice) |
| Stream API | The capture service writes them for you | `capture_interval` (default 30s) |
| Segmenter output | `$S3_SEGMENTS_BUCKET` | ~5s |

**Ingest status:** after either path, use `retrieval/dashboard`
(`GET /api/v1/dashboard/stats`) for S3 vs VastDB alignment and ingest health. Indexing
takes a few minutes; a video isn't searchable the instant upload returns 200.

Auth: JWT via `retrieval/login`. Credentials and endpoints are already in your
environment.
