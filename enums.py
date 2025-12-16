"""
Enums
"""

from enum import Enum


class JobStatus(Enum):
    """
    Job Status Enum
    """

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
