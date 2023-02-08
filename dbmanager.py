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
            for word in session.execute(select(Words)).scalars().all():
                result.append(word.word_name)
        return result

    def get_words_without_some(self, some: set[str]) -> list:
        with Session(self.engine) as session:
            result = []
            for word in session.execute(
                select(Words).where(Words.word_name.notin_(some)),
            ).scalars().all():
                result.append(word.word_name)
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
            user = session.execute(
                select(Users).where(Users.user_name == user_name),
            ).scalar()
            if user:
                return user.user_id
            else:
                raise AssertionError(f'User {user_name} not found.')

    def get_user_names(self) -> list[str]:
        with Session(self.engine) as session:
            users = session.execute(select(Users)).scalars().all()
            names = []
            if len(users) > 0:
                for user in users:
                    names.append(user.user_name)
        return names

    def rename_user(self, user_name: str, new_user_name: str) -> None:
        with Session(self.engine) as session:
            user = session.execute(
                select(Users).where(Users.user_name == user_name),
            ).scalars().one()
            user.user_name = new_user_name
            session.commit()

    def delete_user(self, user_name: str) -> None:
        with Session(self.engine) as session:
            user = session.execute(
                select(Users).where(Users.user_name == user_name),
            ).scalars().one()
            session.delete(user)
            session.commit()

#  ----- GameLog Section -----

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

    def get_all_game_stats(self) -> dict[str, tuple[int, int]]:
        result = {}
        for user_name in self.get_user_names():
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
            result[user_name] = (won_games, lost_games)
        return result

    def get_game_details_by_user(self, user_name: str) -> list[list]:
        user_id = self.get_user_id_by_name(user_name)
        results = []
        with Session(self.engine) as session:
            games = session.execute(
                select(GameLog)
                .where(GameLog.user_id == user_id),
            ).scalars().all()
            for game in games:
                if game.user_won:
                    won = 'won'
                else:
                    won = 'lost'
                results.append(
                    [game.user_guessed_count, game.game_guessed_count, won],
                )
            return results

    def delete_games_by_userid(self, user_id: int) -> None:
        with Session(self.engine) as session:
            games = session.execute(
                select(GameLog)
                .where(GameLog.user_id == user_id),
            ).scalars().all()
            for game in games:
                session.delete(game)
            session.commit()
