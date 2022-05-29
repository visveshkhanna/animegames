import re
import time


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
