#  from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Words(Base):
    __tablename__ = 'words'
    #  word_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word_name: Mapped[str] = mapped_column(String(50), primary_key=True)

    def __repr__(self) -> str:
        return f'Words: {self.word_name=}'
