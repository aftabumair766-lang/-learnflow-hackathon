#!/usr/bin/env bash
set -e

echo "Installing Dapr on Kubernetes..."

# Check if dapr CLI is installed
if ! command -v dapr &> /dev/null; then
    echo "✗ Dapr CLI not found. Install: curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash"
    exit 1
fi

# Initialize Dapr on Kubernetes
dapr init -k --wait --timeout 300 > /dev/null 2>&1

echo "✓ Dapr installed in namespace 'dapr-system'"
