from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from prod_level.database import get_db
from prod_level.models import Post

router = APIRouter()

class PostCreate(BaseModel):
    title : str
    content : str
    isPublished : bool = True

@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return {"status": "success", "data": posts}

@router.get("/posts/{id}")
def get_post(id : int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    return {"status": "success", "data": post}

@router.post("/posts")
def create_post(post : PostCreate, db: Session = Depends(get_db)):
    new_post = Post(title = post.title, content = post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"status": "success", "data": new_post}

@router.delete("/posts/{id}")
def delete_post(id : int, db:Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"status": "success", "data": post}

@router.put("/posts/{id}")
def update_post(id : int, post_data : PostCreate, db:Session = Depends(get_db)):
    existing_post = db.query(Post).filter(Post.id == id).first()
    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    existing_post.title = post_data.title
    existing_post.content = post_data.content
    db.commit()
    db.refresh(existing_post)
    print("nothing is there just for testing")
    return {"status": "success", "data": existing_post}