from telegram import Update
from telegram.ext import CallbackContext

from anilist.character import character_inline
from const import LOADING
from handles.extras import bold
from handles.userhandle import check_user, unregistered


def searchcharacter(update: Update, context: CallbackContext):
    user = update.effective_user
    msg = update.effective_message.text
    if check_user(user):
        data = msg.split("/character")[1].strip()
        markup = character_inline(user, data)
        update.message.reply_animation(
            animation=LOADING,
            caption=f"Searching for {bold(data.capitalize())} ...",
            reply_markup=markup,
            parse_mode="HTML"
        )
    else:
        unregistered(update, context)
