# ADR-0060: The lab carries no third-party branding

- **Status:** Accepted
- **Date:** 2026-09-11
- **Deciders:** Marcos Soto
- **Related:** [ADR-0031](0031-local-web-app.md)

## Context

This lab has a downstream sibling: a private fork maintained inside a company. The two
checkouts have **unrelated git histories** — the fork was seeded by squash-imports of
the lab rather than from a shared root commit, so `git merge-base` between them is
empty and no `git merge` can join them. Improvements are carried across as a
content-level port: check the fork's files out by path, apply its deletions by hand,
then re-derive anything generated.

The fork is effectively a superset — at the time of this decision, 273 files and
roughly 38k inserted lines ahead — and almost all of it is work this lab wants: new
backend modules, the repository-audit subsystem, twenty-one ADRs, and a full visual
redesign of the web app.

Almost all. The fork also carries its employer's identity: a company logo component,
a company branding skill under `.github/skills-external/`, a CSS palette commented as
that company's official brand palette under company-initialled token names, its
favicon and page title, its name as a badge in the sidebar footer, and its org slug
in every repository URL.

That identity is not this repository's to carry. This lab is a personal, public
project; shipping another organisation's mark would misattribute it, and the mark
would keep leaking back in on every future sync unless the exclusion is written down
and enforced.

A *visual redesign* and a *brand* are not the same thing, though, and the naive
exclusion — "skip the frontend" — would throw away the larger, wanted half.

## Decision

**Port everything from the fork except the third-party identity itself, and enforce
the exclusion mechanically.**

"Identity" means exactly four things, and nothing more:

1. **The name.** The company's name must not appear anywhere in the tree, in any
   case — not in code, not in docs, not in this ADR. `tests/test_no_third_party_branding.py`
   greps the tracked tree for it and fails the quality gate if it reappears. That test
   is the authoritative definition of what is banned; this ADR deliberately does not
   repeat the string it guards.
2. **The logo.** The fork's logo component is replaced by
   `frontend/src/components/LabMark.tsx` — a neutral geometric mark (a three-bar
   ascending ladder) drawn entirely from the design tokens. It exposes the *same*
   props (`variant`, `size`, `width`, `height`) and the same variant names, so every
   call site, layout and CSS rule the fork wrote ports across unchanged.
3. **The token names.** The palette's **hex values are kept verbatim** — they are the
   redesign, and the redesign is wanted — but the fork's company-initialled token
   prefix is renamed to `--brand-*` and the brand-palette comment is dropped. The whole
   UI is token-driven, so this is a rename at the definition plus five consumers. As
   with the name, the old prefix is not spelled here; the guard test holds it, assembled
   from fragments, and is the authoritative definition.
4. **The branding skill.** The fork's branding skill directory is never copied.
   Because `skills-lock.json`, `.agents/skills/.generated-manifest.tsv` and the
   `BEGIN GENERATED SKILLS` regions of the adapter files are all *derived* by walking
   `.github/skills-external/` on disk, `make sync-skills` removes every trace of it
   with no manual edit. `make check-sync` then proves the derived artifacts agree.

Everything else the fork's redesign contains — fonts, spacing, the accent colour, the
component library, the navigation regrouping — is ported as-is. Fonts are typography,
not trademark.

Repository slugs resolve to `marcosdh1987/*`, which is what this lab already used.

## Consequences

The lab gets the fork's improvements without carrying anyone else's name, and the
exclusion survives contact with the next sync: the guard test turns a silent
regression into a red build, and the skill-sync engine makes the branding skill
unremovable-by-accident rather than something to remember.

The `LabMark` API mirroring the fork's logo component is deliberate coupling. It keeps
future ports cheap — a fork change that touches the logo's call sites applies verbatim
— at the cost of a component whose prop list (`accent-white`, `accent-dark`) is shaped
by a design it no longer draws. That is the right trade while the fork stays ahead.

Keeping the hex values means the two apps still look alike. They are not the same
product and may drift; the token indirection is where that drift will be cheap to
absorb.

Naming the banned string in exactly one place — the guard test — costs a small
indirection when reading this ADR, and buys a tree in which the only occurrence of a
third party's name is the assertion that it must not occur.

This is not the only place the two repositories intentionally differ. The full list,
including the divergences that have nothing to do with branding, is maintained in
`docs/guide-fork-divergence.md`, which is the document to read before the next sync.
