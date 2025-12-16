"""
Schemas
"""

import uuid

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class JobBase(BaseModel):
    """
    Base schema for Job
    """

    class Config:
        """
        Enable ORM mode
        """

        from_attributes = True

    id: uuid.UUID
    status: str


class JobCreate(BaseModel):
    """
    Schema for creating a Job
    """

    pass


class JobUpdate(BaseModel):
    """
    Schema for updating a Job
    """

    class Config:
        """
        Enable ORM mode
        """

        from_attributes = True

    status: Optional[str] = None


class Job(JobBase):
    """
    Schema for a Job with timestamps
    """

    created_at: datetime
    updated_at: datetime
