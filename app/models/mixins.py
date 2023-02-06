from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class CreateAndCloseDateMixin:
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None, nullable=True)


@declarative_mixin
class InvestedMixin(CreateAndCloseDateMixin):
    full_amount = Column(Integer, nullable=False,)
    fully_invested = Column(Boolean, default=False, nullable=False, index=True)
    invested_amount = Column(Integer, default=0, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "full_amount > 0", name='check_full_amount_positive'
            ),
        CheckConstraint(
            "invested_amount >= 0", name='check_pos_invested_amount'
            ),
    )

    def close(self):
        self.invested_amount = self.full_amount
        self.fully_invested = True
        self.close_date = datetime.now()
