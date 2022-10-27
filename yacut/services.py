import random
import string

from yacut.models import URL_map


def get_unique_short_id() -> str:
    short = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    if URL_map.query.filter_by(short=short).first() == short:
        get_unique_short_id()
    return short


def is_custom_id_exist(custom_id: str) -> bool:
    return bool(URL_map.query.filter_by(short=custom_id).first())


def get_url_through_custom_id(custom_id: str) -> URL_map:
    url = URL_map.query.filter_by(short=custom_id).first()
    return url
