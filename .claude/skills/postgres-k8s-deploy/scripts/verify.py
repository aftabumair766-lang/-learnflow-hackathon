#!/usr/bin/env python3
import subprocess
import json
import sys

NAMESPACE = sys.argv[1] if len(sys.argv) > 1 else "learnflow"
DATABASES = ["students", "tutors", "matching"]

def run(cmd):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()

# Check all PostgreSQL pods
all_running = True
for db in DATABASES:
    pods_json = run(
        f"kubectl get pods -n {NAMESPACE} -l app.kubernetes.io/name=postgresql,app.kubernetes.io/instance=postgres-{db} -o json"
    )

    if not pods_json:
        print(f"✗ postgres-{db} pods not found")
        all_running = False
        continue

    pods = json.loads(pods_json)["items"]
    if not pods:
        print(f"✗ postgres-{db} not deployed")
        all_running = False
        continue

    running = sum(1 for p in pods if p["status"]["phase"] == "Running")
    if running == 0:
        print(f"✗ postgres-{db} not running")
        all_running = False

if all_running:
    print(f"✓ All PostgreSQL databases ready in namespace '{NAMESPACE}'")
    sys.exit(0)
else:
    print(f"✗ Some PostgreSQL databases not ready")
    sys.exit(1)
