"""
Rules management routes (checklist items, screening questions, sensitive keywords)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from database import get_db
from models import User
from dependencies import get_current_active_user
from schemas.rules import (
    ChecklistItemCreate, ChecklistItemUpdate, ChecklistItemResponse, ChecklistItemReorder,
    ScreeningQuestionCreate, ScreeningQuestionUpdate, ScreeningQuestionResponse, ScreeningQuestionReorder,
    SensitiveKeywordCreate, SensitiveKeywordUpdate, SensitiveKeywordResponse, SensitiveKeywordBulkImport,
    AuditLogResponse
)
import crud_rules


router = APIRouter(prefix="/rules", tags=["rules"])


# Checklist Items Endpoints
@router.get("/checklist", response_model=List[ChecklistItemResponse])
async def list_checklist_items(
    category: Optional[str] = Query(None, description="Filter by category: DPA, OTIA, GENERAL"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all checklist items with optional filters"""
    try:
        items = await crud_rules.get_checklist_items(db, category, is_active)
        return [item.to_dict() for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/checklist/{item_id}", response_model=ChecklistItemResponse)
async def get_checklist_item(
    item_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a single checklist item"""
    try:
        item = await crud_rules.get_checklist_item(db, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Checklist item not found")
        return item.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/checklist", response_model=ChecklistItemResponse, status_code=status.HTTP_201_CREATED)
async def create_checklist_item(
    item_data: ChecklistItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new checklist item"""
    try:
        item = await crud_rules.create_checklist_item(
            db,
            item_data.model_dump(),
            current_user.id
        )
        return item.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/checklist/{item_id}", response_model=ChecklistItemResponse)
async def update_checklist_item(
    item_id: str,
    item_data: ChecklistItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a checklist item"""
    try:
        item = await crud_rules.update_checklist_item(
            db,
            item_id,
            item_data.model_dump(exclude_unset=True),
            current_user.id
        )
        if not item:
            raise HTTPException(status_code=404, detail="Checklist item not found")
        return item.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/checklist/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_checklist_item(
    item_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Soft delete a checklist item"""
    try:
        success = await crud_rules.delete_checklist_item(db, item_id, current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Checklist item not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/checklist/reorder")
async def reorder_checklist_items(
    reorder_data: ChecklistItemReorder,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Reorder checklist items"""
    try:
        await crud_rules.reorder_checklist_items(db, reorder_data.items, current_user.id)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Screening Questions Endpoints
@router.get("/questions", response_model=List[ScreeningQuestionResponse])
async def list_screening_questions(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all screening questions with optional filters"""
    try:
        questions = await crud_rules.get_screening_questions(db, is_active)
        return [q.to_dict() for q in questions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/questions/{question_id}", response_model=ScreeningQuestionResponse)
async def get_screening_question(
    question_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a single screening question"""
    try:
        question = await crud_rules.get_screening_question(db, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Screening question not found")
        return question.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/questions", response_model=ScreeningQuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_screening_question(
    question_data: ScreeningQuestionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new screening question"""
    try:
        question = await crud_rules.create_screening_question(
            db,
            question_data.model_dump(),
            current_user.id
        )
        return question.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/questions/{question_id}", response_model=ScreeningQuestionResponse)
async def update_screening_question(
    question_id: str,
    question_data: ScreeningQuestionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a screening question"""
    try:
        question = await crud_rules.update_screening_question(
            db,
            question_id,
            question_data.model_dump(exclude_unset=True),
            current_user.id
        )
        if not question:
            raise HTTPException(status_code=404, detail="Screening question not found")
        return question.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_screening_question(
    question_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Soft delete a screening question"""
    try:
        success = await crud_rules.delete_screening_question(db, question_id, current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Screening question not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/questions/reorder")
async def reorder_screening_questions(
    reorder_data: ScreeningQuestionReorder,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Reorder screening questions"""
    try:
        await crud_rules.reorder_screening_questions(db, reorder_data.items, current_user.id)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Sensitive Keywords Endpoints
@router.get("/keywords", response_model=List[SensitiveKeywordResponse])
async def list_sensitive_keywords(
    category: Optional[str] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all sensitive keywords with optional filters"""
    try:
        keywords = await crud_rules.get_sensitive_keywords(db, category, is_active)
        return [k.to_dict() for k in keywords]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/keywords/{keyword_id}", response_model=SensitiveKeywordResponse)
async def get_sensitive_keyword(
    keyword_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a single sensitive keyword"""
    try:
        keyword = await crud_rules.get_sensitive_keyword(db, keyword_id)
        if not keyword:
            raise HTTPException(status_code=404, detail="Sensitive keyword not found")
        return keyword.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/keywords", response_model=SensitiveKeywordResponse, status_code=status.HTTP_201_CREATED)
async def create_sensitive_keyword(
    keyword_data: SensitiveKeywordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new sensitive keyword"""
    try:
        keyword = await crud_rules.create_sensitive_keyword(
            db,
            keyword_data.model_dump(),
            current_user.id
        )
        return keyword.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/keywords/{keyword_id}", response_model=SensitiveKeywordResponse)
async def update_sensitive_keyword(
    keyword_id: str,
    keyword_data: SensitiveKeywordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a sensitive keyword"""
    try:
        keyword = await crud_rules.update_sensitive_keyword(
            db,
            keyword_id,
            keyword_data.model_dump(exclude_unset=True),
            current_user.id
        )
        if not keyword:
            raise HTTPException(status_code=404, detail="Sensitive keyword not found")
        return keyword.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/keywords/{keyword_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sensitive_keyword(
    keyword_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Soft delete a sensitive keyword"""
    try:
        success = await crud_rules.delete_sensitive_keyword(db, keyword_id, current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Sensitive keyword not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/keywords/import")
async def bulk_import_keywords(
    import_data: SensitiveKeywordBulkImport,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Bulk import sensitive keywords"""
    try:
        count = await crud_rules.bulk_import_keywords(db, import_data.keywords, current_user.id)
        return {"status": "ok", "imported": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Audit Logs Endpoint
@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def list_audit_logs(
    table_name: Optional[str] = Query(None, description="Filter by table name"),
    record_id: Optional[str] = Query(None, description="Filter by record ID"),
    limit: int = Query(100, le=500, description="Limit number of results"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List audit logs with optional filters"""
    try:
        logs = await crud_rules.get_audit_logs(db, table_name, record_id, limit)
        return [log.to_dict() for log in logs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
