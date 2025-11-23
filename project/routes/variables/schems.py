from uuid import UUID

from pydantic import BaseModel


class WriteVariableResponse(BaseModel):
    id: UUID | None = None
    name: str
    value: str | None = None
    is_secret: bool = False
    project_id: str | None = None


class VariableBulkCreateRequest(BaseModel):
    project_id: str
    variables_text: str
