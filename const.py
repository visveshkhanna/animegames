from dotenv import dotenv_values

ABOUT = "AgACAgUAAxkBAAI5sWKOZiXc3MlSUj8C4-Xci-UlH6lFAAJfsDEbGcVxVM6j1RK3DRmcAQADAgADeQADJAQ"
LOADING = "CgACAgUAAxkBAAEJI21ikSJue-BNmGtigcspwCQiV7pZtQACIAYAAgzPiVSXXyVvRzIsFiQE"
EMPTY = "⠀"

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
