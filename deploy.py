# deploy.py
import os
import sys

import vertexai
from dotenv import load_dotenv
load_dotenv()

from vertexai import agent_engines
from vertexai.preview import reasoning_engines

from manager_agent.agent import root_agent  # Your original ADK agent

PROJECT_ID = os.environ.get("PROJECT_ID", "vidyanxt-c5816")
LOCATION = os.environ.get("LOCATION", "us-central1")
STAGING_BUCKET = os.environ.get("STAGING_BUCKET", "gs://vidyanxt-agnets")

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET
)

app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True
)

remote_app = agent_engines.create(
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "python-dotenv",
        "fastapi",
        "uvicorn[standard]", 
        "pydantic",
        "google-genai"  # Added this since you're using types from google.genai
    ],
    extra_packages=["./manager_agent"],
)
print(f"Created remote app: {remote_app.resource_name}")

# Save the deployment info for reference
deployment_info = {
    "resource_name": remote_app.resource_name,
    "project_id": PROJECT_ID,
    "location": LOCATION,
    "staging_bucket": STAGING_BUCKET
}

# Optionally save deployment info to a file
import json
with open('.deployment_info.json', 'w') as f:
    json.dump(deployment_info, f, indent=2)

print("✅ Deployment completed!")
print(f"📄 Deployment info saved to .deployment_info.json")
