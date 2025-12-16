"""
Main
"""

from fastapi import FastAPI, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from services import database
import schemas
from db import get_db


app = FastAPI()


@app.get("/{job_id}", response_model=schemas.Job)
async def get_job(job_id: str, db: Session = Depends(get_db)):
    """
    Get job by ID
    """
    job = database.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.post("/", response_model=schemas.Job)
async def create_job(file: UploadFile, db: Session = Depends(get_db)):
    """
    Create a new job
    """
    return database.create_job(db, schemas.JobCreate())
