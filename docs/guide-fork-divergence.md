# Syncing from the company fork

This lab has a downstream sibling: a private fork maintained inside a company, which
runs ahead of it. Improvements flow **fork → lab**. This document is the checklist for
doing that port, and the complete record of every place the two trees are meant to
differ.

Read it before the next sync. Its purpose is that nobody has to re-derive these
decisions — or accidentally "fix" one of them by pulling the fork's version back over
it.

## Why this is a port and not a merge

The two checkouts have **unrelated git histories**. The fork was seeded by
squash-imports of the lab (`Sync/lab v2`, `Feat/lab v3`) rather than branched from a
shared root, so:

```bash
git merge-base main xl-fork/main   # prints nothing
```

`git merge` and `git rebase` cannot join them. The sync is a **content-level port**:
check the fork's files out by path, apply its deletions by hand, then re-derive the
generated artifacts.

> An older memory note claimed the two were joined by a merge commit and could be
> synced with a plain `git merge` through a `lab-upstream` remote. That is wrong and
> has been corrected.

## The procedure

```bash
# 1. Point at the fork (once).
git remote add xl-fork /path/to/the/company/checkout
git fetch xl-fork

# 2. Work on a branch.
git switch -c sync/xl-fork

# 3. See the shape of the divergence.
git diff --name-status HEAD xl-fork/main -- .

# 4. Take the adds, modifications and renames — minus the exclusions below.
#    (`xargs -a` is not available on macOS; feed the list through `tr`.)
tr '\n' '\0' < /tmp/port_final.txt | xargs -0 git checkout xl-fork/main --

# 5. Apply the fork's deletions selectively (see "Deletions" below).
# 6. Re-derive everything generated.
make sync-skills

# 7. Prove it.
make ci          # check + check-sync
make check-frontend
```

Step 6 is not optional and not cosmetic. `skills-lock.json`,
`.agents/skills/.generated-manifest.tsv` and the `BEGIN GENERATED SKILLS` regions of
`CLAUDE.md`, `AGENTS.md`, `OPENCODE.md`, `.agents/rules/GEMINI.md` and
`.github/copilot-instructions.md` are **derived** by walking `.github/skills-external/`
on disk. Never hand-edit them; never copy the fork's copies of them either.

## What is deliberately different

Everything below is an intentional divergence. When a future `git diff xl-fork/main`
shows one of these, that is the system working — not drift to repair.

### 1. No third-party branding — ADR-0060

The single hard exclusion. See
[ADR-0060](adr/0060-the-lab-carries-no-third-party-branding.md) for the reasoning; the
mechanics are:

| Fork artifact | In this lab |
|---|---|
| Company logo component | `frontend/src/components/LabMark.tsx` — a neutral three-bar mark with the **same props** (`variant`, `size`, `width`, `height`) so call sites port unchanged |
| `--xl-*` CSS tokens, "official brand palette" comment | `--brand-*`, **same hex values**, comment dropped (`frontend/src/styles.css`) |
| Company favicon and page title | Ladder glyph and "Agentic Harness Lab" (`frontend/index.html`) |
| Company badge in the sidebar footer | `LOCAL` (`frontend/src/components/Shell.tsx`) |
| Branding skill under `.github/skills-external/` | Never copied; `make sync-skills` then erases it from every derived artifact |
| `CLAUDE.md.tmp` | Not ported — a stray file from the fork's branding pass |

**Never copy the branding skill directory and then run `make sync-skills`.** Removing
the source directory *is* the entire removal; everything downstream re-derives.

Enforced by `tests/test_no_third_party_branding.py`, which greps the tracked tree and
fails the gate if the name, or an `--xl-*` token, reappears. The banned string is
assembled from fragments inside that test so the tree's true occurrence count is zero.

Fonts are **not** branding. The fork's Outfit / Space Grotesk pairing, the accent
colour, the spacing scale, the component library and the navigation regrouping are all
ported as-is.

### 2. Repository slugs

All slugs resolve to `marcosdh1987/*`, which is what this lab already used:

| Fork | Lab |
|---|---|
| `<org>/sdlc-ml-python-harness-lab` | `marcosdh1987/ai-agentic-harness-lab` |
| `<org>/sdlc-ml-python-base`, `<org>/ml-python-base` | `marcosdh1987/ml-python-base` |
| `<org>/sdlc-harness-engineering-guide` | `marcosdh1987/harness-engineering-guide` |

Substitute longest-pattern-first, or `sdlc-ml-python-harness-lab` will be half-rewritten
by the shorter rule. The slug appears in roughly 34 files, including `.env.example`,
`Makefile`, `src/harness_lab_app/config.py`, `.github/CODEOWNERS`,
`.github/ISSUE_TEMPLATE/config.yml`, `scripts/lab_improve.py` and several tests.

`.github/CODEOWNERS` also drops the fork's org-team migration note: this repo has an
individual owner, not a team.

### 3. `NOTICE` stays at the lab's version

The fork's `NOTICE` removes the full MIT License text, two copyright notices and the
`ui-ux-pro-max` provenance. That is a licensing regression, not an improvement. **Do
not port `NOTICE`**, in this sync or any future one.

