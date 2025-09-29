"""Classification model for email categorization."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ClassificationLabel(str, Enum):
    """Email classification labels."""
    SPAM = "spam"
    URGENT = "urgent"
    ACAO = "acao"  # Action required
    RESPONDER = "responder"  # Needs response
    IGNORAR = "ignorar"  # Can be ignored


class ClassificationOrigin(str, Enum):
    """Origin of the classification decision."""
    AUTO = "auto"  # Automatically generated
    USER_CORRECTED = "user_corrected"  # User manually corrected


class Classification(BaseModel):
    """Classification entity for email categorization.
    
    Records automatic and user-corrected email classifications
    with confidence scores and rationale tracking.
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    email_id: UUID = Field(..., description="Email being classified (foreign key)")
    label: ClassificationLabel = Field(..., description="Classification category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score [0,1]")
    origin: ClassificationOrigin = Field(default=ClassificationOrigin.AUTO, description="Source of classification")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When classification was created")
    rationale_ref: Optional[UUID] = Field(None, description="Reference to explanation (foreign key)")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True

    def __str__(self) -> str:
        """String representation."""
        return f"Classification(label={self.label}, confidence={self.confidence:.2f}, origin={self.origin})"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"Classification(id={self.id}, email_id={self.email_id}, "
            f"label={self.label}, confidence={self.confidence:.3f}, "
            f"origin={self.origin}, created_at={self.created_at})"
        )

    @property
    def is_high_confidence(self, threshold: float = 0.8) -> bool:
        """Check if classification has high confidence.
        
        Args:
            threshold: Minimum confidence level to consider "high"
            
        Returns:
            True if confidence is above threshold
        """
        return self.confidence >= threshold

    @property
    def is_user_verified(self) -> bool:
        """Check if classification was verified/corrected by user."""
        return self.origin == ClassificationOrigin.USER_CORRECTED

    @property
    def requires_action(self) -> bool:
        """Check if classification indicates action is required."""
        action_labels = {ClassificationLabel.URGENT, ClassificationLabel.ACAO, ClassificationLabel.RESPONDER}
        return self.label in action_labels