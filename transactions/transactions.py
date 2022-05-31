from telegram import Update
from telegram.ext import CallbackContext

from handles.userhandle import unregistered, check_user
from transactions.transactions_handle import get_transactions


async def view_trans(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = update.effective_user
    if check_user(user):
        get_transactions(user)
    else:
        await unregistered(update, context)
