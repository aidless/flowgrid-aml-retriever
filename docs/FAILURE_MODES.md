# FAILURE_MODES

Three ways this repository can look healthier than it is. These are limits of
the evidence, not a second scoreboard. There is still no official Agent Memory
Leaderboard score.

## False greens from synthetic queries

`aml_retriever/evaluation/dataset.py` builds the queries it later scores. Gold
messages reuse the entities, dates, numbers, and update phrasing that the
lexical ranker is built to notice. Recall@20 near 1.0 on the classic medium
suite means that generator and that ranker agree. It does not mean the same
ranker would place official items first.

`./scripts/run_tests.sh` does not run that ablation unless you pass
`--with-eval`. A green unit-test run is not a leaderboard result.

The README table is a historical local run of that synthetic suite. Current
`DEFAULT_FLAGS` also turn on `ebbinghaus_decay` and `consolidation_dedup`.
Those two flags are not what the identical L11 and L12 rows measured. This
clone has no re-measurement, so those rows are not today's default.

LoCoMo-style figures and the DeepSeek end-to-end notes in the README refer to
files that are not in this repository. `scripts/run_eval.py` cannot reproduce
them. Code comments that cite LoCoMo or BEAM deltas are the same kind of note:
not an official score, and not output of the synthetic harness.

## User isolation leaks

Search is specified to return evidence for exactly one `user_id`. The store is
one SQLite file. In the FTS5 table, `user_id` is an `UNINDEXED` column.
Isolation is the SQL predicate `AND user_id=?` on that shared table, not a
per-user database.

A channel that unions document ids before that predicate (FTS, facts, entity
edges, dense vectors) can mix another user's ids into ranking even when a
later filter drops the text. `delete-user` has to name every table or leftover
rows stay searchable. The offline demo checks that one other user gets zero
hits on one query. That does not cover views, facts, graphs, or vectors.

Missing `user_id` must fail the request. It must not fall open to every row.

## Temporal heuristics overclaim

`temporal_intent` amplification was a negative control on the synthetic suite
and stays off. The weak cell is temporal queries whose wording does not repeat
the stored phrase (see the paraphrase rows in `docs/EVAL.md`). Overall MRR
hides that cell.

`content_timestamp_prefix` adds a day-level label on the text returned to a
downstream model. It does not change the stored message and it does not make
the label an exact timestamp. The prefix is gated. An ungated prefix is a
different behavior. Flags that comments call v1.4
(`conflict_pair_return`, `low_confidence_abstain`, `current_value_recency`,
`ordering_prefix`, `chrono_ordering`) default off. Turning one on is not a
released score.

A previous README sentence claimed a local +5.3 percentage-point end-to-end
gain for a time-anchor fallback. No script, table, or fixture in this
repository reproduces that figure. The claim is withdrawn.

Package version is `aml_retriever.__version__` (`1.1.0`). The HTTP banner is
`aml-retriever/1.1`. Ablation names such as L11 and L12 are not that version.
