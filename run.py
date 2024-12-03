import uvicorn

from app.config import UvicornConfig

if __name__ == "__main__":
    uvicorn.run(
        **UvicornConfig().model_dump(),
    )
