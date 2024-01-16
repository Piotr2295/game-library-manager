import json

from sqlalchemy import Column, Integer, String, Text, JSON, BOOLEAN
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


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    scopes = Column(JSON)
    disabled = Column(BOOLEAN, nullable=True, default=False)

    def set_scope(self, scope_list):
        self.scopes = json.dumps(scope_list)

    def get_scope(self):
        return json.loads(self.scopes) if self.scopes else []