"""
Database service for job operations
"""

from sqlalchemy.orm import Session

from schemas import JobCreate
from models import Job
from enums import JobStatus


def create_job(db: Session, data: JobCreate) -> Job:
    """
    Create a new job
    """
    job = Job(**data.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job(db: Session, job_id: str) -> Job | None:
    """
    Get a job by ID
    """
    return db.query(Job).filter(Job.id == job_id).first()


def update_job(db: Session, job_id: str, status: JobStatus) -> Job | None:
    """
    Update a job's status by ID
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.status = status
        db.commit()
        db.refresh(job)
    return job
