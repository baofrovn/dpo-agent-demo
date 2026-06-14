"""
CRUD operations for rules (checklists, questions, keywords)
"""
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from models import (
    ChecklistItem, ScreeningQuestion, SensitiveKeyword, IntakeFormLink,
    RuleAuditLog, ChecklistCategory, QuestionType, FormLinkCategory, AuditAction
)
from typing import Optional, List
import json


# Checklist Items CRUD
async def get_checklist_items(
    db: AsyncSession,
    category: Optional[str] = None,
    is_active: Optional[bool] = None
) -> List[ChecklistItem]:
    """Get checklist items with optional filters"""
    query = select(ChecklistItem).order_by(ChecklistItem.display_order)
    
    if category:
        query = query.where(ChecklistItem.category == ChecklistCategory[category])
    if is_active is not None:
        query = query.where(ChecklistItem.is_active == is_active)
    
    result = await db.execute(query)
    return result.scalars().all()


async def get_checklist_item(db: AsyncSession, item_id: str) -> Optional[ChecklistItem]:
    """Get a single checklist item by ID"""
    result = await db.execute(
        select(ChecklistItem).where(ChecklistItem.id == item_id)
    )
    return result.scalar_one_or_none()


async def create_checklist_item(
    db: AsyncSession,
    data: dict,
    user_id: Optional[str] = None
) -> ChecklistItem:
    """Create a new checklist item"""
    item = ChecklistItem(
        category=ChecklistCategory[data["category"]],
        item_number=data["item_number"],
        title=data["title"],
        description=data.get("description"),
        required_documents=data.get("required_documents"),
        notes=data.get("notes"),
        is_active=data.get("is_active", True),
        display_order=data.get("display_order", 0),
        created_by=user_id
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    
    # Create audit log
    if user_id:
        await create_audit_log(
            db, "checklist_items", item.id, AuditAction.CREATE,
            None, item.to_dict(), user_id
        )
    
    return item


async def update_checklist_item(
    db: AsyncSession,
    item_id: str,
    data: dict,
    user_id: Optional[str] = None
) -> Optional[ChecklistItem]:
    """Update a checklist item"""
    item = await get_checklist_item(db, item_id)
    if not item:
        return None
    
    old_value = item.to_dict()
    
    # Update fields
    if "category" in data and data["category"]:
        item.category = ChecklistCategory[data["category"]]
    if "item_number" in data and data["item_number"] is not None:
        item.item_number = data["item_number"]
    if "title" in data and data["title"] is not None:
        item.title = data["title"]
    if "description" in data:
        item.description = data["description"]
    if "required_documents" in data:
        item.required_documents = data["required_documents"]
    if "notes" in data:
        item.notes = data["notes"]
    if "is_active" in data and data["is_active"] is not None:
        item.is_active = data["is_active"]
    if "display_order" in data and data["display_order"] is not None:
        item.display_order = data["display_order"]
    
    await db.flush()
    await db.refresh(item)
    
    # Create audit log
    if user_id:
        await create_audit_log(
            db, "checklist_items", item.id, AuditAction.UPDATE,
            old_value, item.to_dict(), user_id
        )
    
    return item


async def delete_checklist_item(
    db: AsyncSession,
    item_id: str,
    user_id: Optional[str] = None
) -> bool:
    """Soft delete a checklist item (set is_active = False)"""
    item = await get_checklist_item(db, item_id)
    if not item:
        return False
    
    old_value = item.to_dict()
    item.is_active = False
    
    await db.flush()
    
    # Create audit log
    if user_id:
        await create_audit_log(
            db, "checklist_items", item.id, AuditAction.DELETE,
            old_value, {"is_active": False}, user_id
        )
    
    return True


async def reorder_checklist_items(
    db: AsyncSession,
    items: List[dict],
    user_id: Optional[str] = None
) -> bool:
    """Reorder checklist items"""
    for item_data in items:
        item_id = item_data.get("id")
        display_order = item_data.get("display_order")
        
        if item_id and display_order is not None:
            await db.execute(
                update(ChecklistItem)
                .where(ChecklistItem.id == item_id)
                .values(display_order=display_order)
            )
    
    await db.flush()
    return True


# Intake Form Links CRUD
async def get_form_links(
    db: AsyncSession,
    category: Optional[str] = None,
    is_active: Optional[bool] = None
) -> List[IntakeFormLink]:
    """Get form links with optional filters"""
    query = select(IntakeFormLink).order_by(IntakeFormLink.display_order)
    
    if category:
        query = query.where(IntakeFormLink.category == FormLinkCategory[category])
    if is_active is not None:
        query = query.where(IntakeFormLink.is_active == is_active)
    
    result = await db.execute(query)
    return result.scalars().all()


async def get_form_link(db: AsyncSession, link_id: str) -> Optional[IntakeFormLink]:
    """Get a single form link by ID"""
    result = await db.execute(
        select(IntakeFormLink).where(IntakeFormLink.id == link_id)
    )
    return result.scalar_one_or_none()


async def create_form_link(
    db: AsyncSession,
    data: dict,
    user_id: Optional[str] = None
) -> IntakeFormLink:
    """Create a new form link"""
    link = IntakeFormLink(
        name=data["name"],
        url=data["url"],
        description=data.get("description"),
        category=FormLinkCategory[data["category"]],
        conditions=data.get("conditions"),
        is_active=data.get("is_active", True),
        display_order=data.get("display_order", 0),
        created_by=user_id
    )
    db.add(link)
    await db.flush()
    await db.refresh(link)
    
    # Create audit log
    if user_id:
        await create_audit_log(
            db, "intake_form_links", link.id, AuditAction.CREATE,
            None, link.to_dict(), user_id
        )
    
    return link


async def update_form_link(
    db: AsyncSession,
    link_id: str,
    data: dict,
    user_id: Optional[str] = None
) -> Optional[IntakeFormLink]:
    """Update a form link"""
    link = await get_form_link(db, link_id)
    if not link:
        return None
    
    old_value = link.to_dict()
    
    # Update fields
    if "name" in data and data["name"] is not None:
        link.name = data["name"]
    if "url" in data and data["url"] is not None:
        link.url = data["url"]
    if "description" in data:
        link.description = data["description"]
    if "category" in data and data["category"]:
        link.category = FormLinkCategory[data["category"]]
    if "conditions" in data:
        link.conditions = data["conditions"]
    if "is_active" in data and data["is_active"] is not None:
        link.is_active = data["is_active"]
    if "display_order" in data and data["display_order"] is not None:
        link.display_order = data["display_order"]
    
    await db.flush()
    await db.refresh(link)
    
    # Create audit log
    if user_id:
        await create_audit_log(
            db, "intake_form_links", link.id, AuditAction.UPDATE,
            old_value, link.to_dict(), user_id
        )
    
    return link


async def delete_form_link(
    db: AsyncSession,
    link_id: str,
    user_id: Optional[str] = None
) -> bool:
    """Soft delete a form link (set is_active = False)"""
    link = await get_form_link(db, link_id)
    if not link:
        return False
    
    old_value = link.to_dict()
    link.is_active = False
    
    await db.flush()
    
    # Create audit log
    if user_id:
        await create_audit_log(
            db, "intake_form_links", link.id, AuditAction.DELETE,
            old_value, {"is_active": False}, user_id
        )
    
    return True


async def reorder_form_links(
    db: AsyncSession,
    items: List[dict],
    user_id: Optional[str] = None
) -> bool:
    """Reorder form links"""
    for item_data in items:
        link_id = item_data.get("id")
        display_order = item_data.get("display_order")
        
        if link_id and display_order is not None:
            await db.execute(
                update(IntakeFormLink)
                .where(IntakeFormLink.id == link_id)
                .values(display_order=display_order)
            )
    
    await db.flush()
    return True


# Screening Questions CRUD
async def get_screening_questions(
    db: AsyncSession,
    is_active: Optional[bool] = None
) -> List[ScreeningQuestion]:
    """Get screening questions with optional filters"""
    query = select(ScreeningQuestion).order_by(ScreeningQuestion.display_order)
    
    if is_active is not None:
        query = query.where(ScreeningQuestion.is_active == is_active)
    
    result = await db.execute(query)
    return result.scalars().all()


async def get_screening_question(db: AsyncSession, question_id: str) -> Optional[ScreeningQuestion]:
    """Get a single screening question by ID"""
    result = await db.execute(
        select(ScreeningQuestion).where(ScreeningQuestion.id == question_id)
    )
    return result.scalar_one_or_none()


async def create_screening_question(
    db: AsyncSession,
    data: dict,
    user_id: Optional[str] = None
) -> ScreeningQuestion:
    """Create a new screening question"""
    question = ScreeningQuestion(
        question_text=data["question_text"],
        question_type=QuestionType[data.get("question_type", "yes_no")],
        options=data.get("options"),
        is_active=data.get("is_active", True),
        display_order=data.get("display_order", 0)
    )
    db.add(question)
    await db.flush()
    await db.refresh(question)
    
    # Create audit log
    if user_id:
        await create_audit_log(
            db, "screening_questions", question.id, AuditAction.CREATE,
            None, question.to_dict(), user_id
        )
    
    return question


async def update_screening_question(
    db: AsyncSession,
    question_id: str,
    data: dict,
    user_id: Optional[str] = None
) -> Optional[ScreeningQuestion]:
    """Update a screening question"""
    question = await get_screening_question(db, question_id)
    if not question:
        return None
    
    old_value = question.to_dict()
    
    # Update fields
    if "question_text" in data and data["question_text"] is not None:
        question.question_text = data["question_text"]
    if "question_type" in data and data["question_type"]:
        question.question_type = QuestionType[data["question_type"]]
    if "options" in data:
        question.options = data["options"]
    if "is_active" in data and data["is_active"] is not None:
        question.is_active = data["is_active"]
    if "display_order" in data and data["display_order"] is not None:
        question.display_order = data["display_order"]
    
    await db.flush()
    await db.refresh(question)
    
    # Create audit log
    if user_id:
        await create_audit_log(
            db, "screening_questions", question.id, AuditAction.UPDATE,
            old_value, question.to_dict(), user_id
        )
    
    return question


async def delete_screening_question(
    db: AsyncSession,
    question_id: str,
    user_id: Optional[str] = None
) -> bool:
    """Soft delete a screening question"""
    question = await get_screening_question(db, question_id)
    if not question:
        return False
    
    old_value = question.to_dict()
    question.is_active = False
    
    await db.flush()
    
    # Create audit log
    if user_id:
        await create_audit_log(
            db, "screening_questions", question.id, AuditAction.DELETE,
            old_value, {"is_active": False}, user_id
        )
    
    return True


async def reorder_screening_questions(
    db: AsyncSession,
    items: List[dict],
    user_id: Optional[str] = None
) -> bool:
    """Reorder screening questions"""
    for item_data in items:
        question_id = item_data.get("id")
        display_order = item_data.get("display_order")
        
        if question_id and display_order is not None:
            await db.execute(
                update(ScreeningQuestion)
                .where(ScreeningQuestion.id == question_id)
                .values(display_order=display_order)
            )
    
    await db.flush()
    return True


# Sensitive Keywords CRUD
async def get_sensitive_keywords(
    db: AsyncSession,
    category: Optional[str] = None,
    is_active: Optional[bool] = None
) -> List[SensitiveKeyword]:
    """Get sensitive keywords with optional filters"""
    query = select(SensitiveKeyword).order_by(SensitiveKeyword.keyword)
    
    if category:
        query = query.where(SensitiveKeyword.category == category)
    if is_active is not None:
        query = query.where(SensitiveKeyword.is_active == is_active)
    
    result = await db.execute(query)
    return result.scalars().all()


async def get_sensitive_keyword(db: AsyncSession, keyword_id: str) -> Optional[SensitiveKeyword]:
    """Get a single sensitive keyword by ID"""
    result = await db.execute(
        select(SensitiveKeyword).where(SensitiveKeyword.id == keyword_id)
    )
    return result.scalar_one_or_none()


async def create_sensitive_keyword(
    db: AsyncSession,
    data: dict,
    user_id: Optional[str] = None
) -> SensitiveKeyword:
    """Create a new sensitive keyword"""
    keyword = SensitiveKeyword(
        keyword=data["keyword"],
        category=data.get("category"),
        description=data.get("description"),
        is_active=data.get("is_active", True)
    )
    db.add(keyword)
    await db.flush()
    await db.refresh(keyword)
    
    # Create audit log
    if user_id:
        await create_audit_log(
            db, "sensitive_keywords", keyword.id, AuditAction.CREATE,
            None, keyword.to_dict(), user_id
        )
    
    return keyword


async def update_sensitive_keyword(
    db: AsyncSession,
    keyword_id: str,
    data: dict,
    user_id: Optional[str] = None
) -> Optional[SensitiveKeyword]:
    """Update a sensitive keyword"""
    keyword = await get_sensitive_keyword(db, keyword_id)
    if not keyword:
        return None
    
    old_value = keyword.to_dict()
    
    # Update fields
    if "keyword" in data and data["keyword"] is not None:
        keyword.keyword = data["keyword"]
    if "category" in data:
        keyword.category = data["category"]
    if "description" in data:
        keyword.description = data["description"]
    if "is_active" in data and data["is_active"] is not None:
        keyword.is_active = data["is_active"]
    
    await db.flush()
    await db.refresh(keyword)
    
    # Create audit log
    if user_id:
        await create_audit_log(
            db, "sensitive_keywords", keyword.id, AuditAction.UPDATE,
            old_value, keyword.to_dict(), user_id
        )
    
    return keyword


async def delete_sensitive_keyword(
    db: AsyncSession,
    keyword_id: str,
    user_id: Optional[str] = None
) -> bool:
    """Soft delete a sensitive keyword"""
    keyword = await get_sensitive_keyword(db, keyword_id)
    if not keyword:
        return False
    
    old_value = keyword.to_dict()
    keyword.is_active = False
    
    await db.flush()
    
    # Create audit log
    if user_id:
        await create_audit_log(
            db, "sensitive_keywords", keyword.id, AuditAction.DELETE,
            old_value, {"is_active": False}, user_id
        )
    
    return True


async def bulk_import_keywords(
    db: AsyncSession,
    keywords: List[dict],
    user_id: Optional[str] = None
) -> int:
    """Bulk import sensitive keywords"""
    count = 0
    for keyword_data in keywords:
        keyword = SensitiveKeyword(
            keyword=keyword_data["keyword"],
            category=keyword_data.get("category"),
            description=keyword_data.get("description"),
            is_active=keyword_data.get("is_active", True)
        )
        db.add(keyword)
        count += 1
    
    await db.flush()
    return count


# Audit Log CRUD
async def create_audit_log(
    db: AsyncSession,
    table_name: str,
    record_id: str,
    action: AuditAction,
    old_value: Optional[dict],
    new_value: Optional[dict],
    user_id: str
) -> RuleAuditLog:
    """Create an audit log entry"""
    log = RuleAuditLog(
        table_name=table_name,
        record_id=record_id,
        action=action,
        old_value=old_value,
        new_value=new_value,
        changed_by=user_id
    )
    db.add(log)
    await db.flush()
    await db.refresh(log)
    return log


async def get_audit_logs(
    db: AsyncSession,
    table_name: Optional[str] = None,
    record_id: Optional[str] = None,
    limit: int = 100
) -> List[RuleAuditLog]:
    """Get audit logs with optional filters"""
    query = select(RuleAuditLog).order_by(RuleAuditLog.changed_at.desc()).limit(limit)
    
    if table_name:
        query = query.where(RuleAuditLog.table_name == table_name)
    if record_id:
        query = query.where(RuleAuditLog.record_id == record_id)
    
    result = await db.execute(query)
    return result.scalars().all()
