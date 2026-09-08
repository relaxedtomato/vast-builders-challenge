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

Everything under "pre-built, already running" is done for you. The pipeline ingests,
understands, and indexes video, and the models it calls are already deployed and
serving. You build the app that searches and acts.

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

### What "done" looks like
A small app, agent, or a dashboard. A clear use case.

---

## 2. Launch your VM

No setup. Nothing to install, no config to paste, no keys to type.

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

From there, describe the task and the agent picks the matching skill. Start with
[Meet your skills](#3-meet-your-skills), then ingest a clip and search it.

> 💡 **Copy and paste in the VM.** In the terminal it's `Ctrl+Shift+C` and `Ctrl+Shift+V`

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

### What video you have _(draft, review me)_

Your index already holds footage from several sources, all searchable now:

- **Street and intersection cameras** in Bangkok, Dublin and London. Fixed views of traffic
  and crowds.
- **First-person work footage**: baristas, a sushi chef, a cook. Hands at work, close up.
- **Warehouse and forklift POV**, aisles and loading.
- **Dashcam driving** in New York and San Francisco.
- **Overhead and street-level New York**, the same city from two heights.

Filter any search by `scenario`, `city`, `camera_id` or `category`. Scenario values include
`surveillance`, `traffic`, `retail`, `warehouse`, `egocentric` and `general`.

Every folder and camera ID is in
[Video corpus](HACKATHON_GUIDELINES.md#video-corpus-already-indexed), grouped by use case in
[Use-case groups](HACKATHON_GUIDELINES.md#use-case-groups).

### The loop

1. **Pick a use case**
2. **Build an app or agent**
3. **Deploy and iterate**

If the existing captions cover what you need, you never have to think about prompts. If they
don't, ingest the footage again with a different prompt.

> 💡 **Start with a few clips.** Read the captions that come back before you ingest anything
> at volume.

### LLM access

Search and Q&A come from your VSS instance. Anything your app decides on top of that,
classifying results, drafting a summary, choosing an action, runs on serverless LLM
inference from Weights & Biases.

The skills used by Cursor can be used by agent frameworks too. They follow the standard
`SKILL.md` format, so most frameworks load them straight from `.cursor/skills/`.

## 6. Reference

### Health check

If something isn't working, ask the agent first:

```
check that everything is working: log in, and show me the dashboard
```

If it fails, tell an organizer.

### Event dashboard

Live for the event: [video-lab-event.cosmos.vastdata.com](http://video-lab-event.cosmos.vastdata.com/)

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

> 💡 **Have these ready:** a link to your code or repo, your demo video, and an email
> address for each team member. An incomplete submission may not be judged.

**Record the demo on your own laptop, not the VM.** You're already watching the VM in a
window, so your laptop's own recorder captures it: `Cmd+Shift+5` on a Mac, `Win+G` on
Windows. Drop the file in the event Slack channel.

When `SUBMISSION.md` is ready, copy its contents into the event Slack channel.

### Demo

We'll book a time with each team to walk through what you built and to hear how the day
went.

