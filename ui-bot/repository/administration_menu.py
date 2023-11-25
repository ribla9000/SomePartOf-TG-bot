from core.config import SETTINGS, BACK_BUTTON_TEXT, START_MENU, RESPONSE_ERROR
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from repository.tools import keyboard_cols, check_permissions, redis_client, api_request
from repository.bot_menu import check_auth
from db.users import ROLES
from repository.users import UsersRepository


class AdministrationMenu:

    @staticmethod
    async def get_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        keyboard = [
            [InlineKeyboardButton(text="Users", callback_data="administration_get_users"),
             InlineKeyboardButton(text="Userbots", callback_data="administration_get_userbots")],
            [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[0])]
        ]
        await query.edit_message_text(text="Administration Menu" + "ㅤ"*10, reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    async def administration_users_paging(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        data = query.data.split(",")
        page = int(data[1])
        await AdministrationMenu.get_users(update=update, context=context, page=page)

    @staticmethod
    async def get_users(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 1):
        query = update.callback_query
        await query.answer()
        users = await UsersRepository.get_users_by_role(role=ROLES["GUEST"], page=page-1)
        page_buttons = [InlineKeyboardButton(text="◀️", callback_data=f"administration_users_paging,{page - 1}"),
                        InlineKeyboardButton(text="▶️", callback_data=f"administration_users_paging,{page + 1}")]
        keyboard = [InlineKeyboardButton(text=i["nickname"], callback_data=f"current_user_settings,{i['id']}") for i in users]
        keyboard = keyboard_cols(keyboard, 2)
        keyboard = keyboard
        if len(users) > 0:
            if len(users) < 14:
                page_buttons.remove(page_buttons[1])
            if page == 1:
                page_buttons.remove(page_buttons[0])
            keyboard.append(page_buttons)
        keyboard.append([InlineKeyboardButton(text="Find user", callback_data="find_user")])
        keyboard.append([InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[2])])
        await query.edit_message_text(text="Users" + "ㅤ"*10, reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    async def find_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="Paste user's chat id" + " ㅤ"*10)
        return "check_input"

    @staticmethod
    async def check_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        user = await UsersRepository.get_by_chat_id(text)
        if len(user) == 0 or user is None:
            await update.message.reply_text(quote=False,
                                            text=f"Sorry, your chat id is invalid or user doesn't exist. `{text}`",
                                            parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END
        await AdministrationMenu.current_user_settings(update, context, user)
        return ConversationHandler.END

    @staticmethod
    async def current_user_settings(update: Update, context: ContextTypes.DEFAULT_TYPE, user: dict = None):
        query = update.callback_query

        if query is None:
            user_id = user["id"]
            _user = await UsersRepository.get_by_id(user_id)
            keyboard = [[InlineKeyboardButton(text="Change role", callback_data=f"user_role_menu,{user_id}")],
                        [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="administration_get_users")]]
            await update.message.reply_text(quote=False,
                                            text=f"Settings to:\n" + "ㅤ"*10 + ""
                                                 f"nickname: `@{_user['nickname']}`\n"
                                                 f"name: {_user['name']}\n"
                                                 f"role: {_user['role']}",
                                            parse_mode=ParseMode.MARKDOWN,
                                            reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.answer()
            data = query.data.split(",")
            user_id = int(data[1])
            _user = await UsersRepository.get_by_id(user_id)
            keyboard = [[InlineKeyboardButton(text="Change role", callback_data=f"user_role_menu,{user_id}")],
                        [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="administration_get_users")]]
            await query.edit_message_text(text=f"Settings to:\n" + " ㅤ"*10 + ""
                                               f"nickname: `@{_user['nickname']}`\n"
                                               f"name: {_user['name']}\n"
                                               f"role: {_user['role']}",
                                          parse_mode=ParseMode.MARKDOWN,
                                          reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    async def user_role_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        user_id = int(data[1])
        user = await UsersRepository.get_by_id(user_id)
        keyboard = [InlineKeyboardButton(text=i, callback_data=f"change_user_role,{user_id},{i}") for i in ROLES.values()]
        keyboard = keyboard_cols(keyboard, 2)
        keyboard = keyboard
        keyboard.append([InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=f"current_user_settings,{user_id}")])
        await query.edit_message_text(text=f"Choose a role for the `@{user['nickname']}`" + "ㅤ"*10,
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    @check_auth
    async def change_user_role(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        user_id = int(data[1])
        role = data[2]
        user = await UsersRepository.get_by_id(user_id)
        if user_id != user_data["id"] and check_permissions(user_data["role"], role):
            await UsersRepository.update_role(id=user["id"], role=role)
            user["role"] = role
            redis_client.redis_hset_data(key=f"user:{user['chat_id']}", value=user)
            await AdministrationMenu.get_menu(update, context)
            return ConversationHandler.END
        await context.bot.send_message(text="You dont have permissions on this operation", chat_id=user_data["chat_id"])
        await AdministrationMenu.get_menu(update, context)
        return ConversationHandler.END

    @staticmethod
    async def administration_userbots_paging(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int):
        query = update.callback_query
        data = query.data.split(",")
        page = int(data[1])
        await AdministrationMenu.get_userbots(update=update, context=context, page=page)

    @staticmethod
    @check_auth
    async def get_userbots(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict, page: int = 1):
        query = update.callback_query
        await query.answer()
        request = api_request(endpoint="userbots/get-all/", method="GET", params={"page": page-1})
        response = request.json()
        userbots = response.get("result")
        back_button = [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[2])]
        menu = [[InlineKeyboardButton(text="Add", callback_data="add_userbot"),
                InlineKeyboardButton(text="Remove", callback_data="remove")],
                [InlineKeyboardButton(text="Watchers", callback_data="get_type_watchers"),
                InlineKeyboardButton(text="Workers", callback_data="get_type_workers")]]
        page_buttons = [InlineKeyboardButton(text="◀️", callback_data=f"administration_userbots_paging,{page - 1}"),
                        InlineKeyboardButton(text="▶️", callback_data=f"administration_userbots_paging,{page + 1}")]
        keyboard = [InlineKeyboardButton(text=i["nickname"], callback_data=f"get_userbot,{i['id']}") for i in userbots]
        keyboard = keyboard_cols(keyboard, 2)
        keyboard = keyboard

        if len(userbots) > 0:
            if len(userbots) < 14:
                page_buttons.remove(page_buttons[1])
            if page == 1:
                page_buttons.remove(page_buttons[0])
            keyboard.append(page_buttons)

        keyboard.extend(menu)
        keyboard.append(back_button)
        await query.edit_message_text(text="Userbots menu" + "ㅤ"*10, reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def get_userbot(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        userbot_id = int(data[1])
        request = api_request(endpoint="userbots/get-userbot/", method="GET", params={"userbot_id": userbot_id})
        response = request.json()
        userbot = response.get("result")
        reply = ("Current userbot:\n" + "ㅤ"*10 + ""
                 f"nickname: @{userbot['nickname']}\n"
                 f"fullname: {userbot['name']}\n"
                 f"phone number: {userbot['phone_number']}\n"
                 f"type: {userbot['type']}\n")
        keyboard = [[InlineKeyboardButton(text="Change type", callback_data=f"userbot_change_type,{userbot_id}")],
                    [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="administration_get_userbots")]]
        await query.edit_message_text(text=reply, reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    @check_auth
    async def userbot_change_type(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        userbot_id, type = int(data[1]), data[2] if len(data) > 2 else None
        request = api_request(endpoint="userbots/get-types/", method="GET", params=None)
        response = request.json()
        types = response.get("result")

        if type is None:
            keyboard = [[InlineKeyboardButton(text=i, callback_data=f"userbot_change_type,{userbot_id},{i}") for i in types]]
            await query.edit_message_text(text="Chose a type you want" + "ㅤ"*10, reply_markup=InlineKeyboardMarkup(keyboard))
            return ConversationHandler.END

        api_request("userbots/change-type/", method="PUT", params={"userbot_id": userbot_id, "type": type})
        await AdministrationMenu.get_userbots(update, context)
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def add_userbot(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="Paste a userbot session string like: 181746519AKDjnbOASdad7y1dh&^@^!!!%1asv")
        return "input_session"

    @staticmethod
    @check_auth
    async def input_session(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        text = update.message.text
        reply = "You have added your userbot."
        request = api_request(endpoint="userbots/run-userbot", method="POST", params={"session_string": text})
        response: dict = request.json()
        back_button = [[InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="administration_get_userbots")]]
        if response.get("result") == RESPONSE_ERROR:
            reply = "Sorry, Invalid data. Check it and try again."
        await update.message.reply_text(quote=False,
                                        text=reply,
                                        reply_markup=InlineKeyboardMarkup(back_button))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def get_type_watchers(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        request = api_request(endpoint="userbots/get-watchers/", method="GET", params=None)
        response = request.json()
        userbots = response.get("result")
        back_button = [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="administration_get_userbots")]
        keyboard = [InlineKeyboardButton(text=i["nickname"], callback_data=i["id"]) for i in userbots]
        keyboard = keyboard_cols(keyboard, 2)
        keyboard = keyboard
        keyboard.append(back_button)
        await query.edit_message_text(text="Userbots: Watchers" + " ㅤ"*10, reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def get_type_workers(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        request = api_request(endpoint="userbots/get-workers/", method="GET", params=None)
        response = request.json()
        userbots = response.get("result")
        back_button = [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="administration_get_userbots")]
        keyboard = [InlineKeyboardButton(text=i["nickname"], callback_data=i["id"]) for i in userbots]
        keyboard = keyboard_cols(keyboard, 2)
        keyboard = keyboard
        keyboard.append(back_button)
        await query.edit_message_text(text="Userbots: Workers" + " ㅤ"*10, reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

