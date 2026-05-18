from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Red Social")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# conexión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# USERS
@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    updated_user = crud.update_user(
        db,
        user_id,
        user
    )
    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    return {
        "message": "Usuario actualizado",
        "user": {
            "id": updated_user.id_user,
            "username": updated_user.username,
            "email": updated_user.email
        }
    }

@app.post("/login/")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.login_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {
        "message": "Login exitoso",
        "user": {
            "id": db_user.id_user,
            "username": db_user.username,
            "email": db_user.email
        }
    }

# CATEGORIES
@app.post("/categories/")
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@app.get("/categories/")
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

# POSTS
@app.post("/posts/")
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post)

@app.get("/posts/")
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    result = []
    for post in posts:
        result.append({
            "id": post.id_post,
            "content": post.message,
            "likes": post.likes_count,
            "username": post.user.username if post.user else "Anon",
            "category": post.id_category  # luego lo mejoramos
        })

    return result

@app.get("/posts/user/{user_id}")
def get_posts_by_user(user_id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id_user == user_id).all()

    result = []
    for post in posts:
        result.append({
            "id": post.id_post,
            "content": post.message,
            "likes": post.likes_count,
            "username": post.user.username if post.user else "Anon",
            "category": post.id_category
        })

    return result

@app.put("/posts/like/{post_id}")
def like_post(post_id: int, db: Session = Depends(get_db)):

    post = (
        db.query(models.Post)
        .filter(models.Post.id_post == post_id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post no encontrado"
        )

    post.likes_count += 1

    db.commit()
    db.refresh(post)

    return {
        "message": "Like agregado",
        "likes": post.likes_count
    }

# COMMENTS
@app.post("/comments/")
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db, comment)

@app.get("/comments/")
def read_comments(db: Session = Depends(get_db)):
    return crud.get_comments(db)

@app.get("/comments/post/{post_id}")
def get_comments_by_post(
    post_id: int,
    db: Session = Depends(get_db)
):

    comments = (
        db.query(models.Comments)
        .filter(
            models.Comments.id_post == post_id
        )
        .all()
    )

    result = []

    for comment in comments:

        result.append({
            "id": comment.id_comments,
            "content": comment.comment,
            "username": (
                comment.user.username
                if comment.user
                else "Anon"
            )
        })

    return result