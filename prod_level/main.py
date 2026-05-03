from fastapi import FastAPI
from prod_level.database import engine, Base
from prod_level.routes import users, posts, auth
from dotenv import load_dotenv

# Create database tables
Base.metadata.create_all(bind=engine)
load_dotenv()   
app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)