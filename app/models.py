from sqlalchemy import Column, Integer, VARCHAR

from app.database import Base


class BaseMin:
    id = Column(Integer, primary_key=True, index=True)


class WordInfo(BaseMin, Base):
    __tablename__ = "wordinfo"

    word = Column(VARCHAR(5), nullable=False)
    desc = Column(VARCHAR(200), nullable=False)
    len = Column(Integer, nullable=False, index=True)
    pos = Column(VARCHAR(7), nullable=False)
