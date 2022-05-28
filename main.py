import logging
import html
import json
import traceback
from dotenv import dotenv_values

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
from commands.search_anime import *
from commands.search_character import *

from handles.userhandle import *
from handles.inlinehandle import *
from anilist.anime import *
from handles.markups import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ENV
data = dotenv_values(".env")
TOKEN = data["TOKEN"]
OWNER = data["OWNER"]

# Command Handles
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    user = update.effective_user
    nonr_message = f"Hey {user.mention_html('Traveller')},\n\nWelcome to the <b>world</b> of <b><i>Anime Games</i></b>, Register now to get started by clicking the button below!"
    r_message = f"Hey {user.mention_html('Traveller')},\n\nWelcome to the <b>world</b> of <b><i>Anime Games</i></b>, Hope you have fun!"
    if check_user(user):
        await update.message.reply_text(r_message, parse_mode="HTML")
    else:
        await update.message.reply_text(nonr_message, reply_markup=register_markup, parse_mode="HTML")

async def about(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    fileid = data["ABOUT"]
    message = "<b>Anime Games</b> is a Telegram bot that provides you with a variety of games to play."
    await update.message.reply_photo(fileid, message, parse_mode="HTML")

async def info(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if check_user(user):
        user_data = select_user(user)
        userid = user_data[1]
        fullname = user_data[2]
        username = user_data[3]
        d = 0
        if [userid, fullname, username] != [user.id, user.full_name, user.username]:
            d = 1
            update_register_user(user)
            message = "Updated user data succesfully!"
            sentmessage = await update.message.reply_text(message, parse_mode="HTML")

        message = f"<b><i>Anime Games</i></b>\n\n<b>User ID:</b> <code>{user.id}</code>\n<b>Name:</b> {user.full_name}\n<b>Username:</b> @{user.username.lower()}\n<b>Registered Time:</b> {Time()}"
        if d:
            await sentmessage.edit_text(message, parse_mode="HTML")
        else:
            await update.message.reply_text(message, parse_mode="HTML")
    else:
        await unregistered(update, context)

async def error_handler(update: object, context: CallbackContext.DEFAULT_TYPE) -> None:

    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await Bot(TOKEN).send_message(
        chat_id=OWNER, text=message, parse_mode="HTML"
    )

def main() -> None:

    application = Application.builder().token(TOKEN).build()
    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("anime", searchanime))
    application.add_handler(CommandHandler("character", searchcharacter))

    # Inline Handle
    application.add_handler(CallbackQueryHandler(inlinehandle))

    # Error handle
    application.add_error_handler(error_handler)

    # Poll bot
    application.run_polling(drop_pending_updates=True, stop_signals=None)


if __name__ == "__main__":
    main()
