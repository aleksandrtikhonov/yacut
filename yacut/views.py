from flask import render_template, redirect, flash, url_for, Response

from yacut import app, db
from yacut.forms import URL_mapForm
from yacut.models import URL_map
from yacut.services import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view() -> str:
    form = URL_mapForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data or get_unique_short_id()
        link_urls = URL_map(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(link_urls)
        db.session.commit()
        short_url = url_for('redirect_view', custom_id=short_id,
                            _external=True)
        message = ('<p>Ваша новая ссылка готова: '
                   f'<a href="{short_url}">{short_url}</a></p>')
        flash(message)
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:custom_id>', methods=['GET'])
def redirect_view(custom_id: str) -> Response:
    redirect_url = URL_map.query.filter_by(short=custom_id).first_or_404()
    return redirect(redirect_url.original)
