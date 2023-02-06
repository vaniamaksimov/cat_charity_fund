from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_before_update,
                                check_for_zero_invested_amount,
                                check_name_allready_exists,
                                get_charity_project_by_id)
from app.core import current_superuser, get_async_session
from app.crud import charity_project_crud
from app.schemas import (CharityProjectCreate, CharityProjectDB,
                         CharityProjectUpdate)
from app.services import make_a_payment

router = APIRouter()


@router.get(
    path='/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.post(
    path='/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_allready_exists(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    await make_a_payment(session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.delete(
    path='/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await get_charity_project_by_id(
        project_id, session
    )
    await check_for_zero_invested_amount(
        charity_project
    )
    charity_project_deleted = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project_deleted


@router.patch(
    path='/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def patch_charity_project(
    project_id: int,
    update_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await get_charity_project_by_id(
        project_id, session
    )
    await check_charity_project_before_update(
        update_data, charity_project, session
    )
    updated_charity_project = await charity_project_crud.update(
        charity_project, update_data, session
    )
    await make_a_payment(session)
    await session.refresh(updated_charity_project)
    return updated_charity_project
