from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import chat, evals, health, knowledge
from app.services.bok import bok_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    bok_index.load()
    yield


app = FastAPI(
    title="tai-lab",
    description="Backend for the Trustworthy AI evaluation lab",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(evals.router, prefix="/evals", tags=["evals"])
app.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
