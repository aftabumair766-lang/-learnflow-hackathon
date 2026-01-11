#!/usr/bin/env python3
import subprocess
import json
import sys

NAMESPACE = "dapr-system"

def run(cmd):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"✗ Verification failed")
        sys.exit(1)
    return result.stdout.strip()

# Check Dapr pods
pods_json = run(
    f"kubectl get pods -n {NAMESPACE} -o json"
)

pods = json.loads(pods_json)["items"]

if not pods:
    print("✗ No Dapr pods found")
    sys.exit(1)

running = sum(1 for p in pods if p["status"]["phase"] == "Running")
total = len(pods)

if running == total:
    print(f"✓ Dapr ready ({running}/{total} control plane pods Running)")
    sys.exit(0)
else:
    print(f"✗ Dapr not ready ({running}/{total} pods Running)")
    sys.exit(1)
