from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from Models.post import Post
from Schemas.post import PostBase
from Services.database.post import create_post, get_post_by_id, change_post
from Services.database.story import get_all_post_story
from database_initializer import get_db
from Models.user import User


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# не работает
@router.post("/create", response_model=PostBase)
def create_post_endpoint(post: PostBase,
                         token: str = Depends(oauth2_scheme),
                         db: Session = Depends(get_db)):
    return create_post(session=db, post=post, token=token)


@router.get("/get/{post_id}", response_model=PostBase)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post


@router.get("/get_all", response_model=List[PostBase])
def get_all_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()


@router.delete("/delete/{post_id}")
def delete_post(post_id: int,
                db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme)):
    post = get_post_by_id(db, post_id=post_id)
    user = User.get_current_user_by_token(token)
    user_id = user['id']
    if post.owner_id != user_id:
        raise HTTPException(status_code=403, detail="У вас нет прав на удаление этого поста")
    if post is None:
        raise HTTPException(status_code=404, detail="Пост не найден")
    stroys = get_all_post_story(db, post_id=post_id)
    for story in stroys:
        db.delete(story)
    db.delete(post)
    db.commit()
    return {"message": "Пост  и истории к нему успешно удалены "}


@router.patch("/update/{post_id}")
def update_post(post_id: int,
                postscheme: PostBase,
                db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme)):
    post = get_post_by_id(session=db, post_id=post_id)
    user = User.get_current_user_by_token(token)
    user_id = user["id"]
    if post.owner_id != user_id:
        raise HTTPException(status_code=403, detail="У вас нет прав на изменение этого поста")
    if post is None:
        raise HTTPException(status_code=404, detail="Пост не найден")
    change_post(session=db, post_id=post_id, post=postscheme)
    return {"message": "Пост изменен"}