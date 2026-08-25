# VAST Builders Challenge

Spend the day building with video. The infrastructure is already running, so you
skip straight to the interesting part: turning hours of video into something that
searches, reasons, and acts.


---

## 1. Kickoff

### What you're building
An app that understands video and does something with it. Search hours of
footage in plain language, ask what happened, detect and track objects, or fire an action
when something matters. Pick one idea and ship a working app by end of day.

### The Tech Stack
Video runs through a pipeline that understands and indexes it.

```
  INGEST         UNDERSTAND              INDEX          SEARCH / ASK        ACT
  video  ─▶  segment·caption·detect  ─▶  vectors +  ─▶  semantic search ─▶  your agent
            ·embed (Cosmos + YOLO)        metadata       · Q&A · metadata    (Slack, webhook,
                                                                             app, report)
       └────────────── pre-built, already running ──────────────┘      └─ you build ─┘
                                                                     (agent logic: LLM via W&B)
```
<!-- IMAGE: architecture diagram, replacing the ASCII block. Alt: "Pipeline flow from
     video ingest through indexing and search to the agent you build." -->

Everything under "pre-built, already running" is done for you. The pipeline ingests,
understands, and indexes your video, and the models it calls are already deployed and
serving. You build what comes after: the app that searches the index and acts.

<!-- TODO: can we simulate ingestion for testing agents, via re-ingestion? -->

<!-- TODO: describe the VSS UI as a pre-built example, and as the way to sanity-check
     ingest and explore what's indexed. -->
<!-- TODO: link the running app. Is the UI on $INGRESS_URL (what path?) or does it need
     its own env var? Attendees should click into their own instance. -->
The VSS search UI is an example of what you can build, already built and running. Use it to test the pipeline and see what's indexed while you build.

<!-- IMAGE: VSS search UI showing results. Alt: "The VSS search interface showing video
     segments matching a natural-language query." -->

### What you have
- A **VSS instance** running for your team: the pipeline ingests, understands, and indexes
  your video. Cosmos Reason, Cosmos Embed, and YOLO run inside it on CoreWeave GPUs; you
  don't call them directly, you query the vectors generated.
- **Serverless LLM inference from Weights & Biases** for your agent's own logic.
- A **VM with Cursor** pre-loaded, with this repo cloned and your stack credentials and
  endpoints already set as environment variables.
- A set of **Cursor skills** that drive ingest and search in plain language.

### How the day runs
| Time | What |
|------|------|
| 8:30 | Doors + breakfast |
| 9:00 | Opening remarks |
| 9:30 | Build begins |
| 12:30 | Lunch |
| 4:30 | Demos |
| 6:30 | Closing + awards |

### What "done" looks like
Something that runs, not slides. A small app, agent, or a dashboard. Judging rewards a
clear use case and clever use of search plus metadata over polish. Scope it small enough
to demo live.

<!-- TODO: judging criteria. Decide owner: §7 here, or the event page. Needs the rubric
     (categories, weightings, judges, demo length, is code assessed?) and a link from this
     sentence. -->


---

## 2. Launch your VM

No setup. Nothing to install, no config to paste, no keys to type.

1. Open the VM link for your team. <!-- TODO: confirm delivery channel (email / Luma / on-site card) and the one-click flow. -->
2. Wait for the VM to load.
3. If Cursor asks you to sign in, use the email you applied with. Expect one or two tries;
   that's normal.

That's it. You're in.

### Work from the agent
Drive the day from the **Cursor Agent (CLI)**. Describe what you want in plain language
and let the code agent build. That's how the skills are meant to be used.
Alternatively, you can use the IDE.

Start the agent in the terminal:

```sh
cursor-agent            # start an interactive agent session
```
<!-- TODO: confirm the Cursor Agent CLI command and flags; replace the example. -->
<!-- TODO: does signing into the Cursor IDE also authenticate the CLI agent, or is a
     separate sign-in needed? Verify with Cursor. -->

