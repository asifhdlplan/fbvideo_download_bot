import os
import uuid
import yt_dlp

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8702714095:AAEUo4or1v8-mxhXn_6sJ9z6Nafv9OilPnY"

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me a Facebook video link."
    )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "facebook.com" not in url and "fb.watch" not in url:
        await update.message.reply_text(
            "Please send a valid Facebook video link."
        )
        return

    status = await update.message.reply_text(
        "Downloading video..."
    )

    unique_name = str(uuid.uuid4())

    try:
        ydl_opts = {
            "format": "best",
            "outtmpl": f"{DOWNLOAD_FOLDER}/{unique_name}.%(ext)s",
            "noplaylist": True,
            "quiet": False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await status.edit_text("Uploading video...")

        with open(file_path, "rb") as video:
            await update.message.reply_video(
                video=video,
                supports_streaming=True,
            )

        os.remove(file_path)

    except Exception as e:
        await status.edit_text(
            f"Error:\n{e}"
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        download_video
    )
)

print("বট চালু হয়েছে")
app.run_polling()