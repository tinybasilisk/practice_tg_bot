from telebot.types import Message
from loader import bot
from database.models import User, Task
from states.user_states import UserState
from config_data.config import DATE_FORMAT
import datetime


@bot.message_handler(commands=["newtask"])
def handle_new_task(message: Message) -> None:
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return
    bot.send_message(user_id, "Введите название задачи")
    bot.set_state(message.from_user.id, UserState.new_task_title, message.chat.id)
    with bot.retrieve_data(message.from_user.id) as data:
        data["new_task"] = {"user_id": user_id}


@bot.message_handler(state=UserState.new_task_title)
def process_task_title(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id) as data:
        data["new_task"]["title"] = message.text
    bot.set_state(message.from_user.id, UserState.new_task_due_date, message.chat.id)
    bot.send_message(message.from_user.id, "Введите дату (ДД.ММ.ГГГГ):")

@bot.message_handler(state=UserState.new_task_due_date)
def process_task_due_date(message: Message) -> None:
    due_date_string = message.text
    try:
        due_date = datetime.datetime.strptime(due_date_string, DATE_FORMAT)
    except ValueError:
        bot.send_message(message.from_user.id, "Введите дату (ДД.ММ.ГГГГ):")
        return

    with bot.retrieve_data(message.from_user.id) as data:
        data["new_task"]["due_date"] = due_date

    new_task = Task(**data["new_task"])
    new_task.save()
    bot.send_message(message.from_user.id, f"Задача добавлена:\n{new_task}")
    bot.delete_state(message.from_user.id)
