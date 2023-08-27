from fastapi import APIRouter,HTTPException,Depends,status ,Response
from ..schemas import Blog,ShowBlog,CreateBlog,UserBase
from ..database import get_db
from sqlalchemy.orm import Session
import blog.models as models
from ..oauth2 import get_current_user

router=APIRouter()

@router.post("/",response_model=Blog)
def create(blog:CreateBlog,db:Session=Depends(get_db),current_user:UserBase=Depends(get_current_user)):
    print(f"current user :{current_user.id}")
    new_blog=models.Blog(title=blog.title,body=blog.body,published=blog.published,user_id=current_user.id) 
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/",response_model=list[ShowBlog])
def get_blogs(db:Session=Depends(get_db),current_user:UserBase=Depends(get_current_user)):
    return db.query(models.Blog).all()

@router.get("/{id}",response_model=ShowBlog)
def get_blog(id:int,response:Response,db:Session=Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id==id).first()
    if blog:
        return blog
    else :
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"message":"yok"}
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id}'li blog bulunmadı")

@router.delete("/{id}")
def delete_blog(id:int,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if blog.first():
         blog.delete(synchronize_session=False)
         db.commit()
         return {"message":f"{id}'li blog silinidi"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id}'li blog bulunamadı")

@router.put("/{id}",response_model=Blog)
def blog_update(id:int,blog:Blog,db:Session=Depends(get_db)):
    b=db.query(models.Blog).filter(models.Blog.id==id)
    if b.first():
        b.update(values={"title":blog.title,"body":blog.body,"published":blog.published},synchronize_session=False)
        db.commit()
        return b.first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id}'li blog bulunamadı")
    
