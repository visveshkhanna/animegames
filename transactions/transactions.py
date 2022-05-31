from telegram import Update
from telegram.ext import CallbackContext

from handles.userhandle import unregistered, check_user
from transactions.transactions_handle import get_transactions


async def view_trans(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = update.effective_user
    if check_user(user):
        message = get_transactions(user)
        await update.message.reply_text(
            text=message,
            parse_mode="HTML"
        )
    else:
        await unregistered(update, context)
