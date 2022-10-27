import re
from http import HTTPStatus

from yacut.const import regex_url, short_link_regex, msg_illegal_short_id
from yacut.error_handlers import InvalidAPIUsage
from yacut.services import is_custom_id_exist


def validate_input_data(api_data: dict) -> None:
    if not api_data:
        raise InvalidAPIUsage('Отсутствует тело запроса',
                              HTTPStatus.BAD_REQUEST)
    url = api_data.get('url')
    if not url:
        raise InvalidAPIUsage('\"url\" является обязательным полем!',
                              HTTPStatus.BAD_REQUEST)
    validate_url(url)

    short_link = api_data.get('custom_id')
    if short_link:
        validate_custom_id(short_link)


def validate_url(url: str) -> None:
    if re.match(regex_url, url) is None:
        raise InvalidAPIUsage('Некорректный URL', HTTPStatus.BAD_REQUEST)


def validate_custom_id(custom_id: str) -> None:
    if not 1 <= len(custom_id) < 17:
        raise InvalidAPIUsage(msg_illegal_short_id, HTTPStatus.BAD_REQUEST)

    if re.match(short_link_regex, custom_id) is None:
        raise InvalidAPIUsage(msg_illegal_short_id, HTTPStatus.BAD_REQUEST)

    if is_custom_id_exist(custom_id):
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.',
                              HTTPStatus.BAD_REQUEST)


def validate_url_exist(custom_id: str) -> None:
    if not custom_id:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
