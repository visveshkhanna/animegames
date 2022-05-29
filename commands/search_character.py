from telegram import Update
from telegram.ext import CallbackContext
from dotenv import dotenv_values

from handles.userhandle import check_user, unregistered
from anilist.character import character_inline
from handles.extras import bold

LOADING = dotenv_values('.env')["LOADING"]

async def searchcharacter(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.effective_message.text
    if check_user(user):
        data = msg.split("/character")[1].strip()
        markup = character_inline(data)
        await update.message.reply_animation(
            animation=LOADING,
            caption = f"Searching for {bold(data.capitalize())} ...",
            reply_markup=markup,
            parse_mode="HTML"
        )
    else:
        await unregistered(update, context)
