"""Model state for ML model versioning and metrics."""

from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ModelState(BaseModel):
    """Model state entity for ML model versioning and tracking.
    
    Maintains version information, parameters, and performance metrics
    for incremental learning models.
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    version: str = Field(..., description="Model version identifier")
    params: Dict[str, Any] = Field(default_factory=dict, description="Model parameters and configuration")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics")

    def __str__(self) -> str:
        """String representation."""
        return f"ModelState(version='{self.version}', updated={self.updated_at.strftime('%Y-%m-%d %H:%M')})"

    def __repr__(self) -> str:
        """Developer representation."""
        return (
            f"ModelState(id={self.id}, version='{self.version}', "
            f"updated_at={self.updated_at}, params_count={len(self.params)}, "
            f"metrics_count={len(self.metrics)})"
        )

    @property
    def has_metrics(self) -> bool:
        """Check if model has performance metrics."""
        return len(self.metrics) > 0

    @property
    def has_params(self) -> bool:
        """Check if model has stored parameters."""
        return len(self.params) > 0

    def get_accuracy(self) -> float | None:
        """Get overall accuracy metric if available.
        
        Returns:
            Accuracy value or None if not available
        """
        return self.metrics.get("accuracy")

    def get_precision(self, label: str = "urgent") -> float | None:
        """Get precision for a specific label.
        
        Args:
            label: Classification label to get precision for
            
        Returns:
            Precision value or None if not available
        """
        return self.metrics.get(f"precision_{label}")

    def get_recall(self, label: str = "urgent") -> float | None:
        """Get recall for a specific label.
        
        Args:
            label: Classification label to get recall for
            
        Returns:
            Recall value or None if not available
        """
        return self.metrics.get(f"recall_{label}")

    def get_suggestion_acceptance_rate(self) -> float | None:
        """Get suggestion acceptance rate.
        
        Returns:
            Acceptance rate or None if not available
        """
        return self.metrics.get("suggestion_acceptance_rate")

    def update_metrics(self, new_metrics: Dict[str, Any]) -> None:
        """Update model metrics.
        
        Args:
            new_metrics: Dictionary of new metric values
        """
        self.metrics.update(new_metrics)
        self.updated_at = datetime.utcnow()

    def update_params(self, new_params: Dict[str, Any]) -> None:
        """Update model parameters.
        
        Args:
            new_params: Dictionary of new parameter values
        """
        self.params.update(new_params)
        self.updated_at = datetime.utcnow()

    def set_accuracy_metrics(
        self,
        accuracy: float,
        urgent_precision: float,
        urgent_recall: float,
        suggestion_acceptance: float
    ) -> None:
        """Set key accuracy metrics for the model.
        
        Args:
            accuracy: Overall classification accuracy
            urgent_precision: Precision for urgent classification
            urgent_recall: Recall for urgent classification
            suggestion_acceptance: Rate of suggestion acceptance
        """
        self.metrics.update({
            "accuracy": accuracy,
            "precision_urgent": urgent_precision,
            "recall_urgent": urgent_recall,
            "suggestion_acceptance_rate": suggestion_acceptance,
        })
        self.updated_at = datetime.utcnow()

    def meets_quality_targets(self) -> bool:
        """Check if model meets quality targets from spec.
        
        Quality targets from spec:
        - Urgent precision ≥ 90%
        - Urgent recall ≥ 80% 
        - Overall accuracy ≥ 75%
        - Suggestion acceptance ≥ 40%
        
        Returns:
            True if all targets are met
        """
        urgent_precision = self.get_precision("urgent")
        urgent_recall = self.get_recall("urgent")
        accuracy = self.get_accuracy()
        acceptance = self.get_suggestion_acceptance_rate()

        return all([
            urgent_precision is not None and urgent_precision >= 0.90,
            urgent_recall is not None and urgent_recall >= 0.80,
            accuracy is not None and accuracy >= 0.75,
            acceptance is not None and acceptance >= 0.40,
        ])