# from logging import getLogger
# from ..echo.config import load_config

from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request

from chatacc.models import Message
from chatacc.models import Profile

# Region for LOGGER
# config = load_config()
# logger = getLogger(__name__)
# end of region


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    name = update.message.from_user.first_name

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    Message(
        profile=p,
        text=text,
    ).save()

    reply_text = "{}, я получил от тебя сообщение:\n{}".format(name, text)
    update.message.reply_text(
        text=reply_text,
    )


@log_errors
def do_count(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    count = Message.objects.filter(profile=p).count()

    update.message.reply_text(
        text=f'У Вас {count} сообщений',
    )


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        # 1--getting connected
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.BOT_TOKEN,
            base_url=settings.BOT_URL,
        )
        print(bot.get_me())
        # end of region -- getting connected

        # 2--updaters
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)
        # end of region -- updaters

        message_handler2 = CommandHandler('count', do_count)
        updater.dispatcher.add_handler(message_handler2)

        # 3--ignite the limitless handler of incoming messages
        updater.start_polling()
        updater.idle()
        # end of region -- limitless handler

# Region for BUTTONS
