from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    platform = Column(String)
    genre = Column(String)
    cover_image = Column(String)
    screenshots = Column(Text)
    video_links = Column(Text)

    def __repr__(self):
        return f"<Game name={self.title}>"
