from uuid import UUID

from pydantic import BaseModel


class WriteProjectGroupRequest(BaseModel):
    id: UUID | None = None

    name: str
