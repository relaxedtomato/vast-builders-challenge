# Before you build

## Do these before you arrive

**1. Sign up for Cursor now, using the email you applied with.** We add your credits to that account before the day. No sign up means no credits.

**2. Form a team.** Up to four people. Come on your own and we'll help you find one.

**3. Bring one use case.** See below. It's the most useful thing you can prepare.

## What you're building

**A video agent**: an app that understands video and does something useful with it. Search hours of footage in plain words, ask what happened, spot events, or trigger an action when something matters.

One idea, working, shipped by the end of the day.

## The Builders Stack: What's already running

**VAST AI OS / DataEngine** implements the video ingestion pipeline at scale. Vectors, metadata, and video data are in one unified platform.
<!-- TODO: add a VAST docs link. -->

**The VSS UI** is a working example of what you can build on this stack, and a quick way to
see what's indexed. [VSS UI implementation overview](https://drive.google.com/file/d/110rh4vdBSFRNhdFX9Q5qXB9umqrm3nEO/view?usp=drive_link)
<!-- TODO: confirm this Drive link is shareable with external attendees. A Drive link that
     asks for access is worse than no link. Consider hosting it publicly instead. -->

**NVIDIA VSS Blueprint** turns raw video into something searchable, using three models. Cosmos Reason describes each segment, Cosmos Embed turns it into vectors you can search by meaning, and YOLO finds objects. You query the results instead of calling the models. [NVIDIA VSS Blueprint docs](https://docs.nvidia.com/vss/latest/)

**CoreWeave** provides the GPUs the models run on.
<!-- TODO: add a CoreWeave link. -->

**Weights & Biases** provides serverless LLM inference for your own app's reasoning, on an OpenAI-compatible endpoint. [W&B Serverless Inference docs](https://docs.wandb.ai/inference)

**Cursor** is how you build, and where you'll spend the day. The repo ships with skills that drive the whole stack in plain language, so you describe what you want rather than memorising endpoints.

Worth twenty minutes beforehand if you haven't used the CLI: [Cursor CLI docs](https://cursor.com/docs/cli/overview). To try it on your own machine first:

```sh
curl https://cursor.com/install -fsS | bash
agent login
agent                    # interactive session
```
<!-- TODO: confirm the command name. Cursor's docs show `agent`; BUILD_DAY section 2 says
     `cursor-agent`. One of them is wrong. Verify on the VM image. -->
<!-- TODO: add a Cursor CLI link. -->

## Think about your use case

Pick a question worth answering about video, and be specific. "Which moments show someone in
a restricted area" is something you can build for. "Do something with video" isn't.

**Hold the use case loosely.** You'll see what footage is indexed on build day, and your idea may need to adjust to fit it.

> 💡 Every segment gets a description written by a model following an initial prompt, and
> anything that prompt didn't ask about isn't in there, so you can't search for it later.
> During build day you'll be able to reingest with a different prompt if you need to.

<!-- TODO: reingest is possible through the VSS UI, but no skill covers it, so the agent
     can't do it for them. Either write a `reingest` skill or say in BUILD_DAY that this
     one is a UI job. See the reingest TODO in BUILD_DAY section 4. -->

<!-- TODO: no logistics section for now. The invite and Luma carry date, venue and
     timings. Add one only if the invite doesn't cover what to bring, when to arrive, and
     where to ask questions. -->
