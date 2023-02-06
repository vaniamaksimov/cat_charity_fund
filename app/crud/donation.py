from typing import List

from sqlalchemy import select
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Donation, User
from app.schemas import DonationCreate, DonationUpdate


class CRUDDonation(CRUDBase[Donation,
                            DonationCreate,
                            DonationUpdate]):
    async def get_user_donations(
        self,
        user: User,
        session: AsyncSession
    ) -> List[Donation]:
        donations_db: Result = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        donations_db = donations_db.scalars().all()
        return donations_db


donation_crud = CRUDDonation(Donation)
