import os
import logging
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
SESSION_STRING = os.getenv("TELEGRAM_SESSION", "")

# Agar SESSION_STRING bo'lsa (Render uchun) shundan foydalanadi,
# bo'lmasa oddiy lokal 'muhammaddiyor_session' faylidan foydalanadi
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
    Sizning lichkangizga kim yozsa ham avtomatik javob beradi.
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

    logger.info(f"Yangi xabar keldi [{user_name}]: {user_text}")

    try:
        async with client.action(event.chat_id, "typing"):
            await event.reply(AUTO_REPLY_TEXT)

        logger.info(f"Javob muvaffaqiyatli yuborildi [{user_name}]")
    except Exception as e:
        logger.error(f"Xatolik: {e}", exc_info=True)


async def main():
    logger.info("Bot ishga tushirilmoqda...")
    await client.start()
    me = await client.get_me()
    print(f"\n✅ Dastur faol! Akkaunt: {me.first_name}")
    print(f"=======================================================\n")
    await client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
