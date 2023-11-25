import os
from core.config import START_MENU, SETTINGS, CHANNELS, AUTOCOMMENT, BACK_BUTTON_TEXT
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from repository.tools import keyboard_cols
from repository.user_channels import UserChannelsRepository
from repository.channels_menu import ChannelsMenu


class AutoCommentMenu:

    @staticmethod
    async def get_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        keyboard = [
            [InlineKeyboardButton(text="Channels", callback_data=AUTOCOMMENT[0]),
             InlineKeyboardButton(text="Status", callback_data=AUTOCOMMENT[1]),
             InlineKeyboardButton(text="Settings", callback_data=AUTOCOMMENT[2])],
            [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[0])]
        ]
        await query.edit_message_text(text="Autocomment Menu", reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    async def get_autocomment_channels(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
                #ribla9000

    @staticmethod
    async def add_autocomment_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
                #ribla9000

    @staticmethod
    async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
                #ribla9000

    @staticmethod
    async def get_channel_settings(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        is_active = True
        keyboard = [
            [InlineKeyboardButton(text="Enable/Disable", callback_data=f"remove_channel,{data[1]}")],
            [InlineKeyboardButton(text="Remove", callback_data=f"autocomment,{data[1]}")],
            [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[0])]
        ]
        await query.edit_message_text(text=f"Settings of '{data[0]}'", reply_markup=InlineKeyboardMarkup(keyboard))
        return "get_choice_of_channel_settings"

    @staticmethod
    async def get_choice_of_channel_settings(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        data = query.data.split(",")
        await query.answer()
        if data[0] == "toggle_channel":
            pass
        elif data[0] == "remove_channel":
            pass
        elif data[0] == "autocomment":
            result = await AutoCommentMenu.auto_comment_get_menu(update, context)
        elif data[0] == "autolike":
            pass
        return result

    @staticmethod
    async def auto_comment_get_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        channel = await UserChannelsRepository.get_by_id(int(data[1]))
        is_active, title = channel["is_active"], channel["title"]
        keyboard = [
            [InlineKeyboardButton(text="Status now: 🟢" if is_active is True else "Status now: ❌",
                                  callback_data=f"toggle_autocomment,{data[1]},{is_active}"),
             InlineKeyboardButton(text="Settings", callback_data="settings_autocomment")],
            [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=CHANNELS[2])]
        ]
        await query.edit_message_text(text=f"{title}\nAutoComment Menu✉️",
                                      reply_markup=InlineKeyboardMarkup(keyboard))

        return "get_choice_of_autocomment"

    @staticmethod
    async def get_choice_of_autocomment(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        data = query.data.split(",")
        await query.answer()
        if data[0] == "toggle_autocomment":
            result = await AutoCommentMenu.toggle_autocomment(update, context)
        elif data[0] == "settings_autocomment":
            pass
        return result

    @staticmethod
    async def toggle_autocomment(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
                #ribla9000
