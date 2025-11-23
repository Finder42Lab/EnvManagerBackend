from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models.project import Project, ProjectGroup
from db.session import get_db_session
from helpers.db import upsert_entities
from helpers.project import get_available_project_parents
from routes.projects.schema import (
    ProjectGroupResponse,
    WriteProjectRequest,
    ProjectRetrieveResponse,
)
from schemas.project import ShortProjectSchema

router = APIRouter()


@router.get("/", response_model=list[ProjectGroupResponse])
async def list_projects(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    query = (
        select(ProjectGroup)
        .order_by(ProjectGroup.name)
        .options(selectinload(ProjectGroup.projects))
    )
    query_result = await db_session.execute(query)
    projects = query_result.scalars().all()

    return projects


@router.get("/free/", response_model=list[ShortProjectSchema])
async def get_project_free_parents(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    project_id: Annotated[str | None, Query()] = None,
):
    if project_id is not None and project_id != "undefined":
        return await get_available_project_parents(project_id, db_session, False)

    query = select(Project)
    query_result = await db_session.execute(query)

    return query_result.scalars().all()


@router.get("/{project_id}/", response_model=ProjectRetrieveResponse)
async def retrieve_project(
    project_id: str,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    query = (
        select(Project)
        .where(Project.id == project_id)
        .options(selectinload(Project.group))
    )
    query_result = await db_session.execute(query)
    project = query_result.scalar_one()

    return project


@router.post("/")
async def write_project(
    body: WriteProjectRequest,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    new_ids = await upsert_entities(
        db_session=db_session,
        model_cls=Project,
        fields=[body.model_dump()],
        returning_ids=True,
    )

    return new_ids[0]


@router.delete("/{project_id}/")
async def delete_project(
    project_id: str,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    child_query = select(Project).where(project_id == Project.includes.any_())
    query_result = await db_session.execute(child_query)
    has_children = query_result.scalar_one_or_none()

    if has_children:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Невозможно удалить проект, тк у него есть дочерние проекты.",
            },
        )

    delete_query = delete(Project).where(Project.id == project_id)
    await db_session.execute(delete_query)
