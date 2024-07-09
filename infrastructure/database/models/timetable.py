from .base import Base, TimestampMixin, TableNameMixin, int_pk_with_incr
from typing import Optional

from sqlalchemy import INT, FLOAT, TIME
from sqlalchemy.orm import Mapped, mapped_column


class TimeTable(Base, TableNameMixin):
    id: Mapped[int_pk_with_incr]
    article: Mapped[int] = mapped_column(INT, nullable=False)
    time_start: Mapped[TIME] = mapped_column(TIME, nullable=False)
    price: Mapped[FLOAT] = mapped_column(FLOAT, nullable=False)

    def __repr__(self):
        return f"<TimeTable {self.article} с {self.time_start} цена {self.price}>"
