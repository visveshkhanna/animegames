from telegram import Update
from telegram.ext import CallbackContext
from speedtest import Speedtest
from handles.extras import italic

def speedtest(update: Update, context: CallbackContext):
    speed = update.message.reply_text(
        text=italic("Running Speed Test . . . "),
        parse_mode="HTML"
    )
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    result = test.results.dict()
    string_speed = f'''
<b>Server</b>
<b>Name:</b> <code>{result['server']['name']}</code>
<b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
<b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
<b>ISP:</b> <code>{result['client']['isp']}</code>
<b>SpeedTest Results</b>
<b>Upload:</b> <code>{speed_convert(result['upload'] / 8)}</code>
<b>Download:</b>  <code>{speed_convert(result['download'] / 8)}</code>
<b>Ping:</b> <code>{result['ping']} ms</code>
<b>ISP Rating:</b> <code>{result['client']['isprating']}</code>
'''
    speed.edit_text(
        text=string_speed,
        parse_mode="HTML"
    )


def speed_convert(size):

    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "MB/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"
