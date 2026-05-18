from pydantic import BaseModel

# USER
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# CATEGORY
class CategoryCreate(BaseModel):
    name_category: str
    description_category: str

# POST
class PostCreate(BaseModel):
    message: str
    likes_count: int
    id_category: int
    id_user: int

# COMMENT
class CommentCreate(BaseModel):
    comment: str
    id_post: int
    id_user: int

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    username: str
    email: str