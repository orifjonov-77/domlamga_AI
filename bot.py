import os
import logging
import asyncio
from aiohttp import web
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import User

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_STRING = os.getenv("TELEGRAM_SESSION", "").strip()

if not API_ID or not API_HASH:
    logger.critical("TELEGRAM_API_ID yoki TELEGRAM_API_HASH yo'q!")

# Render uchun StringSession majburiy
if not SESSION_STRING:
    logger.error("DIQQAT: TELEGRAM_SESSION topilmadi! Render Environment Variables bo'limiga TELEGRAM_SESSION ni qo'shing.")
    session = "muhammaddiyor_session"
else:
    session = StringSession(SESSION_STRING)

client = TelegramClient(session, int(API_ID) if API_ID else 0, API_HASH)

AUTO_REPLY_TEXT = (
    "Men Muhammaddiyorning AI yordamchisiman. "
    "U hozir band edi, bo'shashi bilan o'zi sizga xabar beradi."
)


@client.on(events.NewMessage(incoming=True))
async def handle_incoming_message(event):
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
        logger.info(f"Javob yuborildi [{user_name}]")
    except Exception as e:
        logger.error(f"Xatolik: {e}", exc_info=True)


async def health_check(request):
    return web.Response(text="Bot faol ishlamoqda!")


async def start_web_server():
    port = int(os.getenv("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Port {port} da veb-server ishga tushdi.")


async def main():
    # Telegramga ulanish (hech qanday input kutmaydi)
    await client.connect()
    if not await client.is_user_authorized():
        logger.critical("Sessiya avtorizatsiyadan o'tmagan! TELEGRAM_SESSION kalitini to'g'ri kiriting.")
        return

    me = await client.get_me()
    logger.info(f"Muvaffaqiyatli ulandi: {me.first_name} (@{me.username})")

    await start_web_server()
    await client.run_until_disconnected()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
