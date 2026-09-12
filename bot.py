import os
import subprocess
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = "TOKEN = os.environ["BOT_TOKEN"]"


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("⏳ Converting your voice message to MP3...")

        voice = update.message.voice
        file = await voice.get_file()

        input_file = f"/tmp/{update.message.message_id}.ogg"
        output_file = f"/tmp/{update.message.message_id}.mp3"

        await file.download_to_drive(input_file)

        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", input_file,
            "-codec:a", "libmp3lame",
            "-q:a", "2",
            output_file
        ], check=True)

        with open(output_file, "rb") as audio:
            await update.message.reply_audio(
                audio=audio,
                title="Converted MP3"
            )

        os.remove(input_file)
        os.remove(output_file)

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("❌ Something went wrong while converting.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
