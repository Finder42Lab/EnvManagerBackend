from uuid import UUID

from pydantic import BaseModel, computed_field, ConfigDict, Field

from schemas.common import IdNameSchema


class VariableSchema(BaseModel):
    id: UUID
    name: str
    value: str | None = None

    is_secret: bool = False

    project: IdNameSchema

    model_config = ConfigDict(from_attributes=True)
