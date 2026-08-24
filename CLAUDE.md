# CLAUDE.md

## Commit message convention

This repo does not use conventional-commits prose. Commit subjects are a bracketed tag, and bodies
are a plain numbered list (no paragraphs), e.g.:

```
[bar-hbar-major-2]

1. `plotez` no longer applies its `rcParams` styling convention automatically on import; opt in via
   `plotez.enable_style()` / `plotez.disable_style()` at runtime, or `PLOTEZ_AUTO_STYLE=1` at import time.
2. Added `grid` kwarg to `update_style()`/`enable_style()` to toggle `axes.grid` independently.
3. Fixed a double-grid artifact on twin-axis (`plot_with_dual_axes`) plots via `ax2.grid(False)`.
```

**Tag format**: `[<branch>-<major|minor>-N]`, optionally with a sub-index like `[<branch>-minor-2-1]`
for a follow-up tweak to `minor-2`.
- `<branch>` is the current working branch name (e.g. `bar-hbar`, `docfix`, `plotxy-fix`, `dev`).
- `major` = a substantive change: new public API, breaking/behavior changes, refactors, or anything that
  also touches `docs/CHANGELOG.md`.
- `minor` = smaller iterative work: cosmetic fixes, small corrections, doc/README tweaks, cleanup.
- `major` and `minor` are **independent counters** — each continues from its own most recent tag on the
  branch (`git log --oneline` for the branch), regardless of how many commits of the *other* kind happened
  in between. A `major` commit does not reset or bump the `minor` counter, and vice versa. Example: if the
  most recent tags on a branch are `...-major-1`, then `...-minor-1`, then a new `major` commit, the next
  `minor` commit is still `...-minor-2` (continuing from `...-minor-1`), not `...-minor-3`.
- Do not create the squash/merge commit back to `main` (e.g. via a PR) — that step is done manually by the
  repo owner, not by Claude.

**Body**: plain numbered list, one line per change, backtick any identifiers (function/file/class names).
No prose paragraphs, no "why" narrative — just what changed.

Keep the `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` / `Claude-Session:` trailer on commits
made by Claude, appended after the numbered list, regardless of the tag format above.

## Fixing an unpushed commit

If the tip commit on the current branch hasn't been pushed yet (check with `git status -sb` — no
`[ahead N]` beyond what's expected, or compare `git log -1 --format=%H` against
`git log origin/<branch> -1 --format=%H`), it can be corrected in place with `git commit --amend` instead
of adding a new commit on top. This rewrites that one commit (message and/or staged file changes) without
touching any commit that's already on `origin`. Never amend a commit that's already been pushed unless
explicitly asked to force-push.
