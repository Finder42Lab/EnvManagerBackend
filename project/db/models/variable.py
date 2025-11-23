from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .project import Project
from db.models.base import BaseDBModel


class Variable(BaseDBModel):
    __tablename__ = "variable"

    name: Mapped[str]
    value: Mapped[str | None]

    is_secret: Mapped[bool] = mapped_column(server_default="f")

    project_id: Mapped[str] = mapped_column(
        ForeignKey(
            "project.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )

    project: Mapped[Project] = relationship()
