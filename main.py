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

# Функция-обработчик для обработки нажатий на кнопки клавиатуры
async def button_click(update, context):
    query = update.callback_query
    if query.data == 'gif':
        await send_gif(update, context)
    elif query.data == 'help':
        await help(update, context)

async def count_to(update, context):
    try:
        # Получаем аргумент из сообщения (который должен содержать число)
        count_to_number = int(context.args[0])
        if count_to_number > 0:
            # Считаем от 1 до заданного числа и отправляем сообщение с результатом
            count_result = '\n'.join(str(i) for i in range(1, count_to_number + 1))
            await update.message.reply_text(f"От 1 до {count_to_number}:\n{count_result}")
        else:
            await update.message.reply_text("Число должно быть положительным.")
    except (IndexError, ValueError):
        await update.message.reply_text("Пожалуйста, укажите положительное число после команды /count.")

async def calculator(update, context):
    try:
        number = int(context.args[0])
        result = sum(range(1, number + 1))
        await update.message.reply_text(f"Сумма от 1 до {number} равна {result}")
    except (IndexError, ValueError):
        await update.message.reply_text("Использование: /calc N, где N - целое положительное число.")

# Функция калькулятора для вычисления математических выражений
async def calculate_expression(update, context):
    try:
        expr = ' '.join(context.args)
        result = eval(expr)
        await update.message.reply_text(f"Результат выражения '{expr}' равен {result}")
    except Exception as e:
        await update.message.reply_text("Ошибка при вычислении выражения.")

async def handle_message(update, context):
    message_text = update.message.text.lower()
    if "мне скучно" in message_text:
        await update.message.reply_text("Я знаю, что делать 😉", reply_markup=get_youtube_button())
    else:
        random_response = random.choice(random_responses)
        await update.message.reply_text(random_response, reply_markup=get_main_keyboard_markup())

# Функция для создания кнопки с ссылкой на YouTube
def get_youtube_button():
    keyboard = [
        [InlineKeyboardButton("Перейти на YouTube", url="https://www.youtube.com/")]
    ]
    return InlineKeyboardMarkup(keyboard)

def main():
    # Создаём объект Application с использованием токена
    application = Application.builder().token("5620066176:AAF90Pk79HdfdiJ1p91F5MyW_ecct7qxP70").build()

    # Создаём обработчик команды /start
    start_handler = CommandHandler("start", start)

    # Создаём обработчик команды /help
    help_handler = CommandHandler("help", help)

    # Создаём обработчик команды /gif
    gif_handler = CommandHandler("gif", send_gif)

    # Создаём обработчик для любого сообщения
    message_handler = MessageHandler(filters.Text() & ~filters.Command(), reply_with_random_response)

    # Создаём обработчик для нажатий на кнопку /gif
    gif_button_handler = CallbackQueryHandler(button_click, pattern="^gif$")

    # Создаём обработчик для нажатий на кнопку /help
    help_button_handler = CallbackQueryHandler(button_click, pattern="^help$")

    count_handler = CommandHandler("count", count_to)

    calc_handler = CommandHandler("calc", calculator)

    # Создаём обработчик команды /calc_expr
    calc_expr_handler = CommandHandler("calc_expr", calculate_expression)
    message_handler = MessageHandler(filters.Text() & ~filters.Command(), handle_message)

# Регистрируем обработчики в приложении
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(gif_handler)
    application.add_handler(message_handler)
    application.add_handler(gif_button_handler)
    application.add_handler(help_button_handler)
    application.add_handler(count_handler)
    application.add_handler(calc_handler)
    application.add_handler(calc_expr_handler)

    application.run_polling()

# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
