import logging
import openai
from telegram import Update, Filters
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext

# Укажите ваш токен для OpenAI
openai.api_key = "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"

# Укажите токен вашего телеграм-бота
TELEGRAM_BOT_TOKEN = "6007270444:AAHREzJ4nfr-GRIOd7k9wi4q5tFq8scEUuM"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот, который объясняет значение контекста с помощью ChatGPT. Пиши свои вопросы, и я постараюсь помочь!")

def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Объясните значение следующего контекста: {user_text}",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    chatgpt_response = response.choices[0].text.strip()
    update.message.reply_text(chatgpt_response)

def main():
    logging.basicConfig(level=logging.INFO)

    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()