from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    date_created = Column(TIMESTAMP, server_default=func.now())

    posts = relationship("Post", back_populates="user", cascade="all, delete")


class Category(Base):
    __tablename__ = "categories"

    id_category = Column(Integer, primary_key=True, index=True)
    name_category = Column(String(100), nullable=False)
    description_category = Column(String(255))


class Post(Base):
    __tablename__ = "posts"

    id_post = Column(Integer, primary_key=True, index=True)
    message = Column(String(300), nullable=False)
    likes_count = Column(Integer, default=0)

    id_category = Column(Integer, ForeignKey("categories.id_category"))
    id_user = Column(Integer, ForeignKey("users.id_user"))

    user = relationship("User", back_populates="posts")
    comments = relationship("Comments", back_populates="post", cascade="all, delete")


class Comments(Base):
    __tablename__ = "comments"

    id_comments = Column(Integer, primary_key=True, index=True)
    comment = Column(String(200), nullable=False)

    id_post = Column(Integer, ForeignKey("posts.id_post"))
    id_user = Column(Integer, ForeignKey("users.id_user"))

    post = relationship("Post", back_populates="comments")