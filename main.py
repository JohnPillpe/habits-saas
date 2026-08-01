from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db.database import Base, engine

from app.api import auth
from app.api import habits
from app.api import jobs
from app.api import stats
from app.api import ai
from app.api.documents import router as documents_router
from app.api import career

app = FastAPI(title="Seguimiento de Hábitos")

Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth.router)
app.include_router(habits.router)
app.include_router(jobs.router)
app.include_router(stats.router)
app.include_router(ai.router)
app.include_router(documents_router)
app.include_router(career.router)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def pagina_principal(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )



