from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.game import router as game_router


app = FastAPI(
    title="Loki Escape Game API",
    version="1.0.0",
    description="Backend FastAPI V1 pour un escape game de Pâques en faux chat.",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(game_router)


@app.get("/", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
