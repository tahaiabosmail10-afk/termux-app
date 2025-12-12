import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

TELEGRAM_TOKEN = 8406948337:AAFxpPcOd6BHbuQ2Hu2SV8xBI4dpDVOPLds
OPENAI_API_KEY =import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أرسل لي نوع الأسئلة التي تريد، وسأولدها لك ✨")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI that generates medical MCQs and short essay questions."},
            {"role": "user", "content": user_text}
        ]
    )

    answer = response.choices[0].message["content"]
    await update.message.reply_text(answer)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
