#!/bin/bash
set -e

SPEC_FILE="$1"
OUTPUT_DIR="$2"

if [ -z "$SPEC_FILE" ] || [ -z "$OUTPUT_DIR" ]; then
  echo "Usage: $0 <spec-file> <output-dir>"
  exit 1
fi

echo "Generating Next.js + Dapr frontend from spec..."

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Generate basic Next.js structure
python3 "$(dirname "$0")/generator.py" "$SPEC_FILE" "$OUTPUT_DIR"

echo "✓ Frontend generated at '$OUTPUT_DIR'"
