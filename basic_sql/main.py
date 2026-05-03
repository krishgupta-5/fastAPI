from fastapi import Body, FastAPI
import psycopg2
from pydantic import BaseModel
from random import randrange
from fastapi import Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    isPublished : bool = True

while True:
    try:
        conn = psycopg2.connect(
            host = "localhost",
            database = "fastapi",
            user = "postgres",
            password = "password",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as e:
        print("Database connection failed")
        print("Error:", e)
        time.sleep(2)


# GET Request
@app.get("/")
async def root():
    return {"message" : "Hello World"}



@app.get("/posts{id}")
async def get_posts(id : int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    return {"data": post}


@app.post("/createpost")
async def create_post():
    cursor.execute("INSERT INTO posts (title, content, is_published) VALUES ('Post From API CALL', 'this is the content of the post from the api call', 'true')")
    conn.commit()
    return {"data": "create post"}

@app.post("/create_post")
async def create_post(post : Post):
    cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """, (post.title, post.content) )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.put("/update_post{id}")
async def update_post(id : int, post : Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", (post.title, post.content, id))
    updated_post = cursor.fetchone() 
    conn.commit()
    if updated_post is None :
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return {"data": updated_post}

@app.delete("/delete_post{id}")
async def delete_post(id : int):
    cursor.execute("DELETE FROM posts Where id = %s", (id))
    deleted_post = cursor.fetchone()
    conn.commit()
    return {"data": deleted_post}

@app.delete("/delete_table")
async def delete_table():
    cursor.execute("""DROP TABLE posts """)
    conn.commit()
    return {"data": "table deleted"}