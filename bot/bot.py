import telebot
from telebot import types

TOKEN = "token"
bot = telebot.TeleBot(TOKEN)

products = {
    "холодильник1": {"name": "Холодильник Samsung RL55", "description": "Отличный холодильник с No Frost", "price": 35000, "image": "url_изображения_холодильника1"},
    "стиралка1": {"name": "Стиральная машина Bosch Serie 6", "description": "Надежная стиральная машина с инверторным двигателем", "price": 28000, "image": "url_изображения_стиралки1"},
    "плита1": {"name": "Газовая плита Gefest 6100", "description": "Простая и надежная газовая плита", "price": 15000, "image": "url_изображения_плиты1"},
}

# Функция для отправки информации о товаре
def send_product(chat_id, product_id):
    if product_id in products:
        product = products[product_id]
        name = product["name"]
        description = product["description"]
        price = product["price"]
        # TODO: Отправка изображения товара (требует отдельной библиотеки и настройки)
        message = f"*{name}*\n\n{description}\n\nЦена: {price} руб."
        bot.send_message(chat_id, message, parse_mode="Markdown")  # Используем Markdown для форматирования
    else:
        bot.send_message(chat_id, "Товар не найден.")


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Просмотреть товары")
    item2 = types.KeyboardButton("Помощь")
    keyboard.add(item1, item2)
    bot.send_message(message.chat.id, "Добро пожаловать в магазин бытовой техники!", reply_markup=keyboard)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.text == "Просмотреть товары":
        show_products(message)
    elif message.text == "Помощь":
        bot.send_message(message.chat.id, "Доступные команды: \n\nПросмотреть товары - просмотр доступных товаров.")
    else:
        bot.send_message(message.chat.id, "Я не понимаю эту команду.")

# Обработчик команды /products
@bot.message_handler(commands=['products'])
def show_products(message):
          keyboard = types.InlineKeyboardMarkup(row_width=2)
          for product_id, product in products.items():
              button = types.InlineKeyboardButton(text=product["name"], callback_data=f"product_{product_id}")
        keyboard.add(button)
    bot.send_message(message.chat.id, "Выберите товар:", reply_markup=keyboard)


# Обработчик CallbackQuery (нажатия на кнопки)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswith("product_"):
        product_id = call.data[8:]  # Извлекаем ID товара из callback_data
        send_product(call.message.chat.id, product_id)


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()    
