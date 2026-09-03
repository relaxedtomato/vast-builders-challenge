# VAST Builders Challenge: Video Agents

Spend the day building with video. The infrastructure is already running, so you
skip straight to the interesting part: turning hours of video into something that
searches, reasons, and acts.


---

## 1. Kickoff

### What you're building
An app that understands video and does something with it. Search hours of
footage in plain language, ask what happened, detect and track objects, or call an action
when something matters. Pick one idea and ship a working app by end of day.

### The Builders Stack
Video runs through a pipeline that understands and indexes it:

```
  INGEST          UNDERSTAND                 INDEX          SEARCH / ASK       ACT
  video   ─▶  segment                  ─▶  vectors +  ─▶  semantic search ─▶  your app
              describe  (Cosmos Reason)    metadata       · Q&A · metadata    (alert, report,
              embed     (Cosmos Embed)                                         dashboard, bot)
              detect    (YOLO)
       └─────────────── pre-built, already running ───────────────┘      └─ you build ─┘
                                                                    (your app's reasoning: W&B)
```
<!-- IMAGE: architecture diagram, replacing the ASCII block. Alt: "Pipeline flow from
     video ingest through indexing and search to the agent you build." -->

Everything under "pre-built, already running" is done for you. The pipeline ingests,
understands, and indexes video, and the models it calls are already deployed and
serving. You build the app that searches and acts.

<!-- TODO: can we simulate ingestion for testing agents, via re-ingestion? -->

<!-- TODO: describe the VSS UI as a pre-built example, and as the way to sanity-check
     ingest and explore what's indexed. -->
<!-- TODO: confirm the UI path. The guide now says the UI is at $INGRESS_URL; check
     whether it's served at the root or on a subpath, and correct if so. -->
**The VSS search UI.** Type what you want to see in plain words and it returns matching
clips. Open `$INGRESS_URL` and log in with your team's `USERNAME` and `PASSWORD`.

Three tabs:
**Search** to query videos, **Explore** to browse what's indexed, and **Dashboard** to get stats:

![The VSS search interface with the search box, filters, and suggested prompts](docs/images/vss-search.png)

> 💡 The VSS search UI runs on the same API as the skills (`.cursor/skills`) you will be using. It's a working example of what
> you can build, and a quick way to see what's indexed while you work.

### What you have
- A **VSS instance** running for your team: the pipeline ingests, understands, and indexes
  your video. Cosmos Reason, Cosmos Embed, and YOLO run inside it on CoreWeave GPUs; you
  don't call them directly, you query the vectors generated.
- **Serverless LLM inference from Weights & Biases** for your app's own logic.
- A **VM with Cursor** pre-loaded, with this repo cloned and your  credentials and
  endpoints already available as environment variables.
