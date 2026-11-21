import os
import logging
import asyncio
from aiohttp import web
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import User

# .env yuklash
load_dotenv()

# Log sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Sozlamalar
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_STRING = os.getenv("TELEGRAM_SESSION", "").strip()

if not API_ID or not API_HASH:
    logger.critical("TELEGRAM_API_ID yoki TELEGRAM_API_HASH ko'rsatilmagan!")

# Render uchun StringSession yoki lokal sessiya
if SESSION_STRING:
    session = StringSession(SESSION_STRING)
else:
    session = "muhammaddiyor_session"

client = TelegramClient(session, int(API_ID) if API_ID else 0, API_HASH)

AUTO_REPLY_TEXT = (
    "Men Muhammaddiyorning AI yordamchisiman. "
    "U hozir band edi, bo'shashi bilan o'zi sizga xabar beradi."
)


@client.on(events.NewMessage(incoming=True))
async def handle_incoming_message(event):
    """
    Shaxsiy chatlardan kelgan xabarlarga avto-javob qaytarish.
    """
    if not event.is_private:
        return

    sender = await event.get_sender()

    if not isinstance(sender, User) or sender.bot or sender.is_self:
        return

    user_text = event.raw_text.strip()
    user_name = sender.first_name or "Foydalanuvchi"

    if not user_text:
        return

    logger.info(f"Yangi xabar [{user_name}]: {user_text}")

    try:
        async with client.action(event.chat_id, "typing"):
            await event.reply(AUTO_REPLY_TEXT)
        logger.info(f"Javob muvaffaqiyatli yuborildi [{user_name}]")
    except Exception as e:
        logger.error(f"Xatolik: {e}", exc_info=True)


# Render Web Service uchun portni ochiq tutuvchi yengil server
async def health_check(request):
    return web.Response(text="Bot is running active 24/7!")


async def start_web_server():
    port = int(os.getenv("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Web server Render uchun {port}-portda ishga tushdi.")


async def main():
    logger.info("Bot ishga tushirilmoqda...")
    await client.start()
    me = await client.get_me()
    logger.info(f"Akkaunt ulandi: {me.first_name} (@{me.username})")

    # Render Web Service portini ochish
    await start_web_server()

    # Botni doimiy rejimda ushlab turish
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
