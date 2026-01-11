#!/usr/bin/env python3
import sys
import os
import yaml
import json

def generate_frontend(spec_file, output_dir):
    # Read spec
    with open(spec_file, 'r') as f:
        spec = yaml.safe_load(f)

    app_name = spec.get('frontend', 'learnflow-web')
    port = spec.get('metadata', {}).get('port', 3000)

    # Create directories
    os.makedirs(f"{output_dir}/app", exist_ok=True)
    os.makedirs(f"{output_dir}/components", exist_ok=True)
    os.makedirs(f"{output_dir}/k8s", exist_ok=True)
    os.makedirs(f"{output_dir}/public", exist_ok=True)

    # Generate package.json
    package_json = {
        "name": app_name,
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start -p " + str(port)
        },
        "dependencies": {
            "next": "14.0.0",
            "react": "18.2.0",
            "react-dom": "18.2.0"
        }
    }

    with open(f"{output_dir}/package.json", 'w') as f:
        json.dump(package_json, f, indent=2)

    # Generate app/page.tsx (Next.js 13+ App Router)
    page_tsx = f"""export default function Home() {{
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold mb-8">LearnFlow</h1>
      <p className="text-lg mb-4">AI-Powered Learning Platform</p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="border p-4 rounded">
          <h2 className="text-2xl font-bold">Students</h2>
          <p>Register and find tutors</p>
        </div>

        <div className="border p-4 rounded">
          <h2 className="text-2xl font-bold">Tutors</h2>
          <p>Offer your expertise</p>
        </div>

        <div className="border p-4 rounded">
          <h2 className="text-2xl font-bold">Matching</h2>
          <p>AI-powered connections</p>
        </div>
      </div>
    </main>
  )
}}
"""

    with open(f"{output_dir}/app/page.tsx", 'w') as f:
        f.write(page_tsx)

    # Generate app/layout.tsx
    layout_tsx = """export const metadata = {
  title: 'LearnFlow',
  description: 'AI-Powered Learning Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
"""

    with open(f"{output_dir}/app/layout.tsx", 'w') as f:
        f.write(layout_tsx)

    # Generate Dockerfile
    dockerfile = f"""FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE {port}
CMD ["npm", "start"]
"""

    with open(f"{output_dir}/Dockerfile", 'w') as f:
        f.write(dockerfile)

    # Generate k8s/deployment.yaml
    deployment_yaml = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
  namespace: learnflow
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "{app_name}"
        dapr.io/app-port: "{port}"
    spec:
      containers:
      - name: {app_name}
        image: {app_name}:latest
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
  name: {app_name}
  namespace: learnflow
spec:
  selector:
    app: {app_name}
  ports:
  - port: {port}
    targetPort: {port}
"""

    with open(f"{output_dir}/k8s/deployment.yaml", 'w') as f:
        f.write(deployment_yaml)

    # Generate next.config.js
    next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {}

module.exports = nextConfig
"""

    with open(f"{output_dir}/next.config.js", 'w') as f:
        f.write(next_config)

    # Generate tsconfig.json
    tsconfig = """{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
"""

    with open(f"{output_dir}/tsconfig.json", 'w') as f:
        f.write(tsconfig)

    print(f"✓ Generated {app_name}")
    print(f"  - package.json")
    print(f"  - app/page.tsx")
    print(f"  - app/layout.tsx")
    print(f"  - Dockerfile")
    print(f"  - k8s/deployment.yaml")
    print(f"  - next.config.js")
    print(f"  - tsconfig.json")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: generator.py <spec-file> <output-dir>")
        sys.exit(1)

    generate_frontend(sys.argv[1], sys.argv[2])
