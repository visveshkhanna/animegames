import mysql.connector
import requests
from telegram import Update
from telegram.ext import CallbackContext

from const import mysql_data
from handles.userhandle import check_user, unregistered


def waifu_com(update: Update, context: CallbackContext):
    user = update.effective_user
    if check_user(user):
        gen = waifu_gen()
        if check_waifu(gen):
            wai = get_waifu(gen)
            update.message.reply_photo(
                photo=wai
            )
        else:
            data = update.message.reply_photo(
                photo=gen
            )
            fileid = data["photo"][-1].file_id
            save_waifu(fileid, gen)
    else:
        unregistered(update, context)


def waifu_gen():
    url = "https://api.waifu.im/random/"
    data = requests.get(url).json()
    return data["images"][0]["url"]


def check_waifu(gen):
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "SELECT * FROM waifu WHERE url = %s"
    values = (gen,)
    cursor.execute(query, values)
    rc = cursor.rowcount
    cursor.close()
    conn.close()
    if rc == 0:
        return False
    return True


def get_waifu(gen):
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True, dictionary=True)
    query = "SELECT * FROM waifu WHERE url = %s"
    values = (gen,)
    cursor.execute(query, values)
    data = list(cursor)[0]
    cursor.close()
    conn.close()
    return data["fileid"]


def save_waifu(fileid, url):
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "INSERT INTO waifu (url, fileid) VALUES (%s, %s)"
    values = (url, fileid)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
