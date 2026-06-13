import json
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from models import Session, Settings, AgentConfig
from typing import Optional, List


# Session CRUD operations
async def create_session(db: AsyncSession, name: str) -> Session:
    """Create a new chat session"""
    session = Session(name=name, messages=[])
    db.add(session)
    await db.flush()
    await db.refresh(session)
    return session


async def get_session(db: AsyncSession, session_id: str) -> Optional[Session]:
    """Get a session by ID"""
    result = await db.execute(
        select(Session).where(Session.id == session_id)
    )
    return result.scalar_one_or_none()


async def get_all_sessions(db: AsyncSession) -> List[Session]:
    """Get all sessions ordered by updated_at desc"""
    result = await db.execute(
        select(Session).order_by(Session.updated_at.desc())
    )
    return result.scalars().all()


async def update_session(
    db: AsyncSession,
    session_id: str,
    name: Optional[str] = None,
    messages: Optional[list] = None
) -> Optional[Session]:
    """Update a session"""
    session = await get_session(db, session_id)
    if not session:
        return None
    
    if name is not None:
        session.name = name
    if messages is not None:
        session.messages = messages
    
    await db.flush()
    await db.refresh(session)
    return session


async def delete_session(db: AsyncSession, session_id: str) -> bool:
    """Delete a session"""
    result = await db.execute(
        delete(Session).where(Session.id == session_id)
    )
    return result.rowcount > 0


# Settings CRUD operations
async def get_setting(db: AsyncSession, key: str) -> Optional[str]:
    """Get a setting value by key"""
    result = await db.execute(
        select(Settings).where(Settings.key == key)
    )
    setting = result.scalar_one_or_none()
    return setting.value if setting else None


async def set_setting(db: AsyncSession, key: str, value: str) -> Settings:
    """Set a setting value"""
    result = await db.execute(
        select(Settings).where(Settings.key == key)
    )
    setting = result.scalar_one_or_none()
    
    if setting:
        setting.value = value
    else:
        setting = Settings(key=key, value=value)
        db.add(setting)
    
    await db.flush()
    await db.refresh(setting)
    return setting


async def get_all_settings(db: AsyncSession) -> dict:
    """Get all settings as a dictionary"""
    result = await db.execute(select(Settings))
    settings = result.scalars().all()
    return {s.key: s.value for s in settings}


async def init_default_settings(db: AsyncSession):
    """Initialize default settings if not exists"""
    defaults = {
        "model": "gpt-4o-mini",
        "custom_instructions": "",
        "available_models": json.dumps([
            {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "provider": "openai"},
            {"id": "gpt-4o", "name": "GPT-4o", "provider": "openai"},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "provider": "openai"},
            {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro", "provider": "google"},
            {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash", "provider": "google"},
            {"id": "qwen-max", "name": "Qwen Max", "provider": "alibaba"},
            {"id": "qwen-plus", "name": "Qwen Plus", "provider": "alibaba"}
        ])
    }
    
    for key, value in defaults.items():
        existing = await get_setting(db, key)
        if existing is None:
            await set_setting(db, key, value)


# Agent Config CRUD operations
async def get_agent_config(db: AsyncSession) -> Optional[dict]:
    """Get the agent configuration"""
    result = await db.execute(
        select(AgentConfig).order_by(AgentConfig.id.desc()).limit(1)
    )
    config = result.scalar_one_or_none()
    return config.config_data if config else None


async def set_agent_config(db: AsyncSession, config_data: dict) -> AgentConfig:
    """Set the agent configuration"""
    # Delete old configs and create new one
    await db.execute(delete(AgentConfig))
    
    config = AgentConfig(config_data=config_data)
    db.add(config)
    await db.flush()
    await db.refresh(config)
    return config


async def init_default_agent_config(db: AsyncSession):
    """Initialize default agent configuration if not exists"""
    existing = await get_agent_config(db)
    if existing is None:
        default_config = {
            "company_name": "Công ty Fintech ABC",
            "form_a_link": "https://company.form/privacy-domestic-intake",
            "form_b_link": "https://company.form/privacy-cross-border-intake",
            "custom_instructions": "",
            "screening_questions": [
                "Đối tác nhận dữ liệu ở Việt Nam hay nước ngoài?",
                "Dữ liệu dự kiến chia sẻ gồm những field nào?",
                "Dữ liệu có liên quan khách hàng/người dùng không?",
                "Đối tác dùng dữ liệu để làm gì?",
                "Dữ liệu gửi bằng cách nào: API, file Excel, SFTP hay email?",
                "Đối tác lưu dữ liệu bao lâu?",
                "Đã có hợp đồng/DPA với đối tác chưa?"
            ],
            "sensitive_data_keywords": [
                "credit score", "transaction", "BNPL", "loan", "payment",
                "bank account", "salary", "income", "biometric", "health"
            ]
        }
        await set_agent_config(db, default_config)
