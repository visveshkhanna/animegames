import mysql.connector

from telegram import Update
from telegram.ext import CallbackContext

from telegram import Update
from handles.extras import *
from handles.markups import *
from dotenv import dotenv_values

data = dotenv_values(".env")

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

async def unregistered(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text("<i>You are not registered in <b><i>Anime Games</i></b>, Register now! by clicking the button below</i>", reply_markup=register_markup, parse_mode="HTML")

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
    uid = user.id
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "SELECT * FROM users WHERE userid = %s"
    values = (uid,)
    cursor.execute(query, values)
    datas = list(cursor)[0]
    cursor.close()
    conn.close()
    return datas


def register_user(user: Update.effective_user):
    id = user.id
    name = user.full_name
    username = user.username
    if username is None:
        username = ""
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
