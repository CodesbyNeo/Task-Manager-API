from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, tasks

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="A production-style REST API for managing tasks with JWT authentication.",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Task Manager API is running"}
