from fastapi import FastAPI
from app.routers import user


print("Hello from app!")
app = FastAPI()

app.include_router(user.router)



