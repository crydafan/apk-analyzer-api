"""
Models
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID

from db import Base
from enums import JobStatus


class Job(Base):
    """
    Job Model
    """

    __tablename__ = "jobs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    status = Column(Enum(JobStatus), nullable=False, default=JobStatus.PENDING)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
