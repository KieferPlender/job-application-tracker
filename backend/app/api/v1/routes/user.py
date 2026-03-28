from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies.auth import get_current_user
from app.services.user import create_user
from app.schemas.user import UserCreate
from app.db.session import get_db
from app.dependencies.auth import generate_token
from app.services.user import user_login

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/me")
async def read_current_user(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at
    }

@router.post("/register")
async def register_user(user: UserCreate, db=Depends(get_db)):
    new_user = await create_user(user, db)
    token = generate_token(new_user.id)
    return {
        "user": {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "created_at": new_user.created_at
    },
    "token": token,
    "token_type": "bearer"
    }

@router.post("/login")
async def login_user(user: UserCreate, db=Depends(get_db)):
    try:
        existing_user = await user_login(user, db)
        token = generate_token(existing_user.id)
        return {
            "user": {
                "id": existing_user.id,
                "username": existing_user.username,
                "email": existing_user.email,
                "created_at": existing_user.created_at
            },
            "token": token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    



