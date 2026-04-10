from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import models, session
from app.core.security import create_access_token, verify_password
from app.schemas.pydantic_models import UserCreate, UserOut
from app.db.crud import get_user_by_username

def register_user(user: UserCreate, db: Session):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = user.password  # Replace with actual hashing
    db_user = models.User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(username: str, password: str, db: Session):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def login_user(username: str, password: str, db: Session):
    user = authenticate_user(username, password, db)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(session.get_db)):
    credentials = oauth2_scheme.verify_token(token)
    if credentials is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = get_user_by_username(db, credentials.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user