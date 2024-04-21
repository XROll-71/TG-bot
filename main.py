import logging
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import random

# Запускаем логгирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция-обработчик команды /start
async def start(update, context):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(
        f"Привет, {user_name}! Я бот от DDCompany. Рад вас видеть!",
        reply_markup=get_main_keyboard_markup()
    )
    
# Список рандомных фраз
random_responses = [
    "Привет!",
    "Как дела?",
    "Погода сегодня прекрасная!",
    "Давайте пообщаемся!",
    "Чем могу помочь?",
    "Я здесь, чтобы помочь вам!",
    "Случайный ответ на ваше сообщение!"
]

# Функция для получения разметки клавиатуры с кнопками /gif и /help
def get_main_keyboard_markup():
    keyboard = [
        [InlineKeyboardButton("Получить случайную гифку", callback_data='gif')],
        [InlineKeyboardButton("Помощь", callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)
