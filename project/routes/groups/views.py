from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ProjectGroup, Project
from db.session import get_db_session
from helpers.db import upsert_entities
from routes.groups.schemas import WriteProjectGroupRequest
from schemas.common import IdNameSchema

router = APIRouter()


@router.get("/", response_model=list[IdNameSchema])
async def groups_list(db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    query = select(ProjectGroup).order_by(ProjectGroup.name)
    query_result = await db_session.execute(query)
    return query_result.scalars().all()


@router.get("/{group_id}/", response_model=IdNameSchema)
async def retrieve_group(
    group_id: UUID,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    query = select(ProjectGroup).where(ProjectGroup.id == group_id)
    query_result = await db_session.execute(query)
    item = query_result.scalar_one()

    return item


@router.post("/")
async def write_group(
    body: WriteProjectGroupRequest,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    new_ids = await upsert_entities(
        model_cls=ProjectGroup,
        db_session=db_session,
        fields=[body.model_dump(exclude_unset=True)],
        returning_ids=True,
    )

    return new_ids[0]


@router.delete("/{group_id}/")
async def delete_group(
    group_id: UUID,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    exist_query = select(Project).where(Project.group_id == group_id)
    query_result = await db_session.execute(exist_query)
    item = query_result.scalar_one_or_none()

    if item is not None:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Невозможно удалить группу, тк у неё есть дочерние проекты.",
            },
        )

    delete_query = delete(ProjectGroup).where(ProjectGroup.id == group_id)
    await db_session.execute(delete_query)
