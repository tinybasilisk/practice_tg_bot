from telebot.types import Message
from loader import bot
from states.user_states import UserState
from database.models import Task


@bot.message_handler(state=UserState.tasks_make_done)
def process_task_done(message: Message) -> None:
    if not message.text.isdigit():
        bot.send_message(message.from_user.id, "ID задачи должен быть числом.\nВведите номер задачи, чтобы изменить её статус.")
        return
    task_id = int(message.text)
    task = Task.get_or_none(Task.task_id == task_id)
    if task is None:
        bot.send_message(message.from_user.id, "Задачи с таким ID не существует.\nВведите корректный номер задачи, чтобы изменить её статус.")
        return
    if task.user.user_id != message.from_user.id:
        bot.send_message(
            message.from_user.id, "Вы не являетесь владельцем данной задачи.\nВведите номер вашей задачи, чтобы изменить её статус."
        )
        return
    task.is_done = not task.is_done
    task.save()
    bot.send_message(message.from_user.id, task)
    bot.delete_state(message.from_user.id)
