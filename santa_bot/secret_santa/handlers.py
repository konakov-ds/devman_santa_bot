#from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from collections import defaultdict
from datetime import datetime
from environs import Env
from telegram import KeyboardButton, ReplyKeyboardMarkup,\
    ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler,\
    Filters, MessageHandler

from secret_santa.models import SantaGame, Participant

env = Env()
env.read_env()

participants_info = defaultdict()
games_info = defaultdict()


START_GAME_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать игру'),
        ],
    ],
    resize_keyboard=True
)

GIFT_PRICE_LIMIT_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да'),
            KeyboardButton(text='Нет'),
        ],
    ],
    resize_keyboard=True
)

GIFT_PRICE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='До 500 рублей'),
            KeyboardButton(text='500-1000 рублей'),
            KeyboardButton(text='1000-2000 рублей'),
        ],
    ],
    resize_keyboard=True
)

REGISTRATION_DATE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='До 25.12.2021'),
            KeyboardButton(text='До 31.12.2021'),
        ],
    ],
    resize_keyboard=True
)


def start(update, context):
    message = update.message
    user_name = message.chat.first_name
    user_id = message.chat_id
    context.bot.send_message(
        chat_id=user_id,
        text=(
            f'Привет, {user_name}.🤚\n\n'
            'Организуй тайный обмен подарками, запусти праздничное настроение!'
        ),
        reply_markup=START_GAME_KEYBOARD
    )

    return 1


def ask_gift_price_limit(update, context):
    message = update.message
    user_id = message.chat_id
    context.bot.send_message(
        chat_id=user_id,
        text='Ограничение стоимости подарка?',
        reply_markup=GIFT_PRICE_LIMIT_KEYBOARD
    )

    return 2


def get_gift_price_limit(update, context):
    message = update.message
    user_id = message.chat_id
    if message.text == 'Нет':
        context.bot.send_message(
            chat_id=user_id,
            text=(
                'Период регистрации участников'
            ),
            reply_markup=REGISTRATION_DATE_KEYBOARD
        )
        return 4
    else:
        context.bot.send_message(
            chat_id=user_id,
            text='Выберите диапазон стоимости подарка',
            reply_markup=GIFT_PRICE_KEYBOARD
        )
        return 3


def save_gift_price_limit(update, context):
    message = update.message
    user_id = message.chat_id
    games_info[user_id] = {}
    if message.text == 'До 500 рублей':
        games_info[user_id]['gift_price_to'] = 500
    elif message.text == '500-1000 рублей':
        games_info[user_id]['gift_price_from'] = 500
        games_info[user_id]['gift_price_to'] = 1000
    else:
        games_info[user_id]['gift_price_from'] = 1000
        games_info[user_id]['gift_price_to'] = 2000
    context.bot.send_message(
        chat_id=user_id,
        text='Период регистрации участников',
        reply_markup=REGISTRATION_DATE_KEYBOARD
    )
    return 4


def get_game_registration_date(update, context):
    message = update.message
    user_id = message.chat_id
    if message.text == 'До 25.12.2021':
        games_info[user_id]['registration_limit'] = datetime(2021, 12, 25, 12, 0)
    else:
        games_info[user_id]['registration_limit'] = datetime(2021, 12, 31, 12, 0)

    context.bot.send_message(
        chat_id=user_id,
        text='Дата отправки подарка\n\nПример: 2022-01-03',
        reply_markup=ReplyKeyboardRemove()
    )
    return 5


def test(update, context):
    message = update.message
    user_id = message.chat_id
    # TODO проверка даты
    games_info[user_id]['sending_gift_limit'] = datetime.strptime(message.text, '%Y-%m-%d')
    print(games_info[user_id])

    bot_link = 'https://t.me/dvmn_team_santa_bot'
    param = '?start=santa001'
    context.bot.send_message(
        chat_id=user_id,
        text=f'Cсылка на вашу игру {bot_link + param}',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def help(update, context):
    update.message.reply_text("Справка по проекту")


def stop(update):
    update.message.reply_text("Стоп")
    return ConversationHandler.END


def start1(update, context):
    message = update.message
    user_id = message.chat_id
    param_value = context.args[0]
    if param_value == 'santa001':
        context.bot.send_message(
            chat_id=user_id,
            text='ДОБАВЛЯЙТЕСЬ В ИГРУ',
        )

        return 6


game_handler = ConversationHandler(

    entry_points=[CommandHandler('start', start)],

    states={
        1: [MessageHandler(Filters.text, ask_gift_price_limit)],
        2: [MessageHandler(Filters.text, get_gift_price_limit)],
        3: [MessageHandler(Filters.text, save_gift_price_limit)],
        4: [MessageHandler(Filters.text, get_game_registration_date)],
        5: [MessageHandler(Filters.text, test)],
    },

    fallbacks=[CommandHandler('stop', stop)]
)

participant_handler = ConversationHandler(

    entry_points=[CommandHandler('start', start1)],

    states={
        6: [MessageHandler(Filters.text, ask_gift_price_limit)],

    },

    fallbacks=[CommandHandler('stop', stop)]
)