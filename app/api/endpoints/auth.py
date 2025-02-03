from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserAuth, UserOut, SystemUser
from app.schemas.token import TokenSchema
from app.utils.auth_utils import create_access_token, create_refresh_token
from app.core.config import supabase
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
        })
        user = response.user
        return {"email": user.email, "id": user.id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": form_data.username,
            "password": form_data.password,
        })
        user = response.user
        access_token = create_access_token(user.email, form_data.password)
        refresh_token = create_refresh_token(user.email, form_data.password)
        return { "access_token": access_token, "refresh_token": refresh_token}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
        
@router.post('/logout', summary="Logout user")
async def logout(user: SystemUser = Depends(get_current_user)):
    try:
        print(user.email)
        response = supabase.auth.sign_out()
        return {"message": "User logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user