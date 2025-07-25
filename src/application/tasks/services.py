from uuid import UUID
from src.domain.tasks.models import Task
from src.domain.tasks.interfaces import TaskRepository
from .dto import TaskCreateDTO, TaskUpdateDTO


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create_task(self, data: TaskCreateDTO) -> Task:
        task = Task(title=data.title, description=data.description, status=data.status)
        await self.repo.add(task)
        return task

    async def list_tasks(self, status: str | None = None) -> list[Task]:
        return await self.repo.list(status=status)

    async def update_task(self, task_id: UUID, data: TaskUpdateDTO) -> Task | None:
        task = await self.repo.get(task_id)
        if task is None:
            return None
        task.update(title=data.title, description=data.description, status=data.status)
        await self.repo.update(task)
        return task

    async def delete_task(self, task_id: UUID) -> bool:
        task = await self.repo.get(task_id)
        if task is None:
            return False
        await self.repo.delete(task_id)
        return True
