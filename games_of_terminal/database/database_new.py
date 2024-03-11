# -------------------------------------
# New unfinished version of current DB logic, but with SQLAlchemy lib
# -------------------------------------


from games_of_terminal.constants import ITEMS
from games_of_terminal.database.constants import DB_FILENAME
from games_of_terminal.database.models import (
    Base, GameModel, GameDataModel, AchievementModel,
)

from os import path
from pathlib import Path
from sqlalchemy import (
    create_engine, ForeignKey, text,
    select, insert, update, inspect, and_,
)
from sqlalchemy.orm import sessionmaker


BASE_DIR = Path(__file__).parents[1]
DB_FILEPATH = str(path.join(BASE_DIR, DB_FILENAME))
ENGINE_URL = f'sqlite:////{DB_FILEPATH}'

engine = create_engine(
    url=ENGINE_URL,
    # echo=True,
)
session_factory = sessionmaker(engine)


def create_and_fill_db_tables():
    if not inspect(engine).has_table('game'):
        GameModel.metadata.create_all(engine)
        # fill_game_table()

    if not inspect(engine).has_table('game_data'):
        GameDataModel.metadata.create_all(engine)
        # fill_game_data_table()

    if not inspect(engine).has_table('achievement'):
        AchievementModel.metadata.create_all(engine)
        # fill_achievement_table()


# def fill_game_table():
#     with session_factory() as session:
#         session.execute(insert(GameModel), [
#             {'name': 'SomeGameName'},
#         ])
#         session.commit()

def get_game_id_by_game_name(game_name, session):
    get_game_id_query = (
        select(GameModel.id_game)
        .filter_by(name=game_name)
    )
    data = session.execute(get_game_id_query)
    game_id = data.one()[0]

    return game_id


def get_game_settings(game_name):
    with session_factory() as session:
        game_id = get_game_id_by_game_name(game_name, session)

        get_game_settings_query = (
            select(GameDataModel.name, GameDataModel.value)
            .select_from(GameDataModel)
            .filter(and_(
                GameDataModel.id_game == game_id,
                GameDataModel.data_type == 'settings'
            ))
        )
        settings_data = session.execute(get_game_settings_query).all()

    return settings_data


def get_game_stat_value(*args, **kwargs):
    pass


def update_game_stat(*args, **kwargs):
    pass


def get_games_statistic(*args, **kwargs):
    pass


def get_all_achievements(*args, **kwargs):
    pass


def get_all_settings(*args, **kwargs):
    pass


def reset_all_user_data(*args, **kwargs):
    pass


def get_username(*args, **kwargs):
    pass


def save_username(*args, **kwargs):
    pass


def unlock_achievement(*args, **kwargs):
    pass


def save_selected_option(*args, **kwargs):
    pass


# def create_tables():
#     Base.metadata.create_all(engine)
#
#
# def drop_tables():
#     Base.metadata.drop_all(engine)


# def insert_games():
#     new_games = [
#         GameModel(name='Meta'),
#         GameModel(name='Teta'),
#     ]
#
#     with session_factory() as session:
#         session.add_all(new_games)
#         session.commit()
#
#
# def select_games():
#     with session_factory() as session:
#         query = select(GameModel)
#         data = session.execute(query)
#
#         print(data.scalars().all())
#
#
# def update_game(game_id: int = 2, new_game_name: str = 'Hehe'):
#     with session_factory() as session:
#         game = session.get(GameModel, game_id)
#         game.name = new_game_name
#         session.commit()
