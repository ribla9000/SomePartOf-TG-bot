import datetime
from repository.bot_menu import check_auth
from core.config import SETTINGS, BACK_BUTTON_TEXT, START_MENU
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler


class StatisticsMenu:

    @staticmethod
    @check_auth
    async def get_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        keyboard = [
            [InlineKeyboardButton(text="Bots🤖", callback_data=SETTINGS[1]),
             InlineKeyboardButton(text="Channels🌈", callback_data=SETTINGS[2])],
            [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[0])]
        ]
        await query.edit_message_text(text="Statistics menuㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ",
                                      reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END