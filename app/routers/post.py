from sys import api_version
from fastapi import  Depends, FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm  import Session
from typing import  List, Optional

from app import oauth2
from .. import models, schemas , oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)



#@router.get("/", response_model= List[schemas.Post])
@router.get("/",response_model= List[schemas.PostOut])
async def posts(db: Session = Depends(get_db),limit:int = 10,skip:int = 0, search : Optional[str]=""):
    
    print(limit)
    #post =db.query(models.post).filter(models.post.title.contains(search)).limit(limit).offset(offset=skip).all()
    
    posts = db.query(models.post,func.count(models.post.id).label("votes")).join(models.Vote, models.Vote.post_id == models.post.id, isouter = True).group_by(models.post.id).filter(models.post.title.contains(search)).limit(limit).offset(offset=skip).all()
    #print(results)
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    # print(posts)
    return  posts

@router.post("/", response_model= schemas.Post,status_code=status.HTTP_201_CREATED)
async def create(payload:schemas.PostCreate ,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # print(payload)
    # print(payload.dict())
    new_post = models.post(owner_id = current_user.id, **payload.dict())
    #new_post = models.post( title=payload.title, content=payload.content)
    print(current_user.id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post
    

@router.get("/{id}", response_model= schemas.PostOut)
async def get_post(id:int,db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #post = db.query(models.post).filter(models.post.id == str(id)).first()

    post = db.query(models.post,func.count(models.post.id).label("votes")).join(models.Vote, models.Vote.post_id == models.post.id, isouter = True).group_by(models.post.id).filter(models.post.id == str(id)).first()
    # cursor.execute("""select * from posts where id = %s""",(str(id)))
    # post= cursor.fetchone()
    # print(post)
    # # post=find(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")
    # #print(post)
    return  post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    
    post_q = db.query(models.post).filter(models.post.id == id)
    post=post_q.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")
    
    # index=find_index(id)
    # data.pop(index)
    print(post.owner_id, current_user.id)
    
    if (post.owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="Cant  perform opp")

    post_q.delete(synchronize_session= False)
    db.commit()
    return "successfully deleted"

@router.put("/{id}", response_model= schemas.Post,status_code=status.HTTP_202_ACCEPTED)
def upadate_post(id:int,payload:schemas.PostBase,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):

    post_q = db.query(models.post).filter(models.post.id == id)
    post=post_q.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authenticated")

    post_q.update(payload.dict(),synchronize_session= False)
    db.commit()

    # cursor.execute("""update posts set title = %s, content = %s where id = %s returning* """,(payload.title,payload.content,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    #index=find_index(id)
    #post_dict=payload.dict()
    #post_dict['id']=id
    #data[index]=post_dict

    #print(updated_post)
    return post_q.first()