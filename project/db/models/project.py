from sqlalchemy import func, String, ForeignKey, UUID, text
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseDBModel


class ProjectGroup(BaseDBModel):
    __tablename__ = "project_group"

    name: Mapped[str]

    projects: Mapped[list["Project"]] = relationship(
        order_by=lambda: [
            func.array_length(Project.includes, 1).nullsfirst(),
            Project.name,
        ]
    )


class Project(BaseDBModel):
    __tablename__ = "project"

    id: Mapped[str] = mapped_column(primary_key=True)

    name: Mapped[str]
    description: Mapped[str | None] = None

    includes: Mapped[list[str]] = mapped_column(ARRAY(String))

    group_id: Mapped[UUID | None] = mapped_column(ForeignKey(ProjectGroup.id))

    group: Mapped[ProjectGroup] = relationship()
