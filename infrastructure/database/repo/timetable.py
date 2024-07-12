from typing import Optional

from sqlalchemy import select
from infrastructure.database.models.timetable import TimeTable
from datetime import datetime
from infrastructure.database.repo.base import BaseRepo


class TimeTableRepo(BaseRepo):
    async def create_time(self,
                          article: str,
                          time_start: datetime,
                          price: float):
        time = TimeTable(article, time_start, price)

        self.session.add(time)
        await self.session.commit()

    async def update_time(self,
                          article: str,
                          time_start: Optional[datetime],
                          price: Optional[float]):
        time = self.session.get(TimeTable, article)
        if time_start is not None:
            time.time_start = time_start
        if price is not None:
            time.price = price

        await self.session.commit()

    async def delete_time(self, article: str):
        time = self.session.get(TimeTable, article)
        await self.session.delete(time)
        await self.session.commit()

    async def get_all_timetable(self) -> list[TimeTable]:
        result = await self.session.execute(select(TimeTable))
        return result.scalars().all()

    async def get_time_by_article(self, article: str) -> TimeTable:
        return self.session.get(TimeTable, article)
