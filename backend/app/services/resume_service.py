import os
import io
import re
import uuid
import logging
from typing import Dict, Any, Optional
import pymupdf
import docx
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings
from app.core.database import db_instance
from app.schemas.analysis import ResumeUploadResponse

logger = logging.getLogger("accesshire.resume_service")

# In-memory store for development/offline fallback
_in_memory_resumes: Dict[str, Dict[str, Any]] = {}

class ResumeService:
    """
    Handles PDF/DOCX file validation, text extraction, local storage,
    and metadata persistence in MongoDB with in-memory fallback.
    """

    ALLOWED_EXTENSIONS = {".pdf", ".docx"}
    ALLOWED_MIME_TYPES = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
        "application/octet-stream",  # Fallback for binary uploads from some browsers
    }

    @classmethod
    def _extract_text_from_pdf(cls, file_bytes: bytes) -> str:
        """Extracts text content from PDF bytes using PyMuPDF."""
        try:
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
            pages_text = []
            for page in doc:
                text = page.get_text()
                if text:
                    pages_text.append(text)
            doc.close()
            return "\n\n".join(pages_text).strip()
        except Exception as exc:
            logger.error("Failed to parse PDF: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to parse PDF resume file: {exc}"
            )

    @classmethod
    def _extract_text_from_docx(cls, file_bytes: bytes) -> str:
        """Extracts text content from DOCX bytes using python-docx."""
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            
            # Also extract text from any tables in the resume
            for table in doc.tables:
                for row in table.rows:
                    row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_text:
                        paragraphs.append(" | ".join(row_text))

            return "\n\n".join(paragraphs).strip()
        except Exception as exc:
            logger.error("Failed to parse DOCX: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to parse DOCX resume file: {exc}"
            )

    @classmethod
    def extract_text(cls, filename: str, file_bytes: bytes) -> str:
        """Determines format and extracts plaintext from file bytes."""
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".pdf":
            return cls._extract_text_from_pdf(file_bytes)
        elif ext == ".docx":
            return cls._extract_text_from_docx(file_bytes)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file format '{ext}'. Allowed: .pdf, .docx"
            )

    @classmethod
    async def process_and_save_resume(
        cls,
        file: UploadFile,
        user_id: str
    ) -> ResumeUploadResponse:
        """
        Validates uploaded resume, extracts text, stores file on disk,
        and saves resume record to MongoDB (or in-memory store).
        """
        filename = file.filename or "resume.pdf"
        ext = os.path.splitext(filename)[1].lower()

        if ext not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file extension '{ext}'. Only .pdf and .docx documents are supported."
            )

        # Read content
        content = await file.read()
        file_size = len(content)
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if file_size > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
            )

        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty."
            )

        # Extract plaintext
        extracted_text = cls.extract_text(filename, content)
        if not extracted_text:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not extract any readable text from the uploaded resume."
            )

        resume_id = f"res_{uuid.uuid4().hex[:10]}"

        # Save file to disk
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        safe_name = re.sub(r"[^a-zA-Z0-9_\.-]", "_", filename)
        disk_filename = f"{resume_id}_{safe_name}"
        disk_path = os.path.join(settings.UPLOAD_DIR, disk_filename)
        try:
            with open(disk_path, "wb") as f:
                f.write(content)
        except Exception as exc:
            logger.warning("Could not persist file to disk: %s", exc)

        resume_doc = {
            "resume_id": resume_id,
            "user_id": user_id,
            "filename": filename,
            "disk_path": disk_path,
            "file_size": file_size,
            "char_count": len(extracted_text),
            "extracted_text": extracted_text,
            "storage_mode": "mongodb"
        }

        # Save to database
        db = db_instance.db
        storage_mode = "in_memory_fallback"
        if db is not None:
            try:
                await db.resumes.replace_one(
                    {"resume_id": resume_id},
                    resume_doc,
                    upsert=True
                )
                storage_mode = "mongodb"
            except Exception as exc:
                logger.warning("MongoDB write for resume failed (%s); using in-memory store.", exc)

        resume_doc["storage_mode"] = storage_mode
        _in_memory_resumes[resume_id] = resume_doc

        logger.info(
            "Resume %s (%s, %d bytes) processed for user %s (storage: %s)",
            resume_id, filename, file_size, user_id, storage_mode
        )

        preview = extracted_text[:300] + ("..." if len(extracted_text) > 300 else "")

        return ResumeUploadResponse(
            resume_id=resume_id,
            filename=filename,
            file_size=file_size,
            char_count=len(extracted_text),
            text_preview=preview,
            storage_mode=storage_mode
        )

    @classmethod
    async def get_resume_text(cls, resume_id: str, user_id: str) -> Optional[str]:
        """Retrieves extracted text for a specific resume ID with ownership check."""
        db = db_instance.db
        if db is not None:
            try:
                doc = await db.resumes.find_one({"resume_id": resume_id})
                if doc:
                    if doc.get("user_id") != user_id:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Access denied: you do not own this resume."
                        )
                    return doc.get("extracted_text")
            except HTTPException:
                raise
            except Exception as exc:
                logger.warning("MongoDB query for resume failed (%s); checking in-memory store.", exc)

        doc = _in_memory_resumes.get(resume_id)
        if doc:
            if doc.get("user_id") != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: you do not own this resume."
                )
            return doc.get("extracted_text")

        return None
