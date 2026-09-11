"""The tree must carry no third-party branding (ADR-0060).

This lab is periodically re-synced from a company fork that is a superset of it.
Everything in that fork is wanted except its employer's identity, and the identity
would silently ride back in on the next port unless something fails when it does.
This is that something.

The banned name is assembled from fragments rather than written out, so that the
grep below finds nothing *including in this file*. Spelling it here would make the
test its own only violation, and every caller would then need a self-exclusion — an
exclusion that the next person to add a doc about branding would be tempted to widen.
One assembled constant keeps the invariant literally true: zero occurrences, anywhere.
"""

from __future__ import annotations

import re
import subprocess  # nosec B404 - fixed argv, no shell, repo-local git only
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The forbidden name, never spelled as one literal. See the module docstring.
BANNED_NAME = "xmart" + "labs"

#: Token prefix the fork used for its brand palette. ADR-0060 renames these to
#: ``--brand-*`` while keeping the hex values, so any survivor is an un-ported token.
BANNED_TOKEN_PREFIX = "--xl-"


def _tracked_matches(pattern: str) -> list[str]:
    """Return ``git grep`` hits for *pattern* across the tracked tree.

    Tracked-only is the point: untracked scratch files and the ``.git`` directory
    (where the fork's remote URL legitimately lives) are not part of what the repo
    publishes.
    """
    result = subprocess.run(  # nosec B603 B607 - fixed argv, no shell
        ["git", "grep", "-I", "-i", "-n", "-e", pattern],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    # git grep exits 1 with no output when nothing matched; anything else is a real
    # failure to search, which must not be mistaken for a clean tree.
    if result.returncode not in (0, 1):
        raise AssertionError(f"git grep failed: {result.stderr.strip()}")
    return [line for line in result.stdout.splitlines() if line.strip()]


def test_third_party_name_appears_nowhere_in_the_tracked_tree() -> None:
    matches = _tracked_matches(BANNED_NAME)
    assert not matches, (
        "Third-party branding has re-entered the tree (ADR-0060). "
        "Remove it from:\n  " + "\n  ".join(matches)
    )


def test_brand_palette_tokens_use_the_neutral_prefix() -> None:
    matches = _tracked_matches(BANNED_TOKEN_PREFIX)
    assert not matches, (
        "The fork's brand-palette tokens survived the port (ADR-0060): rename "
        f"{BANNED_TOKEN_PREFIX}* to --brand-* and keep the hex values.\n  "
        + "\n  ".join(matches)
    )


def test_the_neutral_mark_is_what_the_app_renders() -> None:
    """The replacement component exists and is the one the shell and login import."""
    mark = REPO_ROOT / "frontend" / "src" / "components" / "LabMark.tsx"
    assert mark.is_file(), "frontend/src/components/LabMark.tsx is missing (ADR-0060)"

    for relative in (
        "frontend/src/components/Shell.tsx",
        "frontend/src/pages/Login.tsx",
    ):
        source = (REPO_ROOT / relative).read_text(encoding="utf-8")
        assert re.search(r"\bLabMark\b", source), (
            f"{relative} no longer renders LabMark (ADR-0060)"
        )


def test_the_branding_skill_was_never_ingested() -> None:
    """No external skill directory carries the fork's branding pack.

    ``skills-lock.json`` and the generated adapter regions are derived by walking
    this directory, so its absence is the whole removal — nothing downstream needs
    a manual edit.
    """
    external = REPO_ROOT / ".github" / "skills-external"
    if not external.is_dir():
        return
    offenders = [
        entry.name for entry in external.iterdir() if BANNED_NAME in entry.name.lower()
    ]
    assert not offenders, (
        f"A third-party branding skill is present in .github/skills-external/: {offenders} "
        "(ADR-0060). Delete it and re-run `make sync-skills`."
    )
