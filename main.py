import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "9264077879:AAHrujgevUaZ2thY64M-zE14xnB_hmUXTVo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("नमस्ते! Nath Store वॉयस बॉट ऑनलाइन है। मुझे कोई वॉइस नोट या मैसेज भेजें!")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_file = await update.message.voice.get_file()
    oga_path = "user_voice.oga"
    wav_path = "user_voice.wav"
    reply_voice_path = "reply.mp3"

    await voice_file.download_to_drive(oga_path)

    audio = AudioSegment.from_file(oga_path)
    audio.export(wav_path, format="wav")

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="hi-IN")
            reply_text = f"आपने बोला: {text}"
    except Exception:
        reply_text = "माफ़ करना, मैं आपकी आवाज़ ठीक से समझ नहीं पाया।"

    tts = gTTS(text=reply_text, lang='hi')
    tts.save(reply_voice_path)

    with open(reply_voice_path, 'rb') as voice_reply:
        await update.message.reply_voice(voice=voice_reply)

    for f in [oga_path, wav_path, reply_voice_path]:
        if os.path.exists(f):
            os.remove(f)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(f"आपने लिखा: {user_text}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Voice Bot chalu ho gaya hai...")
    app.run_polling()
