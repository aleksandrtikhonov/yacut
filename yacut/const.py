import re

short_link_regex = re.compile(r"^[A-Za-z0-9_.]+$")
regex_url = re.compile(
    r"^[a-z]+://"
    r"(?P<host>[^\/\?:]+)"
    r"(?P<port>:[0-9]+)?"
    r"(?P<path>\/.*?)?"
    r"(?P<query>\?.*)?$", re.IGNORECASE
)

msg_illegal_short_id = 'Указано недопустимое имя для короткой ссылки'
