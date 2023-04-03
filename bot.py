import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, ApplicationBuilder, filters

# Здесь введите токен вашего бота
TELEGRAM_BOT_TOKEN = '6007270444:AAHREzJ4nfr-GRIOd7k9wi4q5tFq8scEUuM'

# Здесь введите ваш API-ключ OpenAI
OPENAI_API_KEY = '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'

# Инициализируем подключение к API OpenAI
openai.api_key = OPENAI_API_KEY


# Функция-обработчик текстовых сообщений
async def reply_message(update: Updater, context: CallbackContext):
    # Получаем текст сообщения, отправленного пользователем
    user_message = update.message.text

    # Задаем параметры для запроса к API OpenAI
    prompt = f"Explain '{user_message}' in simple terms"
    model = 'text-davinci-002'
    temperature = 0.5
    max_tokens = 100

    # Получаем ответ от API OpenAI
    response = openai.Completion.create(engine=model, prompt=prompt, temperature=temperature, max_tokens=max_tokens)
    bot_reply = response.choices[0].text

    # Отправляем ответ от бота
    await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_reply)

# Функция-обработчик команды /start
async def start(update: Updater, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот.")

# Функция для запуска бота
if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    print("Успех")
    start_handler = CommandHandler('Start', start)
    application.add_handler(start_handler)
    application.run_polling()