# Domlaga AI - Muhammaddiyorning Shaxsiy AI Yordamchisi (Userbot)

Ushbu dastur **sizning shaxsiy Telegram profilingizga kim yozsa ham**, AI (OpenAI ChatGPT) orqali avtomatik tarzda:
> *"Men Muhammaddiyorning yordamchisiman..."*

deb sizning nomingizdan javob qaytaradi. Suhbat kontekstini (oxirgi 10 ta xabar) eslab qoladi va qaysi tilda yozishsa, o'sha tilda javob beradi.

---

## 📁 Loyiha fayllari

```text
domlaga ai/
├── bot.py             # Asosiy Telegram Userbot kodi
├── .env.example       # Muhit o'zgaruvchilari namunasi
├── .gitignore         # .env va .session (maxfiy fayllar) ni yashirish
├── requirements.txt   # Kerakli kutubxonalar (Telethon, OpenAI, dotenv)
└── README.md          # Ishga tushirish qo'llanmasi
```

---

## ⚙️ Sozlash va ishga tushirish bosqichlari

### 1. Kutubxonalarni o'rnatish
Terminalda loyiha papkasiga o'tib, kutubxonalarni o'rnating:

```bash
cd "C:\Users\777 comp service\Desktop\domlaga ai"
pip install -r requirements.txt
```

### 2. Telegram API ma'lumotlarini olish
1. Brauzeringizda **[my.telegram.org](https://my.telegram.org)** saytiga kiring.
2. Telefon raqamingizni kiriting va Telegramga kelgan tasdiqlash kodini yozing.
3. **API development tools** bo'limiga kiring.
4. Ilova nomi (masalan: `MyAssistant`) yozib, **App api_id** va **App api_hash** ni oling.

### 3. `.env` faylini yaratish
`.env.example` nusxasidan `.env` fayli yarating:

```bash
copy .env.example .env
```

`.env` faylini ochib, ma'lumotlaringizni kiriting:
```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcd1234efgh5678ijkl...
TELEGRAM_PHONE=+998901234567

OPENAI_API_KEY=sk-...
AI_MODEL=gpt-4o-mini
```

---

## 🚀 Ishga tushirish

Terminalda quyidagi buyruqni bering:

```bash
python bot.py
```

> **Eslatma:** Birinchi marta ishga tushirganingizda, Telegram profilingizga kirish uchun telefon raqamingizga yoki Telegram ilovangizga **tasdiqlash kodi** yuboradi. Uni terminalda kiriting. Shundan so'ng `.session` fayli yaratiladi va keyingi safar kod so'ramaydi.
