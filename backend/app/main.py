from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection, db_instance
from app.utils.logger import logger

# Routers
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.resumes import router as resumes_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.interviews import router as interviews_router
from app.api.routes.reports import router as reports_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up %s...", settings.PROJECT_NAME)
    await connect_to_mongo()
    yield
    logger.info("Shutting down %s...", settings.PROJECT_NAME)
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Agentic AI-powered accessible mock interview platform backend",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers under settings.API_V1_STR ("/api")
api_prefix = settings.API_V1_STR
app.include_router(auth_router, prefix=api_prefix)
app.include_router(users_router, prefix=api_prefix)
app.include_router(resumes_router, prefix=api_prefix)
app.include_router(jobs_router, prefix=api_prefix)
app.include_router(interviews_router, prefix=api_prefix)
app.include_router(reports_router, prefix=api_prefix)

@app.get(f"{api_prefix}/health", tags=["Health"])
async def health_check():
    db_connected = False
    if db_instance.client is not None:
        try:
            await db_instance.client.admin.command("ping")
            db_connected = True
        except Exception:
            db_connected = False

    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "database_connected": db_connected,
        "llm_provider": settings.LLM_PROVIDER,
        "version": "0.1.0"
    }
