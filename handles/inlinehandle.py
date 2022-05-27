from telegram import Update, Bot
from telegram.ext import CallbackContext
from handles.userhandle import *
from commands.search_anime import *
from handles.extras import *

data = dotenv_values(".env")
TOKEN = data["TOKEN"]

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
    if "ani" in query.data:
        anime_id = int(query.data.split(" ")[-1])
        anime = get_anime(anime_id)["data"]["Media"]
        anime_banner = f'http://img.anili.st/media/{anime_id}'
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
        message = f'{bold(italic(romaji))} [ {code(native)} ]\n\n{bold("Format")}: {anime_format} - {bold("Source")}: {anime_source}\n{bold("Status")}: {anime_status} - {bold("NSFW")}: {anime_nsfw}\n{bold("Score")}: {anime_score} - {anime_popularity}\n{bold("Episodes")}: {anime_episodes} - {bold("Duration")}: {anime_duration} min(s) / epi\n{bold("Aired")}: {start} - {end}\n\n{bold("Genres")}: {anime_genre}\n{bold("Authors")}: {anime_authors}\n{bold("Studios")}: {anime_studios}\n\n{clean(anime_description)[:200]}...{anchor("Read more", "https://anilist.co/anime/{anime_id}")}'
        
        await query.answer()
        await query.delete_message()

        await Bot(TOKEN).send_photo(
            chat_id=update.effective_chat.id,
            photo=anime_banner,
            caption=message,
            parse_mode="HTML"
        )
        
        