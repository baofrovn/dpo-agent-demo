from sqlalchemy import Column, String, Text, DateTime, Integer, JSON, Boolean, Enum as SQLEnum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import uuid
import enum


def generate_uuid():
    """Generate UUID as string"""
    return str(uuid.uuid4())


class ChecklistCategory(str, enum.Enum):
    """Checklist category enum"""
    DPA = "DPA"
    OTIA = "OTIA"
    GENERAL = "GENERAL"


class FormLinkCategory(str, enum.Enum):
    """Form link category enum"""
    DOMESTIC = "DOMESTIC"
    CROSS_BORDER = "CROSS_BORDER"
    GENERAL = "GENERAL"


class QuestionType(str, enum.Enum):
    """Question type enum"""
    YES_NO = "yes_no"
    MULTIPLE_CHOICE = "multiple_choice"
    TEXT = "text"


class AuditAction(str, enum.Enum):
    """Audit action enum"""
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class Session(Base):
    """Chat session model"""
    __tablename__ = "sessions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    messages = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "messages": self.messages or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "message_count": len(self.messages or [])
        }


class Settings(Base):
    """Application settings model"""
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class AgentConfig(Base):
    """Agent configuration model"""
    __tablename__ = "agent_configs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    config_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "config_data": self.config_data or {},
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ChecklistItem(Base):
    """Checklist item model"""
    __tablename__ = "checklist_items"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    category = Column(SQLEnum(ChecklistCategory), nullable=False, index=True)
    item_number = Column(String(10), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    required_documents = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String(36), ForeignKey('users.id'), nullable=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "category": self.category.value if self.category else None,
            "item_number": self.item_number,
            "title": self.title,
            "description": self.description,
            "required_documents": self.required_documents,
            "notes": self.notes,
            "is_active": self.is_active,
            "display_order": self.display_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by
        }


class ScreeningQuestion(Base):
    """Screening question model"""
    __tablename__ = "screening_questions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    question_text = Column(Text, nullable=False)
    question_type = Column(SQLEnum(QuestionType), nullable=False, default=QuestionType.YES_NO)
    options = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "question_text": self.question_text,
            "question_type": self.question_type.value if self.question_type else None,
            "options": self.options,
            "is_active": self.is_active,
            "display_order": self.display_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class SensitiveKeyword(Base):
    """Sensitive keyword model"""
    __tablename__ = "sensitive_keywords"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    keyword = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=True, index=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "keyword": self.keyword,
            "category": self.category,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class IntakeFormLink(Base):
    """Intake form link model"""
    __tablename__ = "intake_form_links"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(SQLEnum(FormLinkCategory), nullable=False, index=True)
    conditions = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String(36), ForeignKey('users.id'), nullable=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "category": self.category.value if self.category else None,
            "conditions": self.conditions,
            "is_active": self.is_active,
            "display_order": self.display_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by
        }


class RuleAuditLog(Base):
    """Audit log for rule changes"""
    __tablename__ = "rule_audit_logs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    table_name = Column(String(50), nullable=False, index=True)
    record_id = Column(String(36), nullable=False, index=True)
    action = Column(SQLEnum(AuditAction), nullable=False)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    changed_by = Column(String(36), ForeignKey('users.id'), nullable=True)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "table_name": self.table_name,
            "record_id": self.record_id,
            "action": self.action.value if self.action else None,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "changed_by": self.changed_by,
            "changed_at": self.changed_at.isoformat() if self.changed_at else None
        }
