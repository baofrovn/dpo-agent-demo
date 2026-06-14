import json
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from models import Session, Settings, AgentConfig, User, ChecklistItem, ScreeningQuestion, SensitiveKeyword, RuleAuditLog, IntakeFormLink, FormLinkCategory
from typing import Optional, List
from auth import get_password_hash


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
        "model": "qwen/qwen3-5-27b",
        "custom_instructions": "",
        "available_models": json.dumps([
            {"id": "qwen/qwen3-5-27b", "name": "Qwen 3.5 27B", "provider": "VNG Cloud"},
            {"id": "openai/gpt-5", "name": "GPT-5", "provider": "VNG Cloud"}
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


# User CRUD operations
async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """Get a user by username"""
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
    """Get a user by ID"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, password: str, is_active: bool = True) -> User:
    """Create a new user"""
    password_hash = get_password_hash(password)
    user = User(username=username, password_hash=password_hash, is_active=is_active)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def get_all_users(db: AsyncSession) -> List[User]:
    """Get all users"""
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    return result.scalars().all()


async def init_default_user(db: AsyncSession):
    """Initialize default admin user if not exists"""
    existing = await get_user_by_username(db, "admin")
    if existing is None:
        await create_user(db, "admin", "admin123", is_active=True)
        await db.commit()


# Intake Form Links CRUD operations
async def get_intake_form_links(db: AsyncSession) -> List[IntakeFormLink]:
    """Get all intake form links"""
    result = await db.execute(
        select(IntakeFormLink).order_by(IntakeFormLink.display_order)
    )
    return result.scalars().all()


async def init_default_form_links(db: AsyncSession):
    """Initialize default form links from agent config if not exists"""
    # Check if any form links already exist
    existing_links = await get_intake_form_links(db)
    if existing_links:
        return  # Already initialized
    
    # Get current agent config to migrate old form links
    config = await get_agent_config(db)
    
    default_links = []
    
    # Migrate Form A if exists in config
    if config and config.get("form_a_link"):
        default_links.append(IntakeFormLink(
            name="Form A - Domestic Data Sharing Intake",
            url=config["form_a_link"],
            description="Dùng cho chia sẻ dữ liệu cá nhân với đối tác trong nước",
            category=FormLinkCategory.DOMESTIC,
            conditions="Đối tác và server đều ở Việt Nam",
            is_active=True,
            display_order=0
        ))
    else:
        # Default Form A
        default_links.append(IntakeFormLink(
            name="Form A - Domestic Data Sharing Intake",
            url="https://company.form/privacy-domestic-intake",
            description="Dùng cho chia sẻ dữ liệu cá nhân với đối tác trong nước",
            category=FormLinkCategory.DOMESTIC,
            conditions="Đối tác và server đều ở Việt Nam",
            is_active=True,
            display_order=0
        ))
    
    # Migrate Form B if exists in config
    if config and config.get("form_b_link"):
        default_links.append(IntakeFormLink(
            name="Form B - Cross-border Data Transfer Intake",
            url=config["form_b_link"],
            description="Dùng cho chia sẻ dữ liệu cá nhân ra nước ngoài",
            category=FormLinkCategory.CROSS_BORDER,
            conditions="Đối tác hoặc server ở nước ngoài",
            is_active=True,
            display_order=1
        ))
    else:
        # Default Form B
        default_links.append(IntakeFormLink(
            name="Form B - Cross-border Data Transfer Intake",
            url="https://company.form/privacy-cross-border-intake",
            description="Dùng cho chia sẻ dữ liệu cá nhân ra nước ngoài",
            category=FormLinkCategory.CROSS_BORDER,
            conditions="Đối tác hoặc server ở nước ngoài",
            is_active=True,
            display_order=1
        ))
    
    # Add all default links
    for link in default_links:
        db.add(link)
    
    await db.flush()
    await db.commit()

