from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from db.supabase_client import supabase
from api.dependencies import get_current_user

router = APIRouter()

@router.get("/me")
def get_my_profile(user = Depends(get_current_user)):
    return {"email": user["email"], "id": user["id"]}

# Example of a correctly protected route
@router.get("/profile")
def get_profile(current_user = Depends(get_current_user)):
    return {"user": current_user}
  
# route to check supabase connection
@router.get("/check_connection")
def check_connection():
    try:
        # Attempt to fetch a simple query
        response = supabase.table("users").select("*").limit(1).execute()
        if response.status_code == 200:
            return JSONResponse(content={"message": "Connection successful"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Connection failed"}, status_code=response.status_code)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)