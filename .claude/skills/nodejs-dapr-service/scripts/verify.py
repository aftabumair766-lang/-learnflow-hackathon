#!/usr/bin/env python3
import sys
import os
from pathlib import Path

def verify_service(output_dir):
    """Verify generated service structure"""

    required_files = [
        "package.json",
        "src/index.js",
        "Dockerfile",
        "k8s/deployment.yaml"
    ]

    missing = []
    for file in required_files:
        if not os.path.exists(f"{output_dir}/{file}"):
            missing.append(file)

    if missing:
        print(f"✗ Missing files: {', '.join(missing)}")
        sys.exit(1)

    print(f"✓ Service structure valid ({len(required_files)} files)")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: verify.py <output-dir>")
        sys.exit(1)

    verify_service(sys.argv[1])
