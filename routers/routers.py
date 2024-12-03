import traceback
from typing import List
from fastapi import APIRouter,status,HTTPException,UploadFile,File,Form
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from schemas.schemas import Users,InvitePayload
from database.database import db
from utilities.email_utils import send_invitation_email

router = APIRouter()

@router.post("/add_users")
def create_users(user: Users):
    try:
        timestamp, add_new_user = db.add(
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
                       "username": user.username, 
                       "email": user.email,
                       "project_id" : user.project_id}
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

@router.delete("/delete_users")
def delete_users(user_id: str):
    try:
        user_ref = db.document(user_id)
        user_data = user_ref.get()
        if not user_data:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User Details Not Found")
        user_ref.delete()
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {"message" : "Deleted Successfully"}
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

@router.post("/send_invite")
async def send_invite(recipient_email : str = Form(...),
                      redoc_link : str = Form(None),
                      swagger_link: str = Form(None),
                      github_code_link: str = Form(None),
                      image: UploadFile = File(...)):
    try:
        recipient_email_list = recipient_email.split(',')            
        image_data = await image.read()
        image_filename = image.filename
        payload = InvitePayload(
            recipient_email=recipient_email_list,
            redoc_link=redoc_link,
            swagger_link=swagger_link,
            github_code_link=github_code_link
        )

        response = send_invitation_email(payload, image_data, image_filename)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = response
        )
    
    except HTTPException as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=e.status_code,
            content=e.detail
        )
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {"message" : "Something Went Wrong"}
        )       
        