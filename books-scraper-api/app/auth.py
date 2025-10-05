"""
Autenticação e Segurança
=========================
"""

import hashlib
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

security = HTTPBearer()

# Base de dados fake de usuários
USERS_DB = {
    "admin": {
        "username": "admin",
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin"
    },
    "user": {
        "username": "user",
        "password_hash": hashlib.sha256("user123".encode()).hexdigest(),
        "role": "user"
    }
}


def hash_password(password: str) -> str:
    """Cria hash da senha"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
    """Verifica senha"""
    return hash_password(plain) == hashed


def create_token(data: dict, token_type: str, expires_delta: timedelta) -> str:
    """Cria token JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(username: str, role: str) -> str:
    """Cria access token"""
    return create_token(
        {"sub": username, "role": role},
        "access",
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(username: str) -> str:
    """Cria refresh token"""
    return create_token(
        {"sub": username},
        "refresh",
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Autentica usuário"""
    user = USERS_DB.get(username)
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return user


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Obtém usuário atual do token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type")
        
        if not username or token_type != "access":
            raise HTTPException(status_code=401, detail="Token inválido")
        
        user = USERS_DB.get(username)
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        return user
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


async def get_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
    """Verifica se usuário é admin"""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas admins.")
    return current_user