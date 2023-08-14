import telebot
from telebot.types import ReplyKeyboardRemove

import requests
from geopy.geocoders import Nominatim

import buttons
import database
import texts

bot = telebot.TeleBot('5839487510:AAHgDvsP-fdQiBo6DoF7CXXwfWc4AhJ0hN0')

geolocator = Nominatim(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
               'Safari/537.36')


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id

    checker = database.check_user(user_id)

    if checker:
        if database.user_menu_view(user_id) == 'text':
            bot.send_message(user_id,
                             texts.text_menu)

        else:
            bot.send_message(user_id,
                             'Выберите пункт меню',
                             reply_markup=buttons.start_buttons())

    else:
        bot.send_message(user_id,
                         'Добро пожаловать!\n\nВведите имя или никнейм для регистрации.')
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    user_id = message.from_user.id
    nickname = message.text

    if message.from_user.last_name is None:
        surname = ''
        surname_in_text = ''

    else:
        surname = message.from_user.last_name
        surname_in_text = ' ' + message.from_user.last_name

    database.register_user(user_id, nickname,
                           message.from_user.first_name,
                           surname,
                           message.from_user.username,
                           'text')

    bot.send_message(user_id,
                     'Вы успешно зарегистрированы.\nОтличного использования бота!')

    bot.send_message(-1001942585169,
                     f'Новый пользователь!\n\n'
                     f'{nickname} ({message.from_user.first_name}{surname_in_text}) – @{message.from_user.username}')

    about(message)


@bot.message_handler(commands=['about'])
def about(message):
    user_id = message.chat.id
    bot.send_message(user_id,
                     texts.about_text)

    start_message(message)


@bot.message_handler(commands=['view'])
def view(message):
    user_id = message.chat.id

    if database.user_menu_view(user_id) == 'text':
        bot.delete_message(user_id, message.id)
        bot.delete_message(user_id, message.id - 1)

    else:
        bot.delete_message(user_id, message.id)

    database.swap_user_menu_view(user_id, database.user_menu_view(user_id))
    start_message(message)


@bot.message_handler(commands=['review'])
def review(message):
    user_id = message.chat.id
    message_id = message.id

    bot.delete_message(user_id, message_id)

    bot.send_message(user_id,
                     'Выберите пункт меню',
                     reply_markup=buttons.review_buttons())


@bot.message_handler(commands=['dev'])
def dev(message):
    user_id = message.chat.id

    bot.delete_message(user_id, message.id)
    bot.send_message(user_id,
                     'Разработчик – @prof1exx')
    bot.send_message(user_id,
                     'Выберите пункт меню',
                     reply_markup=buttons.start_buttons())


@bot.message_handler(commands=['updates'])
def updates(message):
    user_id = message.chat.id

    bot.delete_message(user_id, message.id)
    bot.send_message(user_id,
                     texts.updates_text)
    bot.send_message(user_id,
                     'Выберите пункт меню',
                     reply_markup=buttons.start_buttons())


@bot.message_handler(commands=['calculator'])
def calculator(message):
    user_id = message.chat.id

    expression = message.text

    if '__import__' not in expression:
        try:
            if '^' in expression:
                expression = expression.replace('^', '**')

            result = eval(expression)

            if result % 10 == 0:
                print('a')
                bot.send_message(user_id, str(int(result)))
            else:
                bot.send_message(user_id, result)

        except:
            bot.send_message(user_id,
                             'Неправильное выражение')
    else:
        bot.send_message(user_id,
                         'Неправильное выражение')

    bot.send_message(user_id,
                     'Выберите пункт меню',
                     reply_markup=buttons.start_buttons())


@bot.message_handler(commands=['my_location'])
def my_location(message):
    user_id = message.from_user.id

    latitude = message.location.latitude
    longitude = message.location.longitude

    address = geolocator.reverse((latitude, longitude), language='ru').address

    bot.send_message(user_id,
                     f'Ваш адрес местоположения:\n\n{address}',
                     reply_markup=ReplyKeyboardRemove())

    start_message(message)


@bot.message_handler(commands=['converter'])
def converter(message):
    user_id = message.chat.id

    web_site = requests.get("https://cbu.uz/ru/arkhiv-kursov-valyut/json/")
    currency_list = web_site.json()

    currencies_text = f'{currency_list[0]["CcyNm_RU"]} – {currency_list[0]["Rate"]} сумм\n' \
                      f'{currency_list[1]["CcyNm_RU"]} – {currency_list[1]["Rate"]} сумм\n' \
                      f'{currency_list[2]["CcyNm_RU"]} – {currency_list[2]["Rate"]} сумм\n' \
                      f'{currency_list[3]["CcyNm_RU"]} – {currency_list[3]["Rate"]} сумм\n'
    bot.send_message(user_id,
                     currencies_text)

    start_message(message)


def leave_review(message):
    user_id = message.chat.id

    bot.send_message(user_id,
                     'Спасибо за отзыв!')

    if message.from_user.last_name is None:
        surname_in_text = ''

    else:
        surname_in_text = ' ' + message.from_user.last_name

    bot.send_message(-1001942585169,
                     f'Новый отзыв!\n\n'
                     f'{message.text}\n\n'
                     f'{database.get_nickname(user_id)} ({message.from_user.first_name}{surname_in_text}) – '
                     f'@{message.from_user.username}')

    start_message(message)


def leave_suggestion(message):
    user_id = message.chat.id
    bot.send_message(user_id,
                     'Спасибо за предложение!')

    if message.from_user.last_name is None:
        surname_in_text = ''

    else:
        surname_in_text = ' ' + message.from_user.last_name

    bot.send_message(-1001942585169,
                     f'Новое предложение!\n\n'
                     f'{message.text}\n\n'
                     f'{database.get_nickname(user_id)} ({message.from_user.first_name}{surname_in_text}) – '
                     f'@{message.from_user.username}')
    start_message(message)


@bot.callback_query_handler(lambda call: call.data in ['about', 'view',
                                                       'converter', 'calculator', 'my_location',
                                                       'review', 'dev', 'updates'])
def start_buttons_handler(call):
    user_id = call.message.chat.id

    if call.data == 'about':
        about(call.message)

    elif call.data == 'view':
        view(call.message)

    elif call.data == 'converter':
        converter(call.message)

    elif call.data == 'calculator':
        bot.send_message(user_id,
                         texts.calculator_text)
        bot.register_next_step_handler(call.message, calculator)

    elif call.data == 'my_location':
        bot.send_message(user_id,
                         'Отправьте локацию',
                         reply_markup=buttons.location_button())

        # Переход на сохранение локации
        bot.register_next_step_handler(call.message, my_location)

    elif call.data == 'review':
        review(call.message)

    elif call.data == 'dev':
        dev(call.message)

    elif call.data == 'updates':
        updates(call.message)


@bot.callback_query_handler(lambda call: call.data in ['leave_review', 'leave_suggestion'])
def review_handler(call):
    user_id = call.message.chat.id

    if call.data == 'leave_review':
        bot.send_message(user_id,
                         'Оставьте отзыв написав его в сообщении, затем отправив его.')
        bot.register_next_step_handler(call.message, leave_review)

    elif call.data == 'leave_suggestion':
        bot.send_message(user_id,
                         'Оставьте отзыв написав его в сообщении, затем отправив его.')
        bot.register_next_step_handler(call.message, leave_suggestion)


bot.polling()
