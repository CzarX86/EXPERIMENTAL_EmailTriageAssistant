"""Attachment model for email attachments."""

from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class OCRStatus(str, Enum):
    """OCR processing status for attachments."""
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"


class Attachment(BaseModel):
    """Attachment entity representing email attachments.
    
    Handles file attachments with OCR text extraction capabilities.
    Supports content hashing for deduplication and integrity checks.
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    email_id: UUID = Field(..., description="Parent email ID (foreign key)")
    filename: str = Field(..., description="Original filename")
    mime_type: str = Field(..., description="MIME type of the attachment")
    size_bytes: int = Field(..., ge=0, description="File size in bytes")
    extracted_text: Optional[str] = Field(None, description="OCR extracted text content")
    ocr_status: OCRStatus = Field(default=OCRStatus.PENDING, description="OCR processing status")
    hash: str = Field(..., description="Content hash for deduplication")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True

    def __str__(self) -> str:
        """String representation."""
        return f"Attachment(filename='{self.filename}', size={self.size_bytes}B, status={self.ocr_status})"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"Attachment(id={self.id}, email_id={self.email_id}, "
            f"filename='{self.filename}', mime_type='{self.mime_type}', "
            f"size_bytes={self.size_bytes}, ocr_status={self.ocr_status})"
        )

    @property
    def is_text_extractable(self) -> bool:
        """Check if attachment type supports text extraction."""
        text_extractable_types = {
            "application/pdf",
            "image/jpeg",
            "image/png", 
            "image/tiff",
            "image/bmp",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
            "text/html"
        }
        return self.mime_type in text_extractable_types

    @property
    def requires_ocr(self) -> bool:
        """Check if attachment requires OCR processing."""
        ocr_types = {
            "image/jpeg",
            "image/png",
            "image/tiff", 
            "image/bmp"
        }
        return self.mime_type in ocr_types