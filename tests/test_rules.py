from triage.rules import triage


def kinds(p):
    return {k for k, _ in triage(p)}


def test_slow_query_flags_everything_expected():
    p = {"total_ms": 125000, "planning_ms": 45000, "queue_ms": 500,
         "phases": [{"name": "x", "max_ms": 80000, "avg_ms": 9000, "spilled_bytes": 1}],
         "reflections_considered": 3, "reflections_used": 0}
    assert kinds(p) == {"planning", "skew", "spill", "reflection"}


def test_healthy_query():
    p = {"total_ms": 1000, "planning_ms": 50, "queue_ms": 0, "phases": []}
    assert triage(p) == []
