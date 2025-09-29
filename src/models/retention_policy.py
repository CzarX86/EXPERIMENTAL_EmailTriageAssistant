"""Retention policy model for data lifecycle management."""

from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RetentionItemType(str, Enum):
    """Types of items that can have retention policies."""
    INDEX = "index"    # Semantic index entries
    MODEL = "model"    # Model states and parameters
    DERIVED = "derived"  # Derived data like OCR text


class RetentionPolicy(BaseModel):
    """Retention policy entity for data lifecycle management.
    
    Defines data retention rules with configurable TTL and auto-purge
    based on item type. Supports user overrides for specific needs.
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    item_type: RetentionItemType = Field(..., description="Type of item this policy applies to")
    default_ttl_days: int = Field(..., gt=0, description="Default time-to-live in days")
    user_override_ttl_days: Optional[int] = Field(None, gt=0, description="User-specified TTL override")
    auto_purge: bool = Field(default=True, description="Whether to automatically purge expired items")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True

    def __str__(self) -> str:
        """String representation."""
        ttl = self.effective_ttl_days
        return f"RetentionPolicy({self.item_type}, {ttl}d, auto_purge={self.auto_purge})"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"RetentionPolicy(id={self.id}, item_type={self.item_type}, "
            f"default_ttl_days={self.default_ttl_days}, "
            f"user_override_ttl_days={self.user_override_ttl_days}, "
            f"auto_purge={self.auto_purge})"
        )

    @property
    def effective_ttl_days(self) -> int:
        """Get the effective TTL considering user overrides.
        
        Returns:
            Effective TTL in days (user override if set, otherwise default)
        """
        return self.user_override_ttl_days or self.default_ttl_days

    @property
    def has_user_override(self) -> bool:
        """Check if user has overridden the default TTL."""
        return self.user_override_ttl_days is not None

    def set_user_override(self, ttl_days: int) -> None:
        """Set user override for TTL.
        
        Args:
            ttl_days: New TTL in days (must be positive)
        """
        if ttl_days <= 0:
            raise ValueError("TTL must be positive")
        self.user_override_ttl_days = ttl_days

    def clear_user_override(self) -> None:
        """Clear user override, reverting to default TTL."""
        self.user_override_ttl_days = None

    def enable_auto_purge(self) -> None:
        """Enable automatic purging of expired items."""
        self.auto_purge = True

    def disable_auto_purge(self) -> None:
        """Disable automatic purging of expired items."""
        self.auto_purge = False

    @classmethod
    def create_default_policies(cls) -> list["RetentionPolicy"]:
        """Create default retention policies per spec requirements.
        
        From spec FR-014:
        - Indices: 365 days (auto purge)
        - Models: indefinite (no auto purge)
        - Derived (OCR/temp): 90 days (auto purge)
        
        Returns:
            List of default retention policies
        """
        return [
            cls(
                item_type=RetentionItemType.INDEX,
                default_ttl_days=365,
                user_override_ttl_days=None,
                auto_purge=True
            ),
            cls(
                item_type=RetentionItemType.MODEL,
                default_ttl_days=999999,  # "Indefinite" as very large number
                user_override_ttl_days=None,
                auto_purge=False
            ),
            cls(
                item_type=RetentionItemType.DERIVED,
                default_ttl_days=90,
                user_override_ttl_days=None,
                auto_purge=True
            )
        ]

    @classmethod
    def get_policy_for_type(
        cls,
        policies: list["RetentionPolicy"],
        item_type: RetentionItemType
    ) -> "RetentionPolicy | None":
        """Get retention policy for a specific item type.
        
        Args:
            policies: List of retention policies to search
            item_type: Type of item to find policy for
            
        Returns:
            Matching retention policy or None if not found
        """
        for policy in policies:
            if policy.item_type == item_type:
                return policy
        return None