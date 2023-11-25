from core.config import (START_MENU, SETTINGS, BOTS,
                         NOT_APPROVE, BACK_BUTTON_TEXT, RESPONSE_ERROR, RESPONSE_DONE, SUPERADMIN_IDS)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler
from db.users import ROLES
from repository.admin_bots import AdminBotsRepository
from repository.tools import keyboard_cols, api_request, redis_client
from repository.users import UsersRepository


async def get_user(update: Update):

    if update.message is not None:
        nickname = update.message.from_user.username
        name = update.message.from_user.full_name
        chat_id = str(update.message.chat_id)
    elif update.callback_query is not None:
        nickname = update.callback_query.from_user.username
        name = update.callback_query.from_user.full_name
        chat_id = str(update.callback_query.from_user.id)

    user_data_redis = redis_client.redis_hget_data(f"user:{chat_id}")
    redis_user_exist = len(user_data_redis) != 0

    if redis_user_exist:
        user_data_redis["id"] = int(user_data_redis["id"])
        return user_data_redis

    user_data_db = await UsersRepository.get_by_chat_id(chat_id)
    db_user_exist = len(user_data_db) != 0

    if not redis_user_exist and db_user_exist:
        redis_client.redis_hset_data(key=f"user:{chat_id}",
                                     value=user_data_db)
        user_data_redis = redis_client.redis_hget_data(f"user:{chat_id}")
        user_data_redis["id"] = int(user_data_redis["id"])
        return user_data_db
    else:
        user = {"name": name,
                "nickname": nickname,
                "chat_id": chat_id}

        if user["chat_id"] in SUPERADMIN_IDS:
            user["role"] = "superadmin"

        user_id = await UsersRepository.create(user)
        user_data_db = await UsersRepository.get_by_id(user_id)

        return user_data_db


def check_auth(f: callable):
    auth = [ROLES["USER"], ROLES["MANAGER"], ROLES["ADMIN"], ROLES["SUPERADMIN"]]

    async def wrapper(*args: tuple, **kwargs: dict):
        try:
            if len(args) == 0:
                return await f(*args, **kwargs)
            update = args[0]
            user_data = await get_user(update)
            kwargs["user_data"] = user_data
            if user_data["role"] not in auth:
                if update.message is not None:
                    await update.message.reply_text(quote=False, text=f"{NOT_APPROVE} `{user_data['chat_id']}`", parse_mode=ParseMode.MARKDOWN)
                    return ConversationHandler.END
                await update.callback_query.edit_message_text(text=NOT_APPROVE)
                return ConversationHandler.END

            return await f(*args, **kwargs)

        except Exception as e:
            error_message = f'ERROR: {e}'
            print(error_message)
            return None
    return wrapper


@check_auth
async def get_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
    administration_menu_item = InlineKeyboardButton(text="Administration🔑", callback_data=START_MENU[2])
    settings_menu_item = InlineKeyboardButton(text="Settings⚙️", callback_data=START_MENU[0])
    statistics_menu_item = InlineKeyboardButton(text="Statistics🗃", callback_data=START_MENU[3])
    competitor_menu_item = InlineKeyboardButton(text="Competitor Menu👾", callback_data=START_MENU[1])
    keyboard = [[settings_menu_item, administration_menu_item],
                [statistics_menu_item, competitor_menu_item]]
    if user_data["role"] == ROLES["ADMIN"]:
        keyboard[0].remove(administration_menu_item)
    if user_data["role"] == ROLES["MANAGER"]:
        keyboard = [[competitor_menu_item]]
    if user_data["role"] == ROLES["USER"]:
        keyboard = [[]]
    if update.message is not None:
        await update.message.reply_text(text="You're in the main menu.ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ",
                                        reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="You're in the main menu.ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ",
                                  reply_markup=InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END


@check_auth
async def start_menu_to_settings(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text="AutoComment✉️", callback_data=SETTINGS[3]),
         InlineKeyboardButton(text="AutoLike💜", callback_data=SETTINGS[4])],
        # [InlineKeyboardButton(text="Support", callback_data=SETTINGS[5])],
        [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[0])]
    ]
    await query.message.edit_text(text="Settings⚙️", reply_markup=InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END


class BotsMenu:

    @staticmethod
    @check_auth
    async def get_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        keyboard = [[InlineKeyboardButton(text="Add⭐️", callback_data=BOTS[1]),
                     InlineKeyboardButton(text="List🗒", callback_data=BOTS[2])],
                    [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[3])]]
        try:
            query = update.callback_query
            await query.answer()
            await query.message.edit_text(text="Bots menu ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ", reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            await update.message.edit_text(text="Bots menu ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ", reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    @check_auth
    async def add_bot(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        await query.message.edit_text(text="Paste your Bot's token here")
        return "check_token"

    @staticmethod
    @check_auth
    async def check_token(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        params = {"token": update.message.text, "user_id": user_data["id"]}
        request =         #ribla9000
        response = request.json()
        keyboard = [[InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[1])]]
        if response["result"] == RESPONSE_ERROR:
            await update.message.reply_text(quote=False,
                                            text="Sorry, invalid token or bot already exists",
                                            reply_markup=InlineKeyboardMarkup(keyboard))
            return ConversationHandler.END

        await update.message.reply_text(quote=False,
                                        text="You have added your bot successfully.",
                                        reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def get_bots_list(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        bots = await AdminBotsRepository.get_all(user_id=user_data["id"])
        if bots is None or len(bots) == 0:
            keyboard = [[InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[1])]]
            await query.message.edit_text(text="There are no your bots, add it",
                                          reply_markup=InlineKeyboardMarkup(keyboard))
            return ConversationHandler.END

        keyboard = [InlineKeyboardButton(text=i["name"], callback_data=i["id"]) for i in bots]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_cols(keyboard, 3))
        await query.message.edit_text(text="The list of your bots",
                                      reply_markup=reply_markup)


@check_auth
async def stop_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
    await update.message.reply_text(text="Okey. Stoped", quote=False)
    return ConversationHandler.END

