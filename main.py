import os
import asyncio
import logging
from aiohttp import web
from config import Config
from pyrogram import Client as bot, idle

logging.basicConfig(
    level=logging.INFO,    
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S'
)
LOGGER = logging.getLogger(__name__)
LOGGER.info("Live log streaming to telegram.")

plugins = dict(root="plugins")

# Simple health check endpoint for Render
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)
    
    # Render passes the port via the PORT environment variable (defaults to 8080 locally)
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    LOGGER.info(f"Web server started on port {port}")

if __name__ == "__main__":
    bot = bot(
        "Bot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=120,
        plugins=plugins,
        workers=10,
    )

    async def main():
        # Start the internal HTTP server to satisfy Render's port detection
        await start_web_server()
        
        await bot.start()
        bot_info = await bot.get_me()
        LOGGER.info(f"<--- @{bot_info.username} Started --->")
        for user_id in Config.AUTH_USERS:
            try:
                await bot.send_message(
                    chat_id=user_id, 
                    text=f"__Congrats! You Are DRM member ... if You get any error then contact me -  {Config.CREDIT}__"
                )
            except Exception as e:
                LOGGER.error(f"Failed to send message to user {user_id}: {e}")
                continue
        await idle()

    asyncio.get_event_loop().run_until_complete(main())
    LOGGER.info("<--- Bot Stopped --->")
