from sqlalchemy import select, literal, any_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from db.models import Variable
from db.models.project import Project
from schemas.common import IdNameSchema
from schemas.project import ProjectSchema, ShortProjectSchema
from schemas.variable import VariableSchema


async def get_project_variables(
    project_id: str,
    db_session: AsyncSession,
) -> list[VariableSchema]:
    recursive_anchor = (
        select(
            Variable,
            Project.includes,
            Project.name.label("project_name"),
            literal(0).label("level"),
        )
        .select_from(Project)
        .join(Variable, isouter=True)
        .where(Project.id == project_id)
        .cte("variables_recursive", recursive=True)
    )

    variable_alias = aliased(Variable, name="vr")
    project_alias = aliased(Project, name="pr")

    recursive_body = (
        select(
            variable_alias,
            project_alias.includes,
            project_alias.name.label("project_name"),
            (recursive_anchor.c.level + 1).label("level"),
        )
        .select_from(project_alias)
        .join(variable_alias, isouter=True)
        .join(recursive_anchor, project_alias.id == any_(recursive_anchor.c.includes))
        .distinct(variable_alias.name)
        .order_by(
            variable_alias.name,
            func.array_position(
                recursive_anchor.c.includes, variable_alias.project_id
            ).desc(),
        )
        .subquery()
    )

    recursive_cte = recursive_anchor.union_all(select(recursive_body))

    query = (
        select(recursive_cte)
        .distinct(recursive_cte.c.name)
        .where(recursive_cte.c.id.is_not(None))
        .order_by(recursive_cte.c.name, recursive_cte.c.level)
    )

    query_result = await db_session.execute(query)
    items = query_result.all()

    return [
        VariableSchema(
            id=item.id,
            name=item.name,
            value=item.value,
            is_secret=item.is_secret,
            project=IdNameSchema(id=item.project_id, name=item.project_name),
        )
        for item in items
    ]


async def get_available_project_parents(
    project_id: str,
    db_session: AsyncSession,
    filter_selected: bool = True,
) -> list[ShortProjectSchema]:
    recursive_anchor = (
        select(Project.id, Project.includes)
        .where(Project.id == project_id)
        .cte("projects_recursive", recursive=True)
    )

    project_alias = aliased(Project, name="pr")

    recursive_body = select(project_alias.id, project_alias.includes).join(
        recursive_anchor,
        recursive_anchor.c.id == any_(project_alias.includes),
    )

    recursive_cte = recursive_anchor.union_all(recursive_body)

    exists_query = (
        select(1)
        .select_from(recursive_cte)
        .where(Project.id == recursive_cte.c.id)
        .exists()
    )

    query = (
        select(Project)
        .where(~exists_query)
        .order_by(Project.group_id, func.array_length(Project.includes, 1).desc())
    )

    if filter_selected:
        query = query.where(project_id != any_(Project.includes))

    query_result = await db_session.execute(query)
    projects = query_result.scalars().all()

    return [ProjectSchema.model_validate(project) for project in projects]
