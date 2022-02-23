from logging import exception
from sqlite3 import Cursor
from typing import Optional
from fastapi import  Depends, FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel, BaseSettings
from random import randrange
import psycopg2

from fastapi.middleware.cors import CORSMiddleware

from typing import Optional, List
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm  import Session

from app.routers.vote import vote 
from . import models
from . import schemas , utils
from .database import engine, get_db
from . routers import  post, user, auth, vote
from .config import settings

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





data=[{"title":"Mounika","content":"gvp","id":1},{"title":"Jogendra","content":"gvpce","id":2}]
def find(id):
    for p in data:
        if p["id"]==id:
            return p
def find_index(id):
    for i,p in enumerate(data):
        if p['id']==id:
            return i





app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "good evening"}

