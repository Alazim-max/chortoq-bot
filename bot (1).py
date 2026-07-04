"""
Bolalar Harakati Chortoq — Telegram bot (Python)
Savol-javob menyusi bilan ishlaydi, 24/7 serverda ishga tushirish uchun.
"""

import logging
import os
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ============================================================
# SOZLASH — shu joylarni o'zingizga moslang
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN topilmadi! Railway'da Variables bo'limiga BOT_TOKEN qo'shing."
    )
ADMIN_CHAT_ID = 8235586769  # Al'azim Qobuljanov

SAYT_URL = "https://bolalar-harakati-chortoq.vercel.app/"
TELEFON = "+998 94 352 01 23 / +998 32 627 47 5"
EMAIL = "oyinuchun47@gmail.com"
# ============================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

MENU_BUTTONS = [
    ["📋 Yo'nalishlar", "📞 Aloqa"],
    ["📝 Ariza qanday topshiriladi", "ℹ️ Tashkilot haqida"],
    ["🌐 Saytga o'tish", "🙋 Savolim bor"],
]
MENU_KEYBOARD = ReplyKeyboardMarkup(MENU_BUTTONS, resize_keyboard=True)

RESPONSES = {
    "📋 Yo'nalishlar": (
        "Bizning tashkilotimizda bir nechta yo'nalish (dastur) mavjud.\n"
        f"To'liq ro'yxatni saytimizdagi \"Loyihalar\" bo'limidan ko'ring:\n{SAYT_URL}"
    ),
    "📞 Aloqa": f"📞 Telefon: {TELEFON}\n📧 Email: {EMAIL}\n📍 Manzil: Chortoq tumani",
    "📝 Ariza qanday topshiriladi": (
        "Ariza topshirish uchun saytimizga kiring, kerakli yo'nalishni tanlang "
        "va formani to'ldiring. Ariza yuborilgach, tez orada siz bilan bog'lanamiz."
    ),
    "ℹ️ Tashkilot haqida": (
        "Bolalar Harakati — O'zbekiston Bolalar Tashkilotining Chortoq tuman bo'limi. "
        "Maqsadimiz — bolalar va yoshlarni turli dasturlar orqali rivojlantirish."
    ),
    "🌐 Saytga o'tish": f"🌐 Saytimiz: {SAYT_URL}",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! 👋\n"
        "Bolalar Harakati Chortoq rasmiy botiga xush kelibsiz.\n"
        "Quyidagi menyudan kerakli bo'limni tanlang 👇",
        reply_markup=MENU_KEYBOARD,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    chat_id = update.effective_chat.id
    username = update.effective_user.username or "noma'lum"

    if text in RESPONSES:
        await update.message.reply_text(RESPONSES[text], reply_markup=MENU_KEYBOARD)
    elif text == "🙋 Savolim bor":
        await update.message.reply_text(
            "Savolingizni yozing, operatorga yuboramiz.", reply_markup=MENU_KEYBOARD
        )
    else:
        # Menyuga mos kelmagan matn — operatorga forward qilinadi
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"✉️ Foydalanuvchidan xabar:\n@{username} (chat ID: {chat_id}):\n{text}",
        )
        await update.message.reply_text(
            "Xabaringiz qabul qilindi, tez orada javob beramiz. ✅",
            reply_markup=MENU_KEYBOARD,
        )


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
