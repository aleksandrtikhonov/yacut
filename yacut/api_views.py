from __future__ import annotations

from flask import jsonify, request, Response

from yacut import app, db
from yacut.models import URL_map
from yacut.services import get_unique_short_id, get_url_through_custom_id
from yacut.validators_api import validate_input_data, validate_url_exist


@app.route('/api/id/', methods=['POST'])
def create_url_map() -> tuple[Response, int]:
    data = request.get_json()
    validate_input_data(data)
    custom_id = data.get('custom_id')
    if custom_id is None or len(custom_id) == 0:
        data['custom_id'] = get_unique_short_id()
    link_urls = URL_map()
    link_urls.from_dict(data)
    db.session.add(link_urls)
    db.session.commit()
    return jsonify(link_urls.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id: str) -> tuple[Response, int]:
    url = get_url_through_custom_id(short_id)
    validate_url_exist(url)
    return jsonify(url.to_dict(only_short=True)), 200
