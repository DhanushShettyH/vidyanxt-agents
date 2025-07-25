# main.py
import asyncio
import uuid
import os
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Google ADK imports
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from manager_agent.agent import root_agent

load_dotenv()

# Pydantic models for API requests/responses
class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    user_id: str
    metadata: Optional[Dict[str, Any]] = None

class VidyaNXTService:
    def __init__(self):
        # Setup session service
        self.session_service = InMemorySessionService()
        self.app_name = "VidyaNXT"
        
        # Initial state for new sessions
        self.initial_state = {
            "AI Name": "Vidya",
            "AI Background": """
                You are Vidya, a helpful AI assistant specializing in education for Indian teachers.
                You help with curriculum planning, teaching strategies, and educational content creation.
                You're knowledgeable about multi-grade classrooms and Indian educational contexts.
            """,
            "interaction_history": [],
        }
        
        # Setup runner
        self.runner = Runner(
            agent=root_agent,
            app_name=self.app_name,
            session_service=self.session_service,
        )
        
        # Track active sessions
        self.active_sessions = {}
        
    def get_or_create_session(self, user_id: str, session_id: Optional[str] = None):
        """Get existing session or create new one for user"""
        if session_id is None:
            session_id = str(uuid.uuid4())
            
        # Try to get existing session
        session = self.session_service.get_session(self.app_name, user_id, session_id)
        if not session:
            # Create new session with initial state
            session = self.session_service.create_session(
                app_name=self.app_name,
                user_id=user_id,
                session_id=session_id,
                state=self.initial_state
            )
            print(f"🆕 Created new session for user: {user_id}, session: {session_id}")
        
        # Track session
        self.active_sessions[f"{user_id}:{session_id}"] = True
        
        return user_id, session_id
    
    def add_user_query_to_history(self, user_id: str, session_id: str, query: str):
        """Add user query to session history"""
        session = self.session_service.get_session(self.app_name, user_id, session_id)
        if session:
            if "interaction_history" not in session.state:
                session.state["interaction_history"] = []
            session.state["interaction_history"].append({
                "type": "user",
                "message": query,
                "timestamp": str(asyncio.get_event_loop().time())
            })
    
    async def call_agent_async(self, user_id: str, session_id: str, query: str) -> str:
        """Process query through the agent and return response"""
        try:
            # Create message content
            new_message = types.Content(
                role="user", 
                parts=[types.Part(text=query)]
            )
            
            print(f"🤔 Processing query for user {user_id}: {query[:50]}...")
            
            # Run the agent
            final_response_text = None
            for event in self.runner.run(
                user_id=user_id, 
                session_id=session_id, 
                new_message=new_message
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        final_response_text = event.content.parts[0].text
            
            # Add response to history
            session = self.session_service.get_session(self.app_name, user_id, session_id)
            if session and final_response_text:
                if "interaction_history" not in session.state:
                    session.state["interaction_history"] = []
                session.state["interaction_history"].append({
                    "type": "assistant",
                    "message": final_response_text,
                    "timestamp": str(asyncio.get_event_loop().time())
                })
            
            return final_response_text or "I apologize, I couldn't generate a response."
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    async def ask_question(self, question: str, user_id: str, session_id: Optional[str] = None):
        """Main method to process a question"""
        # Get or create session
        user_id, session_id = self.get_or_create_session(user_id, session_id)
        
        # Add user query to history
        self.add_user_query_to_history(user_id, session_id, question)
        
        # Process through agent
        response = await self.call_agent_async(user_id, session_id, question)
        
        return response, session_id

# Initialize FastAPI app
app = FastAPI(
    title="VidyaNXT AI Service",
    description="Educational AI Assistant for Indian Teachers",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
service = VidyaNXTService()

@app.get("/")
async def root():
    return {
        "service": "VidyaNXT AI",
        "status": "running",
        "version": "1.0.0",
        "active_sessions": len(service.active_sessions)
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "active_sessions": len(service.active_sessions)
    }

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """Main endpoint for asking questions to the AI"""
    # Generate user_id if not provided
    user_id = request.user_id or f"user_{uuid.uuid4().hex[:8]}"
    
    try:
        # Process the question
        answer, session_id = await service.ask_question(
            question=request.question,
            user_id=user_id,
            session_id=request.session_id
        )
        
        return QueryResponse(
            answer=answer,
            session_id=session_id,
            user_id=user_id,
            metadata={
                "question_length": len(request.question),
                "context": request.context
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/new-session")
async def create_new_session(user_id: str):
    """Create a new session for a user"""
    session_id = str(uuid.uuid4())
    _, created_session_id = service.get_or_create_session(user_id, session_id)
    
    return {
        "user_id": user_id,
        "session_id": created_session_id,
        "status": "created"
    }

@app.get("/sessions/{user_id}")
async def get_user_sessions(user_id: str):
    """Get sessions for a user"""
    user_sessions = [
        key.split(":")[1] for key in service.active_sessions.keys() 
        if key.startswith(f"{user_id}:")
    ]
    
    return {
        "user_id": user_id,
        "sessions": user_sessions,
        "count": len(user_sessions)
    }

@app.get("/session/{user_id}/{session_id}/history")
async def get_session_history(user_id: str, session_id: str):
    """Get conversation history for a session"""
    session = service.session_service.get_session(
        service.app_name, user_id, session_id
    )
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    history = session.state.get("interaction_history", [])
    
    return {
        "user_id": user_id,
        "session_id": session_id,
        "history": history,
        "count": len(history)
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
