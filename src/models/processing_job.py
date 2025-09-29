"""Processing job model for background task management."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class JobType(str, Enum):
    """Types of processing jobs."""
    INGEST = "ingest"
    OCR = "ocr"
    INDEX = "index"
    CLASSIFY = "classify"
    SUGGEST = "suggest"
    EXPORT = "export"
    IMPORT = "import"


class JobStatus(str, Enum):
    """Status of processing jobs."""
    QUEUED = "queued"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    NEEDS_ATTENTION = "needs_attention"


class ProcessingJob(BaseModel):
    """Processing job entity for background task management.
    
    Manages asynchronous processing tasks with retry logic,
    error handling, and safe mode for large files.
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    job_type: JobType = Field(..., description="Type of processing job")
    status: JobStatus = Field(default=JobStatus.QUEUED, description="Current job status")
    started_at: datetime = Field(default_factory=datetime.utcnow, description="When job was started")
    finished_at: Optional[datetime] = Field(None, description="When job completed")
    attempts: int = Field(default=0, ge=0, description="Number of execution attempts")
    max_attempts: int = Field(default=3, gt=0, description="Maximum retry attempts")
    error: Optional[str] = Field(None, description="Error message if failed")
    safe_mode: bool = Field(default=False, description="Whether to use safe mode for large files")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True

    def __str__(self) -> str:
        """String representation."""
        return f"ProcessingJob({self.job_type}, status={self.status}, attempts={self.attempts})"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"ProcessingJob(id={self.id}, job_type={self.job_type}, "
            f"status={self.status}, attempts={self.attempts}, "
            f"started_at={self.started_at}, safe_mode={self.safe_mode})"
        )

    @property
    def is_queued(self) -> bool:
        """Check if job is queued for execution."""
        return self.status == JobStatus.QUEUED

    @property
    def is_running(self) -> bool:
        """Check if job is currently running."""
        return self.status == JobStatus.RUNNING

    @property
    def is_done(self) -> bool:
        """Check if job completed successfully."""
        return self.status == JobStatus.DONE

    @property
    def is_failed(self) -> bool:
        """Check if job failed."""
        return self.status == JobStatus.FAILED

    @property
    def needs_attention(self) -> bool:
        """Check if job needs manual attention."""
        return self.status == JobStatus.NEEDS_ATTENTION

    @property
    def can_retry(self) -> bool:
        """Check if job can be retried."""
        return self.attempts < self.max_attempts and self.status in [JobStatus.FAILED, JobStatus.QUEUED]

    @property
    def is_exhausted(self) -> bool:
        """Check if job has exhausted all retry attempts."""
        return self.attempts >= self.max_attempts

    @property
    def duration_seconds(self) -> float | None:
        """Get job duration in seconds if completed.
        
        Returns:
            Duration in seconds or None if not finished
        """
        if self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return None

    def start(self) -> None:
        """Mark job as running."""
        self.status = JobStatus.RUNNING
        if self.attempts == 0:
            self.started_at = datetime.utcnow()

    def complete(self) -> None:
        """Mark job as successfully completed."""
        self.status = JobStatus.DONE
        self.finished_at = datetime.utcnow()
        self.error = None

    def fail(self, error_message: str) -> None:
        """Mark job as failed with error message.
        
        Args:
            error_message: Description of the failure
        """
        self.status = JobStatus.FAILED
        self.finished_at = datetime.utcnow()
        self.error = error_message

    def mark_needs_attention(self, reason: str) -> None:
        """Mark job as needing manual attention.
        
        Args:
            reason: Reason why manual attention is needed
        """
        self.status = JobStatus.NEEDS_ATTENTION
        self.finished_at = datetime.utcnow()
        self.error = f"Needs attention: {reason}"

    def retry(self) -> bool:
        """Attempt to retry the job.
        
        Returns:
            True if retry was scheduled, False if exhausted
        """
        if not self.can_retry:
            return False
            
        self.attempts += 1
        self.status = JobStatus.QUEUED
        self.finished_at = None
        self.error = None
        return True

    def enable_safe_mode(self) -> None:
        """Enable safe mode for processing large files."""
        self.safe_mode = True

    def should_use_exponential_backoff(self) -> bool:
        """Check if exponential backoff should be applied.
        
        Returns:
            True if job has failed at least once
        """
        return self.attempts > 0 and self.status == JobStatus.FAILED

    def get_backoff_seconds(self, base_delay: int = 60) -> int:
        """Calculate exponential backoff delay.
        
        Args:
            base_delay: Base delay in seconds
            
        Returns:
            Delay in seconds for next retry
        """
        if self.attempts == 0:
            return 0
        return base_delay * (2 ** (self.attempts - 1))

    @classmethod
    def create_job(
        cls,
        job_type: JobType,
        max_attempts: int = 3,
        safe_mode: bool = False
    ) -> "ProcessingJob":
        """Create a new processing job.
        
        Args:
            job_type: Type of job to create
            max_attempts: Maximum retry attempts
            safe_mode: Whether to enable safe mode
            
        Returns:
            New ProcessingJob instance
        """
        return cls(
            job_type=job_type,
            max_attempts=max_attempts,
            safe_mode=safe_mode,
            finished_at=None,
            error=None
        )