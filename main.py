import asyncio
import html
import json
import logging
import traceback

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, filters

from commands.extras import ping_command
from commands.search_anime import searchanime
from commands.search_character import searchcharacter
from game import send, info
from handles.inlinehandle import *
from handles.markups import *
from transactions.transactions import view_trans
from waifuu.waifu import waifu_com
from speed.speedtest_command import speedtest

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
    nonr_message = f"Hey {user.mention_html('Traveller')},\n\nWelcome to the <b>world</b> of <b><i>Anime " \
                   f"Games</i></b>, Register now to get started by clicking the button below! "
    r_message = f"Hey {user.mention_html('Traveller')},\n\nWelcome to the <b>world</b> of <b><i>Anime Games</i></b>, " \
                f"Hope you have fun! "
    if check_user(user):
        await update.message.reply_text(r_message, parse_mode="HTML")
    else:
        await update.message.reply_text(nonr_message, reply_markup=register_markup, parse_mode="HTML")


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
    application.add_handler(CommandHandler("start", start, block=False))
    application.add_handler(CommandHandler("info", info.about, block=False))
    application.add_handler(CommandHandler("send", send.send_coins, block=False))
    application.add_handler(CommandHandler("anime", searchanime, block=False))
    application.add_handler(CommandHandler("character", searchcharacter, block=False))
    application.add_handler(CommandHandler("ping", ping_command, block=False))
    application.add_handler(CommandHandler("trans", view_trans, block=False))
    application.add_handler(CommandHandler("waifu", waifu_com, block=False))
    application.add_handler(CommandHandler('speed', speedtest, filters=filters.User(user_id=int(OWNER)), block=False))

    # Inline Handle
    application.add_handler(CallbackQueryHandler(inlinehandle,block=False))

    # Error handle
    application.add_error_handler(error_handler, block=False)

    # Poll bot
    application.run_polling(drop_pending_updates=True, stop_signals=None)


if __name__ == "__main__":
    asyncio.run(main())
