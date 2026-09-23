---
name: submission
description: >-
  Collect everything a team needs to submit their VAST Builders Challenge project and write
  it to SUBMISSION.md. Asks for team name, project description, tech stack, code and demo
  links and feedback. Never collects personal details. Use when a team is ready to submit, or
  wants to check what is still missing.
---

# Submission

Interviews the team, checks nothing is missing, and writes `SUBMISSION.md` in the repo root.

Run it early to see what's outstanding, and again at the end to produce the final file.

## Before you submit

- [ ] Your project runs, from a clean start, without you fixing it live
- [ ] Your code is pushed somewhere the judges can open
- [ ] Your demo video is uploaded and the link works in a private window
- [ ] One person can explain the project in two minutes

## Work it out first

Derive the **project details** only: what the project does, and the technology stack.

Read the team's code. What it does should come from what the code actually does, not from
how they describe it in a hurry at the end of the day. For the stack, note which skills they
called, which parts of the pipeline that implies (Cosmos Reason for captions, Cosmos Embed
for search, YOLO for detection), whether they called a W&B model, and what they built the
app itself with.

Keep the description to two or three sentences: what it does, and who would use it. The
stack is a list, not prose. Judges read a lot of these.

Draft both, show them, and let them correct it. A team that has been building for eight
hours writes a better description by editing yours than by starting from a blank prompt.

Ask for everything else: team name, links and feedback. Those are not in
the code, and a wrong value that looks right gets submitted without anyone noticing.

If you aren't sure, leave it empty and ask.

## What to collect

Go section by section. Present what you already worked out, ask for the gaps, and wait for
an answer before moving to the next section. Don't dump all four sections at once.

**Team**
- Team name

Do not ask for member names, emails, or any other personal detail. Those fields stay blank.

**Project**
- Description: what it does and who it's for, in two or three sentences
- Technology stack: which skills, which models, what you built on top
- Link to the code or repo
- Link to the demo video, dropped in the event Slack channel

<!-- TODO: dry run only. For the real events, code goes back to GitHub or any public URL,
     and the demo video needs a proper home (a Google Form with file upload, or unlisted
     YouTube). Slack is fine for a dry run but the video scrolls away and judges may not be
     in the workspace. -->
- Links to supplementary material, if any

**Feedback**
- Overall feedback on the day. Invite them to call out anything specific, but don't ask
  about each product in turn. Honest criticism is more useful than praise.

## Nothing should be left blank, except personal details

This is a contest entry. An incomplete one may not be judged, and the team won't find out
until it's too late to fix.

Personal details are the exception. They are left blank on purpose and never count as
missing (see the agent instructions).

For everything else: never invent a value, but never quietly accept a blank either. If a field is missing,
say what it is and why it matters, then ask again. Two of them are worth pushing on:

- **Code and demo links.** Judges assess what they can open. A project nobody can run or
  watch is judged on its description alone.
- **The demo video is recorded on your own laptop, not the VM.** You're already looking at
  the VM in a window, so your laptop's built-in recorder captures it: `Cmd+Shift+5` on a
  Mac, `Win+G` on Windows. Recording inside the VM means installing a capture tool, using
  GPU you need for other things, and then getting a large file back out.

When you finish, list what's still missing and tell them the entry isn't complete. Don't
end on a summary that reads like success when four fields say `NOT PROVIDED`.

## Writing the file

Write `SUBMISSION.md` in the repo root using this shape. Leave a field as `NOT PROVIDED`
rather than inventing a value.

```markdown
# <Team name>

## Team
**Members:**

## Project
<description>

**Stack:** <stack>
**Code:** <url>
**Demo video:** <url>
**Supplementary:** <urls, or none>

## Feedback
<overall feedback, with anything product-specific they mentioned>

```

## Agent instructions

1. Never ask for, collect, or write personal details: member names, emails, ages, contact
   or consent confirmations. Leave those fields blank. Blank personal fields are not
   `NOT PROVIDED` and don't make the entry incomplete. If a team volunteers one, don't
   write it into the file.
2. Read `SUBMISSION.md` first if it exists, and only ask for what's missing.
3. Derive only the project description and technology stack, and show them for correction.
   Ask for everything else.
4. Take one section at a time: team name, then project, then feedback.
5. Never invent a value. When unsure, leave the field empty rather than guessing.
6. Write `SUBMISSION.md` but do not commit or push it unless asked.
7. When you finish, list anything still `NOT PROVIDED`, say the entry is incomplete, and
   offer to fill the gaps now. Confirm the checklist at the top of this skill.

## After the file is written

Tell the team to copy the contents of `SUBMISSION.md` into the event Slack channel. Writing
the file is not submitting. Nothing is entered until it's posted.

<!-- TODO: name the Slack channel here once known, and confirm whether teams paste the
     contents, upload the file, or post a link. Also confirm with whoever owns the Terms &
     Conditions whether confirmations collected this way are sufficient, or whether the
     official form must still be signed separately. -->
