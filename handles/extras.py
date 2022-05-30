import re
import time
from random import randint


def bold(string):
    return f"<b>{string}</b>"


def italic(string):
    return f"<i>{string}</i>"


def code(string):
    return f"<code>{string}</code>"


def anchor(string, url):
    return f'<a href="{url}">{string}</a>'


TAG_RE = re.compile(r'<[^>]+>')


def clean(text):
    return TAG_RE.sub('', text)


def Time():
    return time.strftime("%Y:%m:%d %H:%M:%S")


def animetransid():
    succ = False
    context = "AGTRANS_"
    range_start = 10 ** (10 - 1)
    range_end = (10 ** 10) - 1
    num = randint(range_start, range_end)
    context += str(num)
    return context
