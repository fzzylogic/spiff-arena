
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

    # { job_type: [some_function], args: { job_id: [id] }}
    payload: dict = deferred(db.Column(db.JSON, nullable=False))  # type: ignore

    # make sure we're always using the same scheduler instance

    # 1. use apscheduler for future stuff. this will result in bugs when you "reset" a timer start event, because existing scheudled jobs probably can't be cancelled.

    # 2. timer in db, use apscheduler, but only "run now". Use JobQueueModel a bit more.

    # 3. avoid apscheduler, just do everything syncronously

    # first order columns:
    #   run_at_time
    #   remaining_cycles
    #   duration
    #   completed_at
    #   locked_by
    #   locked_at_in_seconds
    #   process_model_identifier

    # scheduler.add_job(process_model_timer_start_event)

    # perhaps if you have a five second cycle, it starts at 1:07:07, completes at 1:07:10, then the run_at_time should be set to 1:07:15 (5 seconds after it completes)

    # what if it's :11 when the app boots, it was supposed to run at :08, do you run?
    #   if completed_at is :09, then no
    #   if completed_at is :08, then ?
    #   if completed_at is :07, then yes

    # traps
