import asyncio

from hypercorn.asyncio import serve

from app import app
from app.config import ASGIConfig, HypercornConfig


async def main():
    await serve(app, HypercornConfig())


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
