import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID", 0))
API_HASH = os.getenv("TELEGRAM_API_HASH")

# Sinxron mijoz orqali sessiyani ochish
with TelegramClient("muhammaddiyor_session", API_ID, API_HASH) as client:
    # Mavjud sessiyadan StringSession kalitini olish
    session_string = StringSession.save(client.session)
    
    print("\n" + "="*60)
    print("MANA SIZNING RENDER UCHUN 'TELEGRAM_SESSION' KALITINGIZ:")
    print("="*60)
    print(session_string)
    print("="*60 + "\n")
    
    # Uni oson nusxalash uchun alohida session_string.txt fayliga ham yozib qo'yamiz
    with open("session_string.txt", "w", encoding="utf-8") as f:
        f.write(session_string)
    print("✅ Kalit 'session_string.txt' fayliga ham saqlandi!\n")
