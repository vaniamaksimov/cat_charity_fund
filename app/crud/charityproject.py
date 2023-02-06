from sqlalchemy import select
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectCreate, CharityProjectUpdate


class CRUDCharityProject(CRUDBase[CharityProject,
                                  CharityProjectCreate,
                                  CharityProjectUpdate]):
    async def get_by_name(
        self, name: str, session: AsyncSession
    ) -> CharityProject:
        charity_project: Result = await session.execute(
            select(self.model).where(
                self.model.name == name,
            )
        )
        charity_project = charity_project.scalars().first()
        return charity_project


charity_project_crud = CRUDCharityProject(CharityProject)
