from fastapi import Body, FastAPI
import psycopg2
from pydantic import BaseModel
from random import randrange
from fastapi import Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()
app.state.count = 0

class Post(BaseModel):
    title : str
    content : str
    category : str
    isPublished : bool = True

my_posts = [{"title": "title", "content": "content", "category": "category", "id": 1}]


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

def findPost(id) :
    for post in my_posts:
        if post["id"] == id:
            return post

def findPostIndex(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

# GET Request
@app.get("/")
async def root():
    app.state.count += 1
    return {"message" : "Hello World", "count" : app.state.count}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

# POST Request
# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return{"message": "Successfully created post"}

# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return{"new post": f"title {payLoad["title"]}, content {payLoad["content"]}"}

@app.post("/createposts")
def create_posts(new_post : Post):
    print(new_post)
    return{"new post": f"title : {new_post.title}, content : {new_post.content}, category : {new_post.category}, isPublished : {new_post.isPublished}"}
    # return new_post 


@app.post("/posts")
def create_post(post : Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    print(post_dict)
    return post_dict    


@app.get("/posts/{id}")
def get_post(id: int, response : Response):
    post = findPost(id)
    if not post :
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post not found for id {id}"}
    return {"post details" : post}

# DELETE Request
@app.delete("/posts/{id}")
def delete_post(id : int):
    index = findPostIndex(id)
    if not index:
        return Response(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found for id {id}")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#UPDATE Request
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = findPostIndex(id)
    if index is None : 
        return Response(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found for id {id}")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    print(post)
    return {"message": f"Post updated for id {id}"}