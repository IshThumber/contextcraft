from fastapi import APIRouter, HTTPException, Body
from db.supabase_client import supabase
from pydantic import BaseModel

router = APIRouter()

@router.post("/signup")
def signup(email: str = Body(...), password: str = Body(...)):
    try:
        result = supabase.auth.sign_up({"email": email, "password": password, "options": {'email_confirm': True,}})
        if result.user:
            return {"message": "User created successfully", "user": result.user}
        else:
            raise HTTPException(status_code=400, detail="User creation failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(email: str = Body(...), password: str = Body(...)):
    try:
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {"access_token": result.session.access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
