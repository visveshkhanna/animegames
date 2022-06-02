import requests
from handles.userhandle import check_user, unregistered
from const import mysql_data
import mysql.connector
from telegram import Update
from telegram.ext import CallbackContext

async def waifu_com(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = update.effective_user
    if check_user(user):
        gen = waifu_gen()
        if check_waifu(gen):
            wai = get_waifu(gen)
            await update.message.reply_photo(
                photo=wai
            )
        else:
            await update.message.reply_photo(
                photo=gen
            )
    else:
        await unregistered(update, context)

def waifu_gen():
    url = "https://api.waifu.im/random/"
    data = requests.get(url).json()
    return data["images"][0]["url"]

def check_waifu(gen):
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "SELECT * FROM waifu WHERE url = %s"
    values = (gen, )
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
    values = (gen, )
    cursor.execute(query, values)
    data = list(cursor)[0]
    cursor.close()
    conn.close()
    return data["fileid"]
