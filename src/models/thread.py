"""Thread model for email conversation threads."""

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Thread(BaseModel):
    """Thread entity representing email conversation threads.
    
    Groups related emails together for context-aware processing
    and thread-based urgency detection.
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    subject: str = Field(..., description="Thread subject (normalized)")
    participants: List[str] = Field(default_factory=list, description="All email addresses in thread")
    last_activity_at: datetime = Field(..., description="Timestamp of most recent activity")
    message_ids: List[UUID] = Field(default_factory=list, description="Email IDs in this thread")

    def __str__(self) -> str:
        """String representation."""
        return f"Thread(subject='{self.subject[:50]}...', {len(self.message_ids)} messages)"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"Thread(id={self.id}, subject='{self.subject[:30]}...', "
            f"participants={len(self.participants)}, messages={len(self.message_ids)}, "
            f"last_activity_at={self.last_activity_at})"
        )

    @property
    def message_count(self) -> int:
        """Number of messages in this thread."""
        return len(self.message_ids)

    @property
    def participant_count(self) -> int:
        """Number of unique participants in this thread."""
        return len(self.participants)

    def add_message(self, email_id: UUID, participant_email: str, activity_time: datetime) -> None:
        """Add a message to this thread.
        
        Args:
            email_id: ID of the email to add
            participant_email: Email address of the sender/recipient
            activity_time: Timestamp of the email
        """
        if email_id not in self.message_ids:
            self.message_ids.append(email_id)
        
        if participant_email not in self.participants:
            self.participants.append(participant_email)
        
        if activity_time > self.last_activity_at:
            self.last_activity_at = activity_time

    def is_active_recently(self, hours: int = 24) -> bool:
        """Check if thread has recent activity within specified hours.
        
        Args:
            hours: Number of hours to check for recent activity
            
        Returns:
            True if thread has activity within the specified timeframe
        """
        from datetime import timedelta
        
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        return self.last_activity_at > cutoff