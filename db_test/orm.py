from base import Base
from db import sync_engine, async_engine, Worker, session_factory, async_sessions_factory
from sqlalchemy import select


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
