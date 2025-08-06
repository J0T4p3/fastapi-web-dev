from fastapi import FastAPI

from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from models import Posts, Post
from sqlite3 import Connection, Row

templates = Jinja2Templates(directory="templates")

app = FastAPI()
connection = Connection("database.db")
connection.row_factory = Row  # This allows us to access columns by name


@app.get("/")
async def home(request:Request) -> HTMLResponse:
    from database import get_posts
    posts = get_posts(connection).posts
    return templates.TemplateResponse(request, "index.html", context={"posts": posts})


@app.get("/posts")
async def posts(request: Request) -> Posts:
    from database import get_posts
    posts = get_posts(connection)
    return posts


@app.post("/new_post")
async def create_post(post: Post) -> None:
    from database import insert_post
    insert_post(connection, post)
