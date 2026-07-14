# Codex Agent365 Outlook connector notes

## Proven access pattern

When Codex CLI already has Microsoft 365 connectors configured, use a temporary Git repository because `codex exec` may require a trusted/project directory:

```bash
TMPDIR=$(mktemp -d)
git -C "$TMPDIR" init -q
cd "$TMPDIR"
codex exec --sandbox read-only '<read-only Outlook probe or briefing prompt>'
```

Before the probe:

```bash
codex login status
codex mcp list
```

Expected connector names may include:

- `outlook-calendar`
- `outlook-mail`

## Minimal low-disclosure probe

Ask the calendar connector only for:

- success/failure
- mailbox timezone
- today’s event count
- confirmation that canceled events were excluded

Explicitly prohibit event details and all writes. This proves live access without putting sensitive calendar content into setup logs.

Example intent:

> Use the Outlook Calendar connector read-only. Verify mailbox timezone and whether today’s default calendar can be queried. Return only success, timezone, event count, and cancellation filtering. Do not create, edit, delete, or RSVP.

## Lazy-auth interpretation

`codex mcp list` can display `Not logged in`, and startup logs can briefly show `AuthRequired`, while the subsequent connector tool call completes successfully through on-demand authentication. Therefore:

1. Record registry output as a preliminary signal.
2. Run the minimal read-only probe.
3. Treat the connector call result as authoritative for current usability.
4. Report a blocker only if the actual tool call fails.

This is a retry/verification pattern, not a claim that every `Not logged in` state is harmless.

## KST weekday cron mapping

For a scheduler operating in UTC:

```text
0 23 * * 0-4
```

maps to Monday–Friday 08:00 KST. The UTC weekday range is Sunday–Thursday because the execution crosses midnight after adding nine hours.

Always verify `next_run_at` with a timezone-aware command or tool, for example:

```bash
TZ=Asia/Seoul date -d '<next_run_at ISO timestamp>' '+%Y-%m-%d (%a) %H:%M %Z'
```

Do not hard-code this conversion for users in other timezones or if scheduler semantics change.

## Self-contained cron prompt checklist

A scheduled Outlook briefing prompt should include:

- human schedule and timezone
- connector/CLI route
- current-date lookup in the target timezone
- calendar window and canceled-event policy
- mail lookback policy, including Monday/weekend behavior
- importance criteria and item limit
- duplicate/repeat handling for unresolved items
- output format
- privacy/quotation limits
- explicit read-only prohibitions
- honest blocker output on authentication failure
- assignee, completion condition, internal deadline, delivery target, approval state, and review requirement where organizational policy requires them

## Suggested concise final verification

Report only what the user needs:

- active/inactive
- `월~금 08:00 KST`
- next run converted to KST
- job ID and delivery destination
- whether the live read-only probe succeeded

Avoid making the user reason from a UTC cron expression; include it only as secondary technical evidence.