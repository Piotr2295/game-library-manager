from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends, status, Security

import models
from auth import User, get_current_active_user, router as login_router
from database import get_db
from registration import router as registration_router

from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()
app.include_router(registration_router)
app.include_router(login_router)


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


@app.post("/games/", status_code=status.HTTP_201_CREATED, response_model=Game)
async def create_game(
        game: Game,
        current_user: Annotated[User, Security(get_current_active_user, scopes=["write"])],
        db: Session = Depends(get_db)
):
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
