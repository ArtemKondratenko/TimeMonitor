from datetime import timedelta

from pydantic import BaseModel, ConfigDict

from model.base import DatabaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from model.request import RequestInDB

class MonitorInDB(DatabaseModel):
    __tablename__ = "MonitorInDB"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        init=False
    )

    url: Mapped[str]
    email: Mapped[str]
    interval: Mapped[timedelta]
    tg_api_token: Mapped[str]
    tg_chat_id: Mapped[int]
    requests: Mapped[list["RequestInDB"]] = relationship("RequestInDB", back_populates='monitor', init = False, cascade="all, delete")
    is_pause: Mapped[bool] = mapped_column(default=False)


class CreateMonitor(BaseModel):
    url: str
    email: str
    interval: timedelta
    tg_api_token: str
    tg_chat_id: int



class Monitor(BaseModel):
    id: int
    url: str
    email: str
    is_pause: bool
    interval: timedelta
    tg_api_token: str
    tg_chat_id: int


    model_config = ConfigDict(from_attributes=True)


class UpdateMonitor(BaseModel):
    url: str|None = None
    email: str|None = None
    is_pause: bool|None = None
    interval: timedelta|None = None
    tg_api_token: str|None = None
    tg_chat_id: int|None = None