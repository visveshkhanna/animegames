import mysql.connector
from dotenv import dotenv_values

from handles.extras import bold, italic, code, anchor

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


def character_message(character_id, character):
    character_name = character["name"]["full"]
    character_native = character["name"]["native"]
    character_alt = ', '.join(character["name"]["alternative"])
    character_description = character["description"]
    character_age = character["age"]
    character_gender = character["gender"]
    character_dob = character["dateOfBirth"]
    month = character_dob["month"]
    day = character_dob["day"]

    message = f'{italic(bold(character_name))} [ {code(character_native)} ]\n\n{bold("Alternative")}: {character_alt}\n\n{bold("Gender")}: {character_gender}\n{bold("Age")}: {character_age} - {bold("DOB")}: {day}/{month}\n\n{character_description[:300]}...{anchor("Read more", f"https://anilist.co/character/{character_id}")}\n\n{bold(italic("From Anilist ❤️"))} '
    return message


def check_character(characterid):
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "SELECT * FROM characters WHERE characterid = %s"
    values = (characterid,)
    cursor.execute(query, values)
    rc = cursor.rowcount
    cursor.close()
    conn.close()
    if rc == 0:
        return False
    else:
        return True


def fetch_character(characterid):
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "SELECT * FROM characters WHERE characterid = %s"
    values = (characterid,)
    cursor.execute(query, values)
    data = list(cursor)[0]
    cursor.close()
    conn.close()
    return data[1], data[2], data[3]


def save_character(characterid, caption, fileid):
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "INSERT INTO characters (characterid, caption, fileid) VALUES (%s, %s, %s)"
    values = (characterid, caption, fileid)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
