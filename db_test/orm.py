from typing import Optional

from base import Base
from db import sync_engine, async_engine, Worker, session_factory, async_sessions_factory, TimeTable
from sqlalchemy import select
from datetime import datetime


class SyncOrmWorker:
    @staticmethod
    def create_tables():
        Base.metadata.drop_all(bind=sync_engine)
        Base.metadata.create_all(bind=sync_engine)

    @staticmethod
    def insert_workers():
        worker_1 = Worker(id=1, name="worker1")
        worker_2 = Worker(id=2, name="worker2")

        with session_factory() as session:
            session.add_all([worker_1, worker_2])
            session.commit()

    @staticmethod
    def insert_worker(worker_id: int, name: str):
        worker = Worker(id=worker_id, name=name)

        with session_factory() as session:
            session.add_all(worker)
            session.commit()

    @staticmethod
    def get_workers() -> list[Worker]:
        with session_factory() as session:
            return session.execute(select(Worker)).scalars().all()

    @staticmethod
    def get_worker_by_id(worker_id: int) -> Worker:
        with session_factory() as session:
            return session.get(Worker, worker_id)

    @staticmethod
    def update_worker(worker_id: int, new_name: str):
        with session_factory() as session:
            worker = session.get(Worker, worker_id)
            worker.name = new_name
            session.commit()


class AsyncOrm:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def get_all() -> list[TimeTable]:
        async with async_sessions_factory() as session:
            result = await session.execute(select(TimeTable))
            return result.scalars().all()

    @staticmethod
    async def insert_time(id_: int, article: str, time_start: datetime, price: float):
        async with async_sessions_factory() as session:
            time = TimeTable(id=id_, article=article, time_start=time_start, price=price)
            session.add(TimeTable, time)
            session.commit()

    @staticmethod
    async def update_time(id_: int, time_start: Optional[datetime], price: Optional[float]):
        async with async_sessions_factory() as session:
            time = session.get(TimeTable, id_)

            if time_start is not None:
                time.time_start = time_start
            if price is not None:
                time.price = price

            session.commit()
