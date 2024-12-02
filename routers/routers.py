import traceback
from fastapi import APIRouter,status,HTTPException
from fastapi.responses import JSONResponse
from schemas.schemas import Users
from database.database import db

router = APIRouter()

@router.post("/add_users")
def create_users(user: Users):
    try:
        add_new_user = db.add(
            {
                "username" : user.username,
                "email" : user.email,
                "project_id" : user.project_id
            }
        )
        
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {"message" : "User Added Successfully",
                       "user_id" : add_new_user.id, 
                       "username": add_new_user.username, 
                       "email": add_new_user.email,
                       "project_id" : add_new_user.project_id}
        )
        
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {"message" : "Something Went Wrong"}
        )

@router.get("/get_users")
def get_users():
    try:
        users = []
        for doc in db.stream():
            users.append(doc.to_dict())
            
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {"users" : users}
        )
    
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {"message" : "Something Went Wrong"}
        )

@router.patch("/update_users")
def update_users(user_id: str, user: Users):
    try:
        user_ref = db.document(user_id)
        user_data = user_ref.get()
        if not user_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User Details Not Found")
        user_ref.update({
            "username" : user.username,
            "email" : user.email,
            "project_id" : user.project_id
        })
        
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {"message" : "Updated Successfully"}
        )
            
    except HTTPException as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=e.status_code,
            content = e.detail
        )
    
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {"message" : "Something Went Wrong"}
        )