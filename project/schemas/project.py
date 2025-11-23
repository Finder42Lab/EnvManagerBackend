from pydantic import BaseModel, ConfigDict

from .common import IdNameSchema


class ShortProjectSchema(BaseModel):
    id: str
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ProjectSchema(ShortProjectSchema):
    includes: list[str]
