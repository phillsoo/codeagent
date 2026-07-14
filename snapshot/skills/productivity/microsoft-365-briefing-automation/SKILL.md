---
name: microsoft-365-briefing-automation
description: "Create, verify, and operate read-only Microsoft 365 Outlook mail/calendar briefings, especially recurring Hermes cron deliveries through Codex CLI Agent365 connectors."
version: 1.0.0
author: Astra
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Microsoft 365, Outlook, Calendar, Email, Cron, Briefing, Codex]
---

# Microsoft 365 Briefing Automation

Use this skill when a user asks for a one-time or recurring briefing from Outlook mail and calendar, or asks to verify/change the schedule of an existing Microsoft 365 briefing.

This is a class-level workflow for **read-only mailbox/calendar summarization and scheduled delivery**. It does not authorize sending mail, replying, RSVP changes, mailbox mutations, or calendar edits.

## Core workflow

1. **Recover prior setup context first.** If the user says Outlook is “now connected” or refers to a previous setup, search session history before assuming Graph credentials, IMAP, browser login, or a particular connector.
2. **Identify the working access path.** Prefer the already-proven route. A common route is Codex CLI with Microsoft Agent365 MCP connectors named `outlook-mail` and `outlook-calendar`. Do not replace a working OAuth connector with IMAP merely because an email skill is available.
3. **Verify with a minimal read-only probe.** Check CLI login and configured connectors, then make a low-disclosure calendar probe that returns only success, mailbox timezone, event count, and whether cancellations were excluded. Do not expose event or message content during connectivity testing.
4. **Create a self-contained scheduled job.** Cron jobs run without current-chat context. Include the account/connector route, date range, importance criteria, output structure, read-only restrictions, failure behavior, delivery destination, and internal completion deadline in the job prompt.
5. **Verify the actual scheduler state.** Re-list the created job and check `enabled`, `state`, schedule, delivery target, and `next_run_at`.
6. **Convert and report the next run in the user’s timezone.** Never merely show the server/UTC cron expression. Use a time tool to convert the scheduler timestamp and state the timezone explicitly.

## Timezone discipline

Timezone is part of the requirement, not presentation polish.

- Repeat the user-facing schedule as an explicit timezone-qualified time, such as `월~금 08:00 KST`.
- Hermes cron expressions are interpreted in the scheduler/server timezone unless the current implementation says otherwise. For a UTC scheduler, weekday 08:00 KST is `0 23 * * 0-4`: Sunday–Thursday 23:00 UTC produces Monday–Friday 08:00 KST.
- Verify the first/next execution by converting `next_run_at` with a time tool. Do not rely on mental arithmetic.
- If the user clarifies “한국시간,” treat it as a correction requiring scheduler-state verification, even if the existing expression appears right.
- Include the timezone in the job name and prompt so future maintainers do not reinterpret an unqualified `08:00`.

## Read-only safety boundary

A request to “summarize and tell me” approves reading and delivery of the requested summary. It does **not** approve mailbox or calendar mutation.

The job prompt must prohibit:

- sending, replying, forwarding, or drafting mail for delivery
- moving, deleting, archiving, marking read/unread, or changing flags
- creating, editing, or deleting events
- accepting/declining meetings or changing RSVP state

If the user later asks for any of those actions, stop at a prepared draft or proposed change and obtain explicit approval before execution.

## Briefing scope defaults

Unless the user specifies otherwise:

### Calendar
- Query the user’s default personal calendar for today in the mailbox/user timezone.
- Include all-day events.
- Exclude canceled events.
- Sort by start time.
- Show location/online status, RSVP state, preparation notes, overlaps, and back-to-back meetings.

### Mail
- Tuesday–Friday: inspect roughly the prior 24 hours.
- Monday: inspect from the previous Friday morning so weekend and late-Friday mail is not missed.
- Also consider unresolved high-importance/flagged/action-request mail from the prior 7 days.
- Prioritize direct action, explicit deadlines, customer/incident/executive issues, security/account risk, and meeting/approval requests.
- Exclude newsletters, ads, routine automated notices, canceled items, and clearly completed threads unless still actionable.
- Limit the final briefing to a manageable number (usually eight) and include sender, exact subject, received time in the user timezone, concise summary, required action, deadline, and importance rationale.

## Failure handling

- If connector authentication or lookup fails, do not fabricate an empty inbox/calendar.
- Report `차단`, the failing stage, impact, attempted checks, and the user action needed.
- Connector registries can show a lazy-auth or “not logged in” status while an actual connector call still succeeds. Treat the minimal read-only probe as the decisive test; do not stop at registry text alone.
- Keep the job active only if its failure output is useful and non-spammy. Otherwise pause it and explain why.

## Verification evidence to report

Include:

- cron job ID
- enabled/state status
- timezone-qualified human schedule
- converted next run time
- delivery destination
- read-only probe result and execution/session ID when available
- any unresolved authentication or policy caveat

Do not over-explain UTC conversion after verification; the user primarily needs confirmation that the human schedule is correct.

## Reference

See `references/codex-agent365-outlook.md` for the proven Codex CLI probe pattern, cron prompt checklist, and lazy-auth interpretation.