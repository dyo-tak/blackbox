# How we collaborate via PRs

## The loop (chosen: manual ping)
1. Agent pushes work to a `feat/*` branch and opens a PR.
2. Human reviews: inline line comments or PR-level comments.
3. Human pings Hermes in Discord ("review", "pr 1") — comments are NOT
   picked up automatically; Hermes only sees the repo when pinged or when
   a cron job runs.
4. Agent fetches comments (`gh pr view N --comments` for discussion,
   `gh api repos/dyo-tak/blackbox/pulls/N/comments` for inline review
   comments), replies, and pushes fixes to the same branch. PR updates
   automatically on every push.
5. Merge when approved (`gh pr merge N --squash`).

## Optional: comment poller (not enabled)
A cron job can watch PRs autonomously:
- Runs on a schedule (e.g. every 10 min) in a fresh session.
- Each tick: script checks comment count / latest comment ID on the
  target PR(s) via `gh api` and prints a fingerprint. If unchanged from
  the previous tick, the agent does NOT run (tick is nearly free).
- On change: agent wakes with the new comments, acts, pushes fixes, and
  posts a summary back to the Discord thread.
- Scope: per-PR jobs (e.g. "watch PR #7 only") or one job for all open
  PRs. Create/pause/remove on demand.

## Conventions
- One PR = one roadmap item.
- Agent never merges without approval.
- Commit style: conventional commits (`feat:`, `chore:`, `fix:`, `docs:`).
