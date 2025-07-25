from typing import List
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.tasks.models import Task, TaskStatus
from src.domain.tasks.interfaces import TaskRepository
from .models import TaskORM


class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, task_id: UUID) -> Task | None:
        result = await self.session.execute(
            select(TaskORM).where(TaskORM.id == task_id)
        )
        task_orm = result.scalar_one_or_none()
        if task_orm is None:
            return None
        return self._to_domain(task_orm)

    async def list(self, status: TaskStatus | None = None) -> List[Task]:
        query = select(TaskORM)
        if status:
            query = query.where(TaskORM.status == status)
        result = await self.session.execute(query)
        tasks_orm = result.scalars().all()
        return [self._to_domain(t) for t in tasks_orm]

    async def add(self, task: Task) -> None:
        task_orm = self._to_orm(task)
        self.session.add(task_orm)
        await self.session.commit()

    async def update(self, task: Task) -> None:
        task_orm = await self.session.get(TaskORM, task.id)
        if task_orm:
            task_orm.title = task.title
            task_orm.description = task.description
            task_orm.status = task.status
            await self.session.commit()

    async def delete(self, task_id: UUID) -> None:
        task_orm = await self.session.get(TaskORM, task_id)
        if task_orm:
            await self.session.delete(task_orm)
            await self.session.commit()

    @staticmethod
    def _to_domain(task_orm: TaskORM) -> Task:
        return Task(
            id=task_orm.id,
            title=task_orm.title,
            description=task_orm.description,
            status=task_orm.status,
            created_at=task_orm.created_at,
        )

    @staticmethod
    def _to_orm(task: Task) -> TaskORM:
        return TaskORM(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            created_at=task.created_at,
        )
