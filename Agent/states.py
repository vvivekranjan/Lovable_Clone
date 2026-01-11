from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import TypedDict


class File(BaseModel):
    """Represents a file to be created or modified."""
    path: str = Field(description="The path of the file to be created or modified")
    purpose: str = Field(description="The purpose of the file, e.g. 'main application logic', 'data processing module', etc.")


class Plan(BaseModel):
    """Project plan with architecture and features."""
    name: str = Field(description="The name of the app to be built")
    description: str = Field(description="A one-line description of the app to be built, e.g. 'A web application for managing personal finances'")
    techstack: str = Field(description="The tech stack to be used for the app, e.g. 'python', 'javascript', 'react', 'flask', etc.")
    features: List[str] = Field(description="A list of features that the app should have, e.g. 'user authentication', 'data visualization', etc.")
    files: List[str] = Field(description="A list of files to be created, each with a 'path' and 'purpose'")

    @field_validator("name", "description", "techstack")
    @classmethod
    def validate_non_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class ImplementationTask(BaseModel):
    """A single implementation task."""
    filepath: str = Field(description="The path to the file to be modified")
    task_description: str = Field(description="A detailed description of the task to be performed")

    @field_validator("filepath", "task_description")
    @classmethod
    def validate_non_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class TaskPlan(BaseModel):
    """Plan containing all implementation steps."""
    implementation_steps: List[ImplementationTask] = Field(description="A list of steps to be taken to implement the task")
    model_config = ConfigDict(extra="allow")


class CoderState(BaseModel):
    """State of the coder agent during implementation."""
    task_plan: TaskPlan = Field(description="The plan for the task to be implemented")
    current_step_idx: int = Field(default=0, description="The index of the current step in the implementation steps")
    current_file_content: Optional[str] = Field(default=None, description="The content of the file currently being edited or created")

    @field_validator("current_step_idx")
    @classmethod
    def validate_non_negative(cls, v):
        if v < 0:
            raise ValueError("Step index cannot be negative")
        return v


class AgentState(TypedDict):
    """State maintained throughout the agent workflow."""
    user_prompt: str
    project_plan: Plan
    architect_plan: List[ImplementationTask]
    coder_state: CoderState
    status: str  # Tracking agent status
