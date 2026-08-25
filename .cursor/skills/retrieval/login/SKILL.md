---
name: retrieval-login
description: >-
  Authenticate to the VSS retrieval backend and get a JWT via POST /api/v1/auth/login
  (VAST username/password → bearer token), verify it with GET /api/v1/auth/me, and pass
  it on later calls. Use first for any authenticated retrieval/ingest backend request.
---

# Retrieval: login

The backend authenticates the user against VMS and returns a JWT. VMS host and tenant come
from backend config, not the request. You only send username and password.

Your team's credentials and backend URL are already in the environment as `USERNAME`,
`PASSWORD`, and `INGRESS_URL`. Do not ask the user for them.

## Login

`POST /api/v1/auth/login`, body `{ "username", "password" }` → `{ access_token, token_type: "bearer", username }`.

```bash
TOKEN=$(curl -s -X POST "$INGRESS_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}" \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
```

401 means bad credentials, or the user is not valid for the tenant configured in the
backend. If you get one, the environment is misconfigured. Flag it to an organizer rather
than prompting for a different password.

## Use the token

- Most routes: header `Authorization: Bearer $TOKEN`.
- `/videos/stream`, `/videos/playback-url`: JWT as `?token=$TOKEN` query param (browser `<video>` limitation).

```bash
curl -s "$INGRESS_URL/api/v1/auth/me" -H "Authorization: Bearer $TOKEN"   # {username,email,auth_type}
```

## Notes

- This is the backend-issued JWT for the retrieval and ingest APIs. It is **separate** from raw VastDB SDK access (`retrieval/vastdb-read`).
- Token lifetime is set by backend config. On a 401 mid-session, re-login.
- Every result is ACL-filtered to this user (private rows plus public rows they can see).

## Agent instructions

1. Read `USERNAME`, `PASSWORD`, `INGRESS_URL` from the environment. Never log the password or token.
2. Cache the token for the session; re-login on 401.
3. Then proceed to `search`, `dashboard`, `videos`, `agent-qa`, etc.
