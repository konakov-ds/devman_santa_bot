# from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from collections import defaultdict
import uuid
from datetime import datetime
from environs import Env
from telegram import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler, \
    Filters, MessageHandler

from secret_santa.models import SantaGame, Participant

env = Env()
env.read_env()

participants_info = defaultdict()
games_info = defaultdict()
param_value = defaultdict()

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

BECOME_SANTA_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Стать сантой'),
        ],
    ],
    resize_keyboard=True
)


def start(update, context):
    message = update.message
    user_name = message.chat.first_name
    user_id = message.chat_id
    if context.args:
        param_value[user_id] = []
        param_value[user_id].append(context.args[0])
        update.message.reply_text(
            text='***** HAPPY NEW YEAR *****',
            reply_markup=BECOME_SANTA_KEYBOARD
        )
        ConversationHandler.END
    else:
        context.bot.send_message(
            chat_id=user_id,
            text=(
                f'Привет, {user_name}.🤚\n\n'
                'Организуй тайный обмен подарками, запусти праздничное настроение!'
            ),
            reply_markup=START_GAME_KEYBOARD
        )

        return 1


def ask_game_name(update, context):
    message = update.message
    user_id = message.chat_id
    context.bot.send_message(
        chat_id=user_id,
        text='Придумайте название для игры',
        reply_markup=ReplyKeyboardRemove()
    )

    return 2


def ask_gift_price_limit(update, context):
    message = update.message
    user_id = message.chat_id
    games_info[user_id] = {}
    games_info[user_id]['game_id'] = uuid.uuid4().hex
    games_info[user_id]['name'] = message.text
    context.bot.send_message(
        chat_id=user_id,
        text='Ограничение стоимости подарка?',
        reply_markup=GIFT_PRICE_LIMIT_KEYBOARD
    )

    return 3


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
        return 5
    else:
        context.bot.send_message(
            chat_id=user_id,
            text='Выберите диапазон стоимости подарка',
            reply_markup=GIFT_PRICE_KEYBOARD
        )
        return 4


def save_gift_price_limit(update, context):
    message = update.message
    user_id = message.chat_id
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
    return 5


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
    return 6


def get_description_of_the_game(update, context):
    user = update.effective_user
    user_name = user.first_name
    user_id = update.message.chat_id
    participants_info[user_id] = {}

    game = SantaGame.objects.get(game_id=param_value[user_id][-1])

    context.bot.send_message(
        chat_id=user_id,
        text=(
            f'Привет, {user_name}.\n\n'
            f'Замечательно, ты собираешься участвовать в игре:'
            f'{game.name}\n'
            f'Ограничение стоимости подарка: от {game.gift_price_from} до {game.gift_price_to}\n'
            f'Период регистрации: {game.registration_limit}\n'
            f'Дата отправки подарков: {game.sending_gift_limit}\n\n'
            f'Пожалуйста, введите Ваше имя:\n'

        ),
        reply_markup=ReplyKeyboardRemove()
    )

    return 22


def get_participant_name(update, context):
    message = update.message
    user_id = message.chat_id
    participants_info[user_id]['name'] = message.text

    context.bot.send_message(
        chat_id=user_id,
        text=(
            f'Пожалуйста, введите Ваш адрес электронной почты:\n'
        ),
    )

    return 23


def get_participant_email(update, context):
    message = update.message
    user_id = message.chat_id
    participants_info[user_id]['email'] = message.text

    context.bot.send_message(
        chat_id=user_id,
        text=(
            f'Пожалуйста, введите Ваши пожелания и интересы:\n'
        ),
    )

    return 24


def get_participant_wish_list(update, context):
    message = update.message
    user_id = message.chat_id
    participants_info[user_id]['wish_list'] = message.text

    context.bot.send_message(
        chat_id=user_id,
        text=(
            f'Пожалуйста, напишите письмо Санте:\n'
        ),
    )

    return 25


def get_participant_letter_to_santa(update, context):
    message = update.message
    user_id = message.chat_id
    participants_info[user_id]['note_for_santa'] = message.text

    participant = Participant.objects.create(
        tg_id=user_id,
        game=SantaGame.objects.get(game_id=param_value[user_id][-1])
    )

    participant.note_for_santa = message.text
    participant.name = participants_info[user_id]['name']
    participant.email = participants_info[user_id]['email']
    participant.wish_list = participants_info[user_id]['wish_list']
    participant.save()

    context.bot.send_message(
        chat_id=user_id,
        text=(
            f'Превосходно, ты в игре!'
            f'{participant.game.registration_limit} мы проведем жеребьевку'
            f' и ты узнаешь имя и контакты своего тайного друга. Ему и нужно будет подарить подарок!'

        ),
    )


def save_game_to_db(user_id):
    SantaGame.objects.create(
        game_id=games_info[user_id]['game_id'],
        name=games_info[user_id]['name'],
        registration_limit=games_info[user_id].get('registration_limit'),
        sending_gift_limit=games_info[user_id].get('sending_gift_limit'),
        gift_price_from=games_info[user_id].get('gift_price_from'),
        gift_price_to=games_info[user_id].get('gift_price_to')
    )
    print(SantaGame.objects.get(game_id=games_info[user_id]['game_id']))


def test(update, context):
    message = update.message
    user_id = message.chat_id
    # TODO проверка даты
    games_info[user_id]['sending_gift_limit'] = datetime.strptime(message.text, '%Y-%m-%d')

    # bot_link = 'https://t.me/dvm_bot_santa_bot'  ссылка для бота Ростислава
    bot_link = 'https://t.me/dvmn_team_santa_bot'
    param = f'?start={games_info[user_id]["game_id"]}'
    context.bot.send_message(
        chat_id=user_id,
        text=f'Cсылка на вашу игру {bot_link + param}',
        reply_markup=ReplyKeyboardRemove()
    )
    save_game_to_db(user_id)
    games_info[user_id] = {}
    return ConversationHandler.END


def help(update, context):
    update.message.reply_text("Справка по проекту")


def stop(update):
    update.message.reply_text("Стоп")
    return ConversationHandler.END


game_handler = ConversationHandler(

    entry_points=[CommandHandler('start', start)],

    states={
        1: [MessageHandler(Filters.text, ask_game_name)],
        2: [MessageHandler(Filters.text, ask_gift_price_limit)],
        3: [MessageHandler(Filters.text, get_gift_price_limit)],
        4: [MessageHandler(Filters.text, save_gift_price_limit)],
        5: [MessageHandler(Filters.text, get_game_registration_date)],
        6: [MessageHandler(Filters.text, test)],
    },

    fallbacks=[CommandHandler('stop', stop)]
)

participant_handler = ConversationHandler(

    entry_points=[MessageHandler(Filters.text('Стать сантой'), get_description_of_the_game)],

    states={

        22: [MessageHandler(Filters.text, get_participant_name)],
        23: [MessageHandler(Filters.text, get_participant_email)],
        24: [MessageHandler(Filters.text, get_participant_wish_list)],
        25: [MessageHandler(Filters.text, get_participant_letter_to_santa)],

    },

    fallbacks=[CommandHandler('stop', stop)]
)
