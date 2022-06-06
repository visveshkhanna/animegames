import mysql.connector
from telegram import Update

from const import mysql_data
from handles.extras import Time, code, bold, italic


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
    contents = list(cursor)
    cursor.close()
    conn.close()
    return contents

def transaction_message(content, n):
    transid = content["transid"]
    coins = content["coins"]
    type = type_handle(content["type"])
    if coin_handle(type):
        coins *= -1
    time = content["time"]
    message = code(f'{n} {type} {transid} {coins} {time}\n')
    return message


def type_handle(data):
    ans = ""
    if data == "debit":
        ans = "DB"
    elif data == "credit":
        ans = "CR"
    return ans


def coin_handle(type):
    ans = False
    if type == "DB":
        ans = True
    return ans

def ListHandle(List, n):
	parts = []
	for i in range(0, len(List), n):
		parts.append(List[i:i+n])
	return parts
