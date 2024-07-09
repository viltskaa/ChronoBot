from typing import Optional

from base import Base, TimestampMixin, TableNameMixin, int_pk
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column, Session, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class Worker(Base, TableNameMixin):
    id: Mapped[int_pk]
    name: Mapped[str]

    def __repr__(self):
        return f"<Worker : name : {self.name}>"


class TimeTable(Base, TableNameMixin):
    id: Mapped[int_pk]
    article: Mapped[int]
    time_start: Mapped[datetime]
    price: Mapped[float]

    def __repr__(self):
        return f"<TimeTable {self.article} с {self.time_start} цена {self.price}>"


sync_engine = create_engine(
    url=r'sqlite:///D:\\tsukanova\\work\\ChronoBot\\db_test\\test.db',
    echo=True
)

async_engine = create_engine(
    url='sqlite:///D:/tsukanova/work/ChronoBot/test.db',
    echo=True
)

session_factory = sessionmaker(bind=sync_engine)
async_sessions_factory = async_sessionmaker()


def create_tables():
    Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)


def insert_data():
    worker_1 = Worker(name="worker1")
    worker_2 = Worker(name="worker2")

    with session_factory() as session:
        session.add_all([worker_1, worker_2])
        session.commit()


create_tables()
