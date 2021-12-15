import os
from django.core.management.base import BaseCommand
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, Updater


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # updater = Updater(token, use_context=True)
        # dispatcher = updater.dispatcher
        print('Hello Santa!')

        # updater.start_polling()
        # updater.idle()
