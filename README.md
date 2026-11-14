# Query Profile Triage

A small rule engine that turns a query-profile summary into plain-language findings: planning-heavy queries, queueing, thread skew, spilling and reflections that never matched.

```bash
python -m triage examples/slow_query.json
```

This is a teaching tool built from patterns seen in day-to-day support work. It reads a simplified JSON summary, not the raw profile format. Extend triage/rules.py with your own rules.

Tests: pip install pytest, then pytest.
