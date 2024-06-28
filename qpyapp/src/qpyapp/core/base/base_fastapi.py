from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

app = FastAPI()


def setup_static_folder(static_folder: str) -> FastAPI:
    app.mount("/static", StaticFiles(directory=static_folder), name="static")
    return app


