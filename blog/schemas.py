from pydantic import BaseModel


class CreateBlog(BaseModel):
    title:str
    body:str
    published:bool

class Blog(BaseModel):
    id:int
    title:str
    body:str
    published:bool
    user_id:int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    id:int
    name:str | None=None
    username:str
    class Config:
        from_attributes = True


class User(UserBase):
    username:str
    password:str
    class Config:
        from_attributes = True

class LoginUser(BaseModel):
    username:str
    password:str


class ShowBlog(Blog):
    creator:UserBase

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None