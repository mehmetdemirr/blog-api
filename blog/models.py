from sqlalchemy import Column,Integer,Text,Boolean,String,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Blog(Base):
    __tablename__="blogs"
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    title=Column(String)
    body=Column(Text)
    published=Column(Boolean,default=True)
    user_id=Column(Integer,ForeignKey("users.id"))

    creator = relationship("User", back_populates="blogs")

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String)
    username=Column(String,unique=True)
    password=Column(String)

    blogs=relationship("Blog",back_populates="creator")