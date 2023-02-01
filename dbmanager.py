from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from db_tables import Words


class DBManager:
    def __init__(self) -> None:
        self.engine = create_engine('sqlite:///slovni_fotbal.db', echo=False)
        Words.metadata.create_all(self.engine)

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
