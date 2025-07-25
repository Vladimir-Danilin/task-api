from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.domain.tasks.models import TaskStatus
from src.application.tasks.dto import TaskCreateDTO, TaskUpdateDTO, TaskReadDTO
from src.application.tasks.services import TaskService
from src.infra.db import async_session
from src.infra.persistence.repositories import SQLAlchemyTaskRepository
from .dependencies import get_current_token


router = APIRouter(prefix="/tasks", tags=["tasks"])


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_task_service(session: AsyncSession = Depends(get_session)) -> TaskService:
    repo = SQLAlchemyTaskRepository(session)
    return TaskService(repo)


@router.post("/", response_model=TaskReadDTO, dependencies=[Depends(get_current_token)])
async def create_task(data: TaskCreateDTO, service: TaskService = Depends(get_task_service)):
    task = await service.create_task(data)
    return TaskReadDTO.model_validate(task)


@router.get("/", response_model=list[TaskReadDTO], dependencies=[Depends(get_current_token)])
async def list_tasks(status: TaskStatus | None = Query(None), service: TaskService = Depends(get_task_service)):
    tasks = await service.list_tasks(status)
    return [TaskReadDTO.model_validate(task) for task in tasks]


@router.patch("/{task_id}", response_model=TaskReadDTO, dependencies=[Depends(get_current_token)])
async def update_task(task_id: UUID, data: TaskUpdateDTO, service: TaskService = Depends(get_task_service)):
    task = await service.update_task(task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskReadDTO.model_validate(task)


@router.delete("/{task_id}", dependencies=[Depends(get_current_token)])
async def delete_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    success = await service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
