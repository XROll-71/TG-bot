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
# Функция-обработчик команды /help
async def help(update, context):
    help_message = (
        "Список доступных команд:\n"
        "/start - Начать взаимодействие с ботом\n"
        "/help - Получить справку о доступных командах\n"
        "/gif - Получить случайную гифку\n"
        "/calc N - Посчитать сумму от 1 до N\n"
        "/calc_expr выражение - Решить математическое выражение"
    )
    await update.message.reply_text(help_message, reply_markup=get_main_keyboard_markup())

# Функция-обработчик команды /gif
async def send_gif(update, context):
    gif_url = get_random_gif()
    if gif_url:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=gif_url)
    else:
        await update.message.reply_text("Извините, не удалось получить гифку на данный момент.")

# Функция для получения случайной гифки из Giphy
def get_random_gif():
    giphy_api_key = "GNa1pdAQue70ircdkDwDTzZhQbz3o4pa"
    url = f"https://api.giphy.com/v1/gifs/random?api_key={giphy_api_key}&tag=&rating=g"

    response = requests.get(url)
    gif_data = response.json()
    logger.info("Giphy API response: %s", gif_data)

    if "data" in gif_data and "image_url" in gif_data["data"]:
        gif_url = gif_data["data"]["image_url"]
        return gif_url
    else:
        logger.error("Failed to get gif URL from Giphy API response")
        return None

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

# Функция-обработчик для любого сообщения, кроме "мне скучно"
async def reply_with_random_response(update, context):
    message_text = update.message.text.lower()
    if "мне скучно" not in message_text:
        random_response = random.choice(random_responses)
        await update.message.reply_text(random_response, reply_markup=get_main_keyboard_markup())



# Функция для получения разметки клавиатуры с кнопками /gif и /help
def get_main_keyboard_markup():
    keyboard = [
        [InlineKeyboardButton("Получить случайную гифку", callback_data='gif')],
        [InlineKeyboardButton("Помощь", callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)
