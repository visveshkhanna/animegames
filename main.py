from ast import If
import logging
from multiprocessing import context
from tabnanny import check
import time
import mysql.connector
from dotenv import dotenv_values

from telegram import Bot, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ENV
data = dotenv_values(".env")
TOKEN = data["TOKEN"]
mysql_user = data["USER"]
mysql_password = data["PASSWORD"]
mysql_host = data["HOST"]
mysql_db = data["DB"]

mysql_data = {
        "user": mysql_user,
        "password": mysql_password,
        "host": mysql_host,
        "database": mysql_db
    }

# Inline Keyboards
register_button = [
    [
        InlineKeyboardButton(text="Register", callback_data="register")
    ]
]
register_markup = InlineKeyboardMarkup(register_button)

def Time():
    return time.strftime("%Y:%m:%d %H:%M:%S")

def check_user(user: Update.effective_user):
    id = user.id
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "SELECT * FROM users WHERE userid = %s"
    values = (id,)
    cursor.execute(query, values)
    rc = cursor.rowcount
    cursor.close()
    conn.close()
    if rc == 0:
        return False
    else:
        return True
    
def select_user(user: Update.effective_user):
    id = user.id
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "SELECT * FROM users WHERE userid = %s"
    values = (id,)
    cursor.execute(query, values)
    data = list(cursor)[0]
    cursor.close()
    conn.close()
    return data

def register_user(user: Update.effective_user):
    id = user.id
    name = user.full_name
    username = user.username
    date = Time()

    # MySQL Connection
    conn = mysql.connector.connect(**mysql_data)

    # MySQL cursor
    cursor = conn.cursor(buffered=True)

    # MySQL Query
    query = "INSERT INTO users (userid, fullname, username, time) VALUES (%s, %s, %s, %s)"
    values = (id, name, username, date)

    # MySQL Execute
    cursor.execute(query, values)

    # Commit
    conn.commit()

    # Close
    cursor.close()
    conn.close()

def update_register_user(user: Update.effective_user):
    id = user.id
    name = user.full_name
    username = user.username
    date = Time()

    # MySQL Connection
    conn = mysql.connector.connect(**mysql_data)

    # MySQL cursor
    cursor = conn.cursor(buffered=True)

    # MySQL Query
    query = "UPDATE users SET fullname = %s, username = %s WHERE userid = %s"
    values = (name, username, id)

    # MySQL Execute
    cursor.execute(query, values)

    # Commit
    conn.commit()

    # Close
    cursor.close()
    conn.close()


async def inlinehandle(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = update.effective_user
    query = update.callback_query
    await query.answer()
    if query.data == "register":
        register_user(user)
        await query.edit_message_text(
            write_timeout=5,
            text="<i>Registering...</i>",
            parse_mode="HTML"
        )
        await query.delete_message(5)
        await Bot(TOKEN).send_message(chat_id=update.effective_chat.id, text="<i>Register complete</i>", parse_mode="HTML")
        
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
    application.run_polling()


if __name__ == "__main__":
    main()
