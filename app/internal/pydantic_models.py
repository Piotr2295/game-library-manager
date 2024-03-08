from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class User(BaseModel):
    username: str
    email: str | None = None
    scopes: list[str]
    disabled: bool


class UserInDB(User):
    hashed_password: str


class RegistrationUser(BaseModel):
    id: int
    username: str
    email: str
    password: str
    scopes: list[str]
    disabled: bool



class Game(BaseModel):
    id: int
    title: str
    platform: str
    genre: str
    cover_image: str = None
    screenshots: str = None
    video_links: str = None

    class Config:
        orm_mode = True
