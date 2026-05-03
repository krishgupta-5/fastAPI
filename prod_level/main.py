from fastapi import FastAPI
from prod_level.database import engine, Base
from prod_level.routes import users, posts, auth

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)