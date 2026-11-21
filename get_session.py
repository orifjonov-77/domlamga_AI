from telethon import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

# Mavjud fayldan ochish
client = TelegramClient("muhammaddiyor_session", API_ID, API_HASH)

async def main():
    await client.connect()
    # StringSession ga aylantirish
    string = StringSession.save(client.session)
    print("\n" + "="*50)
    print("RENDER UCHUN 'TELEGRAM_SESSION' QIYMATI:")
    print("="*50)
    print(string)
    print("="*50 + "\n")

with client:
    client.loop.run_until_complete(main())
