# manager/agent.py
from google.adk.agents import Agent

from .sub_agent.profile_agent.agent import profile_agent

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="""
    You are a manager agent responsible for overseeing other agents.
    
    Always delegate tasks to the appropriate agent:
    - profile_agent: For teacher profile analysis and processing
    
    """,
    sub_agents=[profile_agent],
 
)
