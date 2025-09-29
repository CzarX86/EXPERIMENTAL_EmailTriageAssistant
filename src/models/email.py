"""Email model for the email assistant."""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EmailLanguage(str, Enum):
    """Supported email languages."""
    PT = "pt"
    EN = "en"
    ES = "es"
    UNKNOWN = "unknown"


class EmailSource(str, Enum):
    """Email ingestion sources."""
    M365 = "m365"
    IMAP = "imap"
    MBOX = "mbox"


class Email(BaseModel):
    """Email entity representing a single email message.
    
    Core entity for email processing, classification, and suggestion generation.
    Supports multilingual content and multiple ingestion sources.
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    message_id: str = Field(..., description="Provider-specific message ID")
    thread_id: UUID = Field(..., description="Thread this email belongs to")
    from_: str = Field(..., alias="from", description="Sender email address")
    to: List[str] = Field(default_factory=list, description="Recipient email addresses")
    cc: List[str] = Field(default_factory=list, description="CC recipient email addresses")
    bcc: List[str] = Field(default_factory=list, description="BCC recipient email addresses")
    subject: str = Field(..., description="Email subject line")
    body_text: str = Field(..., description="Plain text body content")
    body_html: Optional[str] = Field(None, description="HTML body content")
    received_at: datetime = Field(..., description="When the email was received")
    language: EmailLanguage = Field(default=EmailLanguage.UNKNOWN, description="Detected language")
    has_attachments: bool = Field(default=False, description="Whether email has attachments")
    source: EmailSource = Field(..., description="Ingestion source")
    metadata: dict = Field(default_factory=dict, description="Additional headers and labels")

    class Config:
        """Pydantic configuration."""
        populate_by_name = True
        use_enum_values = True

    def __str__(self) -> str:
        """String representation."""
        return f"Email(id={self.id}, subject='{self.subject[:50]}...', from={self.from_})"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"Email(id={self.id}, message_id='{self.message_id}', "
            f"thread_id={self.thread_id}, from_='{self.from_}', "
            f"subject='{self.subject[:30]}...', source={self.source})"
        )