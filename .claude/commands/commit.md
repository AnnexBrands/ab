---
description: Stage and commit changes with a conventional commit message derived from the diff.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).
If the user supplies a commit message or hint, use it to guide the
message but still validate it against the diff.

## Outline

1. **Gather context** — run the following in parallel:
   - `git status` (never use `-uall`)
   - `git diff` and `git diff --cached` to see unstaged and staged changes
   - `git log --oneline -10` to capture recent commit message style

2. **Analyze changes**:
   - Identify which files changed and what the changes accomplish.
   - Classify the change type using Conventional Commits:
     `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`,
     `style`, `perf`, `build`.
   - If multiple types apply, use the dominant one; mention others
     in the body.
   - Determine an optional scope from the path or module affected
     (e.g., `feat(auth):`, `docs(constitution):`).

3. **Draft the commit message**:
   - **Subject line**: `<type>(<scope>): <imperative summary>`
     — max 72 characters, lowercase, no trailing period.
   - **Body** (if the diff is non-trivial): blank line, then a
     short paragraph explaining *why* the change was made, not
     just *what* changed. Wrap at 72 characters.
   - **Trailer**: always append:
     ```
     Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
     ```

4. **Stage files**:
   - Prefer staging specific files by name rather than `git add -A`.
   - NEVER stage files that look like secrets (`.env`, credentials,
     tokens, private keys).
   - If untracked files exist that appear relevant, ask the user
     whether to include them.

5. **Present the commit message** to the user and ask for
   confirmation before running `git commit`. If the user supplies
   edits, incorporate them.

6. **Commit**:
   - Use a HEREDOC to pass the message to `git commit -m`.
   - Run `git status` after the commit to verify success.
   - Do NOT push unless the user explicitly asks.

7. **Report**: output the commit hash and a one-line summary.

Rules:
- NEVER amend a previous commit unless the user explicitly asks.
- NEVER use `--no-verify` or skip hooks.
- NEVER force-push.
- If a pre-commit hook fails, fix the issue, re-stage, and create
  a NEW commit (do not amend).
- If there are no changes to commit, say so and stop.
