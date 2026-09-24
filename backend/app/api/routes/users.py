from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.schemas.auth import UserResponse, AccessibilityPreferences

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=current_user.get("id", "guest"),
        name=current_user.get("name", "Candidate"),
        email=current_user.get("email", "candidate@example.com"),
        accessibility_preferences=AccessibilityPreferences()
    )

@router.put("/preferences")
async def update_accessibility_preferences(
    prefs: AccessibilityPreferences,
    current_user: dict = Depends(get_current_user)
):
    return {"status": "success", "preferences": prefs}
