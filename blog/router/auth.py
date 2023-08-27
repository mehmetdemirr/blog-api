from fastapi import APIRouter,Depends,HTTPException,status
from ..database import get_db
from .. import schemas
from .. import models
from ..password_hashed import verify_password
from sqlalchemy.orm import Session
from ..oauth2 import create_access_token
from datetime import timedelta
from fastapi.security.oauth2 import  OAuth2PasswordRequestForm

router=APIRouter()

@router.post("/login")
def login(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    u=db.query(models.User).filter(models.User.username==user.username).first()
    if not u:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Kullanıcı yok")
    if not verify_password(user.password,u.password):
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Şifre yanlış")
    
    access_token = create_access_token(
        data={"id": u.id,}
    )
    return {"access_token": access_token, "token_type": "bearer"}
        
