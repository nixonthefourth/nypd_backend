from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import (
    create_access_token,
    verify_token,
    blacklist_token
)
from app.database.db_raw import *

auth_router = APIRouter(prefix="/login", tags=["Authentication"])
security = HTTPBearer()

# POST
@auth_router.post("/", response_model=TokenResponse)
def login(data: LoginRequest):

    valid_users = {
        "officer_user"
    }

    valid_passwords = {
        "officer_password"
    }

    if data.username not in valid_users or data.password not in valid_passwords:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": data.username})
    return {"access_token": token, "token_type": "bearer"}

# PUT

@auth_router.put("/", response_model=TokenResponse)
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    old_token = credentials.credentials
    payload = verify_token(old_token)

    new_token = create_access_token({"sub": payload["sub"]})

    return {"access_token": new_token, "token_type": "bearer"}

# DELETE

@auth_router.delete("/")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    verify_token(token)

    blacklist_token(token)

    return {"message": "Successfully logged out"}
