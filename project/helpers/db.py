import functools
import operator
from typing import Any

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.base import BaseDBModel


async def upsert_entities(
    model_cls: type[BaseDBModel],
    db_session: AsyncSession,
    fields: list[dict[str, Any]],
    returning_ids: bool = False,
    index_elements: list[str] = ["id"],
):
    if not fields:
        return []

    insert_fields_superset = functools.reduce(
        operator.or_,
        [insert_value.keys() for insert_value in fields],
    )

    query = insert(model_cls).values(fields)

    query = query.on_conflict_do_update(
        index_elements=index_elements,
        set_={
            key: excluded_field
            for key, excluded_field in query.excluded.items()
            if key in insert_fields_superset
        },
    )

    if returning_ids:
        query = query.returning(model_cls.id)

    query_result = await db_session.execute(query)

    if returning_ids:
        return query_result.scalars().all()
    return []
