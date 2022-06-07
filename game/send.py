from telegram import Update
from telegram.ext import CallbackContext

from handles.extras import italic, bold, animetransid, code
from handles.markups import register_markup
from handles.userhandle import update_coins, check_user, unregistered, select_user_v2, update_max_coins
from transactions.transactions_handle import create_transaction, check_transaction


def send_coins(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    message = update.effective_message
    reply_to_message = update.message.reply_to_message
    if check_user(user):
        if reply_to_message:
            coins = message.text.split('/send')[-1].strip()
            if not coins.isnumeric():
                update.message.reply_text(
                    text=italic('Sending Nothing?, Alphabets? Characters? Only numbers allowed'),
                    parse_mode="HTML"
                )
                return
            coins = int(coins)
            from_user = reply_to_message.from_user
            if check_user(from_user):
                if user == from_user:
                    update.message.reply_text(
                        text=f'{italic("Aww, Sending coins to Yourself?")} 😂',
                        parse_mode="HTML"
                    )
                elif coins == 0:
                    update.message.reply_text(
                        text=f'{user.mention_html()}, Please send more than 0 coins!!!',
                        parse_mode="HTML"
                    )
                else:
                    sender = select_user_v2(user)
                    receiver = select_user_v2(from_user)
                    scoins = sender["coins"]
                    rcoins = receiver["coins"]
                    uscoins = scoins - coins
                    if uscoins > 0:
                        transid = animetransid()
                        while check_transaction(transid):
                            transid = animetransid()
                        update_coins(user.id, uscoins)
                        urcoins = rcoins + coins
                        update_coins(from_user.id, urcoins)
                        create_transaction(transid, user.id, coins, "debit")
                        create_transaction(transid, from_user.id, coins, "credit")
                        if urcoins > rcoins:
                            update_max_coins(from_user.id, urcoins)

                        update.message.reply_text(
                            text=f'{user.mention_html()} just send {italic(bold(coins))} to {from_user.mention_html()}\n\nTransaction id: {code(transid)}',
                            parse_mode="HTML"
                        )

                    else:
                        update.message.reply_text(
                            text=italic(f'{user.mention_html()} doesn\'t have enough coins!'),
                            parse_mode="HTML"
                        )

            else:
                update.message.reply_text(
                    text=f"{from_user.mention_html()} haven't registered yet! Kindly register with below button",
                    reply_markup=register_markup,
                    parse_mode="HTML"
                )
        else:
            update.message.reply_text(
                text=italic("Kindly tag a user and send coins!"),
                parse_mode="HTML"
            )
    else:
        unregistered(update, context)
