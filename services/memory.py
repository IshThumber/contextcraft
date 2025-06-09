from db.vector_store import store_blog_memory, retrieve_user_blogs

def save_blog(user_id: str, title: str, content: str):
    return store_blog_memory(user_id, title, content)

def get_user_blogs(user_id: str):
    return retrieve_user_blogs(user_id)