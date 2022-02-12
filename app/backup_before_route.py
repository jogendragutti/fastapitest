from logging import exception
from sqlite3 import Cursor
from typing import Optional
from fastapi import  Depends, FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2

from typing import Optional, List
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm  import Session 
from . import models
from . import schemas , utils
from .database import engine, get_db



models.Base.metadata.create_all(bind=engine)

app = FastAPI()





    

data=[{"title":"Mounika","content":"gvp","id":1},{"title":"Jogendra","content":"gvpce","id":2}]
def find(id):
    for p in data:
        if p["id"]==id:
            return p
def find_index(id):
    for i,p in enumerate(data):
        if p['id']==id:
            return i

@app.get("/")
async def root():
    return {"message": "good afternoon"}


@app.get("/posts", response_model= List[schemas.Post])
async def posts(db: Session = Depends(get_db)):
    post =db.query(models.post).all()

    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()
    # print(posts)
    return  post

@app.post("/createpost", response_model= schemas.Post,status_code=status.HTTP_201_CREATED)
async def create(payload:schemas.PostCreate ,db: Session = Depends(get_db)):
    # print(payload)
    # print(payload.dict())
    new_post = models.post(**payload.dict())
    #new_post = models.post( title=payload.title, content=payload.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post
    
@app.post("/create",status_code=status.HTTP_201_CREATED)
async def create(payload:schemas.PostCreate ):
    cursor.execute("""insert into posts (title,content) values (%s,%s) returning* """,(payload.title,payload.content))
    new_post=cursor.fetchone() 
    conn.commit()
    #post_dict=payload.dict()
    #post_dict['id']=randrange(1,10000)
    #data.append(post_dict)
    return  new_post

@app.get("/post/{id}", response_model= schemas.Post)
async def get_post(id:int,db: Session = Depends(get_db)):
    post = db.query(models.post).filter(models.post.id == str(id)).first()

    # cursor.execute("""select * from posts where id = %s""",(str(id)))
    # post= cursor.fetchone()
    # print(post)
    # # post=find(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")
    # #print(post)
    return  post

@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db)):
    post = db.query(models.post).filter(models.post.id == id)
    # index=find_index(id)
    # data.pop(index)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")

    post.delete(synchronize_session= False)
    db.commit()
    return "successfully deleted"

@app.put("/post/{id}", response_model= schemas.Post,status_code=status.HTTP_202_ACCEPTED)
def upadate_post(id:int,payload:schemas.PostBase,db: Session = Depends(get_db)):

    post_q = db.query(models.post).filter(models.post.id == id)
    post=post_q.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="not found")

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


@app.post("/users",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut )
async def create_user(user:schemas.UserCreate ,db: Session = Depends(get_db)):
    #hast the password - user.password
    
    hasdhed_password = utils.hash(user.password)
    user.password = hasdhed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user


@app.get('/user/{id}', response_model=schemas.UserOut )
def get_user(id:int,db: Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.id== id).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with id: {id}")

    return user







while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='jogendra',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connected")
        break
    except Exception as error:
        print("connection failed")
        print("error=",error)
        time.sleep(2)