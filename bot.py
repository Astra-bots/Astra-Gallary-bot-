import os
import random
from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

PHOTOS_DIR = "photos"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📷 عکس رندوم"]
    ]

    reply = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "🖼 به Astra Gallery خوش آمدی!\n\n"
        "برای دریافت عکس تصادفی روی دکمه زیر بزن.",
        reply_markup=reply
    )


async def random_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photos = os.listdir(PHOTOS_DIR)

    if not photos:
        await update.message.reply_text(
            "❌ هنوز عکسی داخل گالری نیست."
        )
        return

    photo = random.choice(photos)

    path = os.path.join(PHOTOS_DIR, photo)

    await update.message.reply_photo(
        photo=open(path, "rb"),
        caption="📸 Astra Gallery"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex("📷 عکس رندوم"),
            random_photo
        )
    )

    print("✅ Astra Gallery Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
