from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskCreateBody(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Título da tarefa")
    description: Optional[str] = Field(None, max_length=1000, description="Descrição opcional da tarefa")


class TaskUpdateBody(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Novo título")
    description: Optional[str] = Field(None, max_length=1000, description="Nova descrição")
    completed: Optional[bool] = Field(None, description="Status de conclusão")


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse] = Field(..., description="Lista de tarefas")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Mensagem de erro")
