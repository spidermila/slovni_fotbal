from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Words(Base):
    __tablename__ = 'words'
    #  word_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word_name: Mapped[str] = mapped_column(String(50), primary_key=True)

    def __repr__(self) -> str:
        return f'Words: {self.word_name=}'


class Users(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30))

    games: Mapped[list['GameLog']] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return f'Users: {self.user_id=}, {self.user_name=}'


class GameLog(Base):
    __tablename__ = 'gamelog'
    game_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_guessed_count: Mapped[int] = mapped_column(Integer)
    game_guessed_count: Mapped[int] = mapped_column(Integer)
    user_won: Mapped[bool] = mapped_column(Boolean)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))

    user: Mapped['Users'] = relationship(back_populates='games')

    def __repr__(self) -> str:
        return f'GameLog: {self.game_id=}, {self.user_id=}'
