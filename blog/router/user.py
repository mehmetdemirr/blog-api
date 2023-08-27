from typing import List
from fastapi import APIRouter,HTTPException,Depends,status
from blog.schemas import User,UserBase
from blog.database import get_db
from sqlalchemy.orm import Session
from blog.password_hashed import get_password_hash
import blog.models as models

router=APIRouter()

@router.post("/",response_model=UserBase)
def create_user(user:User,db:Session=Depends(get_db)):
    u=db.query(models.User).filter(models.User.username==user.username).first()
    if u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="username bulunuyor başka bir username kullan")
    hashed=get_password_hash(user.password)
    usr=models.User(name=user.name,username=user.username,password=hashed)
    db.add(usr)
    db.commit()
    db.refresh(usr)
    return usr

@router.get("/",response_model=List[UserBase])
def get_users(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users

@router.get("/{id}",response_model=UserBase)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id== id).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id}'li user bulunamadı")
