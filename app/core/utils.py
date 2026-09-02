from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher


pwd_context = PasswordHash((Argon2Hasher(),))

def hash_password(password: str):
    return pwd_context.hash(password=password)

def verify_password(plain_password:str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)