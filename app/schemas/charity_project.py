from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100,)
    description: str = Field(..., min_length=1)

    @validator('name', 'description',)
    def not_null(cls, field):
        if field is None:
            raise ValueError('Cant be null')
        return field


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field('', min_length=1, max_length=100,)
    description: Optional[str] = Field('', min_length=1)
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
