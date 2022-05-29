from telegram import Update
from telegram.ext import CallbackContext
from handles.userhandle import check_user, select_user, unregistered
from handles.extras import bold, italic, code
from const import EMPTY


def about_helper(user):
    data = select_user(user)
    id, userid, fullname, username, coins, max_coins, gems, max_gems, total_donated, banner, date = data
    content = f"{EMPTY}\n{italic(bold('Name'))} - {user.mention_html(fullname)}\n{italic(bold('Coins'))} - {coins} [ {code(f'MAX {max_coins}')} ]\n{italic(bold('Gems'))} - {gems} [ {code(f'MAX {max_gems}')} ]\n{italic(bold('Donated'))} - {total_donated}\n{italic(bold('DOB'))} - {date}\n{EMPTY} "
    return [banner, content]


async def about(update: Update, context: CallbackContext):
    user = update.effective_user
    if check_user(user):
        obj = about_helper(user)
        banner = obj[0]
        message = obj[1]

        await update.message.reply_photo(
            photo=banner,
            caption=message,
            parse_mode="HTML"
        )
    else:
        await unregistered(update, context)
