from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from prod_level import oAuth2, utils
from prod_level.database import get_db
from prod_level import models

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials : OAuth2PasswordRequestForm = Depends(),db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid credentials")

    # create access token
    access_token = oAuth2.create_access_token(data={"user_id": user.id})
    return {"message": "Login successful", "access_token": access_token}