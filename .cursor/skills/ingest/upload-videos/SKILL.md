---
name: ingest-upload-videos
description: >-
  Upload 1..N fixed-length video chunks into the team chunks bucket via
  POST /api/v1/videos/upload (backend proxies to S3), with fallback to direct aws s3 cp.
  Each object should be one time-bounded MP4 chunk (~30s). Use for file-based ingest;
  for live/URL sources use ingest-stream-capture.
---

# Ingest: upload videos

Land **fixed-length MP4 chunks** in your team's ingest bucket (`$S3_CHUNKS_BUCKET`). The
pipeline watches that bucket and takes it from there: segmenter → detector → reasoner →
embedder → writer.

Everything you need is already in the environment: `INGRESS_URL`, `USERNAME`, `PASSWORD`,
`S3_ENDPOINT`, `ACCESS_KEY`, `SECRET_KEY`, `S3_CHUNKS_BUCKET`. Don't ask the user for
credentials or endpoints.

**Two upload paths:**

| Priority | Path | Notes |
|----------|------|-------|
| **1: Preferred** | `POST /api/v1/videos/upload` via `$INGRESS_URL` | Backend holds the S3 credentials and writes the object with ingest metadata |
| **2: Fallback** | `aws s3 cp` to `$S3_ENDPOINT` | Direct write. Needed only if you want to set `capture-interval`, or the API path is failing |

Do **not** use `/batch-sync/*` for simple file upload. That copies from another S3
bucket/prefix.

## Fixed length (important)

Each object should be one bounded clip, typically **~30 seconds**. Split long files locally
first; the segmenter then produces ~5s segments in `$S3_SEGMENTS_BUCKET`.

| Layer | Typical length | Where |
|-------|----------------|-------|
| Your upload | ~30s chunk | `$S3_CHUNKS_BUCKET` |
| Segmenter | ~5s | `$S3_SEGMENTS_BUCKET` |

The backend upload API does not expose `capture-interval` today. Pre-chunked ~30s MP4s are
fine; use the direct S3 path if you need to set it explicitly.

## When to use

- Upload 1..N pre-chunked MP4 files from disk.
- **Not** for live streams / RTSP → use `ingest-stream-capture`.
- Handed a YouTube link? Download it locally first, then use this skill. YouTube
  capture is not supported (see `ingest-stream-capture`).

Optional metadata options: `GET /api/v1/metadata/ingest-config` (public). See
`retrieval/list-metadata`.

## Split a long file into fixed-length chunks

```bash
ffmpeg -i warehouse_full.mp4 -c copy -f segment -segment_time 30 -reset_timestamps 1 \
  chunks/chunk_%03d.mp4
```

---

## Path 1: Backend API upload (preferred)

The backend runs inside the cluster, holds the S3 credentials, and writes the object with
ingest metadata attached.

### Login

See `retrieval/login`. In short:

```bash
TOKEN=$(curl -s -X POST "$INGRESS_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('access_token') or '')")
test -n "$TOKEN" || echo "Login failed: see troubleshooting below"
```

### Single file

```bash
curl -s -w "\nHTTP %{http_code}\n" -X POST "$INGRESS_URL/api/v1/videos/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@chunks/chunk_000.mp4" \
  -F "is_public=true" \
  -F "capture_type=warehouse" \
  -F "location=Warehouse-A" \
  -F "camera_id=cam-01" \
  -F "scenario=general" \
  -F "tags=demo"
```

Success: `{"success":true,"object_key":"<user>/20260101_123456_ab12cd34.mp4",...}`

### Many files (1..N)

```bash
for f in chunks/chunk_*.mp4; do
  echo "Uploading $f ..."
  code=$(curl -s -o /tmp/upload_resp.json -w "%{http_code}" -X POST "$INGRESS_URL/api/v1/videos/upload" \
    -H "Authorization: Bearer $TOKEN" \
    -F "file=@$f" \
    -F "is_public=true" \
    -F "capture_type=warehouse" \
    -F "location=Warehouse-A")
  echo "  HTTP $code, $(cat /tmp/upload_resp.json)"
  test "$code" = "200" || echo "  FAILED: see troubleshooting"
done
```

