from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task:
    def __init__(
        self,
        title: str,
        description: str | None = None,
        status: TaskStatus = TaskStatus.PENDING,
        id: UUID | None = None,
        created_at: datetime | None = None,
    ):
        self.id = id or uuid4()
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.utcnow()

    def update(
        self,
        title: str | None = None,
        description: str | None = None,
        status: TaskStatus | None = None,
    ):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if status is not None:
            self.status = status
