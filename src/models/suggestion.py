"""Suggestion model for email response suggestions."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SuggestionStatus(str, Enum):
    """Status of a suggestion."""
    PENDENTE = "pendente"  # Pending review
    APROVADA = "aprovada"  # Approved by user
    REJEITADA = "rejeitada"  # Rejected by user


class Suggestion(BaseModel):
    """Suggestion entity for email response suggestions.
    
    Stores AI-generated response suggestions with approval tracking
    and correction capabilities for incremental learning.
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    email_id: UUID = Field(..., description="Email this suggestion is for (foreign key)")
    text: str = Field(..., description="Suggested response text")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When suggestion was created")
    status: SuggestionStatus = Field(default=SuggestionStatus.PENDENTE, description="Current status")
    approved_at: Optional[datetime] = Field(None, description="When suggestion was approved")
    corrected_text: Optional[str] = Field(None, description="User-corrected version of suggestion")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True

    def __str__(self) -> str:
        """String representation."""
        preview = self.text[:50] + "..." if len(self.text) > 50 else self.text
        return f"Suggestion(status={self.status}, text='{preview}')"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"Suggestion(id={self.id}, email_id={self.email_id}, "
            f"status={self.status}, created_at={self.created_at}, "
            f"text_length={len(self.text)})"
        )

    @property
    def is_pending(self) -> bool:
        """Check if suggestion is still pending review."""
        return self.status == SuggestionStatus.PENDENTE

    @property
    def is_approved(self) -> bool:
        """Check if suggestion was approved by user."""
        return self.status == SuggestionStatus.APROVADA

    @property
    def is_rejected(self) -> bool:
        """Check if suggestion was rejected by user."""
        return self.status == SuggestionStatus.REJEITADA

    @property
    def has_correction(self) -> bool:
        """Check if user provided a corrected version."""
        return self.corrected_text is not None and len(self.corrected_text.strip()) > 0

    def approve(self) -> None:
        """Mark suggestion as approved."""
        self.status = SuggestionStatus.APROVADA
        self.approved_at = datetime.utcnow()

    def reject(self) -> None:
        """Mark suggestion as rejected."""
        self.status = SuggestionStatus.REJEITADA
        self.approved_at = None

    def correct(self, corrected_text: str) -> None:
        """Apply user correction to the suggestion.
        
        Args:
            corrected_text: User's corrected version of the suggestion
        """
        self.corrected_text = corrected_text.strip()
        self.status = SuggestionStatus.APROVADA
        self.approved_at = datetime.utcnow()