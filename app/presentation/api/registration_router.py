from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import UserModel
from app.infrastructure.database.session import get_db
from app.presentation.schemas.registration import (
    AthleteRegistration,
    CoordinatorRegistration,
    TrainerRegistration,
)
from app.application.use_cases.registration import RegistrationUseCases
from app.presentation.schemas.user import UserRead

router = APIRouter(prefix="/auth/register", tags=["Auth"])


@router.post("/athlete", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_athlete(
    data: AthleteRegistration,
    session: AsyncSession = Depends(get_db),
) -> UserModel:
    return await RegistrationUseCases(session).athlete(data)


@router.post("/trainer", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_trainer(
    data: TrainerRegistration,
    session: AsyncSession = Depends(get_db),
) -> UserModel:
    return await RegistrationUseCases(session).trainer(data)


@router.post(
    "/coordinator", response_model=UserRead, status_code=status.HTTP_201_CREATED
)
async def register_coordinator(
    data: CoordinatorRegistration,
    session: AsyncSession = Depends(get_db),
) -> UserModel:
    return await RegistrationUseCases(session).coordinator(data)
