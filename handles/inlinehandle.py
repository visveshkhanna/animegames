from telegram import Update, Bot
from telegram.ext import CallbackContext
from handles.userhandle import *
from commands.search_anime import *
from handles.extras import *
from handles.anime_helper import *

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
        new = False
        if check_anime(anime_id):
            anime_id, message, anime_banner = fetch_anime(anime_id)
        else:
            anime = get_anime(anime_id)["data"]["Media"]
            anime_banner = f'http://img.anili.st/media/{anime_id}'
            message = anime_message(anime_id, anime)
            new = True
        
        await query.answer()
        await query.delete_message()

        result = await Bot(TOKEN).send_photo(
            chat_id=update.effective_chat.id,
            photo=anime_banner,
            caption=message,
            parse_mode="HTML"
        )
        if new:
            fileid = result["photo"][-1].file_id
            save_anime(anime_id, message, fileid)
        
        