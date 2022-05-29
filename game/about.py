from telegram import Update
from telegram.ext import CallbackContext


async def about(update: Update, context: CallbackContext):
    user = update.effective_user
