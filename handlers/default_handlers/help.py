from loader import bot
from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {desc}" for command, desc in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
