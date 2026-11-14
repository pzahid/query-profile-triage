import json
import sys
from .rules import triage

profile = json.load(open(sys.argv[1]))
found = triage(profile)
print(f"Query {profile.get('query_id', '?')}: {len(found)} finding(s)")
for kind, msg in found:
    print(f"  [{kind}] {msg}")
