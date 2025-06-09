from fastapi import APIRouter, Depends, HTTPException # type: ignore
from api.dependencies import get_current_user
from schemas.blog import BlogEntry
from services.memory import save_blog, get_user_blogs
from typing import List

router = APIRouter()

@router.post("/blog/save")
def save_blog_to_memory(entry: BlogEntry, user = Depends(get_current_user)):
    save_blog(user.id, entry.title, entry.content)
    return {"message": "Blog saved successfully"}

@router.get("/blog/user")
def get_user_blogs_route(user = Depends(get_current_user)):
    blogs = get_user_blogs(user.id)
    if not blogs:
        raise HTTPException(status_code=404, detail="No blogs found")
    return {"blogs": blogs}