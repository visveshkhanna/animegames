import logging
import time
from dotenv import dotenv_values

from telegram import Bot, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler

from handles.userhandle import * 

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ENV
data = dotenv_values(".env")
TOKEN = data["TOKEN"]

# Inline Keyboards
register_button = [
    [
        InlineKeyboardButton(text="Register", callback_data="register")
    ]
]
register_markup = InlineKeyboardMarkup(register_button)

async def inlinehandle(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = update.effective_user
    query = update.callback_query
    await query.answer()
    if query.data == "register":
        if not check_user(user):
            register_user(user)
            await query.edit_message_text(
                write_timeout=5,
                text="<i>Registering...</i>",
                parse_mode="HTML"
            )
            await query.delete_message(5)
            await Bot(TOKEN).send_message(chat_id=update.effective_chat.id, text="<i>Register complete</i>", parse_mode="HTML")
        else:
            await query.edit_message_text(
                text="<i>Already Registered!</i>",
                parse_mode="HTML"
            )
        
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
        id = user_data[0]
        userid = user_data[1]
        fullname = user_data[2]
        username = user_data[3]
        time = user_data[4]
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
        await update.message.reply_text("<i>You are not registered in <b><i>Anime Games</i></b>, Register now! by clicking the button below</i>", reply_markup=register_markup, parse_mode="HTML")    

def main() -> None:

    application = Application.builder().token(TOKEN).build()
    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("info", info))

    # Inline Handle
    application.add_handler(CallbackQueryHandler(inlinehandle))

    # Poll bot
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
