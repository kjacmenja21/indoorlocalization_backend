import uvicorn
from config import FastAPISettings, uvicorn_config
from fastapi import FastAPI


def create_server() -> FastAPI:
    app = FastAPI(**FastAPISettings().model_dump())

    return app


if __name__ == "__main__":
    uvicorn_config.app = create_server()
    uvicorn.run(uvicorn_config)
