from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.task import Task


class TaskRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_all(self) -> List[Task]:
        return self._db.query(Task).all()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self._db.query(Task).filter(Task.id == task_id).first()

    def create(self, title: str, description: Optional[str]) -> Task:
        task = Task(title=title, description=description)
        self._db.add(task)
        self._db.commit()
        self._db.refresh(task)
        return task

    def update(
        self,
        task: Task,
        title: Optional[str],
        description: Optional[str],
        completed: Optional[bool],
    ) -> Task:
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        self._db.commit()
        self._db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self._db.delete(task)
        self._db.commit()
