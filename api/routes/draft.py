from fastapi import APIRouter, Depends, Body, HTTPException
from api.dependencies import get_current_user
from db.vector_store import search_similar_blogs
from services.draft_generator import generate_draft_from_topic
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

# Import the function
from utils.markdown_helper import clean_and_save_draft

router = APIRouter()

class DraftRequest(BaseModel):
    draft: str

@router.post("/blog/draft")
def get_blog_draft(
    topic: str = Body(...),
    extra: str = Body(""),
    user = Depends(get_current_user)
):
    similar_blogs = search_similar_blogs(user.id, topic)
    draft_content = generate_draft_from_topic(topic, similar_blogs, extra)
    
    draft_response = {"draft": draft_content}  
    return draft_response

@router.post("/blog/draft/download")
def download_blog_draft(
    request: DraftRequest
):
    """
    Download a blog draft as a markdown file.
    """
    # Generate the draft content
    draft_data = {"draft": request.draft}
    markdown_path = clean_and_save_draft(draft_data)
    
    # Return the file for download
    return FileResponse(
        path=markdown_path,
        filename=os.path.basename(markdown_path),
        media_type="text/markdown"
    )
