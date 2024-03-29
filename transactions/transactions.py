from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from handles.userhandle import unregistered, check_user
from transactions.transactions_handle import get_transactions, ListHandle, transaction_message


def view_trans(update: Update, context: CallbackContext):
    user = update.effective_user
    if check_user(user):
        split = ListHandle(get_transactions(user), 10)
        if len(split) > 1:
            next_button = [
                [
                    InlineKeyboardButton("Next", callback_data=f'TRA {user.id} 1')
                ]
            ]
            next_button = InlineKeyboardMarkup(next_button)
            data = split[0]
            message = "Transation History\nPage 1\n\n"
            for i, cont in enumerate(data):
                messagecont = transaction_message(cont, i+1)
                message += messagecont
            update.message.reply_text(
                text=message,
                parse_mode="HTML",
                reply_markup=next_button
            )
        else:
            data = split[0]
            message = "Transation History\n\n"
            for i, cont in enumerate(data):
                messagecont = transaction_message(cont, i+1)
                message += messagecont
            update.message.reply_text(
                text=message,
                parse_mode="HTML"
            )
    else:
        unregistered(update, context)
