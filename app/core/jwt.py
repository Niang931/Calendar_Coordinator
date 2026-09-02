import jwt
from datetime import datetime, timedelta
from app.core.config import settings
from fastapi import HTTPException

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
MAX_LENGTH = 72

def create_access_token():
    ...
    
    
def decode_access_token():
    ...