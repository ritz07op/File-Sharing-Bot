import base64
import re
import asyncio
import logging
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import FORCE_SUB_CHANNEL, ADMINS, AUTO_DELETE_TIME, AUTO_DEL_SUCCESS_MSG
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait

# Define the subscription check function
async def is_subscribed(filter, client, update):
    if not FORCE_SUB_CHANNEL:
        return True  # No force-subscription if channel is not set
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True  # Admins are always considered subscribed
    try:
        member = await client.get_chat_member(chat_id=FORCE_SUB_CHANNEL, user_id=user_id)
    except UserNotParticipant:
        return False  # User is not subscribed
    if member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False  # Not subscribed as a member or higher
    return True

# Base64 encoding and decoding functions
async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii").strip("=")
    return base64_string

async def decode(base64_string):
    base64_string = base64_string.strip("=")  # Handle padding errors
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    return string_bytes.decode("ascii")

# Fetch messages by ID from the channel
async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    while total_messages != len(message_ids):
        temp_ids = message_ids[total_messages:total_messages + 200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,  # Ensure db_channel is correctly initialized
                message_ids=temp_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)  # Handle rate limits
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temp_ids
            )
        except Exception as e:
            logging.error(f"Error fetching messages: {e}")
            pass
        total_messages += len(temp_ids)
        messages.extend(msgs)
    return messages

# Extract the message ID from the forwarded message or URL
async def get_message_id(client, message):
    if message.forward_from_chat:
        if message.forward_from_chat.id == client.db_channel.id:
            return message.forward_from_message_id
        return 0
    elif message.forward_sender_name:
        return 0
    elif message.text:
        pattern = r"https://t.me/(?:c/)?(.*)/(\d+)"  # Use raw string to avoid regex warning
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(client.db_channel.id):
                return msg_id
        else:
            if channel_id == client.db_channel.username:
                return msg_id
    return 0  # No valid message ID

# Convert seconds to readable time format
def get_readable_time(seconds: int) -> str:
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    count = 0
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    time_list.reverse()
    up_time = ", ".join([f"{t} {suffix}" for t, suffix in zip(time_list, time_suffix_list)])
    return up_time

# Delete files after a certain period
async def delete_file(messages, client, process):
    await asyncio.sleep(AUTO_DELETE_TIME)
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            logging.error(f"Error deleting message {msg.id}: {e}")
            await asyncio.sleep(e.x)  # Handle rate limiting gracefully
    await process.edit_text(AUTO_DEL_SUCCESS_MSG)

# Create a custom filter for subscription checking
subscribed = filters.create(is_subscribed)

