import mysql.connector
from telegram import Update
from telegram.ext import CallbackContext

from const import mysql_data
from handles.extras import *
from handles.markups import register_markup


async def unregistered(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text(
        "<i>You are not registered in <b><i>Anime Games</i></b>, Register now! by clicking the button below</i>",
        reply_markup=register_markup, parse_mode="HTML")


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


def select_user_v2(user: Update.effective_user):
    uid = user.id
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "SELECT * FROM users WHERE userid = %s"
    values = (uid,)
    cursor.execute(query, values)
    datas = list(cursor)[0]
    id, userid, fullname, username, coins, max_coins, gems, max_gems, total_donated, banner, date = datas
    user_data = {
        'id': id,
        'userid': userid,
        'fullname': fullname,
        'username': username,
        'coins': coins,
        'max_coins': max_coins,
        'gems': gems,
        'max_gems': max_gems,
        'total_donated': total_donated,
        'banner': banner,
        'date': date
    }
    cursor.close()
    conn.close()
    return user_data


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


def update_coins(userid, coins):
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "UPDATE users SET coins = %s WHERE userid = %s"
    values = (coins, userid)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


def update_max_coins(userid, coins):
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "UPDATE users SET max_coins = %s WHERE userid = %s"
    values = (coins, userid)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
