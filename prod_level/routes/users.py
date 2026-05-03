from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from prod_level import schemas, utils
from prod_level.database import get_db
from prod_level.models import User
from prod_level.schemas import UserCreate, UserOut  

router = APIRouter()

@router.post("/users", response_model=UserOut)
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
    # hash the password - user.password
    # user_dict = user.model_dump()
    hashed_password = utils.hash(user.password)
    new_user = User(**user.model_dump())
    new_user.password = hashed_password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}", response_model=UserOut)
def get_user(id : int, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user