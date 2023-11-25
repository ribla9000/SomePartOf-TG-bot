from core.config import START_MENU, SUPPORT, SETTINGS, BACK_BUTTON_TEXT
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from repository.support_messages import SupportMessagesRepository
from repository.bot_menu import check_auth
from repository.users import UsersRepository
from repository.tools import keyboard_cols


class SupportMenu:

    @staticmethod
    @check_auth
    async def get_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        keyboard = [
            [InlineKeyboardButton(text="Check Support channel", callback_data=SUPPORT[0])],
            [InlineKeyboardButton(text="Leave message to support", callback_data=SUPPORT[1])],
            [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[0])]
        ]
        try:
            query = update.callback_query
            await query.answer()
            await query.edit_message_text(text="Support Menu", reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            await update.message.reply_text(quote=False, text="Support Menu", reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def get_support_messages(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        support_messages = await SupportMessagesRepository.get_users()
        if support_messages is None or len(support_messages) == 0:
            keyboard = [[InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[5])]]
            await query.edit_message_text("There are no messages to support", reply_markup=InlineKeyboardMarkup(keyboard))
            return ConversationHandler.END
        keyboard = [InlineKeyboardButton(text=i["nickname"], callback_data=i["id"]) for i in support_messages]
        keyboard = keyboard_cols(buttons=keyboard, cols=2)
        keyboard = keyboard
        keyboard.append([InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[5])])
        await query.edit_message_text("There are messages to support", reply_markup=InlineKeyboardMarkup(keyboard))
        return "get_current_message_from_user"

    @staticmethod
    @check_auth
    async def get_current_message_from_user(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        message = await SupportMessagesRepository.get_by_id(int(query.data))
        to_user = await UsersRepository.get_by_id(message["user_id"])
        keyboard = [[InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SUPPORT[0])]]
        await query.edit_message_text(text=message["message"] + "\n\n" + "To reply, just write something",
                                      reply_markup=InlineKeyboardMarkup(keyboard))
        support_reply = {"to_mid": message["mid"],
                         "to_chat_id": to_user["chat_id"],
                         "user_id": user_data["id"],
                         "is_reply": True,
                         "is_answered": True}
        #ribla9000
        return "reply_to_message"

    @staticmethod
    @check_auth
    async def reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        #ribla9000

    @staticmethod
    @check_auth
    async def leave_message(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        keyboard = [[InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[5])]]
        await query.edit_message_text(text="Write message for support", reply_markup=InlineKeyboardMarkup(keyboard))
        return "send_message_to_support"

    @staticmethod
    @check_auth
    async def send_message_to_support(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        message = #ribla9000
        await SupportMessagesRepository.create(message)
        await update.message.reply_text(quote=False, text="You have sent your message to support")
        await SupportMenu.get_menu(update, context)
        return ConversationHandler.END
