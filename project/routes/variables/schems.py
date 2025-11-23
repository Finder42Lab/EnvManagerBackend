from uuid import UUID

from pydantic import BaseModel


class WriteVariableResponse(BaseModel):
    id: UUID | None = None
    name: str
    value: str | None = None
    is_secret: bool = False
    project_id: str | None = None
