import asyncio

from src.db import database
from src.domain.bot import bot_process


async def main():
    await bot_process.send_msg("test")
    await database.engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
