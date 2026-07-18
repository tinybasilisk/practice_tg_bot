from telebot.types import Message
from loader import bot
from states.user_states import UserState
from database.models import Task, User
from typing import List
import datetime


@bot.message_handler(commands=["today"])
def handle_today(message: Message) -> None:
    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)
    if user is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    tasks: List[Task] = user.tasks.where(Task.due_date == datetime.date.today())

    result = []
    result.extend(map(str, tasks))

    if not result:
        bot.send_message(message.from_user.id, "У вас ещё нет задач")
        return

    result.append("\nВведите номер задачи, чтобы изменить её статус.")
    bot.send_message(message.from_user.id, "\n".join(result))
    bot.set_state(message.from_user.id, UserState.tasks_make_done, message.chat.id)