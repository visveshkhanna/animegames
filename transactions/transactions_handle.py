from telegram import Update
from const import mysql_data
import mysql.connector
from handles.extras import Time

def check_transaction(transid):
    conn = mysql.connector.connect(**mysql_data)
    curser = conn.cursor(buffered=True)
    query = "SELECT * FROM transactions WHERE transid = %s"
    values = (transid,)
    curser.execute(query, values)
    rc = curser.rowcount
    if rc == 0:
        return False
    else:
        return True

def create_transaction(transid, user, coins, type):
    date = Time()
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "INSERT INTO transactions (transid, userid, coins, type, time) VALUES (%s, %s, %s, %s, %s)"
    values = (transid, user, coins, type, date,)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

def get_transactions(user: Update.effective_user):
    user_id = user.id
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True, dictionary=True)
    query = "SELECT * FROM transactions WHERE userid = %s"
    values = (user_id,)
    cursor.execute(query, values)
    print(list(cursor))
    cursor.close()
    conn.close()