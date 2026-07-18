from loader import bot
from utils.set_bot_commands import set_default_commands
from database.models import create_models
from telebot.custom_filters import StateFilter
import handlers # noqa: F401


if __name__ == "__main__":
    create_models()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()

