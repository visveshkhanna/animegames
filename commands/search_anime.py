from telegram import Update
from telegram.ext import CallbackContext

from anilist.anime import anime_inline
from const import LOADING
from handles.extras import bold
from handles.userhandle import check_user, unregistered


async def searchanime(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.effective_message.text
    if check_user(user):
        data = msg.split("/anime")[1].strip()
        markup = anime_inline(data)
        await update.message.reply_animation(
            animation=LOADING,
            caption=f"Searching for {bold(data.capitalize())} ...",
            reply_markup=markup,
            parse_mode="HTML"
        )
    else:
        await unregistered(update, context)
