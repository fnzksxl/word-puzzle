import uuid
from sqlalchemy import Column, Integer, VARCHAR, JSON, ForeignKey

from app.database import Base


class BaseMin:
    id = Column(Integer, primary_key=True, index=True)


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
