# How we collaborate via PRs

1. Agent pushes work to a `feat/*` branch and opens a PR (this one).
2. Human reviews: inline line comments or PR-level comments.
3. Agent reads comments (`gh pr view N --comments` for discussion,
   `gh api repos/dyo-tak/blackbox/pulls/N/comments` for inline review
   comments), replies, and pushes fixes to the same branch.
4. PR auto-updates on every push; merge when approved.

Conventions:
- One PR = one roadmap item.
- Agent never merges without approval.
- Commit style: conventional commits (`feat:`, `chore:`, `fix:`, `docs:`).
