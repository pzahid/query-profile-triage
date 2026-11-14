"""Rule-based triage of a simplified query-profile summary.

The input is a JSON summary you extract from a query profile (the real
profile is far richer). Expected shape:

{
  "query_id": "...",
  "total_ms": 125000,
  "planning_ms": 18000,
  "queue_ms": 500,
  "phases": [{"name": "05-xx-HASH_JOIN", "max_ms": 80000, "avg_ms": 9000,
              "spilled_bytes": 0}],
  "reflections_considered": 3,
  "reflections_used": 0
}
"""


def triage(p):
    findings = []
    total = max(p.get("total_ms", 0), 1)

    if p.get("planning_ms", 0) / total > 0.3:
        findings.append(("planning", "Planning takes over 30% of runtime. "
                         "Check metadata size, number of files and view nesting."))
    if p.get("queue_ms", 0) / total > 0.2:
        findings.append(("queueing", "Query waited in the queue for a large share "
                         "of runtime. Review workload management rules."))
    for ph in p.get("phases", []):
        avg = max(ph.get("avg_ms", 0), 1)
        if ph.get("max_ms", 0) / avg > 5:
            findings.append(("skew", f"{ph['name']}: slowest thread is "
                             f"{ph['max_ms'] / avg:.1f}x the average. Look for data skew."))
        if ph.get("spilled_bytes", 0) > 0:
            findings.append(("spill", f"{ph['name']} spilled to disk. "
                             "Consider more executor memory or a smaller join input."))
    if p.get("reflections_considered", 0) and not p.get("reflections_used", 0):
        findings.append(("reflection", "Reflections were considered but none "
                         "matched. Check the reflection definition and its refresh state."))
    return findings
