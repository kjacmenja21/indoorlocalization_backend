from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/\n
    """
    yield
    # TODO: Handle DB connection closure, something like this:
    # if sessionmanager._engine is not None:
    #    # Close the DB connection
    #    await sessionmanager.close()


def create_server() -> FastAPI:
    app = FastAPI(title="Indoor Localization Backend", lifespan=lifespan)

    return app


app = create_server()
