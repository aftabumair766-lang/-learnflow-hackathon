#!/usr/bin/env python3
import subprocess
import json
import sys

NAMESPACE = "kafka"
KAFKA_NAME = "my-kafka"

def run(cmd):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()

# Check Kafka CR exists
kafka_json = run(f"kubectl get kafka {KAFKA_NAME} -n {NAMESPACE} -o json")
if not kafka_json:
    print(f"✗ Kafka CR '{KAFKA_NAME}' not found")
    sys.exit(1)

kafka = json.loads(kafka_json)
conditions = kafka.get("status", {}).get("conditions", [])
ready = any(c["type"] == "Ready" and c["status"] == "True" for c in conditions)

# Check Kafka pods
pods_json = run(f"kubectl get pods -n {NAMESPACE} -l strimzi.io/name={KAFKA_NAME}-kafka -o json")
if pods_json:
    pods = json.loads(pods_json)["items"]
    running = sum(1 for p in pods if p["status"]["phase"] == "Running")
else:
    running = 0

# Check service
svc = run(f"kubectl get svc {KAFKA_NAME}-kafka-bootstrap -n {NAMESPACE}")

if ready and running > 0 and svc:
    print(f"✓ Kafka ready ({running} pods Running, CR Ready)")
    sys.exit(0)
else:
    print(f"✗ Kafka not ready (Pods: {running}, CR Ready: {ready})")
    sys.exit(1)

