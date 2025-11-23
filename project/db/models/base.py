from sqlalchemy import Uuid, UUID, text
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped


class BaseDBModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
