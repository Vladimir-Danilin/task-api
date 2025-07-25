from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from src.domain.tasks.models import TaskStatus


class TaskCreateDTO(BaseModel):
    title: str
    description: str | None = None


class TaskUpdateDTO(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None


class TaskReadDTO(BaseModel):
    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
