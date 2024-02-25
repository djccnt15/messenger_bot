import asyncio

from src.domain.bot import bot_process


async def main():
    await bot_process.send_msg("test")


if __name__ == "__main__":
    asyncio.run(main())
