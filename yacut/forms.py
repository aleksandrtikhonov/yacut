from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import DataRequired, URL, Optional, Regexp, Length, \
    ValidationError

from yacut.const import short_link_regex
from yacut.services import is_custom_id_exist


class URL_mapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Введите корректный URL')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Regexp(
                message='Только латинские символы и цифры',
                regex=short_link_regex),
            Length(min=1, max=16, message='Максимум 16 символов')
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, custom_id: StringField) -> bool:
        if is_custom_id_exist(custom_id.data):
            raise ValidationError(f'Имя {custom_id.data} уже занято!')
        return True
