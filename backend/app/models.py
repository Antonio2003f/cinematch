from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    year = Column(Integer)
    director = Column(String(255))
    genre = Column(String(255))
    rating = Column(Float)
    plot = Column(Text)
    poster_url = Column(String(500))
