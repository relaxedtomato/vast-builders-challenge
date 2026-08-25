---
name: ingest-stream-capture
description: >-
  Trigger, monitor, and stop live/stream capture via the backend streaming API:
  POST /api/v1/streaming/start, GET /status, POST /stop. The stream service writes
  fixed-length chunks to the team chunks bucket (same ingest path as S3 upload). Not for
  uploading local files — use ingest-upload-videos for direct S3 puts.
---

# Ingest: trigger / status / stop stream

## This skill = API only (you do not upload files)

| | **stream-capture** (this skill) | **upload-videos** (other skill) |
|---|--------------------------------|----------------------------------|
| What you do | Call `POST /streaming/start` (+ status/stop) | Upload fixed-length MP4s to `$S3_CHUNKS_BUCKET` |
| Source | RTSP, HTTP stream, remote file URL | Local files on disk (pre-chunked ~30s) |
| Who writes S3 | the capture service (automatic) | You (upload API or S3) |

Both paths land **fixed-length** chunks in `$S3_CHUNKS_BUCKET`. The ingest pipeline only reacts to S3 objects; it does not call the streaming API.

**This skill:** you trigger capture via API; the stream service reads the source, splits at `capture_interval` (default 30s), and uploads each chunk to S3 for you.

**Not this skill:** if you already have MP4 files, split them locally and use `ingest-upload-videos` — no streaming API involved.

Requires a JWT (`retrieval/login`). Only **one capture runs at a time** (service returns "Capture is already running").

## Source support

Supported for this event: **RTSP streams, HTTP streams, and remote file URLs**, read via
OpenCV/FFmpeg.

**Default source: `$RTSP_URL`.** A looping sample feed is published for the event; use that
value unless the user names a different source. It's a default, not a restriction — your own
camera or phone stream is fair game, it's just not provisioned or supported, so debug source
problems before blaming the pipeline.

If `$RTSP_URL` is unset, no stream was provisioned for this city. Say so and use
`ingest/upload-videos` instead; don't send an empty URL.

**YouTube is not supported.** The field is named `youtube_url` for historical reasons and
the service does have a yt-dlp path, but it isn't enabled here — YouTube throttles and
bot-checks shared egress, which fails unpredictably mid-event. Put your RTSP/HTTP/file URL
in `youtube_url` anyway; that's just what the field is called. If someone hands you a
YouTube link, download it beforehand and use `ingest/upload-videos` instead.

## Prefill S3 credentials

The streaming API takes S3 credentials **per request**. Get them from `/prefill` rather
than typing them; it returns the values the backend already holds for your team.

```bash
curl -s "$INGRESS_URL/api/v1/streaming/prefill" -H "Authorization: Bearer $TOKEN"
```

## Trigger new stream

`POST /api/v1/streaming/start`:

```bash
curl -s -X POST "$INGRESS_URL/api/v1/streaming/start" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d "{
    \"youtube_url\": \"$RTSP_URL\",
    \"access_key\": \"$ACCESS_KEY\", \"secret_key\": \"$SECRET_KEY\", \"s3_endpoint\": \"$S3_ENDPOINT\",
    \"bucket_name\": \"$S3_CHUNKS_BUCKET\",
    \"name\": \"capture\",
    \"capture_interval\": 30,
    \"camera_id\": \"\", \"capture_type\": \"\", \"location\": \"\", \"scenario\": \"\"
  }"
```

| Field | Req | Notes |
|-------|-----|-------|
| `youtube_url` | yes | RTSP / HTTP / file URL, despite the field name. Defaults to `$RTSP_URL`. Not YouTube. |
| `access_key`/`secret_key`/`s3_endpoint` | yes | usually from `/prefill` |
| `bucket_name` | yes | set to `$S3_CHUNKS_BUCKET` explicitly |
| `capture_interval` | no | 1–300s fixed chunk length (default 30) |
| `name` | no | filename prefix |
| metadata fields | no | written as S3 object metadata on each chunk |

(The capture service itself also accepts `max_duration` and `s3_prefix`, but the backend proxy does not forward those, so you can't set them from here.)

## Status (stream + ingest signals)

**Stream capture status:**

```bash
curl -s "$INGRESS_URL/api/v1/streaming/status" -H "Authorization: Bearer $TOKEN"
```

Returns `is_running`, `current_config` (secrets redacted), `temp_files_count`. VOD auto-stops at end; live runs until `/stop`.

**Ingest pipeline status** (chunks indexed after stream writes to S3):

```bash
curl -s "$INGRESS_URL/api/v1/dashboard/stats" -H "Authorization: Bearer $TOKEN"
```

See `retrieval/dashboard` — S3 vs VastDB inventory, ingest quality, recent videos.

## Stop stream

```bash
curl -s -X POST "$INGRESS_URL/api/v1/streaming/stop" -H "Authorization: Bearer $TOKEN"
```

## Flow

```
stream source → capture_interval chunks → $S3_CHUNKS_BUCKET
  → segmenter (~5s) → $S3_SEGMENTS_BUCKET → detector → reasoner → embedder → writer
```

A 30s chunk → ~6 × 5s segments (modulo trim/cap).

## Agent instructions

1. Ensure a JWT; get S3 values from `/prefill` rather than asking the user.
   Use `$RTSP_URL` as the source unless the user names another.
2. Always set `bucket_name` to `$S3_CHUNKS_BUCKET`.
3. Check `/streaming/status` before starting — only one capture at a time, per team.
4. Chunks are **fixed length** (`capture_interval`); same contract as the upload skill.
5. Confirm objects are arriving and indexing via `retrieval/dashboard`.
6. Long live streams keep writing until you `/stop`. Stop a capture you're done with so it doesn't fill the bucket.
