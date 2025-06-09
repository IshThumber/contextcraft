import ssl
import os

os.environ["PYTHONHTTPSVERIFY"] = "0"
ssl._create_default_https_context = ssl._create_unverified_context

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, user, blog, topic, draft

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(blog.router)
app.include_router(topic.router)
app.include_router(draft.router)
