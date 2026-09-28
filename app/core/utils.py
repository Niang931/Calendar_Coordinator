from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core._jwt import decode_access_token
from app.internal.user import get_user
from app.core.database import get_session

pwd_context = PasswordHash((Argon2Hasher(),))

def hash_password(password: str):
    return pwd_context.hash(password=password)

def verify_password(plain_password:str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

security = HTTPBearer(auto_error=False)


def extract_bearer_token(
    credential: HTTPAuthorizationCredentials = Depends(security),
):
    if credential is None:
        raise HTTPException(status_code=401, detail="Missing credentials")

    if credential.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return credential.credentials

def get_current_user(
    session=Depends(get_session),
    token = Depends(extract_bearer_token),
):
    user_id = decode_access_token(token)

    user = get_user(user_id=user_id, session=session)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user_id