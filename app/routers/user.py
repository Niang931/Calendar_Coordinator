from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import exc
from fastapi import HTTPException
from app.schemas.user_schema import UserCreate, UserBase, UserDB, Token
from app.core.database import get_session
from app.core.logger import logger
from app.internal.user import add_user, get_user_by_username
from app.core.utils import verify_password, hash_password
from app.core._jwt import create_access_token

router = APIRouter(prefix='/user',
                   tags=['users'])

@router.post('/register', response_model=str)
async def register_user(user: UserCreate,
                        session=Depends(get_session)):
    username, password = user.username, user.password
    try:
        username_exist = get_user_by_username(username, session)
        if username_exist:
            raise HTTPException(status_code=403,
                                detail="Username already taken. Please take a different one")
        
        hashed_password = hash_password(password)
        add_user(UserDB(username=username,
                        hashed_password=hashed_password,
                        email=user.email), session)
        return user.username
        
    except exc.DataError as e:
        logger.error(e)
        raise
    

@router.post('/logiin', response_model=Token)
async def login_user(user: UserBase,
                     session=Depends(get_session)):
    try:
        user_in_db = get_user_by_username(user.username, session)
        if not user_in_db:
            raise HTTPException(status_code=404,
                                detail="User not found")
        plain_password = user.password
        if not verify_password(plain_password, user_in_db.hashed_password):
            raise HTTPException(status_code=403,
                                detail='Incorrect credential')
        access_token = Token(access_token=create_access_token(user_in_db.user_id))
        return access_token
        
    except exc.DatabaseError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)


