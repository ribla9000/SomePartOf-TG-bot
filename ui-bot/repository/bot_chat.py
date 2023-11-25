from telegram import Update, ChatMember, ChatMemberUpdated, Chat
from telegram.ext import ContextTypes, CallbackContext
from typing import Optional, Tuple


def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))
    if status_change is None:
        return None
    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)
    return was_member, is_member


async def check_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = extract_status_change(update.chat_member)
    if result is None:
        return
    was_member, is_member = result
    if not was_member and is_member:
        print(is_member, "Join")
    elif was_member and not is_member:
        print(was_member, "Leaved")


async def check_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.chat_join_request)


