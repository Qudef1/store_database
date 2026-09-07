from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Банк данных технологий создания продуктов",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.include_router(api_v1_router, prefix="/api/v1")
    return app


app = create_app()