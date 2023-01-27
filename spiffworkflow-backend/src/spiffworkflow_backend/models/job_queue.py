
from dataclasses import dataclass
from sqlalchemy.orm import deferred
from spiffworkflow_backend.models.db import db
from spiffworkflow_backend.models.db import SpiffworkflowBaseDBModel


@dataclass
class JobQueueModel(SpiffworkflowBaseDBModel):
    __tablename__ = "job_queue"

    id: int = db.Column(db.Integer, primary_key=True)
    updated_at_in_seconds: int = db.Column(db.Integer)
    created_at_in_seconds: int = db.Column(db.Integer)

    locked_by: str | None = db.Column(db.String(80))
    locked_at_in_seconds: int | None = db.Column(db.Integer)
    payload: dict = deferred(db.Column(db.JSON, nullable=False))  # type: ignore
