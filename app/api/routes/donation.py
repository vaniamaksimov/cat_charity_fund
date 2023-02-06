from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import current_superuser, current_user, get_async_session
from app.crud import donation_crud
from app.models import User
from app.schemas import DonationCreate, DonationDB
from app.services import make_a_payment

router = APIRouter()


@router.get(
    path='/',
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session=Depends(get_async_session)
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    path='/',
    response_model=DonationDB,
    response_model_exclude={
        'user_id', 'invested_amount', 'fully_invested', 'close_date',
    },
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    donation_db = await donation_crud.create(donation, session, user)
    await make_a_payment(session)
    await session.refresh(donation_db)
    return donation_db


@router.get(
    path='/my',
    response_model=List[DonationDB],
    response_model_exclude={
        'user_id', 'close_date',
        'fully_invested', 'invested_amount',
        'close_date'
    }
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_user_donations(user, session)
    return donations
