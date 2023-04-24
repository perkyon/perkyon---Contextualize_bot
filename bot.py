import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# Здесь введите токен вашего бота
token = '6007270444:AAHREzJ4nfr-GRIOd7k9wi4q5tFq8scEUuM'

# Здесь введите ваш API-ключ OpenAI
openai.api_key = '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'

# Диспетчер
bot = Bot(token)
dp = Dispatcher(bot)

# Функции бота
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я ваш телеграм-бот.")

@dp.message_handler()
async def send_response(message: types.Message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text, 
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["You:"]
    )
    await message.answer(response['choices'][0]['text'])

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)