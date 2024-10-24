import uuid
from sqlalchemy import Column, Integer, VARCHAR, JSON, ForeignKey, DATETIME, func

from app.database import Base


class BaseMin:
    id = Column(Integer, primary_key=True, index=True)


class BaseDate(BaseMin):
    created_at = Column(DATETIME, default=func.now())
    updated_at = Column(DATETIME, default=func.now(), onupdate=func.now())


class WordInfo(BaseMin, Base):
    __tablename__ = "wordinfo"

    word = Column(VARCHAR(5), nullable=False, index=True)
    desc = Column(VARCHAR(200), nullable=False)
    len = Column(Integer, nullable=False)
    pos = Column(VARCHAR(7), nullable=False)


class Puzzle(BaseMin, Base):
    __tablename__ = "puzzle"

    puzzle = Column(JSON, nullable=False)
    name = Column(VARCHAR(50), nullable=False, default=lambda: str(uuid.uuid4()))


class PuzzleAnswer(BaseMin, Base):
    __tablename__ = "puzzleanswer"

    puzzle_id = Column(Integer, ForeignKey("puzzle.id"), nullable=False)
    word_id = Column(Integer, ForeignKey("wordinfo.id"), nullable=False)
    num = Column(Integer, nullable=False)


class User(BaseDate, Base):
    __tablename__ = "user"

    email = Column(VARCHAR(20), unique=True, nullable=False)
    password = Column(VARCHAR(70), nullable=True)
    nickname = Column(VARCHAR(10), nullable=False)
    solved = Column(Integer, default=0)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
