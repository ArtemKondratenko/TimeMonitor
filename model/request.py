from datetime import timedelta
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from database import DatabaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from model.monitor import MonitorInDB


class RequestInDB(DatabaseModel):
    __tablename__ = "RequestInDB"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    url: Mapped[str]
    time: Mapped[timedelta]
    status_code: Mapped[int]
    monitor_id: Mapped[int] = mapped_column(ForeignKey("MonitorInDB.id"))
    monitor: Mapped["MonitorInDB"] = relationship(back_populates="requests", init=False)


class CreateRequest(BaseModel):
    url: str
    time: timedelta
    status_code: int


class Request(BaseModel):
    id: int
    url: str
    time: timedelta
    status_code: int

    model_config = ConfigDict(from_attributes=True)
