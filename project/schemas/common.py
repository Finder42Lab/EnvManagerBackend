from uuid import UUID

from pydantic import BaseModel


class IdNameSchema(BaseModel):
    id: str | UUID
    name: str
