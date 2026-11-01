from fastapi import APIRouter
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register_user(payload: UserRegisterRequest):
    """
    Registers a new candidate account.
    Hashes password using salted bcrypt, persists user profile and
    optional accessibility preferences, and issues a signed JWT token.
    """
    return await AuthService.register(payload)

@router.post("/login", response_model=TokenResponse)
async def login_user(payload: UserLoginRequest):
    """
    Authenticates candidate credentials against the stored bcrypt hash.
    Returns a signed JWT access token upon successful authentication.
    """
    return await AuthService.login(payload)
