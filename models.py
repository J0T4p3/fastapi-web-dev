from pydantic import BaseModel
from typing import List


class Post(BaseModel):
    title: str
    content: str
    author: str
    created_at: str = None
    updated_at: str = None


class Posts(BaseModel):
    posts: List[Post]
