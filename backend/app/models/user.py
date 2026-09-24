from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class UserModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: str
    password_hash: str
    accessibility_preferences: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
