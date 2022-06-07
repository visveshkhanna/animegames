from telegram import Update, Bot
from telegram.ext import CallbackContext

from anilist.anime import *
from anilist.character import *
from handles.anime_helper import *
from handles.character_helper import *
from handles.extras import italic
from handles.userhandle import check_user, register_user
from transactions.transactions_handle import get_transactions, ListHandle, transaction_message

data = dotenv_values(".env")
TOKEN = data["TOKEN"]


def inlinehandle(update: Update, context: CallbackContext):
    user = update.effective_user
    query = update.callback_query
    if query.data == "register":
        query.answer()
        if not check_user(user):
            register_user(user)
            query.edit_message_text(
                write_timeout=5,
                text="<i>Registering...</i>",
                parse_mode="HTML"
            )
            query.delete_message(5)
            Bot(TOKEN).send_message(chat_id=update.effective_chat.id, text=italic("Register complete"),
                                          parse_mode="HTML")
        else:
            query.edit_message_text(
                text=italic(f"{user.mention_html()} have already registered!"),
                parse_mode="HTML"
            )
    if "ani" in query.data:
        anime_id = int(query.data.split(" ")[-1])
        if query.data.split(" ")[1] == str(user.id):
            new = False
            if check_anime(anime_id):
                anime_id, message, anime_banner = fetch_anime(anime_id)
            else:
                anime = get_anime(anime_id)["data"]["Media"]
                anime_banner = f'https://img.anili.st/media/{anime_id}'
                message = anime_message(anime_id, anime)
                new = True

            query.answer()
            query.delete_message()

            result = Bot(TOKEN).send_photo(
                chat_id=update.effective_chat.id,
                photo=anime_banner,
                caption=message,
                parse_mode="HTML"
            )
            if new:
                fileid = result["photo"][-1].file_id
                save_anime(anime_id, message, fileid)
        else:
            query.answer("Not allowed", show_alert=True)

    if "chr" in query.data:
        character_id = int(query.data.split(" ")[-1])
        if query.data.split(" ")[1] == str(user.id):
            new = False
            if check_character(character_id):
                character_id, message, character_banner = fetch_anime(character_id)
            else:
                character = get_character(character_id)["data"]["Character"]
                character_banner = character["image"]["large"]
                message = character_message(character_id, character)
                new = True

            query.answer()
            query.delete_message()

            result = Bot(TOKEN).send_photo(
                chat_id=update.effective_chat.id,
                photo=character_banner,
                caption=message,
                parse_mode="HTML"
            )
            if new:
                fileid = result["photo"][-1].file_id
                save_character(character_id, message, fileid)
        else:
            query.answer("Not allowed", show_alert=True)
    
    if "TRA" in query.data:
        callbackdata = query.data
        if user.id == int(callbackdata.split(" ")[1]):
            query.answer()
            callbackdata = int(callbackdata.split(" ")[-1])
            data = ListHandle(get_transactions(user), 10)
            if (callbackdata == (len(data)-1)):
                button = [
                    [
                        InlineKeyboardButton("Back", callback_data=f'TRA {user.id} {callbackdata-1}')
                    ]
                ]
                button = InlineKeyboardMarkup(button)
            elif (callbackdata == 0):
                button = [
                    [
                        InlineKeyboardButton("Next", callback_data=f'TRA {user.id} {callbackdata+1}')
                    ]
                ]
                button = InlineKeyboardMarkup(button)
            else:
                button = [
                    [
                        InlineKeyboardButton("Back", callback_data=f'TRA {user.id} {callbackdata-1}'),
                        InlineKeyboardButton("Next", callback_data=f'TRA {user.id} {callbackdata+1}')
                    ]
                ]
                button = InlineKeyboardMarkup(button)
            data = data[callbackdata]
            message = f"Transation History\nPage {callbackdata+1}\n\n"
            for i, cont in enumerate(data):
                messagecont = transaction_message(cont, i+1)
                message += messagecont
            query.edit_message_text(
                text=message,
                parse_mode="HTML",
                reply_markup=button
            )
        else:
            query.answer("Not allowed", show_alert=True)
