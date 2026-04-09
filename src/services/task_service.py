from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.task import Task
from src.repositories.task_repository import TaskRepository


class TaskNotFoundError(Exception):
    pass


class TaskService:
    def __init__(self, db: Session):
        self._repo = TaskRepository(db)

    def list_tasks(self) -> List[Task]:
        return self._repo.get_all()

    def get_task(self, task_id: int) -> Task:
        task = self._repo.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        return self._repo.create(title=title, description=description)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Task:
        task = self.get_task(task_id)
        return self._repo.update(task, title=title, description=description, completed=completed)

    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id)
        self._repo.delete(task)
