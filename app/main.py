import uvicorn
from config import FastAPISettings, UvicornConfig
from fastapi import FastAPI


def create_server() -> FastAPI:
    app = FastAPI(**FastAPISettings().model_dump())
    return app


app = create_server()

if __name__ == "__main__":
    uvicorn.run(
        **UvicornConfig().model_dump(),
    )