### API form fields

| Field | Notes |
|-------|--------|
| `file` | Required: `.mp4`, `.mov`, `.webm`, `.avi`, `.mkv` |
| `is_public` | `true` / `false` (form boolean) |
| `tags` | Comma-separated |
| `allowed_users` | Comma-separated extra viewers |
| `scenario` | e.g. `general`, `warehouse`: ignored if `custom_prompt` set |
| `custom_prompt` | Max 800 chars |
| `camera_id`, `capture_type`, `location` | Search / dashboard filters |

Limits (backend defaults): **max ~25 MB per file**, concurrent uploads queued (not
rejected).

---

## Path 2: Direct S3 (fallback)

```bash
export AWS_ACCESS_KEY_ID="$ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="$SECRET_KEY"

aws s3 cp chunks/chunk_000.mp4 \
  "s3://${S3_CHUNKS_BUCKET}/${USERNAME}/$(date -u +%Y%m%d_%H%M%S)_$(uuidgen | cut -c1-8).mp4" \
  --endpoint-url "$S3_ENDPOINT" \
  --metadata \
camera-id=cam-01,capture-type=warehouse,location=Warehouse-A,scenario=general,\
capture-interval=30,is-public=true,owner=$USERNAME,original-filename=chunk_000.mp4
```

`aws s3 sync` works the same way. Set `capture-interval` to match your chunk duration.

### S3 metadata keys (kebab-case)

| Metadata key | Notes |
|--------------|-------|
| `camera-id`, `capture-type`, `location` | ingest filters / search |
| `scenario`, `custom-prompt` | reasoning preset |
| `tags`, `allowed-users` | comma-separated |
| `is-public`, `owner` | ACL |
| `capture-interval` | nominal chunk length (seconds): **S3 path only** today |

---

## Agent workflow

1. Confirm files are **fixed-length chunks** (~30s); split with ffmpeg if needed.
2. Get a JWT (`retrieval/login`).
3. `POST /api/v1/videos/upload` for each file. Report HTTP code + JSON body per file.
4. On failure, see the table below. Don't silently retry the same call.
5. After uploads, check `GET /api/v1/dashboard/stats` (`retrieval/dashboard`). Do not tell the user their video is searchable until explore/dashboard shows the parent.

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| HTTP **200** but search empty for a few minutes | Pipeline lag | Normal. Watch `pipeline_alignment` in `retrieval/dashboard`. |
| HTTP **400** `Invalid file extension` | Non-video extension | Use `.mp4` (or an allowed extension from `GET /api/v1/config`). |
| HTTP **413** `File too large` | Chunk over the 25 MB default | Shorten the chunk (e.g. 30s → 15s) or re-encode smaller. |
| HTTP **401** | Token expired mid-session | Re-login. If a fresh login also 401s, the environment is misconfigured. Tell an organizer. |
| HTTP **500** | Backend or S3 problem on the cluster | Not something you can fix. Tell an organizer; the S3 fallback will likely fail too. |
| `curl` connection failure to `$INGRESS_URL` | Your stack may be restarting | Retry once, then tell an organizer. The VM is pre-wired, so this is not a local config problem. |
| `aws s3 cp` **403 / AccessDenied** | Wrong bucket or key in the command | Confirm you used `$S3_CHUNKS_BUCKET`, `$ACCESS_KEY`, `$SECRET_KEY` from the environment rather than typing values. |

## Flow

```
fixed-length MP4(s) → $S3_CHUNKS_BUCKET  (API proxy or direct S3)
  → segmenter (~5s) → $S3_SEGMENTS_BUCKET → detector → reasoner → embedder → writer
```
