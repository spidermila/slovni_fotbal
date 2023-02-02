from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from db_tables import GameLog
from db_tables import Users
from db_tables import Words
# from sqlalchemy.sql import func


class DBManager:
    def __init__(self) -> None:
        self.engine = create_engine('sqlite:///slovni_fotbal.db', echo=False)
        Words.metadata.create_all(self.engine)
        Users.metadata.create_all(self.engine)
        GameLog.metadata.create_all(self.engine)

#  ----- Word Section -----

    def add_word(self, word: str) -> None:
        with Session(self.engine) as session:
            session.add(Words(word_name=word))
            session.commit()

    def word_in_db(self, word: str) -> bool:
        with Session(self.engine) as session:
            if len(
                session.execute(
                    select(Words).where(Words.word_name == word),
                ).all(),
            ) > 0:
                return True
            return False

    def word_count(self) -> int:
        with Session(self.engine) as session:
            result = len(session.execute(select(Words)).all())
        return result

    def word_count_without_some(self, some: set[str]) -> int:
        with Session(self.engine) as session:
            result = len(
                session.execute(
                    select(Words).where(Words.word_name.notin_(some)),
                ).all(),
            )
        return result

    def get_all_words(self) -> list:
        with Session(self.engine) as session:
            result = []
            for row in session.execute(select(Words)).all():
                result.append(row[0].word_name)
        return result

    def get_words_without_some(self, some: set[str]) -> list:
        with Session(self.engine) as session:
            result = []
            for row in session.execute(
                select(Words).where(Words.word_name.notin_(some)),
            ).all():
                result.append(row[0].word_name)
        return result

#  ----- User Section -----

    def user_in_db(self, user_name: str) -> bool:
        with Session(self.engine) as session:
            if len(
                session.execute(
                    select(Users).where(Users.user_name == user_name),
                ).all(),
            ) > 0:
                return True
            return False

    def add_user(self, user_name: str) -> None:
        with Session(self.engine) as session:
            session.add(Users(user_name=user_name))
            session.commit()

    def get_user_id_by_name(self, user_name: str) -> int:
        with Session(self.engine) as session:
            return session.execute(
                select(Users).where(Users.user_name == user_name),
            ).first()[0].user_id

    def add_game(
        self,
        user_name: str,
        user_guessed_count: int,
        game_guessed_count: int,
        user_won: bool,
    ) -> None:
        with Session(self.engine) as session:
            session.add(
                GameLog(
                    user_guessed_count=user_guessed_count,
                    game_guessed_count=game_guessed_count,
                    user_won=user_won,
                    user_id=self.get_user_id_by_name(user_name),
                ),
            )
            session.commit()

    def get_game_stats_by_user(self, user_name: str) -> tuple[int, int]:
        user_id = self.get_user_id_by_name(user_name)
        with Session(self.engine) as session:
            won_games = len(
                session.execute(
                    select(GameLog)
                    .where(GameLog.user_won.is_(True))
                    .where(GameLog.user_id == user_id),
                ).all(),
            )
            lost_games = len(
                session.execute(
                    select(GameLog)
                    .where(GameLog.user_won.is_(False))
                    .where(GameLog.user_id == user_id),
                ).all(),
            )
            return (won_games, lost_games)
