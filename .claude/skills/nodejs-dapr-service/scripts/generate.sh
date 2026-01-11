#!/usr/bin/env bash
set -e

SPEC_FILE=$1
OUTPUT_DIR=$2

if [ -z "$SPEC_FILE" ] || [ -z "$OUTPUT_DIR" ]; then
  echo "Usage: $0 <spec-file> <output-dir>"
  exit 1
fi

echo "Generating Node.js + Dapr service from spec..."

# Call Python generator
python3 "$(dirname "$0")/generator.py" "$SPEC_FILE" "$OUTPUT_DIR"

echo "✓ Service generated at '$OUTPUT_DIR'"
