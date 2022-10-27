from datetime import datetime

from flask import url_for

from yacut import db


class URL_map(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    original: str = db.Column(db.String(128), nullable=False)
    short: str = db.Column(db.String(16), unique=True, nullable=False)
    timestamp: datetime = db.Column(db.DateTime, index=True,
                                    default=datetime.utcnow)

    db.UniqueConstraint(original, short)

    def to_dict(self, only_short: bool = False) -> dict:
        if only_short:
            return dict(url=self.original)
        return dict(
            short_link=url_for(
                'redirect_view', custom_id=self.short, _external=True
            ),
            url=self.original,
        )

    def from_dict(self, data: dict) -> None:
        map_fields = {
            'url': 'original',
            'custom_id': 'short'
        }
        for field in ['url', 'custom_id']:
            if field in data:
                setattr(self, map_fields[field], data[field])
