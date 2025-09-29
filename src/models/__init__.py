"""Models package for the email assistant.

This package contains all the data models used throughout the application,
including email entities, classification results, suggestions, and metadata.
"""

from .attachment import Attachment, OCRStatus
from .classification import Classification, ClassificationLabel, ClassificationOrigin
from .email import Email, EmailLanguage, EmailSource
from .explanation import Explanation, KeyFactors, SimilarEmail, FeedbackInfluence
from .feedback import Feedback, FeedbackType
from .model_state import ModelState
from .processing_job import ProcessingJob, JobType, JobStatus
from .retention_policy import RetentionPolicy, RetentionItemType
from .semantic_index import SemanticIndexEntry, RefType, IndexLanguage
from .suggestion import Suggestion, SuggestionStatus
from .thread import Thread

__all__ = [
    # Core entities
    "Email",
    "EmailLanguage",
    "EmailSource",
    "Attachment",
    "OCRStatus",
    "Thread",
    
    # Classification and ML
    "Classification",
    "ClassificationLabel",
    "ClassificationOrigin",
    "Suggestion",
    "SuggestionStatus",
    "Feedback",
    "FeedbackType",
    "Explanation",
    "KeyFactors",
    "SimilarEmail",
    "FeedbackInfluence",
    
    # Infrastructure
    "SemanticIndexEntry",
    "RefType",
    "IndexLanguage",
    "ModelState",
    "RetentionPolicy",
    "RetentionItemType",
    "ProcessingJob",
    "JobType",
    "JobStatus",
]
