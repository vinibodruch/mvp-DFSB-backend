from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel

from src.models.database import SessionLocal
from src.schemas.task_schema import ErrorResponse, TaskCreateBody, TaskListResponse, TaskResponse, TaskUpdateBody
from src.services.task_service import TaskNotFoundError, TaskService

tasks_tag = Tag(name="tasks", description="Gerenciamento de tarefas To-Do")
bp = APIBlueprint("tasks", __name__, url_prefix="/tasks")


class TaskPath(BaseModel):
    task_id: int


@bp.get("/", tags=[tasks_tag], responses={200: TaskListResponse})
def list_tasks():
    """Retorna todas as tarefas."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        tasks = service.list_tasks()
        return {"tasks": [TaskResponse.model_validate(t).model_dump(mode="json") for t in tasks]}, 200
    finally:
        db.close()


@bp.post("/", tags=[tasks_tag], responses={201: TaskResponse, 422: ErrorResponse})
def create_task(body: TaskCreateBody):
    """Cria uma nova tarefa."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        task = service.create_task(title=body.title, description=body.description)
        return TaskResponse.model_validate(task).model_dump(mode="json"), 201
    finally:
        db.close()


@bp.get("/<int:task_id>", tags=[tasks_tag], responses={200: TaskResponse, 404: ErrorResponse})
def get_task(path: TaskPath):
    """Retorna uma única tarefa pelo ID."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        task = service.get_task(path.task_id)
        return TaskResponse.model_validate(task).model_dump(mode="json"), 200
    except TaskNotFoundError as e:
        return {"error": str(e)}, 404
    finally:
        db.close()


@bp.patch("/<int:task_id>", tags=[tasks_tag], responses={200: TaskResponse, 404: ErrorResponse})
def update_task(path: TaskPath, body: TaskUpdateBody):
    """Atualiza parcialmente uma tarefa (título, descrição ou status de conclusão)."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        task = service.update_task(
            path.task_id,
            title=body.title,
            description=body.description,
            completed=body.completed,
        )
        return TaskResponse.model_validate(task).model_dump(mode="json"), 200
    except TaskNotFoundError as e:
        return {"error": str(e)}, 404
    finally:
        db.close()


@bp.delete("/<int:task_id>", tags=[tasks_tag], responses={204: None, 404: ErrorResponse})
def delete_task(path: TaskPath):
    """Remove uma tarefa pelo ID."""
    db = SessionLocal()
    try:
        service = TaskService(db)
        service.delete_task(path.task_id)
        return "", 204
    except TaskNotFoundError as e:
        return {"error": str(e)}, 404
    finally:
        db.close()
