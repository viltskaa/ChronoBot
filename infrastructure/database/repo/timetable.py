from sqlalchemy import select
from infrastructure.database.models.timetable import TimeTable
from datetime import datetime
from infrastructure.database.repo.base import BaseRepo


class TimeTableRepo(BaseRepo):
    async def create_time(self,
                          article: str,
                          time_start: datetime,
                          price: float):

        self.session.add(TimeTable(article=article,
                                   time_start=time_start,
                                   price=price))
        await self.session.commit()

    async def update_time(self,
                          id_: int,
                          time_start: datetime):
        time = await self.session.get(TimeTable, id_)
        time.time_start = time_start

        await self.session.commit()

    async def update_price(self,
                           id_: int,
                           price: float):
        time = await self.session.get(TimeTable, id_)
        time.price = price

        await self.session.commit()

    async def delete_time(self, id_: int):
        time = await self.session.get(TimeTable, id_)
        await self.session.delete(time)
        await self.session.commit()

    async def get_all_timetable(self) -> list[TimeTable]:
        result = await self.session.execute(select(TimeTable))
        return result.scalars().all()

    async def get_time_by_article(self, article: str) -> TimeTable:
        # TODO доделать
        pass
