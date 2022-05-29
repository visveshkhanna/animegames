from telegram import Update
from telegram.ext import CallbackContext
from handles.extras import *
from ping3 import ping

async def ping_command(update: Update, context: CallbackContext):
    reply = await update.message.reply_text(
        text=italic("Pinging..."),
        parse_mode="HTML"
    )
    await reply.edit_text(
        text=f"{bold('PING: ')}  {str(ping('api.telegram.org') * 1000)[:5]} ms",
        parse_mode="HTML"
    )