- A set of **skills** that drive the pipeline in plain language. See
  [Meet your skills](#3-meet-your-skills).

<!-- HIDDEN for the dry run: restore the schedule before the real event.
     ### How the day runs
     | Time | What |
     |------|------|
     | 8:30 | Doors + breakfast |
     | 9:00 | Opening remarks |
     | 9:30 | Build begins |
     | 12:30 | Lunch |
     | 4:30 | Demos |
     | 6:30 | Closing + awards |
-->

### What "done" looks like
A small app, agent, or a dashboard. A clear use case.

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

That's it. You're in!

### Coding Agent
Drive the day from the **Cursor Agent (CLI)**. Describe what you want in plain language
and let the code agent build. That's how the skills are meant to be used.
Alternatively, you can use the IDE.

Start the agent in the terminal:

```sh
cd ~/vast-builders-challenge   # the agent works from the current directory
agent                          # start an interactive session
```

Once it's running, set the model to Auto to save tokens:

```
/model
```


<!-- TODO: confirm the Cursor Agent CLI command and flags; replace the example. -->
<!-- TODO: does signing into the Cursor IDE also authenticate the CLI agent, or is a
     separate sign-in needed? Verify with Cursor. -->

From there, describe the task and the agent picks the matching skill. Start with
[Meet your skills](#3-meet-your-skills), then ingest a clip and search it.

> 💡 **Copy and paste in the VM.** In the terminal it's `Ctrl+Shift+C` and `Ctrl+Shift+V`

<!-- IMAGE: the loaded VM. Alt: "The workshop VM with Cursor open on the Builders
     Challenge repo." -->
<!-- TODO: walk through what attendees see on load. Screenshot or short clip. -->

### If something looks off
Run the health check in the Reference section, then flag an organizer if something's wrong.

## 3. Meet your skills

The skills live in `.cursor/skills/`, split into `ingest/` and `retrieval/`. Each
skill guides the coding agent: the endpoint, the request, the response, and
what to do when it fails.

Describe what you want and the coding agent loads the matching skill.

```
"re-ingest the warehouse video with a prompt about safety gear"
"find people near the entrance after 6pm"
"summarize what happens in the warehouse video"
```

Skills read what they need from environment variables, so nothing should ask you for a
password or a URL. If something isn't working, ask for help.

### Ingest: re-running video

Your team's video is already indexed. Ingest here means running it through the pipeline
again with a different prompt, so the descriptions match what you're building.

| Skill | Use it to |
|-------|-----------|
| `reingest-videos` | Re-run a whole indexed video with a new prompt or metadata |
| `reingest-chunk` | Re-run one specific chunk, found by filename, scene, date, or camera |

**Re-ingesting takes a few minutes.** Every segment is described, embedded, and detected
again before it becomes searchable. Ask the agent to confirm before you go looking.

> 💡 **The prompt decides what gets indexed.** Cosmos Reason describes every segment
> following an ingestion prompt. Anything it doesn't ask about never gets written down, so
> you can't search for it later.
>
> On a construction site you might ask it to describe safety gear. In a public space you
> might ask how many people are in frame. Search the existing index for what your idea
> needs; if it isn't there, that's what re-ingesting is for.
>
> Set the prompt with `custom_prompt` (800 characters max), or pick a `scenario` preset.

### Retrieval: Searching Video

| Skill | Use it to |
|-------|-----------|
| `search` | Find moments matching a description, with filters for time, location, camera, tags. |
| `agent-qa` | Ask a question and get an answer with evidence, instead of a list of hits. |
| `videos` | Browse what's indexed, play a clip, read its captions and detections, summarize a whole video. |
| `dashboard` | Check what's indexed and whether ingest is healthy. |
| `suggest-prompts` | Get generated example queries and notable recent events. |

Worth knowing: `vastdb-read` queries the database directly, for when you want to check the database contents.

<!-- TODO: replace both tables with a pointer to the overview skill (/pipeline-skills-101)
     once it exists. See DECISIONS.md "Parked". -->
<!-- TODO: add `cosmos` to the tables once written. `submission` exists but is covered in
     section 7, so decide whether it also needs a row here. -->


## 4. Search and re-ingest

Before you build anything, run one loop by hand. It tells you the whole stack is working
and shows you the one thing that decides what you can build.

### Search what's there

Your team's index already has video in it, so start by looking:

```
what's in the index? show me a few examples
```

Then search for something specific to your idea:

```
find the moment where <something you care about> happens
```

You get back ranked segments with timestamps, scores, and the description the model wrote.
Play one to confirm it's the moment you meant.

### Ask instead of search

```
what happens in <one of those videos>?
```

Same index, different kind of answer. The first hands you moments. The second reads those
moments and writes you an answer.

Do you want to show someone the clip, or tell them what happened? Most of designing a video
app is picking one.

### Find what's missing

Search for something your idea needs that the existing descriptions probably don't mention.
Counts of people. What someone is carrying. Whether a vehicle stopped.

If it comes back empty, that's not a broken search. It means the ingestion prompt never
asked about it, so nothing was written down.

### Re-ingest with your prompt

```
re-ingest <that video> with a prompt that describes <what your app needs>
```

The agent loads `reingest-videos`, shows you what it's about to re-run, and asks for the
prompt. Give it a few minutes, then run the same search again. This time it matches.

To watch progress, ask `is it done yet?` or open the Dashboard tab.

![The VSS UI dashboard showing segment counts, indexed clips, and ingest quality](docs/images/vss-dashboard.png)

> 💡 That gap, between what you searched for and what the prompt asked about, is the thing
> to keep in mind all day. Everything you can build depends on what the descriptions say.

### That's the whole loop

Search, ask, re-ingest, search again. Everything you build today sits on those steps. If
they worked, your stack is healthy and you can start building.

If any of them didn't, run the health check in the Reference section.

## 5. Build

You have a working index and you know how to query it. The rest of the day is what you
build on top.

### What video you have

[describe video sources]

### The loop

1. **Pick a use case**
2. **Build an app or agent**
3. **Deploy and iterate**

If the existing captions cover what you need, you never have to think about prompts. If they
don't, ingest the footage again with a different prompt.

> 💡 **Start with a few clips.** Read the captions that come back before you ingest anything
> at volume.

<!-- TODO: say what footage is actually available. Attendees need to know before picking a
     use case: what's already indexed (source, subject, hours, how many cameras), what's
     staged in ~/samples/, the RTSP feed, and whether they may bring their own. Any footage
     from a third party may carry licence terms that limit what attendees can do with it, so
     state those limits here rather than leaving people to guess. -->

### LLM access

Search and Q&A come from your VSS instance. Anything your app decides on top of that,
classifying results, drafting a summary, choosing an action, runs on serverless LLM
inference from Weights & Biases.

The skills used by Cursor can be used by agent frameworks too. They follow the standard
`SKILL.md` format, so most frameworks load them straight from `.cursor/skills/`.

<!-- TODO: link LangChain Deep Agents (docs.langchain.com/oss/python/deepagents/skills) and
     Pydantic AI Skills (dougtrajano.github.io/pydantic-ai-skills), both of which read
     SKILL.md natively with progressive disclosure. Pydantic AI scans recursively, so it
     handles our two-level ingest/ and retrieval/ nesting as-is. -->

<!-- TODO: restore this line once the script exists:
     Run [`examples/wandb-inference.py`](./examples/wandb-inference.py) to check it works
     before wiring it into your agent. -->

<!-- TODO: examples/wandb-inference.py DOES NOT EXIST YET. The link above is dead until it
     is written. Script should read WANDB_API_KEY / WANDB_TEAM / WANDB_PROJECT from the
     environment, make one call, print the response, and exit non-zero with a clear message
     if inference is unreachable.
     Blocked on: which model is available, and whether the OpenAI-compatible path or the W&B
     SDK is recommended. Also confirm examples/ is where we want it. -->

<!-- TODO: use-case sparks. 4-6 concrete ideas grounded in the footage teams actually have,
     plus a link to the Request for Builds doc. Teams re-decide scope on the morning
     regardless of what they read beforehand, so this needs to be skimmable. -->

## 6. Reference

### Health check

If something isn't working, ask the agent first:

```
check that everything is working: log in, and show me the dashboard
```

If it fails, tell an organizer.

<!-- HIDDEN until we have the details: restore this before the event.

     ### Getting help

     Needs: which organizers to find and where they sit, the event Slack channel name and
     join link, and the `cosmos` skill once it exists (ask a question without leaving the
     agent). Also decide whether questions go to Slack or to a person first. -->

### Event dashboard

Live for the event: [video-lab-event.cosmos.vastdata.com](http://video-lab-event.cosmos.vastdata.com/)

<!-- TODO: say what it actually shows (teams, ingest volume, activity, leaderboard?) so
     attendees know when to open it. Also confirm it resolves from the attendee VM, since
     it's a different host from $INGRESS_URL and may need its own DNS or hosts entry. -->

### Your team's values

Everything the skills need is already in your environment. `config.example` in this repo
lists every variable with a description.

## 7. Submit and demo

Ask the agent to run the submission skill:

```
help me submit our project
```

It asks for your team details, drafts your project description from your code, and collects
the confirmations you need to be eligible. It writes `SUBMISSION.md` in the repo root.

> 💡 **Have these ready:** a link to your code on GitLab, your demo video, and an email
> address for each team member. An incomplete submission may not be judged.

**Record the demo on your own laptop, not the VM.** You're already watching the VM in a
window, so your laptop's own recorder captures it: `Cmd+Shift+5` on a Mac, `Win+G` on
Windows. Drop the file in the event Slack channel.

<!-- TODO: dry run only. For the real events, code links go back to GitHub or any public
     URL, and the video needs a proper home: a Google Form with file upload, or unlisted
     YouTube. Slack works now but videos scroll away and judges may not be in the
     workspace. -->

When `SUBMISSION.md` is ready, copy its contents into the event Slack channel.

<!-- TODO: name the Slack channel and add a join link. Pasting contents is the dry-run
     approach; revisit for the real events, where a form may be needed and where pasting
     member email addresses into a shared channel is worth a second look. -->

### Demo

We'll book a time with each team to walk through what you built and to hear how the day
went.

<!-- HIDDEN for the dry run: restore before the real event.

     Needs: demo logistics (length is five minutes, running order, what should be on screen,
     whether slides are allowed, who presents), and the judging criteria, which is the same
     open question as the TODO in section 1: publish the rubric here or link the event page.
-->
