import os
from django.core.management.base import BaseCommand
from environs import Env
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, Updater
from secret_santa.handlers import game_handler, participant_handler


env = Env()
env.read_env()

tg_token = env('TELEGRAM_TOKEN')


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        updater = Updater(tg_token, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(game_handler)
        dispatcher.add_handler(participant_handler)

        updater.start_polling()
        updater.idle()
