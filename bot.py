from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from telegram import Chat as TGChat

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я бот!")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def main():
    updater = Updater(token='6007270444:AAHREzJ4nfr-GRIOd7k9wi4q5tFq8scEUuM', use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()


if __name__ == '__main__':
    main()