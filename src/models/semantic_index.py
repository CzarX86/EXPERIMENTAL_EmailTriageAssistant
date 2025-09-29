"""Semantic index entry model for vector search."""

from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RefType(str, Enum):
    """Type of reference for semantic index entry."""
    EMAIL = "email"
    ATTACHMENT = "attachment"


class IndexLanguage(str, Enum):
    """Supported languages for semantic indexing."""
    PT = "pt"
    EN = "en"
    ES = "es"
    UNKNOWN = "unknown"


class SemanticIndexEntry(BaseModel):
    """Semantic index entry for vector-based search.
    
    Stores vector embeddings for emails and attachments to enable
    semantic search across multilingual content.
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    ref_type: RefType = Field(..., description="Type of referenced content")
    ref_id: UUID = Field(..., description="ID of referenced email or attachment")
    vector: List[float] = Field(..., description="Embedding vector")
    dim: int = Field(..., gt=0, description="Vector dimensionality")
    language: IndexLanguage = Field(default=IndexLanguage.UNKNOWN, description="Detected language")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When entry was created")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True

    def __str__(self) -> str:
        """String representation."""
        return f"SemanticIndexEntry({self.ref_type}, dim={self.dim}, lang={self.language})"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"SemanticIndexEntry(id={self.id}, ref_type={self.ref_type}, "
            f"ref_id={self.ref_id}, dim={self.dim}, language={self.language}, "
            f"created_at={self.created_at})"
        )

    @property
    def is_email_vector(self) -> bool:
        """Check if this is an email vector."""
        return self.ref_type == RefType.EMAIL

    @property
    def is_attachment_vector(self) -> bool:
        """Check if this is an attachment vector."""
        return self.ref_type == RefType.ATTACHMENT

    @property
    def vector_length(self) -> int:
        """Get the actual length of the vector."""
        return len(self.vector)

    def validate_vector_dimension(self) -> bool:
        """Validate that vector length matches declared dimension.
        
        Returns:
            True if vector length matches dim field
        """
        return len(self.vector) == self.dim

    @classmethod
    def create_email_entry(
        cls,
        email_id: UUID,
        vector: List[float],
        language: IndexLanguage = IndexLanguage.UNKNOWN
    ) -> "SemanticIndexEntry":
        """Create a semantic index entry for an email.
        
        Args:
            email_id: ID of the email
            vector: Embedding vector
            language: Detected language
            
        Returns:
            SemanticIndexEntry for the email
        """
        return cls(
            ref_type=RefType.EMAIL,
            ref_id=email_id,
            vector=vector,
            dim=len(vector),
            language=language
        )

    @classmethod
    def create_attachment_entry(
        cls,
        attachment_id: UUID,
        vector: List[float],
        language: IndexLanguage = IndexLanguage.UNKNOWN
    ) -> "SemanticIndexEntry":
        """Create a semantic index entry for an attachment.
        
        Args:
            attachment_id: ID of the attachment
            vector: Embedding vector
            language: Detected language
            
        Returns:
            SemanticIndexEntry for the attachment
        """
        return cls(
            ref_type=RefType.ATTACHMENT,
            ref_id=attachment_id,
            vector=vector,
            dim=len(vector),
            language=language
        )