import jwt
import uuid
from datetime import datetime, timedelta
from app.core.config import setting
from fastapi import HTTPException

SECRET_KEY = setting.SECRET_KEY
ALGORITHM = setting.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = setting.ACCESS_TOKEN_EXPIRE_MINUTES
MAX_LENGTH = 72

def create_access_token(user_id:str , exp_minute: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    expire = datetime.now() + timedelta(minutes=exp_minute)
    to_encode = {'sub': str(user_id), 
                 'exp': expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
def decode_access_token(token):
    try:
        decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decode['sub']
        return uuid.UUID(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f'Invalid token {e}')