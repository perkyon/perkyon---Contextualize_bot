import openai
import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient import discovery

# Здесь введите токен вашего бота
token = '6007270444:AAHREzJ4nfr-GRIOd7k9wi4q5tFq8scEUuM'

# Здесь введите ваш API-ключ OpenAI
openai.api_key = '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'

# Здесь введите путь к файлу JSON с учетными данными Google API
credentials_file = 'contexbot.json'

# Введите идентификатор вашей таблицы Google Sheets из ссылки
sheet_id = '1KXH9ep8l7qStEnXN9ZOucw8YucHYlTsB9uBbjdR1x_E'

# Диспетчер
bot = Bot(token)
dp = Dispatcher(bot)

async def on_startup(dp):
# Установить команды для бота
    await bot.set_my_commands([types.BotCommand(command["command"], command["description"]) for command in bot_commands])

# Функции бота
@dp.message_handler(commands=['start'])
async def start_help_command(message: types.Message):
    await message.reply("Привет! Я ваш телеграм-бот.")

@dp.message_handler(commands=['about'])
async def about_command(message: types.Message):
    about_text = "Я бот, созданный на основе технологии OpenAI GPT-3, чтобы помочь пользователям с вопросами и ответами. Моя основная цель - предоставлять полезную информацию и облегчать взаимодействие с пользователем."
    await message.reply(about_text)

# Функция добавления ответа в Google Sheets
def append_row_to_sheet(sheet_id, row_values, credentials_file):
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=scopes
        )
        service = discovery.build("sheets", "v4", credentials=credentials)

        body = {
            "range": "Sheet!A1",
            "majorDimension": "ROWS",
            "values": [row_values],
         }
        service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range="Sheet!A1",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body,
        ).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")

@dp.message_handler()
async def send_response(message: types.Message):
# Создайте промпт, который просит модель объяснить смысл текста
    prompt_with_context = f"Объясни смысл следующего сообщения от пользователя: '{message.text}'"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_with_context,
        temperature=1,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.5,
        stop=["You:"]
    )
# Обработка ответа модели и отправка сообщения пользователю
    bot_answer = response.choices[0].text.strip()
    await message.reply(bot_answer)

# Записываем сообщение пользователя и ответ бота в Google Sheets
    append_row_to_sheet(sheet_id, [message.text, bot_answer], credentials_file)

async def on_startup(dp):
    # Загрузить команды из файла bot_commands.json
    with open("cred.json", "r") as file:
        bot_commands = json.load(file)
        
    # Установить команды для бота
    await bot.set_my_commands([types.BotCommand(command["command"], command["description"]) for command in bot_commands])

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)