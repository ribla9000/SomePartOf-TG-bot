import os
from core.config import START_MENU, SETTINGS, CHANNELS, BACK_BUTTON_TEXT, RESPONSE_ERROR, RESPONSE_DONE
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Chat, Bot
from telegram.ext import ContextTypes, ConversationHandler
from repository.admin_bots import AdminBotsRepository
from repository.tools import keyboard_cols, api_request
from repository.users import UsersRepository
from repository.user_channels import UserChannelsRepository
from repository.messages import MessagesRepository
from repository.links import LinksRepository
from repository.bot_menu import check_auth


class ChannelsMenu:
    @staticmethod
    @check_auth
    async def get_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        keyboard = [[InlineKeyboardButton(text="Add⭐️", callback_data=CHANNELS[1]),
                     InlineKeyboardButton(text="List🗒", callback_data=CHANNELS[2])],
                    [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[3])]]
        query = update.callback_query
        await query.answer()
        await query.message.edit_text(text="Channels menu", reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    @check_auth
    async def add_channel_wait_for_post(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="Forward a post from a channel")
        return "add_channel_check_post"

    @staticmethod
    @check_auth
    async def add_channel_check_post(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        is_channel = Chat.CHANNEL
        forwarded_message = update.message
        bots = await AdminBotsRepository.get_all(user_id=user_data["id"])
        keyboard = [[InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[1])],
                    [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[2])]]
        if bots is None or len(bots) == 0:
            await update.message.reply_text(text="You don't have any bots",
                                            quote=False,
                                            reply_markup=InlineKeyboardMarkup([keyboard[0]]))
            return ConversationHandler.END
        if forwarded_message.forward_from_chat is None or forwarded_message.forward_from_chat.type != is_channel:
            await update.message.reply_text(text="Your forwarded message not from a channel.",
                                            quote=False,
                                            reply_markup=InlineKeyboardMarkup([keyboard[1]]))
            return ConversationHandler.END
        from_channel_id, chat_id = forwarded_message.forward_from_chat.id, forwarded_message.chat_id
        channel = {"user_id": user_data["id"],
                   "admin_bot_id": None,
                   "title": forwarded_message.forward_from_chat.title,
                   "chat_id": str(from_channel_id),
                   "readable_index": forwarded_message.forward_from_chat.link,
                   "is_active": False,
                   "is_shown": True}
        is_exists = await UserChannelsRepository.get_by_chat_id(chat_id=channel["chat_id"], user_id=user_data["id"])
        if is_exists is not None:
            await update.message.reply_text(text="This channel already exists. Check your channels list",
                                            quote=False,
                                            reply_markup=InlineKeyboardMarkup([keyboard[1]]))
            return ConversationHandler.END
        user_channel_id = await UserChannelsRepository.create(channel)

        keyboard = [[InlineKeyboardButton(text="Add bot to channel", callback_data=f"add_channel_chose_bot,{user_channel_id}")]]
        await update.message.reply_text(quote=False,
                                        text=f"Your channel is {forwarded_message.forward_from_chat.title}",
                                        reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    @check_auth
    async def add_channel_chose_bot(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        channel_id = data[1]
        bots = await AdminBotsRepository.get_all(user_data["id"])
        keyboard = [InlineKeyboardButton(text=i["nickname"], callback_data=f"add_channel_update_bot,{channel_id},{i['id']}") for i in bots]
        await query.edit_message_text(text="Chose a bot who will manage in this group",
                                      reply_markup=InlineKeyboardMarkup(keyboard_cols(keyboard, 2)))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def add_channel_update_bot(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        keyboard = [[InlineKeyboardButton(text="<<Main menu", callback_data=SETTINGS[0])]]
        params = {"admin_bot_id": int(data[2]), "channel_id": int(data[1])}
        request = api_request(endpoint=        #ribla9000)
        response = request.json()
        if response["result"] == RESPONSE_ERROR:
            await query.edit_message_text(text="This bot doesn't have permissions to add users",
                                          reply_markup=InlineKeyboardMarkup(keyboard))
            await UserChannelsRepository.delete(int(data[1]))
            return ConversationHandler.END
        request = api_request(endpoint=     #ribla9000, 
        method="PUT", params=params)
        await query.edit_message_text(text="You added your bot", reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def get_channels_list(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        channels = await UserChannelsRepository.get_all(id=user_data["id"])
        keyboard = [[InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[2])]]
        if channels is None or len(channels) == 0:
            await query.edit_message_text("You don't have any channels, add it", reply_markup=InlineKeyboardMarkup(keyboard))
            return ConversationHandler.END
        keyboard = [InlineKeyboardButton(text=i["title"], callback_data=f'channel_settings,{i["id"]}') for i in channels]
        keyboard = keyboard_cols(buttons=keyboard, cols=3)
        keyboard = keyboard
        keyboard.append([InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[2])])
        await query.edit_message_text(text="Your channels list", reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def choose_channel_settings(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        channel_id = int(data[1])
        channel = await UserChannelsRepository.get_by_id(channel_id)
        back_button = [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=CHANNELS[2])]
        keyboard = [
            [InlineKeyboardButton(text="Generate Invite Link", callback_data=f"generate_invite_link,{channel_id}")],
            [InlineKeyboardButton(text="Add bot", callback_data=f"add_channel_chose_bot,{channel_id}"),
             InlineKeyboardButton(text="Remove bot", callback_data=f"remove_admin_bot,{channel_id}")],
            [InlineKeyboardButton(text=f"stats{'🟢' if channel['is_active'] is True else '🔴'}",
                                  callback_data=f"toggle_stats_track,{channel_id},{'0' if channel['is_active'] is True else '1'}")]
        ]
        keyboard.append(back_button)
        await query.edit_message_text(text=f"Your channel is: {channel['title']}",
                                      reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def remove_admin_bot(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        channel_id = int(data[1])
        back_button = [[InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=CHANNELS[2])]]
        request = api_request(endpoint="#ribla9000",
                              method="DELETE",
                              params={"channel_id": channel_id})
        response = request.json()
        if response.get("result") == RESPONSE_ERROR:
            await query.edit_message_text(text="There is no bots, add it", reply_markup=InlineKeyboardMarkup(back_button))
            return ConversationHandler.END
        await query.edit_message_text(text="Admin-bot removed successfully", reply_markup=InlineKeyboardMarkup(back_button))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def toggle_stats_track(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        channel_id = int(data[1])
        turn_on = data[2] != '0'
        params = {"user_channel_id": channel_id, "turn_on": turn_on}
        if turn_on:
            request = api_request(endpoint="#ribla9000", method="POST", params=params)
        elif not turn_on:
            request = api_request(endpoint="#ribla9000", method="PATCH", params=params)
        await ChannelsMenu.choose_channel_settings(update, context)
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def generate_post(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()

        data = query.data.split(",")
        channel = await UserChannelsRepository.get_by_id(int(data[1]))
        admin_bot = await AdminBotsRepository.get_by_channel_id(channel["id"])
        keyboard = [[InlineKeyboardButton(text="Test Post Button", url="https://t.me/+Qh5J0dSDz0Q3ZDQy")],
                    [InlineKeyboardButton(text="Test answer button", callback_data="test_button,Hillo motherfuckker")]]
        await query.edit_message_text(text="AAADAADADAAD", reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    @check_auth
    async def request_params_for_link(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        await query.edit_message_text(text="Past a data in the folowing format:\n"
                                           "Open link: your open link\n"
                                           "Price: 100 - per 1000 views or 15000! - as fixed\n"
                                           "User Admin: @Bobadmin\n"
                                           "Text(Optional): Hello, my name is Bob\n\n"
                                           "Example:\nhttp://t.me/mylink,\n350,\n@BobAdmin,\nMy name's Bob")
        pre_message = {"user_id": user_data["id"], "query": data[1]}
        await MessagesRepository.create(pre_message)
        return "create_invite_link"

    @staticmethod
    @check_auth
    async def generate_invite_link(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        message = await MessagesRepository.get_last(update.message.from_user.username)
        await MessagesRepository.update(message["id"], update.message.text)
        channel = await UserChannelsRepository.get_by_id(int(message["query"]))
        admin_bot = await AdminBotsRepository.get_by_channel_id(channel["id"])
        text_data = update.message.text.split(",")
        open_link = text_data[0].replace("\n", "")
        price = text_data[1].replace("\n", "")
        admin = text_data[2].replace("\n", "")
        name = channel["title"] + price
        bot = Bot(token=admin_bot["token"])
        keyboard = [[InlineKeyboardButton(text="<<Main menu", callback_data=START_MENU[3])]]

        try:
            link_obj = await bot.create_chat_invite_link(chat_id=channel["chat_id"],
                                                         expire_date=None,
                                                         member_limit=None,
                                                         creates_join_request=True,
                                                         name=name)
            link = {"invite_link": link_obj.invite_link, "price": price, "admin_username": admin}
            await LinksRepository.create(link)
            await update.message.reply_text(quote=False,
                                            text=f"Your created link is: {link_obj.invite_link}\n",
                                            reply_markup=InlineKeyboardMarkup(keyboard))
           #ribla9000
        except Exception as e:
            print(str(e))

