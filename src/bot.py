import telebot
from telebot import types
from config import BOT_TOKEN
from client import Client, ClientResult

bot = telebot.TeleBot(BOT_TOKEN)


def get_main_buttons():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text="Добавить сессию")
    button2 = types.KeyboardButton(text="Все сессии")

    keyboard.add(button1, button2)
    return keyboard


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Здравствуйте, это тестовый бот.", reply_markup=get_main_buttons())


@bot.message_handler(func=lambda message: message.text == "Добавить сессию")
def add_session(message):
    msg = bot.reply_to(message, "Введите номер телефона.")
    bot.register_next_step_handler(msg, number)


@bot.message_handler(func=lambda message: message.text == "Все сессии")
def get_all_sessions(message):
    sessions = Client().all_sessions
    bot.reply_to(message, '\n'.join(sessions))


def number(message):
    phone = message.text
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Правильно', callback_data='phone_yes'+phone),
        types.InlineKeyboardButton('Не правильно', callback_data=f'phone_no')
    )
    bot.send_message(chat_id, f'Убедитесь в верности телефона:\nТелефон: {phone}', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('phone_yes'))
def phone_yes(message):
    phone = message.data.split('phone_yes')[1]
    client = Client(phone)
    if not client.is_authorized:
        auth = client.authorization()
        print(auth)
        if auth == ClientResult.SEND_CODE_SUCCESS:
            msg = bot.reply_to(message.message, 'Код успешно отправлен. Введите код который вам отправлен')
            bot.register_next_step_handler(msg, code_confirm, client)
        elif auth == ClientResult.SOME_ERROR:
            bot.reply_to(message.message, 'Убедитесь в правильности введенного телефона')
    else:
        bot.reply_to(message.message, 'Сессия с таким номером уже создано')


def code_confirm(message, client):
    client_result = client.set_code(message.text)
    print(client_result)
    if client_result == ClientResult.LOGIN_SUCCESS:
        bot.reply_to(message, 'Сессия создано')
    elif client_result == ClientResult.INVALID_CODE:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button1 = types.KeyboardButton(text="Добавить сессию")
        keyboard.add(button1)
        msg = bot.reply_to(message, 'Не правельный код', reply_markup=keyboard)
    elif client_result == ClientResult.SOME_ERROR:
        msg = bot.reply_to(message, 'Убедитесь в правильности веденных данных')
    elif client_result == ClientResult.CODE_EXPIRED:
        msg = bot.reply_to(message, 'Срок кода истек')
    bot.register_next_step_handler(msg, incorrect_code, client)


def incorrect_code(message, client):
    msg = bot.reply_to(message, 'введите еще раз код')
    bot.register_next_step_handler(msg, code_confirm, client)


@bot.callback_query_handler(func=lambda call: call.data == 'phone_no')
def phone_no(message):
    msg = bot.reply_to(message.message, 'Введите номер телефона')
    bot.register_next_step_handler(msg, number)


@bot.message_handler(func=lambda message: True)
def all_text_handler(message):
	bot.reply_to(message, "Я не знаю что ответить на это. Выберите пожалуйста одну из нижепредставленных кнопок.", reply_markup=get_main_buttons())

