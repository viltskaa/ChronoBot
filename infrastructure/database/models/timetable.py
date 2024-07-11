from .base import Base, TimestampMixin, TableNameMixin
from sqlalchemy.orm import Mapped
from datetime import datetime


class TimeTable(Base, TableNameMixin):
    article: Mapped[str]
    time_start: Mapped[datetime]
    price: Mapped[float]

    def __repr__(self):
        return f"<TimeTable {self.article} с {self.time_start} цена {self.price}>"
