import time

from telegram import Update
from telegram.ext import CallbackContext
from handles.extras import *

async def ping(update: Update, context: CallbackContext):
    start_time = int(round(time.time() * 1000))
    reply = await update.message.reply_text(
        text=italic("Pinging..."),
        parse_mode="HTML"
    )
    end_time = int(round(time.time() * 1000))
    await reply.edit_text(
        text=f"{bold('PING: ')} {end_time - start_time} ms",
        parse_mode="HTML"
    )