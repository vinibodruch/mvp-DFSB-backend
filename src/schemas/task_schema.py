from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskCreateBody(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Optional task description")


class TaskUpdateBody(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="New title")
    description: Optional[str] = Field(None, max_length=1000, description="New description")
    completed: Optional[bool] = Field(None, description="Completion status")


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
    tasks: List[TaskResponse] = Field(..., description="List of tasks")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
