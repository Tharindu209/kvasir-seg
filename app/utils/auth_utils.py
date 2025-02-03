from datetime import timedelta
from typing import Union, Any
from app.core.config import supabase

def create_access_token(email: str, password: str) -> str:
    try:
        # Use Supabase to create an access token
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        return response.session.access_token
    except Exception as e:
        raise Exception(f"Failed to create access token: {str(e)}")

def create_refresh_token(email: str, password: str) -> str:
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        return response.session.refresh_token
    except Exception as e:
        raise Exception(f"Failed to create refresh token: {str(e)}")