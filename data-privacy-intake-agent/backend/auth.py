"""
Authentication utilities for JWT token management and password hashing
"""
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 hours

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bcrypt has a 72-byte limit for passwords
MAX_PASSWORD_BYTES = 72


def _truncate_password(password: str) -> str:
    """
    Truncate password to bcrypt's 72-byte limit
    
    Args:
        password: Plain text password
        
    Returns:
        str: Truncated password (up to 72 bytes when encoded)
    """
    # Encode to bytes and truncate to 72 bytes
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > MAX_PASSWORD_BYTES:
        # Truncate to 72 bytes and decode back to string
        # Handle potential incomplete UTF-8 sequences by using 'ignore'
        password_bytes = password_bytes[:MAX_PASSWORD_BYTES]
        # Decode back, ignoring any incomplete UTF-8 at the end
        password = password_bytes.decode('utf-8', errors='ignore')
    return password


class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model"""
    username: Optional[str] = None
    user_id: Optional[str] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        bool: True if password matches, False otherwise
    """
    # Truncate password to bcrypt's 72-byte limit
    plain_password = _truncate_password(plain_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    # Truncate password to bcrypt's 72-byte limit
    password = _truncate_password(password)
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """
    Decode and verify a JWT access token
    
    Args:
        token: JWT token string
        
    Returns:
        TokenData: Decoded token data, or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        
        if username is None:
            return None
            
        return TokenData(username=username, user_id=user_id)
    except JWTError:
        return None
