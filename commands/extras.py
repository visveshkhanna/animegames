import time

from telegram import Update
from telegram.ext import CallbackContext
from handles.extras import *
from ping3 import ping
from math import ceil

async def ping_command(update: Update, context: CallbackContext):
    reply = await update.message.reply_text(
        text=italic("Pinging..."),
        parse_mode="HTML"
    )
    await reply.edit_text(
        text=f"{bold('PING: ')} {ceil(ping('api.telegram.org') * 100)} ms",
        parse_mode="HTML"
    )