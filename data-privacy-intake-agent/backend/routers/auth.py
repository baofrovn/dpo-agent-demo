"""
Authentication routes
"""
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from database import get_db
from auth import Token, create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from crud import get_user_by_username
from models import User
from dependencies import get_current_active_user


router = APIRouter(prefix="/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str


class UserResponse(BaseModel):
    """User response model"""
    id: str
    username: str
    is_active: bool


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login endpoint - authenticate user and return JWT token
    
    Args:
        login_data: Login credentials
        db: Database session
        
    Returns:
        Token: JWT access token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    user = await get_user_by_username(db, login_data.username)
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user info
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: Current user information
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "is_active": current_user.is_active
    }


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_active_user)
):
    """
    Logout endpoint (client should discard token)
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
    """
    return {"message": "Successfully logged out"}
