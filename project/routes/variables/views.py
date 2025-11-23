from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Variable
from db.session import get_db_session
from helpers.db import upsert_entities
from helpers.project import get_project_variables
from routes.variables.schems import WriteVariableResponse, VariableBulkCreateRequest
from schemas.variable import VariableSchema

router = APIRouter()


@router.get("/")
async def get_project_variables_route(
    project_id: Annotated[str, Query()],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return await get_project_variables(project_id, db_session)


@router.get("/{variable_id}/", response_model=VariableSchema)
async def retrieve_variable(
    variable_id: UUID,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    query = (
        select(Variable)
        .where(Variable.id == variable_id)
        .options(selectinload(Variable.project))
    )
    query_result = await db_session.execute(query)
    variable = query_result.scalar_one_or_none()

    return variable


@router.post("/")
async def write_variable(
    body: WriteVariableResponse,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    await upsert_entities(
        db_session=db_session,
        model_cls=Variable,
        fields=[body.model_dump(exclude_none=True)],
    )


@router.delete("/{variable_id}/")
async def delete_variable(
    variable_id: str,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    query = delete(Variable).where(Variable.id == variable_id)
    await db_session.execute(query)


@router.post("/bulk_create/")
async def bulk_write_variables(
    body: VariableBulkCreateRequest,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    variables_lines = body.variables_text.splitlines()
    variables_data = []
    
    for line in variables_lines:
        if "=" not in line:
            continue
        name, value = line.split("=", 1)
        variables_data.append(
            {
                "name": name.strip(),
                "value": value.strip(),
                "project_id": body.project_id,
            }
        )

    await upsert_entities(
        db_session=db_session,
        model_cls=Variable,
        fields=variables_data,
    )
