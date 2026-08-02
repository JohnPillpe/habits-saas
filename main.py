from fastapi import FastAPI

from app.db.database import Base, engine

from app.api import auth
from app.api import jobs
from app.api.documents import router as documents_router
from app.api import career
from app.api import interview

app = FastAPI(title="MatchAI API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(documents_router)
app.include_router(career.router)
app.include_router(interview.router)


@app.get("/")
def home():
    return {
        "name": "MatchAI API",
        "status": "running",
        "docs": "/docs",
    }