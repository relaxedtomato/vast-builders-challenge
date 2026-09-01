---
name: vast-builder-submission
description: >-
  Collect everything a team needs to submit their VAST Builders Challenge project and write
  it to SUBMISSION.md. Asks for team details, project description, tech stack, code and demo
  links, feedback, and the required confirmations. Use when a team is ready to submit, or
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

Ask for everything else: team details, links, feedback, and confirmations. Those are not in
the code, and a wrong value that looks right gets submitted without anyone noticing.

If you aren't sure, leave it empty and ask.

**Never derive a confirmation.** The four confirmations below come from a person saying so
in the conversation, and from nothing else.

## What to collect

Go section by section. Present what you already worked out, ask for the gaps, and wait for
an answer before moving to the next section. Don't dump all four sections at once.

**Team**
- Team name
- Every member's name and email address
- Organization or university
- Location (which city event)

**Project**
- Description: what it does and who it's for, in two or three sentences
- Technology stack: which skills, which models, what you built on top
- Link to code (GitHub or any public URL)
- Link to demo video (YouTube or any public platform)
- Links to supplementary material, if any

**Feedback**
- Overall feedback on the day. Invite them to call out anything specific, but don't ask
  about each product in turn. Honest criticism is more useful than praise.

**Confirmations** (ask each one separately, record only what they actually say)
- All team members are 18 or older
- Partner opt-in: may partners contact the team
- Agree to the Terms & Conditions
- Agree to be contacted for further feedback on the contest and products

## Nothing should be left blank

This is a contest entry. An incomplete one may not be judged, and the team won't find out
until it's too late to fix.

So: never invent a value, but never quietly accept a blank either. If a field is missing,
say what it is and why it matters, then ask again. Two of them are worth pushing on:

- **Emails.** This is how judges reach the team if they win. A submission without them can't
  be contacted. If someone hesitates, note that only organizers and judges see them.
- **Code and demo links.** Judges assess what they can open. A project nobody can run or
  watch is judged on its description alone.

The four confirmations are eligibility, not paperwork. Without them the entry can't be
accepted, no matter how good the project is. Say that plainly rather than moving on.

When you finish, list what's still missing and tell them the entry isn't complete. Don't
end on a summary that reads like success when four fields say `NOT PROVIDED`.

Check the location is one of the event cities, and ask if it isn't.

## Writing the file

Write `SUBMISSION.md` in the repo root using this shape. Leave a field as `NOT PROVIDED`
rather than inventing a value.

```markdown
# <Team name>

**Location:** <city>
**Organization:** <org or university>

## Team
| Name | Email |
|---|---|
| ... | ... |

## Project
<description>

**Stack:** <stack>
**Code:** <url>
**Demo video:** <url>
**Supplementary:** <urls, or none>

## Feedback
<overall feedback, with anything product-specific they mentioned>

## Confirmations
- 18 or older (all members): <yes / no>
- Partner opt-in: <yes / no>
- Terms & Conditions: <agreed / not agreed>
- Contact for further feedback: <yes / no>
```

## Agent instructions

1. Read `SUBMISSION.md` first if it exists, and only ask for what's missing.
2. Derive only the project description and technology stack, and show them for correction.
   Ask for everything else.
3. Take one section at a time: team, then project, then feedback, then confirmations.
4. Never invent a value, and never assume a confirmation. When unsure, leave the field
   empty rather than offering a guess. If someone hasn't answered a
   confirmation, write `NOT PROVIDED` and tell them it blocks submission.
5. Confirmations must come from a person in this conversation. Do not infer them from
   context, from the team having registered, or from anything said earlier.
6. `SUBMISSION.md` contains personal email addresses. Write it, but do not commit or push it
   unless asked. If the team wants it committed, say plainly that the addresses become part
   of the repo history.
7. When you finish, list anything still `NOT PROVIDED`, say the entry is incomplete, and
   offer to fill the gaps now. Confirm the checklist at the top of this skill.

## After the file is written

Tell the team to copy the contents of `SUBMISSION.md` into the event Slack channel. Writing
the file is not submitting. Nothing is entered until it's posted.

<!-- TODO: name the Slack channel here once known, and confirm whether teams paste the
     contents, upload the file, or post a link. Also confirm with whoever owns the Terms &
     Conditions whether confirmations collected this way are sufficient, or whether the
     official form must still be signed separately. -->
