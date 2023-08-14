from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def start_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)

    about = InlineKeyboardButton(text='❓ О боте', callback_data='about')
    view = InlineKeyboardButton(text='🔁 Сменить вид меню', callback_data='view')
    converter = InlineKeyboardButton(text='💰 Конвертор валют', callback_data='converter')
    calculator = InlineKeyboardButton(text='🧮 Калькулятор', callback_data='calculator')
    my_location = InlineKeyboardButton(text='🗺 Моя локация', callback_data='my_location')
    review = InlineKeyboardButton(text='📒 Отзывы и предложения', callback_data='review')
    dev = InlineKeyboardButton(text='🖌 Написать разработчику', callback_data='dev')
    updates = InlineKeyboardButton(text='📄 Обновления', callback_data='updates')

    keyboard.add(about)
    keyboard.add(view)
    keyboard.add(converter)
    keyboard.add(calculator)
    keyboard.add(my_location)
    keyboard.add(review)
    keyboard.add(dev)
    keyboard.add(updates)

    return keyboard


def review_buttons():
    keyboard = InlineKeyboardMarkup(row_width=1)

    leave_review = InlineKeyboardButton(text='🖌 Оставить отзыв', callback_data='leave_review')
    leave_suggestion = InlineKeyboardButton(text='🖌 Написать предложение', callback_data='leave_suggestion')

    keyboard.add(leave_review)
    keyboard.add(leave_suggestion)

    return keyboard


def location_button():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    location = KeyboardButton('Поделиться локация', request_location=True)

    keyboard.add(location)

    return keyboard
