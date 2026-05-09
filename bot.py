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

TOKEN = os.getenv("8702714095:AAFfgYyCplCoJseV1P_aYNBg2_eAgOsKSLU")

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me a Facebook, Instagram, TikTok or YouTube video link."
    )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    supported = [
        "facebook.com",
        "fb.watch",
        "instagram.com",
        "tiktok.com",
        "youtube.com",
        "youtu.be",
        "twitter.com",
        "x.com",
    ]

    if not any(site in url for site in supported):
        await update.message.reply_text(
            "❌ Unsupported link.\n\nSend a valid social media video link."
        )
        return

    status = await update.message.reply_text(
        "📥 Downloading video..."
    )

    unique_name = str(uuid.uuid4())

    try:
        ydl_opts = {
            "format": "best",
            "outtmpl": f"{DOWNLOAD_FOLDER}/{unique_name}.%(ext)s",
            "noplaylist": True,
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await status.edit_text(
            "📤 Uploading video..."
        )

        with open(file_path, "rb") as video:
            await update.message.reply_video(
                video=video,
                supports_streaming=True,
            )

        os.remove(file_path)

        await status.delete()

    except Exception as e:
        await status.edit_text(
            f"❌ Failed to download video.\n\n{e}"
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        download_video
    )
)

print("✅ Bot is running...")
app.run_polling()