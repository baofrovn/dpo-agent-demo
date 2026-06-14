"""
Pydantic schemas for rules API
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Checklist Item Schemas
class ChecklistItemBase(BaseModel):
    """Base checklist item schema"""
    category: str
    item_number: str
    title: str
    description: Optional[str] = None
    required_documents: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True
    display_order: int = 0


class ChecklistItemCreate(ChecklistItemBase):
    """Create checklist item schema"""
    pass


class ChecklistItemUpdate(BaseModel):
    """Update checklist item schema"""
    category: Optional[str] = None
    item_number: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    required_documents: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class ChecklistItemResponse(ChecklistItemBase):
    """Checklist item response schema"""
    id: str
    created_at: str
    updated_at: str
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


class ChecklistItemReorder(BaseModel):
    """Reorder checklist items schema"""
    items: List[dict]  # [{"id": "xxx", "display_order": 1}, ...]


# Screening Question Schemas
class ScreeningQuestionBase(BaseModel):
    """Base screening question schema"""
    question_text: str
    question_type: str = "yes_no"
    options: Optional[str] = None
    is_active: bool = True
    display_order: int = 0


class ScreeningQuestionCreate(ScreeningQuestionBase):
    """Create screening question schema"""
    pass


class ScreeningQuestionUpdate(BaseModel):
    """Update screening question schema"""
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    options: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class ScreeningQuestionResponse(ScreeningQuestionBase):
    """Screening question response schema"""
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ScreeningQuestionReorder(BaseModel):
    """Reorder screening questions schema"""
    items: List[dict]  # [{"id": "xxx", "display_order": 1}, ...]


# Sensitive Keyword Schemas
class SensitiveKeywordBase(BaseModel):
    """Base sensitive keyword schema"""
    keyword: str
    category: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True


class SensitiveKeywordCreate(SensitiveKeywordBase):
    """Create sensitive keyword schema"""
    pass


class SensitiveKeywordUpdate(BaseModel):
    """Update sensitive keyword schema"""
    keyword: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class SensitiveKeywordResponse(SensitiveKeywordBase):
    """Sensitive keyword response schema"""
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class SensitiveKeywordBulkImport(BaseModel):
    """Bulk import sensitive keywords schema"""
    keywords: List[dict]  # [{"keyword": "xxx", "category": "yyy", ...}, ...]


# Intake Form Link Schemas
class FormLinkBase(BaseModel):
    """Base form link schema"""
    name: str
    url: str
    description: Optional[str] = None
    category: str
    conditions: Optional[str] = None
    is_active: bool = True
    display_order: int = 0


class FormLinkCreate(FormLinkBase):
    """Create form link schema"""
    pass


class FormLinkUpdate(BaseModel):
    """Update form link schema"""
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    conditions: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class FormLinkResponse(FormLinkBase):
    """Form link response schema"""
    id: str
    created_at: str
    updated_at: str
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


class FormLinkReorder(BaseModel):
    """Reorder form links schema"""
    items: List[dict]  # [{"id": "xxx", "display_order": 1}, ...]


# Audit Log Schema
class AuditLogResponse(BaseModel):
    """Audit log response schema"""
    id: str
    table_name: str
    record_id: str
    action: str
    old_value: Optional[dict] = None
    new_value: Optional[dict] = None
    changed_by: Optional[str] = None
    changed_at: str

    class Config:
        from_attributes = True
