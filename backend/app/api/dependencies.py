from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from app.core.database import get_database

security_scheme = HTTPBearer(auto_error=False)

async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)):
    """
    Dependency that extracts and validates the Bearer JWT token.
    For Phase 1 foundation, if no token is passed, can yield a guest/dev identity
    or return 401 when strict auth is active.
    """
    if not credentials:
        # Dev fallback candidate for testing without blocking
        return {"id": "dev_user_1", "email": "dev@accesshire.ai", "name": "Dev Candidate"}

    token = credentials.credentials
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token"
        )
    return {"id": user_id}