### 4. tetris-v1 is archived rather than deleted

The fork deletes the ten `benchmarks/tetris/` files (~1,450 lines). This lab keeps
them, at `benchmarks/_archive/tetris-v1/`, because `runs.yaml` is 738 lines of *this*
lab's tetris-v1 pilot registry — its own measurement record, last edited here in
`994d3ab`. Deleting a measurement lab's run history is not an improvement to import.

The path matters. Leaving the directory at `benchmarks/tetris/` does **not** work, and
the first attempt at this sync proved it: everything that discovers benchmarks globs
`benchmarks/*/` one level deep, so a `task.yaml` sitting there makes tetris-v1 a live
seeded case again — which is precisely what
[ADR-0050](adr/0050-a-case-ships-its-own-tests.md) retired. Four of the fork's own
tests catch it, one of them asserting `"tetris-v1" not in ids` outright. Nesting under
`_archive/` puts it below every glob while leaving it readable.

So the split is: the **case** is retired, as ADR-0050 says; the **record** of what it
measured is kept. `benchmarks/_archive/README.md` states that contract, and the
retirement of the manual-scoring lane (`score_tetris.py`, `show_results.py`,
`summarize_results.py`, the `bench-results` target) did happen here as the ADR
describes. `benchmarks/tetris-v2/` was ported additively.

Historical documents that reference the old `benchmarks/tetris/` path — ADRs,
roadmaps, runbooks, dated plans — are left alone: they correctly describe where it was
when they were written. Only live pointers were repointed.

### 5. `data/harness_lab.db` is never ported

Local runtime state. Each checkout has its own.

### 6. Report language: Spanish, by pre-existing convention

The repository rule is that code artifacts are English (`CLAUDE.md`), and user-facing
UI copy is English too. The web app honours both — `frontend/src` contains no Spanish.

The **auditor subsystem is the documented exception**: its LLM system prompts, the
Markdown reports they generate, and the operator note templates that feed them are
written in Spanish. This predates the fork — `scripts/bench_audit.py` and the
accent-stripping verdict matcher in `src/harness_lab_app/evaluation.py` are the lab's
own — and the fork's newer auditors (`repository_audit_service.py`,
`experiment_audit_service.py`, `bench_agents_audit.py`, `bench_antigravity.py`) simply
follow it.

**Do not translate only the ported half.** Doing so would leave the audit subsystem
reporting in two languages at once, which is worse than either uniform choice. If the
report language is ever changed, change it everywhere in one pass — prompts, section
headings, the tests that assert on them, and the JSON fixtures under
`tests/harness_lab_app/fixtures/`, which all move in lockstep.

Docs that quote those prompts quote them verbatim, in Spanish. That is correct.

**This holds for the four ported auditors, not for new ones.** Auditors written in
this lab from here on are English — starting with the Compare reading
(`compare_audit_service.py`, [ADR-0061](adr/0061-compare-can-ask-a-model-to-read-the-table.md)),
which renders inside the web app and would otherwise put Spanish prose on an English
page. So the subsystem does now report in two languages, which the paragraph above
calls worse than either uniform choice — and it is, as an end state. It is accepted as
an interim one: the fix is to translate the ported four in a single pass, not to write
new Spanish to match them. `test_compare_audit.py` asserts the new prompt is ASCII so
the old convention cannot drift back in by hand.

### 7. `talos` references are left in place — open follow-up

About 30 files and ~270 occurrences reference `talos`, a repository from the fork's
environment, mostly as audit fixtures and worked examples. These are **not** branding
and were ported as-is on purpose. One URL that embedded the company org
(`tests/harness_lab_app/test_audit_pipeline.py`) was neutralised to `example-org`.

Whether a public lab should ship another team's repository as its canonical audit
example is a real question — just a separate one from this sync. Flagged, not decided.

## Behavioural changes worth knowing about

These came from the fork and were accepted. They are listed here because each one
changes what the lab reports, and a reader comparing old output to new deserves to know
why:

- **`src/harness_lab_app/statistics.py` thresholds relaxed.** `USEFUL_COMPARISON` 5 → 2,
  `STRONGER_EVIDENCE` 10 → 5, with the vocabulary "exploratory / judgement /
  validation". More comparisons now qualify as readable, at a weaker evidentiary bar.
- **`POST /api/cases/seed/tetris` → `POST /api/cases/seed`.** The seed endpoint is no
  longer tetris-specific; it walks every `benchmarks/*/task.yaml`. The frontend was
  ported in lockstep.
- **`frontend/src/harnesses.ts` drops `antigravity`** from the selectable harnesses.
  `scripts/bench_antigravity.py` and `make bench-antigravity` still exist for the
  manual lane.
- **`benchmarks/harness-regression-v1/suite.yaml` drops three case ids** that no longer
  exist in the corpus.

## Verifying a sync

```bash
make ci                # make check (ruff, bandit, mypy, pytest+cov) + make check-sync
make check-frontend    # npm run typecheck + vite build
uv run pytest tests/test_no_third_party_branding.py -q
```

Then read the residue — it should contain only the items documented above, nothing else:

```bash
git diff --name-status xl-fork/main -- .
```
