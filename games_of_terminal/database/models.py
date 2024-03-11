from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped, mapped_column,
)

from typing import Annotated
from enum import Enum


int_pk = Annotated[int, mapped_column(primary_key=True)]
id_game_fk = Annotated[int, mapped_column(
    ForeignKey('game.id_game', ondelete='CASCADE')
)]


class Base(DeclarativeBase):
    pass


class GameModel(Base):
    __tablename__ = 'game'

    id_game: Mapped[int_pk]
    name: Mapped[str]


class GameDataModel(Base):
    __tablename__ = 'game_data'

    id_game_data: Mapped[int_pk]
    id_game: Mapped[id_game_fk]
    data_type: Mapped[str]
    name: Mapped[str]
    value: Mapped[str | None]


class AchievementStatus(Enum):
    locked = 'locked'
    unlocked = 'unlocked'


class AchievementModel(Base):
    __tablename__ = 'achievement'

    id_achievement: Mapped[int_pk]
    id_game: Mapped[id_game_fk]
    name: Mapped[str] = mapped_column(unique=True)
    status: Mapped[AchievementStatus] = mapped_column(
        default=AchievementStatus.locked
    )
    description: Mapped[str]
    date_received: Mapped[str | None]
