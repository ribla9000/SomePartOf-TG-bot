from telegram.ext import CommandHandler, ChatMemberHandler, Application
from repository.bot_chat import check_chat_members


def add_handlers(application: Application):
    application.add_handler(ChatMemberHandler(check_chat_members, ChatMemberHandler.CHAT_MEMBER))
