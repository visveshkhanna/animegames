import logging
from dotenv import dotenv_values

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ENV
data = dotenv_values(".env")

# Command Handles
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = f"Hey {user.mention_html()},\nWelcome to Anime Games!"
    await update.message.reply_text(
        text=message,
        parse_mode="HTML"
    )

async def about(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    fileid = data["ABOUT"]
    message = "<b>Anime Games</b> is a Telegram bot that provides you with a variety of games to play.";
    await update.message.reply_photo(fileid, message, parse_mode="HTML")

def main() -> None:

    application = Application.builder().token(data["TOKEN"]).build()

    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("about", about))

    # Poll bot
    application.run_polling()


if __name__ == "__main__":
    main()
