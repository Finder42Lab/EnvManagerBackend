from uuid import UUID

from pydantic import BaseModel, Field

from schemas.common import IdNameSchema
from schemas.project import ShortProjectSchema


class ProjectGroupResponse(BaseModel):
    id: UUID
    name: str

    projects: list[ShortProjectSchema]


class ProjectRetrieveResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    includes: list[str]
    group: IdNameSchema | None = None


class WriteProjectRequest(BaseModel):
    id: str | None = None
    name: str
    description: str | None = None
    includes: list[str] = Field(default_factory=list)
    group_id: UUID
