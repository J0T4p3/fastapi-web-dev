from fastapi import FastAPI

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from models import Posts, Post
from sqlite3 import Connection, Row

templates = Jinja2Templates(directory="templates")

app = FastAPI()
connection = Connection("database.db")
connection.row_factory = Row  # This allows us to access columns by name


@app.get("/")
async def home() -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": {}})


@app.get("/posts")
async def posts() -> Posts:
    from database import get_posts
    return get_posts(connection)


@app.post("/new_post")
async def create_post(post: Post) -> None:
    from database import insert_post
    insert_post(connection, post)
    return {"code": 200, "message": "Post created successfully"}
