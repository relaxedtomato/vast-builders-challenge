---
name: ask-cosmos
description: >-
  Help a team get unstuck by preparing a question worth answering, with the relevant details
  and team name, ready to paste into a Cosmos post or support ticket. Never posts anywhere. Runs the
  health check first so the answer includes whether the stack is healthy.
  Use when someone is blocked, something returns an error they can't place, or they ask how
  to get help.
---

# Ask Cosmos

Most blockers are one of three things: the stack is unhealthy, a filter value doesn't exist,
or the prompt never described what they're searching for. Check those before asking anyone.

## First, check it isn't the stack

Run the health check from `retrieval/login` and `retrieval/dashboard`: get a token, then
read the dashboard. Keep the output; it goes in the question.

If login fails on a fresh attempt, or the dashboard doesn't answer, that's an environment
problem and an organizer needs to see it. Say so plainly rather than suggesting workarounds.

## Then, check the two common ones

- **Search returns nothing.** Confirm the filter values exist with `retrieval/list-metadata`
  before assuming the search is broken. Then consider whether the ingestion prompt ever
  described what they're looking for; if not, that's `ingest/reingest-videos`, not a bug.
- **Something is still indexing.** Re-ingest takes minutes. Check the dashboard rather than
  retrying the search.

## Write the question

Show the team the finished question before they share it. Keep it under 120 words, and
use exactly this layout, one line per field:

```
Team: <team name>
Trying to: <one sentence>
Happened: <what failed, with the exact error, at most 3 lines or 300 characters>
Tried: <one line, or "nothing yet">
Health check: <login ok / failed, dashboard ok / failed / not run>
```

Rules for the fields:
- **Team** is `$USERNAME` (or `$PIPELINE`). If neither is set, use the name in
  `/config/<team>.config`. If you still can't tell, write `unknown`; don't ask.
- **Happened** quotes the error text, not a paraphrase. If it's longer than the cap, keep
  the first and last lines and cut the middle with `...`.
- No stack traces, logs, file dumps or response bodies. Say which command failed instead.

## Keep it safe to share

Nothing from `config.example` may appear in the question. That means no variable's value,
and no value that came from one: endpoints, bucket and collection names, the pipeline name,
usernames, passwords, keys, tokens, and model ids. Refer to a variable by its name if you
must (for example, "`S3_ENDPOINT` is set"), never by its value. The team name is the one
exception, and it goes only in the `Team` line.

Before showing the draft, replace anything specific with a placeholder:

| Replace | With |
|---------|------|
| URLs and hostnames | `<url>` |
| IP addresses | `<ip>` |
| Anything after `Bearer`, `token=`, `key=`, `password=` | `<redacted>` |
| Bucket, collection, or pipeline names | `<name>` |
| Email addresses and personal names | `<redacted>` |

Then check the draft against your own environment: if any environment variable's value
appears in it, mask that too. Do this without printing the values.

A question with the error text and the health check attached usually gets answered in one
reply; a question that says "search isn't working" needs three.

## Hand it over

This skill prepares the question; it does not post it anywhere. Give the team the one block
of text above to copy. Apply the redaction in "Keep it safe to
share" first.

## Agent instructions

1. Run the health check before anything else, and include its result in the question.
2. Never include anything from `config.example` in the question text, and apply the
   placeholders in "Keep it safe to share" before showing the draft.
3. If the cause is one of the known ones above, say so and offer the fix instead of drafting
   a question.
4. Never post, send, or call any external service with the question. Show the draft and let
   the team decide where it goes.
