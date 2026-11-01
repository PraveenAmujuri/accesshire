from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.schemas.auth import UserResponse, AccessibilityPreferences
from app.services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """
    Fetches the authenticated user profile, contact details,
    and configured accessibility preferences.
    """
    return await AuthService.get_user_profile(user_id=current_user["id"])

@router.put("/preferences", response_model=AccessibilityPreferences)
async def update_accessibility_preferences(
    prefs: AccessibilityPreferences,
    current_user: dict = Depends(get_current_user)
):
    """
    Updates the candidate's accessibility preferences
    (e.g., high contrast, font size, simplified language, speech settings).
    """
    return await AuthService.update_preferences(
        user_id=current_user["id"],
        prefs=prefs
    )
