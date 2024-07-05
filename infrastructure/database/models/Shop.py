from typing import Optional

from sqlalchemy import BIGINT
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin


class Shop(Base, TimestampMixin, TableNameMixin):
    shop_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    name: Mapped[Optional[str]] = mapped_column(String(64), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    api_key: Mapped[Optional[str]] = mapped_column(String(256), nullable=False)

    def __repr__(self):
        return f"<Shop {self.name} {self.shop_id}>"
