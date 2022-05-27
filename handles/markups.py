from telegram import InlineKeyboardButton, InlineKeyboardMarkup

register_button = [
    [
        InlineKeyboardButton(text="Register", callback_data="register")
    ]
]
register_markup = InlineKeyboardMarkup(register_button)
