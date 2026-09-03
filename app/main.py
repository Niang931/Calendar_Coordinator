from fastapi import FastAPI
from app.routers import user, tasks


print("Hello from app!")
app = FastAPI()

app.include_router(user.router)

app.include_router(tasks.router)

