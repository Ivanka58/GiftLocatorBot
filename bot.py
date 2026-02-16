import telebot
from telebot import types

# Токен бота
TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения данных пользователя
user_data = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Найти подарок")
    markup.add(item)
    bot.send_message(message.chat.id, "Привет! Этот бот помогает найти определенный подарок в профиле, нажми кнопку ниже ⏬", reply_markup=markup)

# Обработчик кнопки "Найти подарок"
@bot.message_handler(func=lambda message: message.text == "Найти подарок")
def find_gift(message):
    bot.send_message(message.chat.id, "Пришли мне ссылку на профиль")
    bot.register_next_step_handler(message, get_profile_link)

# Получение ссылки на профиль
def get_profile_link(message):
    user_data[message.chat.id] = {"profile_link": message.text}
    bot.send_message(message.chat.id, "Теперь укажи название подарка")
    bot.register_next_step_handler(message, get_gift_name)

# Получение названия подарка
def get_gift_name(message):
    user_data[message.chat.id]["gift_name"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Модель")
    item2 = types.KeyboardButton("Узор")
    item3 = types.KeyboardButton("Фон")
    item4 = types.KeyboardButton("Готово ☑️")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Отлично! Теперь укажи что именно тебя интересует", reply_markup=markup)
    bot.register_next_step_handler(message, get_gift_criteria)

# Получение критериев поиска
def get_gift_criteria(message):
    if message.text == "Готово ☑️":
        search_gifts(message)
    else:
        user_data[message.chat.id]["criteria"] = message.text
        bot.send_message(message.chat.id, f"Укажи название {message.text}")
        bot.register_next_step_handler(message, get_criteria_value)

# Получение значения критерия
def get_criteria_value(message):
    user_data[message.chat.id][user_data[message.chat.id]["criteria"]] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Модель")
    item2 = types.KeyboardButton("Узор")
    item3 = types.KeyboardButton("Фон")
    item4 = types.KeyboardButton("Готово ☑️")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, f"{user_data[message.chat.id]['criteria']} {message.text} добавлены! Это все или хочешь чтото еще?", reply_markup=markup)
    bot.register_next_step_handler(message, get_gift_criteria)

# Поиск подарков
def search_gifts(message):
    # Здесь должна быть логика поиска подарков по указанным критериям
    # Пример:
    gifts = ["https://example.com/gift1", "https://example.com/gift2", "https://example.com/gift3"]
    bot.send_message(message.chat.id, "Ищу подарки 🔎...")
    for gift in gifts:
        bot.send_message(message.chat.id, gift)
    bot.send_message(message.chat.id, "Спасибо за использование бота! Создал - @Ivanka58")

# Запуск бота
bot.polling(none_stop=True)
