from fastapi import FastAPI , Response , status , HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content : str
    published : bool = True



try: 
    conn = psycopg2.connect(host='localhost' , database='fastapi', user='postgres' , password = '9934' ,cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successfull")
except Exception as error:
    print("Connecting to Database failed")
    print("Error :" , error)


my_posts = [{"title" : "title of posts 1" , "content" : "content of post 1" , "id" : 1 } ,
            {"title" : "fav food" , "content" : "pizza" , "id" : 2}]

async def find_post (id ):
    for p in my_posts:
        if p["id"]==id:
            return p     

async def find_index_post(id):
    count = 0
    for i , p in enumerate (my_posts):
        if p["id"]==id:
            return i
        


@app.get("/")
async def root() :
    return {"message": "hey"}

@app.get("/posts")
async def get_post():
    cursor.execute("""SELECT * from posts """)
    posts = cursor.fetchall()
    return {"data" : posts}

@app.post("/posts" , status_code=status.HTTP_201_CREATED)
async def create_posts(post : Post):
    cursor.execute(""" INSERT INTO posts (title , content , published) VALUES (%s , %s , %s) RETURNING *""", (post.title , post.content , post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data" : new_post}

@app.get("/posts/{id}")
async def get_post(id : int  , response : Response) :
    cursor.execute(""" SELECT * FROM posts WHERE id = (%s)""" , (str(id)))
    test_post = cursor.fetchone()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id : {id } not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message' : f"post with it : {id} was not found"}
    return {"posts detail" : test_post}

@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int ):
    cursor.execute(""" DELETE FROM posts where id = (%s) returning * """ , (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"posts with id : {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id : int , post : Post):

    cursor.execute(""" UPDATE posts SET title = (%s) , content = (%s) , published = (%s) WHERE id = (%s) returning *""" , (post.title , post.content , post.published ,str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f"posts with id : {id} does not exist")
    
    return {"data" : updated_post}
 