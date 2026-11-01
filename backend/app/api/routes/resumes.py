from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from app.api.dependencies import get_current_user
from app.schemas.analysis import ResumeUploadResponse
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Uploads a candidate resume in PDF or DOCX format.
    Validates file integrity, extracts clean text, stores file on disk,
    and returns resume metadata and text preview.
    """
    user_id = current_user.get("id") or "user_candidate"
    return await ResumeService.process_and_save_resume(file=file, user_id=user_id)

@router.get("/{resume_id}")
async def get_resume_info(
    resume_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Retrieves extracted plaintext for an uploaded resume owned by the user."""
    user_id = current_user.get("id") or "user_candidate"
    text = await ResumeService.get_resume_text(resume_id, user_id)
    if not text:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume '{resume_id}' not found."
        )
    return {
        "resume_id": resume_id,
        "char_count": len(text),
        "text": text
    }
