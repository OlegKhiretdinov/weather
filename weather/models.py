import datetime
import uuid

from sqlalchemy import DateTime, func, text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from weather.database import Base


class Location(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]


class User(Base):
    __tablename__ = "users"

    uid: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=func.now())


class SearchHistory(Base):
    __tablename__ = "search_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID]
    location_id: Mapped[int]
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=func.now())
