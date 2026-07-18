from telebot.types import Message
from loader import bot
from states.user_states import UserState
from database.models import Task, User
from typing import List


@bot.message_handler(commands=["tasks"])
def handle_tasks(message: Message) -> None:
    user_id = message.from_user.id
    user = User.get_or_none(User.user_id == user_id)
    if user is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return

    tasks: List[Task] = user.tasks.order_by(-Task.due_date, -Task.task_id).limit(10)

    result = []
    result.extend(map(str, reversed(tasks)))

    if not result:
        bot.send_message(message.from_user.id, "У вас ещё нет задач")
        return

    result.append("\nВведите номер задачи, чтобы изменить её статус.")
    bot.send_message(message.from_user.id, "\n".join(result))
    bot.set_state(message.from_user.id, UserState.tasks_make_done, message.chat.id)