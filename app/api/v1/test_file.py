from fastapi import APIRouter

from app.database.dependencies import DatabaseSessionAsync

test_router = APIRouter(prefix="/test", tags=["test"])


@test_router.get("/")
async def test(session: DatabaseSessionAsync):
    await session.aclose()
    return {"test": "success"}
