from .base import Base, TimestampMixin, TableNameMixin
from typing import Optional

from sqlalchemy import BIGINT, INT, FLOAT, TIME
from sqlalchemy.orm import Mapped, mapped_column


class TimeTable(Base):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    article: Mapped[int] = mapped_column(INT, nullable=False)
    time_start: Mapped[TIME] = mapped_column(TIME, nullable=False)
    price: Mapped[FLOAT] = mapped_column(FLOAT, nullable=False)

    def __repr__(self):
        return f"<TimeTable {self.article} с {self.time_start} цена {self.price}>"
