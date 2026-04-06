from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel


tasks_tag = Tag(name="Tasks", description="Operações relacionadas a tarefas")
bp = APIBlueprint("tasks", __name__, url_prefix="/tasks")

class Task(BaseModel):
    task_id: int

@bp.get("/", tags=[tasks_tag], responses={"200": Task})
def list_tasks():
    """
    Rota para obter todas as tarefas.
    """
    return {"tasks": []}, 200