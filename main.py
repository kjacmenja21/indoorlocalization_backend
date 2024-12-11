import asyncio
from time import sleep

from hypercorn.asyncio import serve

from app import app
from app.config import HypercornConfig


async def main():
    sleep(5.0)
    await serve(app, HypercornConfig())


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
