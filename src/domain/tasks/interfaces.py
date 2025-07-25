from abc import ABC, abstractmethod
from uuid import UUID
from .models import Task, TaskStatus


class TaskRepository(ABC):
    @abstractmethod
    async def get(self, task_id: UUID) -> Task | None:
        ...

    @abstractmethod
    async def list(self, status: TaskStatus | None = None) -> list[Task]:
        ...

    @abstractmethod
    async def add(self, task: Task) -> None:
        ...

    @abstractmethod
    async def update(self, task: Task) -> None:
        ...

    @abstractmethod
    async def delete(self, task_id: UUID) -> None:
        ...
