from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

import models
from auth import fake_users_db, fake_hash_password, UserInDB, User, get_current_active_user
from database import get_db
from registration import router as registration_router

from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()
app.include_router(registration_router)


@app.get("/")
async def root():
    return {"message": "Welcome to your game library!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# Pydantic model for game data input
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


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


# Dependency to get the current user's scopes
async def get_user_scopes(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user.scopes


# User access control based on scopes
async def check_user_access(scopes: list = Depends(get_user_scopes)):
    required_scopes = ["write"]  # Specify required scopes for specific endpoints
    for scope in required_scopes:
        if scope not in scopes:
            raise HTTPException(status_code=401, detail="Insufficient scope")


# @app.post("/games/", status_code=status.HTTP_201_CREATED, response_model=Game)
@app.post("/games/", status_code=status.HTTP_201_CREATED, response_model=Game,
          dependencies=[Depends(check_user_access)])
async def create_game(game: Game, db: Session = Depends(get_db)):
    new_game = models.Game(
        title=game.title,
        platform=game.platform,
        genre=game.genre,
        cover_image=game.cover_image,
        screenshots=game.screenshots,
        video_links=game.video_links
    )

    db_item = db.query(models.Game).filter(models.Game.title == new_game.title).first()
    if db_item is not None:
        raise HTTPException(status_code=400, detail="Game already exists")
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


# Retrieve all games
@app.get("/games/", response_model=list[Game])
async def get_games(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Game).offset(skip).limit(limit).all()


# Retrieve a single game by ID
@app.get("/games/{game_id}", response_model=Game)
async def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


# Update a game by ID
@app.put("/games/{game_id}", response_model=Game)
async def update_game(game_id: int, game: Game, db: Session = Depends(get_db)):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    for field, value in game.dict(exclude_unset=True).items():
        setattr(db_game, field, value)
    db.commit()
    db.refresh(db_game)
    return db_game


# Delete a game by ID
@app.delete("/games/{game_id}", response_model=Game)
async def delete_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    db.delete(game)
    db.commit()
    return game
