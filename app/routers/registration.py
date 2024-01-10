from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.orm import Session

from ..internal import models
from ..routers.auth import hash_password
from ..internal.database import get_db

router = APIRouter()


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    scopes: list[str]
    disabled: bool


@router.post("/register/", status_code=201)
async def register_user(user: User, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = hash_password(user.password)
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    new_user.set_scope(user.scopes)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
