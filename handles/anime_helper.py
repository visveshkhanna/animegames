import mysql.connector

from dotenv import dotenv_values
from handles.extras import bold, italic, code, anchor, clean

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

def anime_message(anime_id, anime):
    anime_authors = []
    for i in anime["staff"]["edges"]:
        anime_authors.append(i["node"]["name"]["full"])
    anime_authors = ', '.join(anime_authors[:5])
    anime_studios = []
    for i in anime["studios"]["edges"]:
        anime_studios.append(i["node"]["name"])
    anime_studios = ', '.join(anime_studios[:5])
    anime_title = anime["title"]
    romaji = anime_title["romaji"]
    native = anime_title["native"]
    start = f'{anime["startDate"]["day"]} / {anime["startDate"]["month"]} / {anime["startDate"]["year"]}'
    end = f'{anime["endDate"]["day"]} / {anime["endDate"]["month"]} / {anime["endDate"]["year"]}'
    anime_source = anime["source"]
    anime_popularity = anime["popularity"]
    anime_genre = ', '.join(anime["genres"])
    anime_episodes = anime["episodes"]
    anime_status = anime["status"]
    anime_description = anime["description"]
    anime_duration = anime["duration"]
    anime_nsfw = anime["isAdult"]
    anime_score = anime["averageScore"]
    anime_format = anime["format"]
    message = f'{bold(italic(romaji))} [ {code(native)} ]\n\n{bold("Format")}: {anime_format} - {bold("Source")}: {anime_source}\n{bold("Status")}: {anime_status} - {bold("NSFW")}: {anime_nsfw}\n{bold("Score")}: {anime_score} - {bold("Popularity")}: {anime_popularity}\n{bold("Episodes")}: {anime_episodes} - {bold("Duration")}: {anime_duration} min(s) / epi\n{bold("Aired")}: {start} - {end}\n\n{bold("Genres")}: {anime_genre}\n{bold("Authors")}: {anime_authors}\n{bold("Studios")}: {anime_studios}\n\n{clean(anime_description)[:400]}...{anchor("Read more", f"https://anilist.co/anime/{anime_id}")}\n\n{bold(italic("From Anilist ❤️"))}'

    return message

def check_anime(animeid):
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "SELECT * FROM anime WHERE animeid = %s"
    values = (animeid,)
    cursor.execute(query, values)
    rc = cursor.rowcount
    cursor.close()
    conn.close()
    if rc == 0:
        return False
    else:
        return True 

def fetch_anime(animeid):
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "SELECT * FROM anime WHERE animeid = %s"
    values = (animeid,)
    cursor.execute(query, values)
    data = list(cursor)[0]
    cursor.close()
    conn.close()
    return data[1], data[2], data[3]

def save_anime(animeid, caption, fileid):
    conn = mysql.connector.connect(**mysql_data)
    cursor = conn.cursor(buffered=True)
    query = "INSERT INTO anime (animeid, caption, fileid) VALUES (%s, %s, %s)"
    values = (animeid, caption, fileid)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
