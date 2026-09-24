from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
async def register_user(payload: UserRegisterRequest):
    # Phase 1 foundation stub: validates schema and returns token
    user_id = "user_" + payload.name.lower().replace(" ", "_")
    token = create_access_token(subject=user_id)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user_id,
        name=payload.name,
        email=payload.email
    )

@router.post("/login", response_model=TokenResponse)
async def login_user(payload: UserLoginRequest):
    # Phase 1 foundation stub: validates credentials and returns token
    user_id = "user_candidate"
    token = create_access_token(subject=user_id)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=user_id,
        name="Candidate",
        email=payload.email
    )
