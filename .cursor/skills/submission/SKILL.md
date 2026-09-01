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

Before asking anything, gather what you can from the environment and the repo, then show
the team what you found and ask them to correct it. Never present a guess as a fact.

| Field | Where to look |
|---|---|
| Team name | the bucket prefix in `$S3_CHUNKS_BUCKET`, e.g. `team-b-vss-chunks` gives `team-b` |
| Technology stack | which skills they called, plus Cosmos Reason, Cosmos Embed and YOLO in the pipeline, and the W&B model if they used one. Read their code rather than asking |
| Location | which city event, from `$PIPELINE` or the ingress hostname if either encodes it |

Always ask for these, never derive them:

- **Team members and emails.** This repo arrives pre-cloned with the organizers' commit
  history, so `git log` returns the people who wrote the starter repo, not the team. Commit
  emails are also often noreply addresses nobody can be contacted on.
- **Link to code.** `git remote` points at the starter repo. The team's project may live
  somewhere else entirely.
- **Organization.** Guessing from an email domain is wrong for anyone using a personal
  address.

Check that a derived value is plausible before showing it. `$USERNAME` on a laptop is the
login name, not a team name. An unset variable and a variable set to something unrelated
are different problems.

If you aren't sure, leave it empty. An empty field is obvious and gets filled in. A wrong
one that looks right gets submitted.

Anything you can't determine, ask for.

**Everything you derive must be reviewed.** Show it back as a short list and ask them to
correct anything wrong before you write it to the file. A derived value nobody looked at is
a guess with extra steps.

If your agent has a structured way to ask (a multiple-choice or confirmation prompt), use
it. If not, plain text is fine. Don't assume any particular tool exists.

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
- Description: what it does, who it's for, what question it answers about video
- Technology stack: which skills, which models, what you built on top
- Link to code (GitHub or any public URL)
- Link to demo video (YouTube or any public platform)
- Links to supplementary material, if any

**Feedback**
- Product feedback on each of: NVIDIA VSS Blueprint, VAST, Cursor, CoreWeave.
  Optional per product, and honest criticism is more useful than praise.

**Confirmations** (ask each one separately, record only what they actually say)
- All team members are 18 or older
- Partner opt-in: may partners contact the team
- Agree to be contacted for further feedback on the contest and products
- Agree to the Terms & Conditions

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
**NVIDIA VSS Blueprint:** ...
**VAST:** ...
**Cursor:** ...
**CoreWeave:** ...

## Confirmations
- 18 or older (all members): <yes / no>
- Partner opt-in: <yes / no>
- Contact for further feedback: <yes / no>
- Terms & Conditions: <agreed / not agreed>
```

## Agent instructions

1. Read `SUBMISSION.md` first if it exists, and only ask for what's missing.
2. Work out what you can before asking (see above), and show your answers for correction
   rather than stating them as final.
3. Take one section at a time: team, then project, then feedback, then confirmations.
4. Never invent a value, and never assume a confirmation. When unsure, leave the field
   empty rather than offering a guess. If someone hasn't answered a
   confirmation, write `NOT PROVIDED` and tell them it blocks submission.
5. Confirmations must come from a person in this conversation. Do not infer them from
   context, from the team having registered, or from anything said earlier.
6. `SUBMISSION.md` contains personal email addresses. Write it, but do not commit or push it
   unless asked. If the team wants it committed, say plainly that the addresses become part
   of the repo history.
7. When the file is complete, list anything still `NOT PROVIDED` and confirm the checklist
   at the top of this skill.

<!-- TODO: where does SUBMISSION.md actually go? The skill produces the file but nothing
     tells the team what to do with it. Decide: upload to a form, post in the event Slack,
     push a branch, or hand it to an organizer. Then add a final step here.
     Also confirm with whoever owns the Terms & Conditions whether confirmations collected
     this way are sufficient, or whether the official form must still be signed separately. -->
