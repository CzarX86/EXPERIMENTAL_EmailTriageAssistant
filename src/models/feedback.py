"""Feedback model for user feedback and learning."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class FeedbackType(str, Enum):
    """Types of user feedback."""
    APPROVE = "approve"  # User approves the suggestion/classification
    REJECT = "reject"    # User rejects the suggestion/classification
    CORRECT = "correct"  # User provides a correction


class Feedback(BaseModel):
    """Feedback entity for user corrections and approvals.
    
    Captures user feedback for incremental learning and model improvement.
    Supports various feedback types with flexible payload structure.
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    email_id: UUID = Field(..., description="Email this feedback relates to (foreign key)")
    type: FeedbackType = Field(..., description="Type of feedback provided")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Feedback-specific data (e.g., corrected_text)")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When feedback was provided")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True

    def __str__(self) -> str:
        """String representation."""
        return f"Feedback(type={self.type}, email_id={self.email_id})"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"Feedback(id={self.id}, email_id={self.email_id}, "
            f"type={self.type}, created_at={self.created_at}, "
            f"payload_keys={list(self.payload.keys())})"
        )

    @property
    def is_approval(self) -> bool:
        """Check if feedback is an approval."""
        return self.type == FeedbackType.APPROVE

    @property
    def is_rejection(self) -> bool:
        """Check if feedback is a rejection."""
        return self.type == FeedbackType.REJECT

    @property
    def is_correction(self) -> bool:
        """Check if feedback includes a correction."""
        return self.type == FeedbackType.CORRECT

    @property
    def corrected_text(self) -> str | None:
        """Get corrected text from payload if available."""
        return self.payload.get("corrected_text")

    @property
    def corrected_label(self) -> str | None:
        """Get corrected classification label from payload if available."""
        return self.payload.get("corrected_label")

    @classmethod
    def create_approval(cls, email_id: UUID) -> "Feedback":
        """Create an approval feedback.
        
        Args:
            email_id: ID of the email being approved
            
        Returns:
            Feedback instance for approval
        """
        return cls(
            email_id=email_id,
            type=FeedbackType.APPROVE,
            payload={}
        )

    @classmethod
    def create_rejection(cls, email_id: UUID, reason: str = "") -> "Feedback":
        """Create a rejection feedback.
        
        Args:
            email_id: ID of the email being rejected
            reason: Optional reason for rejection
            
        Returns:
            Feedback instance for rejection
        """
        payload = {}
        if reason:
            payload["reason"] = reason
            
        return cls(
            email_id=email_id,
            type=FeedbackType.REJECT,
            payload=payload
        )

    @classmethod
    def create_text_correction(cls, email_id: UUID, corrected_text: str) -> "Feedback":
        """Create a text correction feedback.
        
        Args:
            email_id: ID of the email being corrected
            corrected_text: User's corrected text
            
        Returns:
            Feedback instance for text correction
        """
        return cls(
            email_id=email_id,
            type=FeedbackType.CORRECT,
            payload={"corrected_text": corrected_text}
        )

    @classmethod
    def create_label_correction(cls, email_id: UUID, corrected_label: str) -> "Feedback":
        """Create a classification label correction feedback.
        
        Args:
            email_id: ID of the email being corrected
            corrected_label: User's corrected classification label
            
        Returns:
            Feedback instance for label correction
        """
        return cls(
            email_id=email_id,
            type=FeedbackType.CORRECT,
            payload={"corrected_label": corrected_label}
        )