from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_current_user
from pydantic import BaseModel
from services.topic_generator import generate_blog_topics
from db.vector_store import retrieve_user_blogs

router = APIRouter()

class TopicRequest(BaseModel):
    user_input: str

@router.post("/topics/generate")
def get_blog_topics(request: TopicRequest, user = Depends(get_current_user)):
    """Generate blog topic suggestions based on user's past blogs and input"""
    try:
        # Get the user's existing blogs
        user_blogs = retrieve_user_blogs(user.id)
        
        # Generate topics based on existing blogs and user input
        topics = generate_blog_topics(user_blogs, request.user_input)
        
        return {"topics": topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating topics: {str(e)}")
