#!/usr/bin/env python3
import sys
import os
import yaml
from pathlib import Path

def generate_service(spec_file, output_dir):
    """Generate complete Node.js + Dapr service from YAML spec"""

    # Read spec
    with open(spec_file, 'r') as f:
        spec = yaml.safe_load(f)

    service_name = spec['service']
    port = spec['metadata']['port']

    # Create directory structure
    os.makedirs(f"{output_dir}/src", exist_ok=True)
    os.makedirs(f"{output_dir}/k8s", exist_ok=True)

    # Generate package.json
    package_json = {
        "name": service_name,
        "version": "1.0.0",
        "main": "src/index.js",
        "scripts": {
            "start": "node src/index.js"
        },
        "dependencies": {
            "express": "^4.18.0"
        }
    }

    with open(f"{output_dir}/package.json", 'w') as f:
        import json
        json.dump(package_json, f, indent=2)

    # Generate src/index.js
    index_js = f"""const express = require('express');
const app = express();
const PORT = process.env.PORT || {port};

app.use(express.json());

// Health endpoint
app.get('/health', (req, res) => {{
  res.json({{ status: 'healthy' }});
}});

// TODO: Add endpoints from spec

app.listen(PORT, () => {{
  console.log(`{service_name} listening on port ${{PORT}}`);
}});
"""

    with open(f"{output_dir}/src/index.js", 'w') as f:
        f.write(index_js)

    # Generate Dockerfile
    dockerfile = f"""FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
EXPOSE {port}
CMD ["npm", "start"]
"""

    with open(f"{output_dir}/Dockerfile", 'w') as f:
        f.write(dockerfile)

    # Generate K8s deployment
    deployment = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  namespace: learnflow
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "{service_name}"
        dapr.io/app-port: "{port}"
    spec:
      containers:
      - name: {service_name}
        image: {service_name}:latest
        imagePullPolicy: Never
        ports:
        - containerPort: {port}
        env:
        - name: PORT
          value: "{port}"
---
apiVersion: v1
kind: Service
metadata:
  name: {service_name}
  namespace: learnflow
spec:
  selector:
    app: {service_name}
  ports:
  - port: {port}
    targetPort: {port}
"""

    with open(f"{output_dir}/k8s/deployment.yaml", 'w') as f:
        f.write(deployment)

    print(f"✓ Generated {service_name}")
    print(f"  - package.json")
    print(f"  - src/index.js")
    print(f"  - Dockerfile")
    print(f"  - k8s/deployment.yaml")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: generator.py <spec-file> <output-dir>")
        sys.exit(1)

    generate_service(sys.argv[1], sys.argv[2])
