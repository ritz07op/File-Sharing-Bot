from bot import Bot
import asyncio

async def main():
    bot = Bot()
    await bot.start()  # Start the bot
    await bot.idle()   # Keep it running

if __name__ == "__main__":
    asyncio.run(main())
