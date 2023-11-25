import requests

from core.config import SETTINGS, RESPONSE_ERROR, BACK_BUTTON_TEXT, START_MENU
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from repository.tools import keyboard_cols, api_request
from repository.external_channels import ExternalChannelsRepository
from repository.grouping import GroupingRepository
from repository.bot_menu import check_auth
import re


class CompetitorMenu:

    @staticmethod
    @check_auth
    async def get_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        keyboard = [
            [InlineKeyboardButton(text="Channels", callback_data="get_competitor_channels_menu")],
            [InlineKeyboardButton(text="Grouping", callback_data="grouping_menu")],
            [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=SETTINGS[0])]
        ]
        await query.edit_message_text(text="Competitor Menu" + "ㅤ"*10, reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    @check_auth
    async def get_competitor_channels_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        keyboard = [
            [InlineKeyboardButton(text="Add", callback_data="add_competitor_channel"),
             InlineKeyboardButton(text="List", callback_data="get_competitor_list")],
            [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[1])]
        ]
        if query is None:
            await update.message.reply_text(text="Channels menu" + " ㅤ"*10, reply_markup=InlineKeyboardMarkup(keyboard))
            return ConversationHandler.END
        await query.answer()
        await query.edit_message_text(text="Channels menu" + " ㅤ"*10, reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def add_competitor_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="Paste an open link to a channel you'd like to track")
        data = query.data.split(",")
        if len(data) > 1:
            context.bot_data.update({user_data["chat_id"]: data[1]})
        return "add_link"

    @staticmethod
    @check_auth
    async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        text = update.message.text
        keyboard = [[InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[1])]]
        request = api_request(endpoint="#ribla9000",
                              method="POST",
                              params={"invite_link": text, "user_id": user_data["id"]})
        response = request.json()

        if response.get("code") == 400:
            await update.message.reply_text(quote=False, text=response.get("message") + " ㅤ"*10,
                                            reply_markup=InlineKeyboardMarkup(keyboard))
            return ConversationHandler.END

        if context.bot_data.get(user_data["chat_id"]) is not None:
            await ExternalChannelsRepository.update_grouping(response["result"], int(context.bot_data.get(user_data["chat_id"])), True)
            await CompetitorMenu.check_24h_grouping(update, context, context.bot_data.get(user_data["chat_id"]))
            await CompetitorMenu.get_grouping(update, context, 1, context.bot_data.get(user_data["chat_id"]))
            context.bot_data.pop(user_data["chat_id"])
            return ConversationHandler.END

        await CompetitorMenu.get_competitor_channels_menu(update, context)
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def competitor_channels_list_page(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        data = query.data.split(",")
        page = int(data[1])
        await CompetitorMenu.get_competitor_list(update=update, context=context, page=page, user_data=user_data)

    @staticmethod
    @check_auth
    async def get_competitor_list(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict, page: int = 1):
        query = update.callback_query
        await query.answer()
        channels = await ExternalChannelsRepository.get_all_by_user(user_id=user_data["id"], page=page-1)
        back_button = [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data=START_MENU[1])]
        if len(channels) == 0 or channels is None:
            await query.edit_message_text(text="No channels added" + " ㅤ"*10,
                                          reply_markup=InlineKeyboardMarkup([back_button]))
            return ConversationHandler.END

        check_24 = [InlineKeyboardButton(text="Check 24h", callback_data=f"check_24h_channels,{page-1}")]
        grouping = await GroupingRepository.get_all(user_id=user_data["id"])
        keyboard = [InlineKeyboardButton(text=i["title"], callback_data=f"get_choice_of_channel,{i['id']}") for i in channels]
        keyboard = keyboard_cols(keyboard, 2)
        keyboard = keyboard
        page_buttons = [InlineKeyboardButton(text="◀️", callback_data=f"competitor_list_page,{page - 1}"),
                        InlineKeyboardButton(text="▶️", callback_data=f"competitor_list_page,{page + 1}")]

        if len(channels) > 0:
            if len(channels) < 14:
                page_buttons.remove(page_buttons[1])
            if page == 1:
                page_buttons.remove(page_buttons[0])
            keyboard.append(page_buttons)

        if len(grouping) == 0 or grouping is None:
            keyboard.append(check_24)

        keyboard.append(back_button)
        await query.edit_message_text(text="There are your channels, choose the one",
                                      reply_markup=InlineKeyboardMarkup(keyboard))

        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def get_choice_of_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        channel_id = int(data[1])
        channel = await ExternalChannelsRepository.get_by_id(channel_id)
        keyboard = [[InlineKeyboardButton(text="Remove channel", callback_data=f"remove_channel,{channel_id}")],
                    [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="get_competitor_list")]]
        await query.edit_message_text(text=f"Channel: {channel['title']}" + " ㅤ"*10, reply_markup=InlineKeyboardMarkup(keyboard))

        return ConversationHandler.END

    @staticmethod
    async def create_info(response: requests.request, com_channels_titles: list, ex_channel: dict):
        ext_channel_link = ex_channel["open_link"]
        regex_link = re.sub("https:\/\/t.me\/\+?", "", ext_channel_link)
        info = ""
        for channel in response.get("data"):
            description = channel['description'].replace('\n\n', '\n')
            link = channel['link']
            message_id = str(channel["message_id"])
            link_to_tgstat = "https://uk.tgstat.com/channel/" + regex_link + "/" + message_id
            tg_stat = f"<a href='{link_to_tgstat}'>TgStat</a>" if message_id != "-" else "-"

            if channel["title"] not in com_channels_titles:
                info += (
                    f"<a href='{link}'>{channel['title']}</a> ({channel['count']})".replace("\n", "") + "<br>"
                    f"#ribla9000: {tg_stat}" + "<br>"
                    f"#ribla9000: {description}" + "<br><br>"
                )
                com_channels_titles.append(channel["title"])
            else:
                info += f"пропущено: <a href='{link}'>{channel['title']}</a>".replace("\n", "") + "<br><br>"
        return info

    @staticmethod
    async def get_ads_in_external_channel(ex_channel: dict, com_channels_titles: list):
        request = api_request(endpoint="#ribla9000",
                              method="POST",
                              params={"external_id": ex_channel["id"]})
        response = request.json()
        if response.get("code") == 400:
            info = response.get("message")
            return info
        if (response.get("data") is None or response.get("data") == "-" or len(response.get("data")) == 0
                or response.get("data") == "\n" or response.get("data") == "" or response.get("data") == " "):
            return "null"
        info = await CompetitorMenu.create_info(response, com_channels_titles, ex_channel)
        return info

    @staticmethod
    @check_auth
    async def check_24h_channels(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        page = int(data[1])
        back_button = [[InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="get_competitor_channels_menu")]]
        ext_channels = await ExternalChannelsRepository.get_all_by_user(user_id=user_data["id"], page=page, by_page=False)
        ind = 0
        com_channels_titles = []
        for ext_channel in ext_channels:
            ind += 1
            info = await CompetitorMenu.get_ads_in_external_channel(ex_channel=ext_channel, com_channels_titles=com_channels_titles)
            info = info.replace("<br>", "\n")
            if info == "null":
                continue
            await context.bot.send_message(
                text=f"<b>💰Рекламні пости в каналі</b>: <a href='{ext_channel['open_link']}'>{ext_channel['title']}</a>\n\n"
                     f"{info}",
                chat_id=update.effective_chat.id,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
        await context.bot.send_message(chat_id=query.from_user.id,
                                       text="Back to menu ㅤ ㅤ   ㅤ ㅤ   ㅤ ㅤ   ㅤ ",
                                       reply_markup=InlineKeyboardMarkup(back_button))

    @staticmethod
    async def check_24h_grouping(update: Update, context: ContextTypes.DEFAULT_TYPE, _grouping_id: int = None):
        query = update.callback_query
        if query is not None:
            await query.answer()
            data = query.data.split(",")
        grouping_id = int(data[1]) if _grouping_id is None else _grouping_id
        back_button = [[InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="get_competitor_channels_menu")]]
        ext_channels = await ExternalChannelsRepository.get_by_grouping(grouping_id=grouping_id)
        com_channels_titles = []
        ind = 0
        for ext_channel in ext_channels:
            ind += 1
            info = await CompetitorMenu.get_ads_in_external_channel(ex_channel=ext_channel,
                                                                    com_channels_titles=com_channels_titles)
            info = info.replace("<br>", "\n")
            if info == "null":
                continue
            await context.bot.send_message(
                text=f"<b>💰Рекламні пости в каналі</b>: <a href='{ext_channel['open_link']}'>{ext_channel['title']}</a>\n\n"
                     f"{info}",
                chat_id=update.effective_chat.id,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )

        await context.bot.send_message(chat_id=query.from_user.id,
                                       text="Back to menu ㅤ ㅤ   ㅤ ㅤ   ㅤ ㅤ   ㅤ ",
                                       reply_markup=InlineKeyboardMarkup(back_button))

    @staticmethod
    @check_auth
    async def grouping_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
     #ribla9000

    @staticmethod
    @check_auth
    async def grouping_add_title_button(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
       #ribla9000

    @staticmethod
    @check_auth
    async def grouping_add_title(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
       #ribla9000

    @staticmethod
    @check_auth
    async def grouping_list_page(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        data = query.data.split(",")
        grouping_id = int(data[1])
        page = int(data[2])
        await CompetitorMenu.get_grouping(update=update, context=context, page=page, user_data=user_data, _grouping_id=grouping_id)

    @staticmethod
    @check_auth
    async def get_grouping(update: Update,
                           context: ContextTypes.DEFAULT_TYPE,
                           user_data: dict,
                           page: int = 1,
                           _grouping_id: int = None):
        def get_emoji(title: str, is_selected: bool):
            return title + "🟢" if is_selected else title + "🔴"
        query = update.callback_query
        await query.answer() if query is not None else ...
        data = query.data.split(",") if query is not None else None
        grouping_id = int(data[1]) if _grouping_id is None else _grouping_id
        channels = await ExternalChannelsRepository.get_all_by_user(user_id=user_data["id"], page=page-1)
       #ribla9000
        page_buttons = [
            InlineKeyboardButton(text="◀️", callback_data=f"grouping_channels_page,{grouping_id},{page - 1}"),
            InlineKeyboardButton(text="▶️", callback_data=f"grouping_channels_page,{grouping_id},{page + 1}")
        ]
        remove_button = [InlineKeyboardButton("Remove", callback_data=f"ask_for_remove_grouping,{grouping_id}")]
        back_button = [InlineKeyboardButton(text=BACK_BUTTON_TEXT, callback_data="grouping_menu")]
        keyboard = keyboard_cols(keyboard, 2)
        keyboard = keyboard

        #ribla9000

        if query is not None:
            await query.edit_message_text(text="A list of your channels. 🟢 - In this grouping and 🔴 - out of this group ",
                                          reply_markup=InlineKeyboardMarkup(keyboard))
            return ConversationHandler.END

        await update.message.reply_text(quote=False,
                                        text="A list of your channels. 🟢 - In this grouping and 🔴 - out of this group ",
                                        reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    @check_auth
    async def toggle_grouping_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        data = query.data.split(",")
        channel_id = data[1]
        grouping_id = data[2]
        old_value = data[3]
        await ExternalChannelsRepository.update_grouping(int(channel_id), int(grouping_id), old_value == '0')
        await CompetitorMenu.get_grouping(update, context, _grouping_id=int(grouping_id))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def remove_channel(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        ex_channel = await ExternalChannelsRepository.get_by_id(int(data[1]))
        request = api_request(endpoint="watchers/leave_channel/",
                              method="DELETE",
                              params={"channel_id": ex_channel["id"]})
        await CompetitorMenu.get_competitor_list(update, context)
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def ask_for_remove_grouping(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        grouiping_id = int(data[1])
        keyboard = [[InlineKeyboardButton(text="Yes, remove", callback_data=f"remove_grouping,{grouiping_id}")],
                    [InlineKeyboardButton(text="No, don't", callback_data="grouping_menu")]]
        await query.edit_message_text(text="Do you want to remove a grouping?",
                                      reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    @staticmethod
    @check_auth
    async def remove_grouping(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data: dict):
        query = update.callback_query
        await query.answer()
        data = query.data.split(",")
        grouping_id = int(data[1])
        await GroupingRepository.delete(grouping_id)
        await CompetitorMenu.grouping_menu(update, context)
        return ConversationHandler.END
