"""Explanation model for classification and suggestion rationale."""

from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SimilarEmail(BaseModel):
    """Reference to a similar email used in decision making."""
    email_id: UUID = Field(..., description="ID of similar email")
    score: float = Field(..., ge=0.0, le=1.0, description="Similarity score [0,1]")


class FeedbackInfluence(BaseModel):
    """Reference to feedback that influenced the decision."""
    feedback_id: UUID = Field(..., description="ID of influential feedback")
    weight: float = Field(..., ge=0.0, description="Influence weight")


class KeyFactors(BaseModel):
    """Key factors that influenced the classification or suggestion."""
    keywords: List[str] = Field(default_factory=list, description="Important keywords found")
    vip: bool = Field(default=False, description="Whether sender is VIP")
    time_window: str | None = Field(default=None, description="Time-sensitive context")
    thread_activity: str | None = Field(default=None, description="Thread activity level")
    mentions: List[str] = Field(default_factory=list, description="Direct mentions of user")


class Explanation(BaseModel):
    """Explanation entity for classification and suggestion rationale.
    
    Provides transparency and auditability for AI decisions by tracking
    key factors, similar examples, and feedback influence.
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    email_id: UUID = Field(..., description="Email this explanation relates to (foreign key)")
    label: str = Field(..., description="Classification label or suggestion type")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the decision")
    key_factors: KeyFactors = Field(default_factory=lambda: KeyFactors(), description="Factors that influenced decision")
    similar_emails: List[SimilarEmail] = Field(default_factory=list, description="Similar emails used as reference")
    feedback_influence: List[FeedbackInfluence] = Field(default_factory=list, description="Feedback that influenced decision")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When explanation was created")

    def __str__(self) -> str:
        """String representation."""
        return f"Explanation(label='{self.label}', confidence={self.confidence:.2f}, factors={len(self.key_factors.keywords)})"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"Explanation(id={self.id}, email_id={self.email_id}, "
            f"label='{self.label}', confidence={self.confidence:.3f}, "
            f"similar_emails={len(self.similar_emails)}, created_at={self.created_at})"
        )

    @property
    def has_keyword_factors(self) -> bool:
        """Check if explanation includes keyword factors."""
        return len(self.key_factors.keywords) > 0

    @property
    def has_vip_factor(self) -> bool:
        """Check if VIP status influenced the decision."""
        return self.key_factors.vip

    @property
    def has_time_factor(self) -> bool:
        """Check if time-sensitive factors influenced the decision."""
        return self.key_factors.time_window is not None

    @property
    def has_thread_factor(self) -> bool:
        """Check if thread activity influenced the decision."""
        return self.key_factors.thread_activity is not None

    @property
    def has_mention_factors(self) -> bool:
        """Check if direct mentions influenced the decision."""
        return len(self.key_factors.mentions) > 0

    @property
    def similarity_count(self) -> int:
        """Number of similar emails referenced."""
        return len(self.similar_emails)

    @property
    def feedback_count(self) -> int:
        """Number of feedback items that influenced decision."""
        return len(self.feedback_influence)

    def add_keyword_factor(self, keyword: str) -> None:
        """Add a keyword factor to the explanation.
        
        Args:
            keyword: Important keyword that influenced the decision
        """
        if keyword not in self.key_factors.keywords:
            self.key_factors.keywords.append(keyword)

    def add_similar_email(self, email_id: UUID, score: float) -> None:
        """Add a similar email reference.
        
        Args:
            email_id: ID of the similar email
            score: Similarity score [0,1]
        """
        similar = SimilarEmail(email_id=email_id, score=score)
        self.similar_emails.append(similar)

    def add_feedback_influence(self, feedback_id: UUID, weight: float) -> None:
        """Add feedback influence to the explanation.
        
        Args:
            feedback_id: ID of the influential feedback
            weight: Influence weight
        """
        influence = FeedbackInfluence(feedback_id=feedback_id, weight=weight)
        self.feedback_influence.append(influence)

    def get_explanation_summary(self) -> Dict[str, Any]:
        """Get a summary of the explanation for display.
        
        Returns:
            Dictionary with explanation summary
        """
        return {
            "label": self.label,
            "confidence": round(self.confidence, 3),
            "key_factors": {
                "keywords": self.key_factors.keywords,
                "vip_sender": self.key_factors.vip,
                "time_sensitive": self.key_factors.time_window,
                "thread_activity": self.key_factors.thread_activity,
                "mentions": self.key_factors.mentions,
            },
            "similar_emails_count": len(self.similar_emails),
            "feedback_influences_count": len(self.feedback_influence),
            "created_at": self.created_at.isoformat(),
        }