#!/usr/bin/env python3
import subprocess
import json
import sys

NAMESPACE = sys.argv[1] if len(sys.argv) > 1 else "learnflow"

def run(cmd):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"✗ Command failed: {cmd}")
        print(result.stderr.strip())
        sys.exit(1)
    return result.stdout.strip()

# Check namespace exists
try:
    ns_json = run(f"kubectl get namespace {NAMESPACE} -o json")
    ns = json.loads(ns_json)

    phase = ns["status"]["phase"]

    if phase == "Active":
        print(f"✓ Namespace '{NAMESPACE}' is Active")
        sys.exit(0)
    else:
        print(f"✗ Namespace '{NAMESPACE}' status: {phase}")
        sys.exit(1)

except Exception as e:
    print(f"✗ Namespace '{NAMESPACE}' not found")
    sys.exit(1)
