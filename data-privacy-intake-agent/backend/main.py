from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import json
from agent_service import AgentService
from database import get_db, init_db, close_db
from sqlalchemy.ext.asyncio import AsyncSession
import crud

app = FastAPI(
    title="Data Privacy Intake Agent API",
    description="API for Data Privacy case analysis and intake",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent_service = AgentService()


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()
    # Initialize default settings
    async for db in get_db():
        await crud.init_default_settings(db)
        await crud.init_default_agent_config(db)
        break


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await close_db()


# Pydantic models
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[list] = None


class ChatResponse(BaseModel):
    answer: str


class ConfigUpdate(BaseModel):
    company_name: Optional[str] = None
    form_a_link: Optional[str] = None
    form_b_link: Optional[str] = None
    custom_instructions: Optional[str] = None
    screening_questions: Optional[list] = None
    sensitive_data_keywords: Optional[list] = None


class SystemPromptUpdate(BaseModel):
    content: str


class SessionCreate(BaseModel):
    name: str


class SessionUpdate(BaseModel):
    name: Optional[str] = None
    messages: Optional[list] = None


class SettingsUpdate(BaseModel):
    model: Optional[str] = None
    custom_instructions: Optional[str] = None


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "version": "2.0.0", "database": "postgresql"}


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Analyze a data privacy case and return structured analysis.
    Supports conversation history for multi-turn chat.
    """
    try:
        # Load config and settings from database
        config = await crud.get_agent_config(db)
        if not config:
            config = {}
        
        settings = await crud.get_all_settings(db)
        
        # Merge custom instructions
        if settings.get("custom_instructions"):
            config["custom_instructions"] = settings["custom_instructions"]
        
        # Update agent model
        if settings.get("model"):
            agent_service.set_model(settings["model"])
        
        answer = await agent_service.analyze_case(
            request.message,
            config,
            conversation_history=request.conversation_history
        )
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Config endpoints
@app.get("/config")
async def get_config(db: AsyncSession = Depends(get_db)):
    """Get current agent configuration"""
    try:
        config = await crud.get_agent_config(db)
        return config or {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/config")
async def update_config(config_update: ConfigUpdate, db: AsyncSession = Depends(get_db)):
    """Update agent configuration"""
    try:
        current_config = await crud.get_agent_config(db) or {}
        
        update_data = config_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                current_config[key] = value
        
        await crud.set_agent_config(db, current_config)
        agent_service.reload_config()
        
        return {"status": "ok", "config": current_config}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Settings endpoints
@app.get("/settings")
async def get_settings(db: AsyncSession = Depends(get_db)):
    """Get current settings (model, custom instructions)"""
    try:
        settings = await crud.get_all_settings(db)
        
        # Parse available_models from JSON string
        if "available_models" in settings:
            try:
                settings["available_models"] = json.loads(settings["available_models"])
            except:
                pass
        
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/settings")
async def update_settings(update: SettingsUpdate, db: AsyncSession = Depends(get_db)):
    """Update settings"""
    try:
        update_data = update.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            if value is not None:
                await crud.set_setting(db, key, str(value))
        
        settings = await crud.get_all_settings(db)
        
        # Parse available_models
        if "available_models" in settings:
            try:
                settings["available_models"] = json.loads(settings["available_models"])
            except:
                pass
        
        return {"status": "ok", "settings": settings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Session endpoints
@app.get("/sessions")
async def list_sessions(db: AsyncSession = Depends(get_db)):
    """List all chat sessions"""
    try:
        sessions = await crud.get_all_sessions(db)
        return {"sessions": [s.to_dict() for s in sessions]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sessions")
async def create_session(request: SessionCreate, db: AsyncSession = Depends(get_db)):
    """Create a new chat session"""
    try:
        session = await crud.create_session(db, request.name)
        return {"status": "ok", "session": session.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions/{session_id}")
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific chat session"""
    try:
        session = await crud.get_session(db, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/sessions/{session_id}")
async def update_session(
    session_id: str,
    update: SessionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a chat session"""
    try:
        update_data = update.model_dump(exclude_unset=True)
        session = await crud.update_session(
            db,
            session_id,
            name=update_data.get("name"),
            messages=update_data.get("messages")
        )
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"status": "ok", "session": session.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a chat session"""
    try:
        success = await crud.delete_session(db, session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"status": "ok"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# System prompt endpoints (for advanced users)
@app.get("/system-prompt")
async def get_system_prompt():
    """Get current system prompt"""
    try:
        prompt = agent_service.get_system_prompt()
        return {"content": prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/system-prompt")
async def update_system_prompt(update: SystemPromptUpdate):
    """Update system prompt"""
    try:
        agent_service.update_system_prompt(update.content)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Knowledge base endpoints
@app.get("/knowledge/{filename}")
async def get_knowledge_file(filename: str):
    """Get content of a knowledge base file"""
    try:
        content = agent_service.get_knowledge_file(filename)
        return {"filename": filename, "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/knowledge/{filename}")
async def update_knowledge_file(filename: str, update: SystemPromptUpdate):
    """Update a knowledge base file"""
    try:
        agent_service.update_knowledge_file(filename, update.content)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/knowledge")
async def list_knowledge_files():
    """List all knowledge base files"""
    try:
        files = agent_service.list_knowledge_files()
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
