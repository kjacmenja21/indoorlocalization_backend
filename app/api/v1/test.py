from fastapi import APIRouter

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/")
async def test():
    return {"test": "success"}
