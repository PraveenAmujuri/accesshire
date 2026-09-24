from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])

class JobDescriptionInput(BaseModel):
    title: str
    description: str

@router.post("/parse")
async def parse_job_description(
    payload: JobDescriptionInput,
    current_user: dict = Depends(get_current_user)
):
    return {
        "status": "received",
        "title": payload.title,
        "message": "Job description received. Will be parsed by JobAgent in Phase 6."
    }