From there, describe the task and the agent picks the matching skill. Start with
[Meet your skills](#3-meet-your-skills), then ingest a clip and search it.

<!-- IMAGE: the loaded VM. Alt: "The workshop VM with Cursor open on the Builders
     Challenge repo." -->
<!-- TODO: walk through what attendees see on load. Screenshot or short clip. -->

### If something looks off
Run the health check in the Reference section to confirm each piece is reachable, then
flag an organizer if anything is red.

## 3. Meet your skills

Your starter code lives in `.cursor/skills/`, split into `ingest/` and `retrieval/`. Each
skill teaches the agent one piece of the stack: the endpoint, the request, the response, and
what to do when it fails.

Describe what you want and the agent loads the matching skill.

```
"upload the clips in ~/samples and tell me when they're searchable"
"find people near the entrance after 6pm"
"summarize what happens in the warehouse video"
```

Skills read what they need from environment variables, so nothing should ask you for a
password or a URL. If something isn't working, ask for help.

### Ingest: Adding Video

| Skill | Use it to |
|-------|-----------|
| `upload-videos` | Upload video files from disk. Handles the chunking rules and reports what indexed. |
| `stream-capture` | Capture from a live RTSP or HTTP stream into the pipeline. |

Both land video in the same place and the pipeline takes over. Two things that catch
people out:

**Video is ingested in ~30 second chunks**, not whole files. The skill splits long files
locally with ffmpeg, then uploads each chunk.

**Indexing takes a few minutes.** Upload succeeding means the file landed, not that it's
searchable. Ask the agent to confirm before you go looking for it.

> 💡 **Your prompt decides what gets indexed.** Cosmos Reason captions every segment using
> an ingestion prompt. Anything it doesn't ask about never gets described, so you can't
> search for it later.
>
> Pick your prompt before ingesting at volume. On a construction site you might ask it to
> describe safety gear. In a public space you might ask how many people are in frame.
> Ingest everything with the safety prompt, then switch to building the crowd monitor, and
> your searches come back empty, because no caption ever mentioned a count. Fixing that
> means ingesting it all over again.
>
> Set the prompt per upload with `custom_prompt` (800 characters max), or pick a `scenario`
> preset.

<!-- TODO: paste the default ingestion prompt verbatim, from the pipeline config /
     VDB_PROMPTS_COLLECTION. -->
<!-- TODO: list the `scenario` presets and what each asks for, plus a stable reference
     for `custom_prompt`. -->
<!-- TODO: net-new `reingest` skill. Re-run captioning/embedding with a different prompt,
     without re-uploading. Open: granularity (segment / filtered set / whole video); the
     writer skips duplicate `source`, so overwrite or version? (`dashboard` already reports
     `re_ingest_rows`, find out what that does first); cost cap on shared Cosmos endpoints.
     Covers the §1 re-ingestion note too. -->
<!-- TODO: can a team change the pipeline DEFAULT prompt, or only override per upload? If
     editable, that's a missing skill and the advice above changes. -->

### Retrieval: Searching Video

| Skill | Use it to |
|-------|-----------|
| `search` | Find moments matching a description, with filters for time, location, camera, tags. |
| `agent-qa` | Ask a question and get an answer with evidence, instead of a list of hits. |
| `videos` | Browse what's indexed, play a clip, read its captions and detections, summarize a whole video. |
| `dashboard` | Check what's indexed and whether ingest is healthy. |
| `suggest-prompts` | Get generated example queries and notable recent events. |

Worth knowing: `vastdb-read` queries the database directly, for when you don't
believe what the API is telling you.

<!-- TODO: replace both tables with a pointer to the overview skill (/pipeline-skills-101)
     once it exists. See DECISIONS.md "Parked". -->
<!-- TODO: add `cosmos` and `vast-builder-submission` to the tables once written. -->


## 4. Ingest and search



## 5. Build

<!-- TODO: 4-6 use-case sparks (search hours of footage, ask-your-video Q&A, incident
     board, alert-on-event agent, highlight reel) + link the Request for Builds doc. Teams
     re-decide scope in the morning regardless. -->

<!-- TODO: absorbs old §6 + §7. Needs: use-case sparks (above); the build loop (pick a
     use case, ingest for it, query, wrap it) kept short; where agent logic runs (W&B) with
     a minimal example. -->

## 6. Reference

<!-- TODO: lookup material, absorbs old §8 + §9. Needs: health check (one command per
     piece, what healthy looks like, what to do when it isn't); getting help (organizers,
     event Slack, `cosmos` skill); the full env var list (S3 buckets, VastDB collections,
     ingress, W&B endpoint) pointing at config.example; and $PIPELINE and $RTSP_URL,
     which no skill provides. -->

## 7. Submit and demo

<!-- TODO: absorbs old §10 + §11. Needs: how to submit (`vast-builder-submission` skill),
     the judging rubric (see §1 TODO), and demo logistics (length, order, what's on screen). -->
