# Archived benchmark material

Directories here are **not part of the case corpus**. Everything that discovers
benchmarks — the seeder (`case_service._find_case_dir_by_task_id`),
`scripts/build_prompt_variants.py`, and the corpus invariant tests — globs
`benchmarks/*/`, one level deep. Nesting a directory under `_archive/` takes it out of
that set while leaving it readable in the tree.

Nothing in here is seeded, scored, or held to the corpus invariants: the two-variant
prompt pair ([ADR-0047](../../docs/adr/0047-a-case-exposes-two-prompt-variants-the-task-and-the-task-plus-the-harness.md))
and the tagged rubric levels ([ADR-0050](../../docs/adr/0050-a-case-ships-its-own-tests.md)).

## `tetris-v1/`

The lab's first pilot. [ADR-0050](../../docs/adr/0050-a-case-ships-its-own-tests.md)
retired it: a case whose automated grade caps at "runs without crashing" cannot carry a
harness experiment, so its manual-scoring lane (`score_tetris.py`, `show_results.py`,
`summarize_results.py`, the `bench-results` target) was deleted and the corpus moved to
`benchmarks/tetris-v2/`.

The *case* is retired. The *measurement record* is not: `runs.yaml` is 738 lines of
this lab's actual tetris-v1 run registry, and `results.csv` holds the scores it
produced. Those are history, and history is the one thing a measurement lab should not
delete. It lives here rather than under `benchmarks/tetris/` because sitting in the
live corpus made it a seeded case again, which is exactly what ADR-0050 forbids.

Read it; do not run it. Its archived run artifacts are under `data/runs/tetris-v1-*`.
