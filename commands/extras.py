from telegram import Update
from telegram.ext import CallbackContext

from handles.extras import *


def ping_command(update: Update, context: CallbackContext):
    start_time = int(round(time.time() * 1000))
    reply = update.message.reply_text(
        text=italic("Pinging..."),
        parse_mode="HTML"
    )
    end_time = int(round(time.time() * 1000))
    reply.edit_text(f'{bold("Ping: ")} {code(end_time - start_time)} ms', parse_mode='HTML')
