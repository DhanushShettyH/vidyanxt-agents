# manager/agent.py
from google.adk.agents import Agent

from .sub_agent.profile_agent.agent import profile_agent
from .sub_agent.classification_agent.agent import classification_agent
from .sub_agent.matching_agent.agent import matching_agent
from .sub_agent.post_orchestration_agent.agent import post_orchestration_agent
from .sub_agent.ai_chat_agent.agent import ai_chat_agent
from .sub_agent.differentiation_agent.agent import differentiation_agent
from .sub_agent.vidya_orchestrator_agent.agent import vidya_orchestrator_agent
from .sub_agent.visual_aid_agent.agent import visual_aid_agent
from .sub_agent.simulated_classroom_agent.agent import simulated_classroom_agent
from .sub_agent.wellness_agent.agent import wellness_agent
from .sub_agent.training_agent.agent import training_agent
from .sub_agent.weekly_planner_agent.agent import weekly_planner_agent




root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="""
    You are a manager agent responsible for overseeing other agents.
    
    Always delegate tasks to the appropriate agent:
    - profile_agent: For teacher profile analysis and processing
    - classification_agent: An agent to classify teacher challenges and determine urgency levels for effective educational support routing
    - matching_agent: An agent to find suitable peer matches for teachers based on their profiles and challenge classification.
    - post_orchestration_agent: An agent to orchestrate and prioritize peer connections and AI chat recommendations for resolving teacher challenges.
    - ai_chat_agent: An AI agent that generates personalized teaching assistant personas, context-aware support responses, session analyses, and wellness insights for teachers
    - vidya_orchestrator_agent: An orchestrator agent coordinating multiple AI sub-agents to generate integrated, culturally relevant, and validated teaching content.
    - hyper_local_agent:  An agent to generate culturally relevant, hyper-localized educational content using regional crops, festivals, landmarks, and heroes.
    - differentiation_agent: An agent to create differentiated instructional content tailored to multiple grade levels aligned with curriculum standards.
    - visual_aid_agent: An agent to generate structured educational visual aids, diagrams, and hands-on activities tailored for Indian multi-grade classrooms.
    - simulated_classroom_agent: An agent to simulate classroom testing of educational materials using diverse student personas to evaluate content effectiveness..
    - wellness_agent:  An agent to analyze teacher wellness indicators from challenges and chats, generate insights, and produce wellness dashboard summaries.
    - training_agent: An agent to analyze teacher training needs, generate micro-learning modules, and create community peer-learning modules.
    - weekly_planner_agent:  An expert curriculum planner agent generating detailed weekly multi-grade lesson plans adapted to student age and syllabus requirements.

    
    
    
    
    """,
    sub_agents=[
        profile_agent,
        classification_agent,
        matching_agent,
        post_orchestration_agent,
        ai_chat_agent,
        vidya_orchestrator_agent,
        differentiation_agent,
        visual_aid_agent,
        simulated_classroom_agent,
        wellness_agent,
        training_agent,
        weekly_planner_agent
        ],
 
)
