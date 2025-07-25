# manager/sub_agents/profile_agent/agent.py
from google.adk.agents import Agent

profile_agent = Agent(
    name="profile_agent",
    model="gemini-2.0-flash",
    description=(
        "An agent to generate a concise, professional teacher profile summary "
        "from given data fields: name, grades, location, experience."
    ),
    instruction="""
You are a Profile Agent focused on producing a professional summary based on teacher data.

Input fields:
- name: teacher's full name
- grades: list of grades taught
- location: teaching location
- experience: years of teaching experience

Generate a concise, professional summary (max 100 words), highlighting teaching strengths and expertise.

Return only the summary text, no additional fields or metadata.
    """
)
