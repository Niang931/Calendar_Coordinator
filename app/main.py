from fastapi import FastAPI
from app.routers import user, groups, tasks, avail

# if __name__ == '__main__':
print("Hello from app!")
app = FastAPI()

app.include_router(user.router)

app.include_router(groups.router)

app.include_router(tasks.router)

app.include_router(avail.router)


