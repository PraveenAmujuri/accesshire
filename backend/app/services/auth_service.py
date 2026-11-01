import uuid
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from app.core.database import db_instance
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    AccessibilityPreferences
)

logger = logging.getLogger("accesshire.auth_service")

# In-memory storage fallback for dev/offline mode
_in_memory_users: Dict[str, Dict[str, Any]] = {}

class AuthService:
    """
    Manages secure user registration, bcrypt password hashing,
    authentication, JWT token issuance, and accessibility preferences.
    """

    @classmethod
    def _now_iso(cls) -> str:
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    async def _find_user_by_email(cls, email: str) -> Optional[Dict[str, Any]]:
        norm_email = email.strip().lower()
        db = db_instance.db
        if db is not None:
            try:
                user = await db.users.find_one({"email": norm_email})
                if user:
                    user.pop("_id", None)
                    return user
            except Exception as exc:
                logger.warning("MongoDB find user failed (%s); checking in-memory store.", exc)

        for u in _in_memory_users.values():
            if u.get("email") == norm_email:
                return u
        return None

    @classmethod
    async def _find_user_by_id(cls, user_id: str) -> Optional[Dict[str, Any]]:
        db = db_instance.db
        if db is not None:
            try:
                user = await db.users.find_one({"user_id": user_id})
                if user:
                    user.pop("_id", None)
                    return user
            except Exception as exc:
                logger.warning("MongoDB find user by id failed (%s); checking in-memory store.", exc)

        return _in_memory_users.get(user_id)

    @classmethod
    async def _save_user(cls, user_doc: Dict[str, Any]) -> None:
        db = db_instance.db
        if db is not None:
            try:
                await db.users.replace_one(
                    {"user_id": user_doc["user_id"]},
                    user_doc,
                    upsert=True
                )
                return
            except Exception as exc:
                logger.warning("MongoDB save user failed (%s); falling back to in-memory store.", exc)

        _in_memory_users[user_doc["user_id"]] = user_doc

    @classmethod
    async def register(cls, payload: UserRegisterRequest) -> TokenResponse:
        norm_email = payload.email.strip().lower()

        # Validate password strength
        if len(payload.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must be at least 6 characters long."
            )

        # Check existing user
        existing = await cls._find_user_by_email(norm_email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An account with email '{norm_email}' already exists."
            )

        # Generate secure salted bcrypt hash
        hashed_pw = get_password_hash(payload.password)
        user_id = f"user_{uuid.uuid4().hex[:10]}"
        now = cls._now_iso()

        prefs = payload.accessibility_preferences or AccessibilityPreferences()

        user_doc = {
            "user_id": user_id,
            "name": payload.name.strip(),
            "email": norm_email,
            "password_hash": hashed_pw,
            "accessibility_preferences": prefs.model_dump(),
            "created_at": now,
            "updated_at": now
        }

        await cls._save_user(user_doc)
        logger.info("Registered new user %s (%s)", user_id, norm_email)

        token = create_access_token(subject=user_id)

        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user_id=user_id,
            name=user_doc["name"],
            email=user_doc["email"]
        )

    @classmethod
    async def login(cls, payload: UserLoginRequest) -> TokenResponse:
        norm_email = payload.email.strip().lower()
        user = await cls._find_user_by_email(norm_email)

        if not user or not verify_password(payload.password, user.get("password_hash", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        token = create_access_token(subject=user["user_id"])
        logger.info("User %s (%s) logged in successfully.", user["user_id"], norm_email)

        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user_id=user["user_id"],
            name=user.get("name", "Candidate"),
            email=user.get("email", norm_email)
        )

    @classmethod
    async def get_user_profile(cls, user_id: str) -> UserResponse:
        user = await cls._find_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User account '{user_id}' not found."
            )

        prefs_data = user.get("accessibility_preferences") or {}
        prefs = AccessibilityPreferences(**prefs_data)

        return UserResponse(
            id=user["user_id"],
            name=user.get("name", "Candidate"),
            email=user.get("email", ""),
            accessibility_preferences=prefs
        )

    @classmethod
    async def update_preferences(
        cls,
        user_id: str,
        prefs: AccessibilityPreferences
    ) -> AccessibilityPreferences:
        user = await cls._find_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User account '{user_id}' not found."
            )

        user["accessibility_preferences"] = prefs.model_dump()
        user["updated_at"] = cls._now_iso()
        await cls._save_user(user)

        logger.info("Updated accessibility preferences for user %s", user_id)
        return prefs
