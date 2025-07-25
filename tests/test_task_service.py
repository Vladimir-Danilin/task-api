import pytest
from unittest.mock import AsyncMock

from src.application.tasks.dto import TaskCreateDTO
from src.domain.tasks.models import TaskStatus
from src.domain.tasks.models import Task
from src.application.tasks.services import TaskService


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def service(mock_repo):
    return TaskService(repo=mock_repo)


@pytest.mark.asyncio
async def test_create_task(service, mock_repo):
    dto = TaskCreateDTO(title="Test task")
    result = await service.create_task(dto)

    assert result.title == "Test task"


@pytest.mark.asyncio
async def test_get_all_tasks(service, mock_repo):
    task1 = Task(id=1, title="Task 1", status=TaskStatus.PENDING)
    task2 = Task(id=2, title="Task 2", status=TaskStatus.DONE)

    mock_repo.list = AsyncMock(return_value=[task1, task2])

    tasks = await service.list_tasks(status=None)
    assert len(tasks) == 2
    mock_repo.list.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_task(service, mock_repo):
    mock_repo.delete.return_value = None
    await service.delete_task(1)

    mock_repo.delete.assert_awaited_once_with(1)
