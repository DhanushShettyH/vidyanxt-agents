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
		"python-dotenv"
	],
	extra_packages=["./manager_agent"],

)
print(f"Created remote app: {remote_app.resource_name}")
