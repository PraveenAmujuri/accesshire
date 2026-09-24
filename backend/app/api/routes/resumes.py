from fastapi import APIRouter, UploadFile, File, Depends
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    return {
        "status": "received",
        "file_name": file.filename,
        "content_type": file.content_type,
        "message": "Resume uploaded successfully. Will be analyzed by ResumeAgent in Phase 6."
    }
