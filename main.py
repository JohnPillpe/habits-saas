from fastapi import FastAPI

from app.db.database import Base, engine

from app.api import auth
from app.api import jobs
from app.api.documents import router as documents_router
from app.api import career
from app.api import interview
from fastapi.middleware.cors import CORSMiddleware
from app.api import analysis
from app.api import upload
from app.api.analysis_runner import router as analysis_runner_router

app = FastAPI(title="MatchAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(documents_router)
app.include_router(career.router)
app.include_router(interview.router)
app.include_router(analysis.router)
app.include_router(upload.router)
app.include_router(analysis_runner_router)


@app.get("/")
def home():
    return {
        "name": "MatchAI API",
        "status": "running",
        "docs": "/docs",
    }